import { chromium } from "file:///C:/Users/Brandon_ChangChien/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright/index.mjs";
import fs from "node:fs";
import path from "node:path";
import { pathToFileURL } from "node:url";

const videoPath = process.argv[2];
const outputDir = process.argv[3];
if (!videoPath || !outputDir) throw new Error("video path and output dir required");

fs.mkdirSync(outputDir, { recursive: true });
const browser = await chromium.launch({
  headless: true,
  executablePath: "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe",
});
const page = await browser.newPage({ viewport: { width: 900, height: 1600 } });
await page.goto(pathToFileURL(videoPath).href, { waitUntil: "load" });
await page.waitForFunction(() => {
  const video = document.querySelector("video");
  return video && Number.isFinite(video.duration) && video.duration > 0;
});

const metadata = await page.locator("video").evaluate((video) => ({
  duration: video.duration,
  width: video.videoWidth,
  height: video.videoHeight,
}));

const times = [0, 0.5, 1, 2, 4, 7, 10, 13, Math.max(0, metadata.duration - 0.2)];
for (let i = 0; i < times.length; i += 1) {
  const time = Math.min(times[i], Math.max(0, metadata.duration - 0.05));
  await page.locator("video").evaluate(async (video, seekTime) => {
    await new Promise((resolve, reject) => {
      const done = () => resolve();
      const fail = () => reject(new Error("video seek failed"));
      video.addEventListener("seeked", done, { once: true });
      video.addEventListener("error", fail, { once: true });
      video.currentTime = seekTime;
    });
    video.pause();
  }, time);
  await page.locator("video").screenshot({ path: path.join(outputDir, `frame_${String(i).padStart(2, "0")}_${time.toFixed(2)}s.png`) });
}

process.stdout.write(JSON.stringify(metadata));
await browser.close();
