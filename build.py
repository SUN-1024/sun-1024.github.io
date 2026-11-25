#!/usr/bin/env python3
"""Generate the AcadHomepage-style static site from publications.json."""
from pathlib import Path
import html
import json

ROOT = Path(__file__).resolve().parent
publications = json.loads((ROOT / 'publications.json').read_text(encoding='utf-8'))
e = html.escape

def authors_html(authors):
    rendered=[]
    for a in authors:
        text=e(a['name'])
        if a['name'].casefold() == 'guanqun sun':
            text=f'<strong>{text}</strong>'
        marks=('†' if a.get('equal') else '') + ('*' if a.get('corresponding') else '')
        rendered.append(text + (f'<sup>{marks}</sup>' if marks else ''))
    return ', '.join(rendered)

def links(p):
    parts=[]
    if p['doi']:
        parts.append(f'<a href="https://doi.org/{e(p["doi"], quote=True)}">Paper</a>')
    if p['doi'].lower() == '10.1016/j.media.2026.104302':
        parts.append('<a href="https://doi.org/10.1016/j.media.2026.104383">Correction</a>')
    return ' '.join('['+part+']' for part in parts)

def venue(p):
    if p['status']=='accepted': return f'<em>{e(p["venue"])}</em> · Accepted, 2026'
    if p['doi'].lower()=='10.1016/j.media.2026.104302':
        return f'<em>{e(p["venue"])}</em>, 115, 104302, 2027 (online 2026)'
    return f'<em>{e(p["venue"])}</em>, {e(p["date"][:4])}'

def card(p):
    title=e(p['title']); src=e(p['figure'],quote=True)
    title_html=f'<a href="https://doi.org/{e(p["doi"],quote=True)}">{title}</a>' if p['doi'] else f'<strong>{title}</strong>'
    points=''.join('<li>'+e(x)+'</li>' for x in p['summary'])
    cc=' · <a href="https://creativecommons.org/licenses/by/4.0/">CC BY 4.0</a>' if p.get('cc_by') else ''
    credit='Figure from the accepted manuscript' if p['status']=='accepted' else 'Figure from the paper'
    award=f'<p><span class="award-tag">★ {e(p["recognition"])}</span></p>' if p.get('recognition') else ''
    return f'''<div class="paper-box"><div class="paper-box-image"><div><div class="badge">{e(p['badge'])}</div><a href="{src}" target="_blank" rel="noopener" aria-label="Open a larger figure for {title}"><img src="{src}" alt="Research figure for {title}" loading="lazy"></a><div class="figure-credit">{credit}{cc}</div></div></div><div class="paper-box-text"><p>{title_html} {links(p)}</p>{award}<p>{authors_html(p['authors'])}</p><p class="publication-venue">{venue(p)}</p><ul>{points}</ul></div></div>'''

def conference_card(p):
    title=e(p['title'])
    doi=e(p['doi'],quote=True)
    award=e(p['conference_award'])
    award_url=e(p['award_url'],quote=True)
    points=''.join('<li>'+e(point)+'</li>' for point in p.get('conference_summary',[]))
    return f"""<article class="conference-paper"><p><a href="https://doi.org/{doi}">{title}</a> [<a href="https://doi.org/{doi}">Paper</a>]</p><p>{authors_html(p['authors'])}</p><p class="publication-venue">{venue(p)}</p><p><a class="award-tag" href="{award_url}" title="Award details from Hangzhou Medical College">★ {award} ↗</a></p><ul>{points}</ul></article>"""

def compact(p):
    title=e(p['title']); anchor=f'<a href="https://doi.org/{e(p["doi"],quote=True)}">{title}</a>' if p['doi'] else title
    extra=(' '+links(p)) if p.get('figure') else ''
    return f'<li>{anchor}{extra}. {authors_html(p["authors"])}. {venue(p)}.</li>'

order={'vision':['clamp','lavic','radar'],'segmentation':['da-transunet','garden']}
groups=[]
heads={'vision':'🩻 Medical Vision–Language Learning','segmentation':'🩺 Medical and Plant Image Segmentation','privacy':'🔐 Federated and Privacy-Aware Learning','other':'🧠 Other Health and AI Applications'}
for topic,names in order.items():
    entries=[next(p for p in publications if p.get('figure','').endswith('/'+name+'.png')) for name in names]
    groups.append(f'<h2>{heads[topic]}</h2>'+''.join(card(p) for p in entries))
conference_awards=sorted((p for p in publications if p.get('conference_award')), key=lambda p:p['date'], reverse=True)
groups.insert(1, '<h2 id="award-conference-papers">🏆 Award-Winning Conference Papers</h2>'+''.join(conference_card(p) for p in conference_awards))
featured_figures={f'assets/papers/{name}.png' for names in order.values() for name in names}
other=[p for p in publications if p.get('figure') not in featured_figures and not p.get('conference_award')]

