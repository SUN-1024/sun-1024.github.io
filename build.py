#!/usr/bin/env python3
"""Build the static homepage from publications.json. No dependencies required."""
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
papers = json.loads((ROOT / 'publications.json').read_text(encoding='utf-8'))
esc = html.escape
featured_dois = [
    '10.1016/j.media.2026.104302',
    '10.1109/tmi.2026.3712240',
    '10.3389/fbioe.2024.1398237',
    '10.1109/access.2024.3372394',
    '10.3389/fbioe.2024.1504249',
]
code_links = {
    '10.1016/j.media.2026.104302':'https://github.com/SUN-1024/LAVIC',
    '10.3389/fbioe.2024.1398237':'https://github.com/SUN-1024/DA-TransUnet',
    '10.1109/access.2024.3372394':'https://github.com/SUN-1024/FKD-Med',
    '10.3389/fbioe.2024.1504249':'https://github.com/SUN-1024/MIPC-Net',
}

def publication(p):
    doi = p['doi'].lower()
    authors=[]
    for raw in p['authors'].split(';'):
        name=raw.strip()
        text=esc(name)
        authors.append(f'<strong>{text}</strong>' if name.lower()=='guanqun sun' else text)
    year=p['date'][:4]
    pubtype='Journal' if p['type']=='journal' else 'Conference'
    year_note=' · Online 2026; volume year 2027' if doi=='10.1016/j.media.2026.104302' else ''
    links=f'<a href="https://doi.org/{esc(p["doi"], quote=True)}">DOI ↗</a>'
    if doi in code_links: links+=f'<a href="{code_links[doi]}">Code ↗</a>'
    if doi=='10.1016/j.media.2026.104302': links+='<a href="https://doi.org/10.1016/j.media.2026.104383">Correction ↗</a>'
    return f'''<article class="publication"><div class="pub-meta"><div class="pub-year">{esc(year)}</div><div class="pub-type">{pubtype}</div></div><div><h3 class="pub-title">{esc(p['title'])}</h3><p class="pub-authors">{', '.join(authors)}</p><p class="pub-venue"><em>{esc(p['venue'])}</em>{year_note}</p><div class="pub-links">{links}</div></div></article>'''

by_doi={p['doi'].lower():p for p in papers}
featured=[by_doi[d] for d in featured_dois if d in by_doi]
other=[p for p in papers if p['doi'].lower() not in featured_dois]
journals=[p for p in other if p['type']=='journal']
conferences=[p for p in other if p['type']=='conference']
selected_html='\n'.join(map(publication,featured))
more_html='<h3 class="subheading">Journal publications</h3>'+''.join(map(publication,journals))+'<h3 class="subheading">Conference publications</h3>'+''.join(map(publication,conferences))

