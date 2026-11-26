// The World Today - Thursday 26 November 2026 (Node 22, standard library only).
//
// Entry for make.fun news-image-20261126: "Sum up 26 November's world news
// in one image". The image itself lives in this repository as entry.png -
// a newspaper front page drawn by render.py (Python + Pillow) - and this
// program writes those exact bytes to /output/entry.png.
//
// Deterministic: no network, no clock, no randomness. Running it twice
// writes the same bytes both times.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const target = join(outDir, 'entry.png');

mkdirSync(outDir, { recursive: true });
const bytes = readFileSync(join(here, 'entry.png'));
writeFileSync(target, bytes);
console.log(`wrote ${target} (${bytes.length} bytes)`);
