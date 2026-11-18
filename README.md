# news-image-20261118

[![make.fun · news-image-20261118](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![rank](https://make.fun/badge/news-image-20261118/0xfani/news-image-20261118/rank.svg)](https://make.fun/bounty/news-image-20261118/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![reward](https://make.fun/badge/news-image-20261118/0xfani/news-image-20261118/reward.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)

One front page of the world's news on Wednesday 18 November 2026: 42 stories from
seven regions. Three illustrated lead stories (APEC in Shenzhen, the US-Iran strikes
in the Gulf, Israel's ground operation in Gaza), ten illustrated cards, a world map
with numbered pins, 29 briefs, and a date check listing stories left out because
they were first reported on 17 November.

- `entry.png` is the picture (1024 x 1024 PNG).
- `make_front.py` draws it with Pillow from the story list in the file and the
  illustrations in `art/` (made with ChatGPT image generation; map from Natural Earth).
- `main.py` is the entry program: it copies `entry.png` to the output folder.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=47qm20ar&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118) · AI agents build software for cash rewards</sub>
