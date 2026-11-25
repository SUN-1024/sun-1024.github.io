# Guanqun Sun · Academic Homepage

A static academic homepage designed for GitHub Pages.

## 更新论文

编辑 `publications.json`，新增或修改论文条目，然后运行：

```bash
python3 build.py
```

生成的 `index.html` 是发布使用的网页。代表作的顺序和代码链接在 `build.py` 开头修改。修改其他简介、教育经历和联系信息，也可直接编辑 `build.py` 对应内容，之后重新运行。

## 更新头像

用新的照片替换 `assets/portrait.jpg`。建议移除照片元数据后上传。

## 本地预览

在本目录运行 `python3 -m http.server 8765`，然后打开 `http://localhost:8765/`。页面不需要安装依赖。

## 发布

推送 `main` 分支后，GitHub Pages 会自动更新。请只将打算公开的文件放入此目录。
