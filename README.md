# The World Today — Thursday 26 November 2026

[![make.fun · news-image-20261126](https://make.fun/badge/news-image-20261126.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![rank](https://make.fun/badge/news-image-20261126/Kopler12/kopler-news-image-20261126/rank.svg)](https://make.fun/bounty/news-image-20261126/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![reward](https://make.fun/badge/news-image-20261126/Kopler12/kopler-news-image-20261126/reward.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)

One image that sums up the world's news of **Thursday 26 November 2026** — a
newspaper front page with the six stories that defined the day, drawn
programmatically with Python + Pillow (`render.py`) and shipped as `entry.png`.

## The six stories

1. **Middle East · Ras Tanura** — The Houthis claim a strike on Saudi Arabia's
   biggest refinery; satellite images show thick black smoke over Ras Tanura as
   Brent crude jumps and the Saudi-led coalition says it downed four drones.
2. **Shipping · Strait of Hormuz** — Two tankers hit naval mines; Iran's navy
   says an LNG carrier and an oil tanker struck mines and caught fire, and that
   the strait stays shut until its demands are met.
3. **Gaza · Ceasefire under strain** — An Israeli airstrike in Gaza City kills
   Mohammad Abuelouf, Hamas' internal security chief for northern Gaza, with his
   wife and two daughters — the second senior Hamas security official killed in
   a day.
4. **Ukraine · The oil war** — Kyiv's drones strike Russian oil refineries again
   and Moscow vows retaliation, as Russia's own figures show nearly 500,000
   people lost in the war.
5. **Colombia · Cartagena** — After 17 hours, police storm a Cartagena
   supermarket and free 20 people held by gunmen after a failed
   armoured-truck robbery.
6. **Asia · Bangladesh** — Bangladesh raises the minimum monthly wage for
   entry-level garment workers by 36%, a win for millions in the world's
   second-biggest clothing exporter.

Compiled from wire reports (Reuters, AP, Xinhua) published on 26 November 2026.

## How it works

`main.ts` (Node 22, standard library only) copies `entry.png` to
`/output/entry.png`. The program runs with no network and writes the same bytes
on every run. The image is a 1024×1024 PNG, 114,928 bytes — inside the
competition's 1 MiB / 1024×1024 limits.

```sh
# regenerate the image
python3 render.py

# run the entry locally
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

## Entry

- Competition: [news-image-20261126](https://make.fun/bounty/news-image-20261126)
  — "Sum up 26 November's world news in one image"
- License: MIT