content='''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="description" content="Guanqun Sun, Hangzhou Medical College: medical image analysis, vision-language learning and privacy-aware AI."><meta property="og:title" content="Guanqun Sun (孙冠群) - Homepage"><meta property="og:description" content="Research in medical image analysis, report generation and privacy-aware AI."><meta property="og:type" content="website"><link rel="canonical" href="https://sun-1024.github.io/"><link rel="icon" href="assets/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="assets/acadhomepage.css"><link rel="stylesheet" href="assets/style.css"><title>Guanqun Sun (孙冠群) - Homepage</title></head>
<body><a class="skip-link" href="#about-me">Skip to content</a>
<header class="masthead"><div class="masthead__inner-wrap"><div class="masthead__menu"><nav class="greedy-nav" aria-label="Main navigation"><ul class="visible-links"><li class="masthead__menu-item masthead__menu-item--lg masthead__menu-home-item"><a href="#about-me">Homepage</a></li><li class="masthead__menu-item"><a href="#about-me">About Me</a></li><li class="masthead__menu-item"><a href="#news">News</a></li><li class="masthead__menu-item"><a href="#publications">Publications</a></li><li class="masthead__menu-item"><a href="#educations">Educations</a></li><li class="masthead__menu-item"><a href="#contact">Contact</a></li></ul></nav></div></div></header>
<main id="main"><aside class="sidebar sticky" aria-label="Researcher profile"><div class="profile_box"><div class="author__avatar"><img src="assets/portrait.jpg" alt="Guanqun Sun teaching" width="540" height="720"></div><div class="author__content"><h3 class="author__name">Guanqun Sun (孙冠群)</h3><p class="author__bio">Hangzhou Medical College<br><span lang="zh-CN">杭州医学院</span></p><p class="author__bio">Lecturer</p></div><div class="author__urls-wrapper"><ul class="author__urls social-icons"><li><span class="profile-icon" aria-hidden="true">●</span> Hangzhou, China</li><li><a href="mailto:sun.guanqun@hmc.edu.cn"><span class="profile-icon" aria-hidden="true">✉</span> Email</a></li><li><a href="https://github.com/SUN-1024"><span class="profile-icon" aria-hidden="true">◆</span> GitHub</a></li><li><a href="https://scholar.google.com/citations?user=XSfz6tUAAAAJ"><span class="profile-icon" aria-hidden="true">▣</span> Google Scholar</a></li><li><a href="https://orcid.org/0009-0008-4704-7072"><span class="profile-icon" aria-hidden="true">iD</span> ORCID</a></li></ul></div></div></aside>
<article class="page"><div class="page__inner-wrap"><section class="page__content"><div id="about-me" class="anchor"></div>
<p>I am a lecturer at the School of Information Engineering, Hangzhou Medical College. I received my Ph.D. in Information Science from the Japan Advanced Institute of Science and Technology (JAIST).</p>
<p>My research interests include medical image analysis, vision–language learning and radiology report generation, and privacy-aware machine learning. I work on models that connect medical images with clinical language, capture changes across images, and support collaborative learning. <strong>Feel free to contact me if you are interested in these topics.</strong></p>
<h1 id="news">🔥 News</h1><ul><li><strong>2026.11:</strong> Our paper on context-predictive representation learning for surgical report generation was accepted by <em>Medical Image Analysis</em>.</li><li><strong>2026.09:</strong> Our paper on lesion-aware radiology report generation was published online in <em>Medical Image Analysis</em>. [<a href="https://doi.org/10.1016/j.media.2026.104302">Paper</a>]</li><li><strong>2026.07:</strong> Our paper on change radiology report generation was published online in <em>IEEE Transactions on Medical Imaging</em>. [<a href="https://doi.org/10.1109/tmi.2026.3712240">Paper</a>]</li></ul>
<h1 id="publications">📝 Publications</h1><p>Selected publications are grouped by research direction. Click a figure to view it at a larger size. More work is listed below and on <a href="https://scholar.google.com/citations?user=XSfz6tUAAAAJ">Google Scholar</a>.</p><p class="author-key">† Equal contribution; * corresponding author.</p>
''' + '\n'.join(groups) + '''
<h2 id="other-publications">📄 Other Publications</h2><ol class="other-publications">''' + ''.join(map(compact,other)) + '''</ol>
<h1 id="educations">📖 Educations</h1><ul class="education-list"><li>Ph.D. in Information Science, Japan Advanced Institute of Science and Technology (JAIST).</li><li>M.Sc. in Computer and Information Sciences, Hosei University.</li><li>M.Eng. in Software Engineering, Tianjin University.</li><li>B.Eng. in Mechanical Engineering, Shanghai University of Electric Power.</li></ul>
<h1 id="contact">✉️ Contact</h1><p>School of Information Engineering, Hangzhou Medical College, Hangzhou, China.<br>Email: <a href="mailto:sun.guanqun@hmc.edu.cn">sun.guanqun@hmc.edu.cn</a></p>
<footer class="site-footer">© 2026 Guanqun Sun · Style based on <a href="https://github.com/RayeRen/acad-homepage.github.io">AcadHomepage</a>.</footer>
</section></div></article></main></body></html>'''
(ROOT/'index.html').write_text(content,encoding='utf-8')
print(f'Built homepage: {len(publications)} papers, {len(featured_figures)} illustrated, {len(conference_awards)} award-winning conference papers, {len(other)} additional')