page=f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="Guanqun Sun is a lecturer at Hangzhou Medical College. His research includes medical image analysis, vision-language learning and privacy-aware AI.">
<meta name="theme-color" content="#fbfcfb">
<meta property="og:title" content="Guanqun Sun | Academic Homepage">
<meta property="og:description" content="Medical image analysis, vision-language learning and privacy-aware AI.">
<meta property="og:type" content="website">
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="assets/style.css">
<title>Guanqun Sun | Academic Homepage</title>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="masthead"><div class="mast-inner"><a class="brand" href="#top"><span class="mark">GS</span><span>Guanqun Sun</span></a><nav aria-label="Main navigation"><a href="#about">About</a><a href="#research">Research</a><a href="#publications">Publications</a><a href="#education">Education</a><a href="#contact">Contact</a></nav></div></header>
<div class="page" id="top">
<aside class="profile" aria-label="Researcher profile">
<div class="portrait-wrap"><img class="portrait" src="assets/portrait.jpg" alt="Portrait of Guanqun Sun" width="540" height="720"></div>
<div class="identity"><h2>Guanqun Sun <span class="cn-name">孙冠群</span></h2><p class="role">Lecturer</p><p class="affil">School of Information Engineering<br>Hangzhou Medical College</p><p class="location">Hangzhou, China</p></div>
<div class="profile-links"><a href="mailto:sun.guanqun@hmc.edu.cn"><span class="link-icon">@</span> Email</a><a href="https://scholar.google.com/citations?user=XSfz6tUAAAAJ"><span class="link-icon">◈</span> Google Scholar ↗</a><a href="https://orcid.org/0009-0008-4704-7072"><span class="link-icon">iD</span> ORCID ↗</a><a href="https://github.com/SUN-1024"><span class="link-icon">⌘</span> GitHub ↗</a></div>
</aside>
<main class="main" id="main">
<section class="hero" id="about"><div class="eyebrow">Researcher &nbsp;·&nbsp; Educator &nbsp;·&nbsp; Hangzhou, China</div><h1>Medical images,<br><em>more meaningful insights.</em></h1><p class="intro">I am a lecturer at the School of Information Engineering, Hangzhou Medical College. I received my Ph.D. in Information Science from the Japan Advanced Institute of Science and Technology (JAIST). My research brings together medical image analysis, vision–language learning, and privacy-aware artificial intelligence.</p><p class="intro" lang="zh-CN">我从事医学图像分析、医学影像与文本多模态学习，以及隐私保护人工智能研究。</p><div class="hero-actions"><a class="button" href="#publications">Explore my research <span aria-hidden="true">↓</span></a><a class="textlink" href="mailto:sun.guanqun@hmc.edu.cn">Get in touch ↗</a></div></section>
<section class="section" id="research"><div class="section-head"><div class="section-title"><span class="section-kicker">01 / Research</span><h2>Research interests</h2></div><span class="section-note" lang="zh-CN">研究方向</span></div><div class="research-grid"><article class="interest"><span class="interest-number">01</span><h3>Medical image analysis</h3><p>Image segmentation, boundary modelling, and chest imaging.</p></article><article class="interest"><span class="interest-number">02</span><h3>Vision–language learning</h3><p>Radiology report generation and longitudinal image understanding.</p></article><article class="interest"><span class="interest-number">03</span><h3>Privacy-aware AI</h3><p>Federated learning and knowledge distillation for medical imaging.</p></article></div></section>
<section class="section" id="news"><div class="section-head"><div class="section-title"><span class="section-kicker">02 / Updates</span><h2>Recent highlights</h2></div><span class="section-note" lang="zh-CN">近期成果</span></div><ul class="news"><li><time datetime="2026-09">2026.09</time><p>Our work on lesion-aware radiology report generation was published online in <em>Medical Image Analysis</em>. <a href="https://doi.org/10.1016/j.media.2026.104302">Read the paper ↗</a></p></li><li><time datetime="2026-07">2026.07</time><p>Our work on change radiology report generation was published online in <em>IEEE Transactions on Medical Imaging</em>. <a href="https://doi.org/10.1109/tmi.2026.3712240">Read the paper ↗</a></p></li></ul></section>
<section class="section" id="publications"><div class="section-head"><div class="section-title"><span class="section-kicker">03 / Publications</span><h2>Selected publications</h2></div><span class="section-note" lang="zh-CN">代表性论文</span></div><div class="pubs">{selected_html}</div><details class="more"><summary>View more publications</summary><div class="pubs">{more_html}</div></details></section>
<section class="section" id="education"><div class="section-head"><div class="section-title"><span class="section-kicker">04 / Education</span><h2>Education</h2></div><span class="section-note" lang="zh-CN">教育经历（节选）</span></div><div class="education"><div class="edu-row"><span class="edu-date">2021 — 2024</span><div><h3>Japan Advanced Institute of Science and Technology</h3><p>Ph.D. in Information Science</p></div></div><div class="edu-row"><span class="edu-date">2017 — 2019</span><div><h3>Hosei University</h3><p>M.Sc. in Computer and Information Sciences</p></div></div><div class="edu-row"><span class="edu-date">2017 — 2020</span><div><h3>Tianjin University</h3><p>M.Eng. in Software Engineering</p></div></div></div></section>
<section class="section" id="contact"><div class="section-head"><div class="section-title"><span class="section-kicker">05 / Contact</span><h2>Let’s connect</h2></div><span class="section-note" lang="zh-CN">联系我</span></div><div class="contact-box"><p>For research discussions and collaborations:<br><a href="mailto:sun.guanqun@hmc.edu.cn">sun.guanqun@hmc.edu.cn</a></p><a class="button" href="mailto:sun.guanqun@hmc.edu.cn">Send an email ↗</a></div></section>
<footer class="footer">© 2026 Guanqun Sun &nbsp;·&nbsp; Hangzhou Medical College</footer>
</main></div>
</body></html>'''
(ROOT/'index.html').write_text(page,encoding='utf-8')
print(f'Built index.html: {len(featured)} selected, {len(other)} additional publications')
