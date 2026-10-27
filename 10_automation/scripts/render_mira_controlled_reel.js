const fs = require('fs');
const path = require('path');

function arg(name) {
  const index = process.argv.indexOf(`--${name}`);
  if (index === -1 || !process.argv[index + 1]) {
    throw new Error(`Missing --${name}`);
  }
  return process.argv[index + 1];
}

async function main() {
  const playwrightModule = arg('playwright-module');
  const edgeExecutable = arg('edge');
  const sourcePath = path.resolve(arg('source'));
  const outputPath = path.resolve(arg('output'));
  const posterPath = path.resolve(arg('poster'));
  const titleLine1 = arg('title-line-1');
  const titleLine2 = arg('title-line-2');

  const { chromium } = require(playwrightModule);
  const browser = await chromium.launch({
    headless: true,
    executablePath: edgeExecutable,
  });

  try {
    const page = await browser.newPage();
    await page.setContent('<canvas id="reel" width="1080" height="1920"></canvas>');

    const imageDataUrl = `data:image/png;base64,${fs.readFileSync(sourcePath).toString('base64')}`;

    const rendered = await page.evaluate(async ({ imageDataUrl, titleLine1, titleLine2 }) => {
      const canvas = document.getElementById('reel');
      const ctx = canvas.getContext('2d', { alpha: false });
      const image = new Image();
      image.src = imageDataUrl;
      await image.decode();
      await document.fonts.load('500 52px "Noto Serif TC"');

      const width = canvas.width;
      const height = canvas.height;
      const durationMs = 6000;
      const objectPositionX = 0.53;
      const objectPositionY = 0.50;

      function drawFrame(progress) {
        const eased = progress * progress * (3 - 2 * progress);
        const zoom = 1 + (0.06 * eased);
        const coverScale = Math.max(width / image.naturalWidth, height / image.naturalHeight);
        const drawWidth = image.naturalWidth * coverScale * zoom;
        const drawHeight = image.naturalHeight * coverScale * zoom;
        const drawX = -(drawWidth - width) * objectPositionX;
        const drawY = -(drawHeight - height) * objectPositionY;

        ctx.fillStyle = '#d9c6ad';
        ctx.fillRect(0, 0, width, height);
        ctx.drawImage(image, drawX, drawY, drawWidth, drawHeight);

        const gradient = ctx.createLinearGradient(0, 0, 0, 500);
        gradient.addColorStop(0, 'rgba(255,250,242,0.08)');
        gradient.addColorStop(1, 'rgba(255,250,242,0)');
        ctx.fillStyle = gradient;
        ctx.fillRect(0, 0, width, 500);

        ctx.fillStyle = '#3b3028';
        ctx.font = '500 52px "Noto Serif TC", "Microsoft JhengHei", serif';
        ctx.textAlign = 'left';
        ctx.textBaseline = 'top';
        ctx.fillText(titleLine1, 650, 220);
        ctx.fillText(titleLine2, 650, 300);
      }

      drawFrame(0);
      const posterBase64 = canvas.toDataURL('image/png').split(',')[1];

      const mimeType = 'video/mp4;codecs=avc1.42E01E';
      if (!MediaRecorder.isTypeSupported(mimeType)) {
        throw new Error(`Unsupported recording type: ${mimeType}`);
      }

      const stream = canvas.captureStream(30);
      const recorder = new MediaRecorder(stream, {
        mimeType,
        videoBitsPerSecond: 6000000,
      });
      const chunks = [];
      recorder.ondataavailable = event => {
        if (event.data.size > 0) chunks.push(event.data);
      };

      const stopped = new Promise(resolve => {
        recorder.onstop = resolve;
      });

      recorder.start(250);
      const startedAt = performance.now();

      await new Promise(resolve => {
        function animate(now) {
          const elapsed = now - startedAt;
          drawFrame(Math.min(elapsed / durationMs, 1));
          if (elapsed < durationMs) {
            requestAnimationFrame(animate);
          } else {
            resolve();
          }
        }
        requestAnimationFrame(animate);
      });

      recorder.stop();
      await stopped;
      stream.getTracks().forEach(track => track.stop());

      const blob = new Blob(chunks, { type: mimeType });
      const videoBase64 = await new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = () => resolve(reader.result.split(',')[1]);
        reader.onerror = reject;
        reader.readAsDataURL(blob);
      });

      return {
        posterBase64,
        videoBase64,
        mimeType: blob.type,
      };
    }, { imageDataUrl, titleLine1, titleLine2 });

    fs.mkdirSync(path.dirname(outputPath), { recursive: true });
    fs.writeFileSync(outputPath, Buffer.from(rendered.videoBase64, 'base64'));
    fs.writeFileSync(posterPath, Buffer.from(rendered.posterBase64, 'base64'));

    const metadata = await page.evaluate(async (videoDataUrl) => {
      const video = document.createElement('video');
      video.preload = 'metadata';
      video.src = videoDataUrl;
      await new Promise((resolve, reject) => {
        video.onloadedmetadata = resolve;
        video.onerror = () => reject(new Error('Unable to read rendered video metadata'));
      });
      return {
        duration: video.duration,
        width: video.videoWidth,
        height: video.videoHeight,
      };
    }, `data:video/mp4;base64,${rendered.videoBase64}`);

    process.stdout.write(JSON.stringify({
      outputPath,
      posterPath,
      mimeType: rendered.mimeType,
      bytes: fs.statSync(outputPath).size,
      ...metadata,
    }, null, 2));
  } finally {
    await browser.close();
  }
}

main().catch(error => {
  console.error(error);
  process.exitCode = 1;
});
