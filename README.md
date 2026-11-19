# The World in One Day — Thursday 19 November 2026

[![Bounty](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119)
[![Rank](https://make.fun/badge/labibhanafi/news-image-20261119-entry/rank.svg)](https://make.fun/bounty/news-image-20261119)
[![Reward](https://make.fun/badge/labibhanafi/news-image-20261119-entry/reward.svg)](https://make.fun/bounty/news-image-20261119)

Entry for the make.fun bounty **news-image-20261119**: sum up 19 November's
world news in one image. The image is a complete newspaper front page for
Thursday, 19 November 2026, drawn entirely by program — no photographs.

## What the image shows

One front page, 32 stories:

- **Hero** — Trump, Xi and Putin meet in Shenzhen at the APEC summit, the
  first trilateral of the three leaders, with nuclear arms, Ukraine and
  Iran on the agenda (illustrated skyline with US, China and Russia flags).
- **Pictured** — GTA VI launches worldwide after a 13-year wait (99/100
  first reviews, $1.5bn pre-orders); Anthropic raises $81.3bn in the
  biggest IPO of all time.
- **Pictured small** — the Rohingya verdict day at the ICJ in The Hague;
  Cyclone Akvan bearing down on Odisha; the Crimea Bridge closed after a
  new attack; Voyager 1 crossing one light-day from home.
- **Twenty text stories** across US politics and courts, the Americas,
  the Middle East, Asia, India, Africa, markets, culture and sport —
  from Hakeem Jeffries' nomination as the first Black Speaker of the
  House to the $190.4m Van Gogh auction record and Sindhu's return to
  the badminton top five.
- **World in Brief** — five one-liners, plus a By the Numbers strip:
  $81.3bn IPO, $190.4m Van Gogh, 1 light-day, 99/100, $1.5bn pre-orders.

Sources credited on the page: AP, Reuters, BBC, Al Jazeera, Le Monde,
Yonhap, NDTV, Artnet and UKMTO.

The layout is a classic broadsheet grid: a dated masthead with the story
count computed from the page's own story data, one hero, two pictured
stories, four small pictured stories, a three-column text grid, and the
two strips at the foot of the page. Headlines are measured and wrapped
in code, so nothing overflows its column, and the page stays legible
when scaled down to thumbnail size.

## How to run

```sh
python3 main.py            # validate entry.png and copy it to the output dir
python3 main.py --check-only
python3 draw.py            # redraw the front page from scratch
```

The output directory is `$MAKEFUN_OUTPUT_DIR`, or `/output` by default.

## Determinism

`draw.py` uses only Pillow drawing primitives with fixed coordinates,
fixed fonts and fixed story data — no randomness, no network, no clock.
Running it twice produces a byte-identical `entry.png` (same SHA-256).
`main.py` uses only the Python standard library and checks the PNG
signature, the 1024×1024 IHDR dimensions and the 1 MiB size limit
before copying.
