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
  const heroPath = path.resolve(arg('hero'));
  const detailPath = path.resolve(arg('detail'));
  const motionPath = path.resolve(arg('motion'));
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
    await page.setContent(`
      <style>
        @font-face {
          font-family: "Mira Noto Serif TC";
          src: local("Noto Serif TC");
        }
      </style>
      <canvas id="reel" width="1080" height="1920"></canvas>
    `);

    function dataUrl(filePath) {
      return `data:image/png;base64,${fs.readFileSync(filePath).toString('base64')}`;
    }

    const rendered = await page.evaluate(async ({
      heroDataUrl,
      detailDataUrl,
      motionDataUrl,
      titleLine1,
      titleLine2,
    }) => {
      const canvas = document.getElementById('reel');
      const ctx = canvas.getContext('2d', { alpha: false });
      const width = canvas.width;
      const height = canvas.height;
      const durationMs = 6000;

      async function loadImage(src) {
        const image = new Image();
        image.src = src;
        await image.decode();
        return image;
      }

      const [hero, detail, motion] = await Promise.all([
        loadImage(heroDataUrl),
        loadImage(detailDataUrl),
        loadImage(motionDataUrl),
      ]);
      await document.fonts.load('500 56px "Mira Noto Serif TC"');

      function drawCover(image) {
        const scale = Math.max(width / image.naturalWidth, height / image.naturalHeight);
        const drawWidth = image.naturalWidth * scale;
        const drawHeight = image.naturalHeight * scale;
        const drawX = (width - drawWidth) / 2;
        const drawY = (height - drawHeight) / 2;
        ctx.drawImage(image, drawX, drawY, drawWidth, drawHeight);
      }

      function drawTitle() {
        ctx.fillStyle = '#2B2926';
        ctx.font = '500 56px "Mira Noto Serif TC", "Noto Serif TC", "Microsoft JhengHei", serif';
        ctx.textAlign = 'left';
        ctx.textBaseline = 'top';
        ctx.fillText(titleLine1, 86, 250);
        ctx.fillText(titleLine2, 86, 320);
      }

      function drawFrame(seconds) {
        ctx.fillStyle = '#2B2926';
        ctx.fillRect(0, 0, width, height);

        if (seconds < 2.10) {
          drawCover(hero);
        } else if (seconds < 4.05) {
          drawCover(detail);
        } else {
          drawCover(motion);
        }

        if (seconds < 1.45) {
          drawTitle();
        }
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
        videoBitsPerSecond: 8000000,
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
          drawFrame(Math.min(elapsed / 1000, durationMs / 1000));
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
    }, {
      heroDataUrl: dataUrl(heroPath),
      detailDataUrl: dataUrl(detailPath),
      motionDataUrl: dataUrl(motionPath),
      titleLine1,
      titleLine2,
    });

    fs.mkdirSync(path.dirname(outputPath), { recursive: true });
    fs.writeFileSync(outputPath, Buffer.from(rendered.videoBase64, 'base64'));
    fs.writeFileSync(posterPath, Buffer.from(rendered.posterBase64, 'base64'));

    const metadata = await page.evaluate(async videoDataUrl => {
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
