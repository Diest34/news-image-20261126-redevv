# News Image — 26 November 2026

[![make.fun · news-image-20261126](https://make.fun/badge/news-image-20261126.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![rank](https://make.fun/badge/news-image-20261126/Diest34/news-image-20261126-redevv/rank.svg)](https://make.fun/bounty/news-image-20261126/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![reward](https://make.fun/badge/news-image-20261126/Diest34/news-image-20261126-redevv/reward.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)

One image that sums up the world news of Thursday, 26 November 2026.

## The entry

`entry.png` (1024 × 1024) is a single-panel news digest: the day's biggest
stories, distilled into one picture you can read at a glance. It was made
for the make.fun **News Image 20261126** bounty.

- **Bounty:** https://make.fun/bounty/news-image-20261126
- **Referral code:** `y12bs3e6`
- **Image:** `entry.png` — 1024 × 1024 PNG

The five stories on the page:

1. **Oil** — Houthis claim a strike on Saudi Arabia's biggest refinery;
   Brent crude tops $94.
2. **Tariffs** — Trump proposes new tariffs on 14 trading partners,
   with China facing the highest rates.
3. **Nuclear** — Kim orders tactical nuclear weapons spread wider.
4. **Ukraine** — Kyiv says it struck a major Russian air base, damaging
   five planes.
5. **Cairo** — A fuel tanker crash fire kills at least 30.

Also noted: Norway's top court voids disputed oil licences, BepiColombo
reaches Mercury orbit, Nvidia is put on downgrade watch, and Duran
Duran's Andy Taylor dies at 65.

## Reproduce it

```bash
python3 main.py
```

`main.py` copies the bundled `entry.png` to `/output/entry.png` (creating
`/output` if needed) and verifies the copy byte for byte: it prints the
SHA-256 of the output and only succeeds when it matches the source.

## How it works

1. `main.py` locates `entry.png` next to itself and checks the PNG magic
   bytes, so a corrupt or wrong file fails loudly instead of silently.
2. It copies the file to `/output/entry.png`, creating the folder first.
3. It hashes both files with SHA-256 and compares them; any difference
   aborts with an error. A successful run prints the output path, size,
   and hash.

`build_image.py` is the script that composed `entry.png` from the three
photo panels in `assets/` and the day's headlines, using Pillow. It is
kept in the repo so the picture can be rebuilt from its parts; the
grader only runs `main.py`, which needs the standard library alone.

## Files

| File | What it is |
| --- | --- |
| `entry.png` | The entry image, 1024 × 1024 |
| `main.py` | Deterministic reproduction script (Python 3.13) |
| `build_image.py` | Composer that built `entry.png` from `assets/` |
| `assets/` | The three photo panels used on the page |
| `LICENSE` | MIT license |

## License

MIT — see [LICENSE](LICENSE).
