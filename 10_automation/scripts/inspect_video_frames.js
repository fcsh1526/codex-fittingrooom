const fs = require('fs');
const path = require('path');

function arg(name) {
  const index = process.argv.indexOf(`--${name}`);
  if (index === -1 || !process.argv[index + 1]) {
    throw new Error(`Missing --${name}`);
  }
  return process.argv[index + 1];
}

function optionalArg(name) {
  const index = process.argv.indexOf(`--${name}`);
  return index === -1 ? undefined : process.argv[index + 1];
}

async function main() {
  const playwrightModule = arg('playwright-module');
  const edgeExecutable = arg('edge');
  const sourcePath = path.resolve(arg('source'));
  const outputDir = path.resolve(arg('output-dir'));
  const requestedTimes = optionalArg('times')
    ?.split(',')
    .map(value => Number(value.trim()))
    .filter(Number.isFinite);

  const { chromium } = require(playwrightModule);
  const browser = await chromium.launch({
    headless: true,
    executablePath: edgeExecutable,
  });

  try {
    const page = await browser.newPage();
    await page.setContent('<video id="source" muted playsinline></video><canvas id="frame"></canvas>');

    const videoDataUrl = `data:video/mp4;base64,${fs.readFileSync(sourcePath).toString('base64')}`;
    const extracted = await page.evaluate(async ({ videoDataUrl, requestedTimes }) => {
      const video = document.getElementById('source');
      const canvas = document.getElementById('frame');
      const ctx = canvas.getContext('2d', { alpha: false });

      video.preload = 'auto';
      video.src = videoDataUrl;
      await new Promise((resolve, reject) => {
        video.onloadedmetadata = resolve;
        video.onerror = () => reject(new Error('Unable to load video metadata'));
      });

      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
      const lastTime = Math.max(0.05, video.duration - 0.08);
      const requested = (requestedTimes?.length ? requestedTimes : [0.05, 1, 2, 3, 4, 5, lastTime])
        .map(value => Math.min(value, lastTime));

      const frames = [];
      for (const seconds of requested) {
        if (Math.abs(video.currentTime - seconds) > 0.001) {
          await new Promise((resolve, reject) => {
            video.onseeked = resolve;
            video.onerror = () => reject(new Error(`Unable to seek to ${seconds}`));
            video.currentTime = seconds;
          });
        }
        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
        frames.push({
          seconds,
          pngBase64: canvas.toDataURL('image/png').split(',')[1],
        });
      }

      return {
        duration: video.duration,
        width: video.videoWidth,
        height: video.videoHeight,
        frames,
      };
    }, { videoDataUrl, requestedTimes });

    fs.mkdirSync(outputDir, { recursive: true });
    const outputFrames = extracted.frames.map((frame, index) => {
      const filename = `frame_${String(index + 1).padStart(2, '0')}_${frame.seconds.toFixed(2).replace('.', 'p')}s.png`;
      const filePath = path.join(outputDir, filename);
      fs.writeFileSync(filePath, Buffer.from(frame.pngBase64, 'base64'));
      return { seconds: frame.seconds, filePath };
    });

    process.stdout.write(JSON.stringify({
      sourcePath,
      duration: extracted.duration,
      width: extracted.width,
      height: extracted.height,
      outputFrames,
    }, null, 2));
  } finally {
    await browser.close();
  }
}

main().catch(error => {
  console.error(error);
  process.exitCode = 1;
});
