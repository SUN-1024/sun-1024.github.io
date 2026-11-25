# Guanqun Sun · Academic Homepage

Personal academic homepage using the stylesheet and paper layout of [AcadHomepage](https://github.com/RayeRen/acad-homepage.github.io). The template license is in `LICENSE.acadhomepage`.

## 更新论文

编辑 `publications.json`。图文展示的论文由 `build.py` 中的 `order` 控制，并使用 `badge`、`figure` 和 `summary` 字段；含 `conference_award`、`award_url` 和 `conference_summary` 的论文显示在获奖会议论文区，并使用 `badge`、`figure` 和 `figure_credit` 字段展示图片及来源，其余论文显示在 Other Publications。新增图片放在 `assets/papers/`。然后运行：

```bash
python3 build.py
```

`index.html` 是生成的网页。分组和代表论文顺序在 `build.py` 的 `order` 中维护。更新简介、新闻和教育经历时，修改 `build.py` 中的相应文字并重新运行。

## 本地预览与发布

在本目录运行 `python3 -m http.server 8765`，然后访问 `http://localhost:8765/`。将更改推送到 GitHub 的 `main` 分支后，GitHub Pages 会自动发布。只将打算公开的文件放入此目录。
