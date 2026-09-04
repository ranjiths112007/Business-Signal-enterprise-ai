const fs = require("fs");
const path = require("path");

const root = path.resolve(__dirname, "..");
const publicDir = path.join(root, "public");
const assets = [
  "Business Signal Neon Analytics Branding.png",
  "Neon Business Signal Emblem.png",
];

fs.mkdirSync(publicDir, { recursive: true });

for (const asset of assets) {
  const source = path.join(root, asset);
  const target = path.join(publicDir, asset);
  if (fs.existsSync(source)) {
    fs.copyFileSync(source, target);
    console.log(`Copied ${asset} -> public/`);
  } else {
    console.warn(`Asset not found: ${asset}`);
  }
}
