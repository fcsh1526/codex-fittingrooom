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
    await page.setContent('<canvas id="reel" width="1080" height="1920"></canvas>');

    const detailDataUrl = `data:image/png;base64,${fs.readFileSync(detailPath).toString('base64')}`;
    const motionDataUrl = `data:image/png;base64,${fs.readFileSync(motionPath).toString('base64')}`;

    const rendered = await page.evaluate(async ({ detailDataUrl, motionDataUrl, titleLine1, titleLine2 }) => {
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

      const [detail, motion] = await Promise.all([
        loadImage(detailDataUrl),
        loadImage(motionDataUrl),
      ]);
      await document.fonts.load('500 52px "Noto Serif TC"');

      function smoothstep(t) {
        const value = Math.max(0, Math.min(1, t));
        return value * value * (3 - 2 * value);
      }

      function drawFocused(image, options) {
        const {
          zoom,
          focalX,
          focalY,
          targetX,
          targetY,
        } = options;
        const coverScale = Math.max(width / image.naturalWidth, height / image.naturalHeight);
        const drawWidth = image.naturalWidth * coverScale * zoom;
        const drawHeight = image.naturalHeight * coverScale * zoom;
        const drawX = (width * targetX) - (drawWidth * focalX);
        const drawY = (height * targetY) - (drawHeight * focalY);
        ctx.drawImage(image, drawX, drawY, drawWidth, drawHeight);
      }

      function drawTitle(opacity) {
        if (opacity <= 0) return;
        const gradient = ctx.createLinearGradient(0, 0, 620, 0);
        gradient.addColorStop(0, `rgba(250,244,235,${0.68 * opacity})`);
        gradient.addColorStop(0.72, `rgba(250,244,235,${0.28 * opacity})`);
        gradient.addColorStop(1, 'rgba(250,244,235,0)');
        ctx.fillStyle = gradient;
        ctx.fillRect(0, 150, 650, 255);

        ctx.globalAlpha = opacity;
        ctx.fillStyle = '#3b3028';
        ctx.font = '500 52px "Noto Serif TC", "Microsoft JhengHei", serif';
        ctx.textAlign = 'left';
        ctx.textBaseline = 'top';
        ctx.fillText(titleLine1, 82, 205);
        ctx.fillText(titleLine2, 82, 285);
        ctx.globalAlpha = 1;
      }

      function drawFrame(seconds) {
        ctx.fillStyle = '#d9c6ad';
        ctx.fillRect(0, 0, width, height);

        if (seconds < 0.72) {
          const p = smoothstep(seconds / 0.72);
          drawFocused(detail, {
            zoom: 1.58 - (0.30 * p),
            focalX: 0.54 - (0.02 * p),
            focalY: 0.62 - (0.08 * p),
            targetX: 0.70,
            targetY: 0.56,
          });
        } else if (seconds < 2.25) {
          const p = smoothstep((seconds - 0.72) / 1.53);
          drawFocused(motion, {
            zoom: 1.06 + (0.07 * p),
            focalX: 0.535 - (0.018 * p),
            focalY: 0.48,
            targetX: 0.68,
            targetY: 0.47,
          });
        } else if (seconds < 3.85) {
          const p = smoothstep((seconds - 2.25) / 1.60);
          drawFocused(detail, {
            zoom: 1.10 + (0.12 * p),
            focalX: 0.53,
            focalY: 0.43 + (0.10 * p),
            targetX: 0.67,
            targetY: 0.46,
          });
        } else {
          const p = smoothstep((seconds - 3.85) / 2.15);
          drawFocused(motion, {
            zoom: 1.10 + (0.10 * p),
            focalX: 0.52 - (0.02 * p),
            focalY: 0.46,
            targetX: 0.68,
            targetY: 0.46,
          });
        }

        const titleOpacity = seconds <= 1.55
          ? 1
          : Math.max(0, 1 - ((seconds - 1.55) / 0.30));
        drawTitle(titleOpacity);
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
        videoBitsPerSecond: 7000000,
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
    }, { detailDataUrl, motionDataUrl, titleLine1, titleLine2 });

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
