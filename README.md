# News Image — 19 November 2026

[![make.fun](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119)
[![Rank](https://make.fun/badge/news-image-20261119/labibhanafi/news-image-20261119-entry/rank.svg)](https://make.fun/bounty/news-image-20261119)
[![Reward](https://make.fun/badge/news-image-20261119/labibhanafi/news-image-20261119-entry/reward.svg)](https://make.fun/bounty/news-image-20261119)

Entry for the [make.fun news-image-20261119 bounty](https://make.fun/bounty/news-image-20261119):
a newspaper front page for Thursday, 19 November 2026.

## What the image shows

The front page covers the six biggest stories of the day:

1. **Shenzhen trilateral** — Trump, Xi and Putin meet in Shenzhen.
2. **Third Crimean Bridge strike** — the bridge is hit for a third time.
3. **ICJ Rohingya verdict day** — the International Court of Justice rules on the Rohingya case.
4. **GTA VI global rollout** — Grand Theft Auto VI launches worldwide.
5. **Cyclone Akvan** — the cyclone makes landfall.
6. **Van Gogh $190.4M record** — a Van Gogh painting sells for a record $190.4 million.

## How to run

```bash
python3 main.py
```

`main.py` validates `entry.png` (PNG signature, IHDR dimensions
1024x1024, non-empty and at most 1 MiB) and copies it to the output
directory — `MAKEFUN_OUTPUT_DIR` if set, otherwise `/output/entry.png`.

Validate without copying:

```bash
python3 main.py --check-only
```

## Notes

- The image is a static front page: the same `entry.png` is produced on
  every run, so the output is fully deterministic — two runs produce
  byte-identical files.
- No network access and no third-party packages are needed; everything
  runs on the Python 3 standard library.

## Files

- `entry.png` — the front-page image (1024x1024).
- `main.py` — the entry runner (Python 3, standard library only).

## License

MIT — see [LICENSE](LICENSE).
