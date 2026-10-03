import json
import html
from pathlib import Path

ROOT = Path(__file__).resolve().parent
data = json.loads((ROOT / 'content.json').read_text())
dist = ROOT / 'docs'
dist.mkdir(exist_ok=True)
esc = html.escape

def tr(en, zh, tag='span', attrs=''):
    return f'<{tag} data-en="{esc(en, quote=True)}" data-zh="{esc(zh, quote=True)}" {attrs}>{esc(en)}</{tag}>'

def authors(s):
    return esc(s).replace('Xicheng Gong', '<strong>Xicheng Gong</strong>')

contact_links = []
identity_links = []
for key, label_en, label_zh in [('gmail', 'Gmail', 'Gmail'), ('academic', 'PKU Email', '北大学生邮箱')]:
    email = data['contact'].get(key)
    if not email:
        continue
    href = 'mailto:' + esc(email, quote=True)
    label = tr(label_en, label_zh)
    identity_links.append(f'<a href="{href}">{label}</a>')
    contact_links.append(f'<a class="email" href="{href}">{label} · {esc(email)}</a>')

papers = []
for p in data['publications']:
    links = ''.join(f'<a href="{esc(link[1], quote=True)}" target="_blank" rel="noopener noreferrer">{esc(link[0])}</a>' for link in p['links'])
    venue = tr(p['venue'], p.get('venue_zh', p['venue']), 'div', 'class="venue"')
    role = tr(p['role_en'], p['role_zh'], 'p', 'class="authors"') if p.get('role_en') else ''
    author_line = f'<p class="authors">{authors(p["authors"])}</p>' if p.get('authors') and p.get('show_authors', True) else ''
    figure = f'<a class="paper-figure" href="{esc(p["figure"], quote=True)}" target="_blank" rel="noopener noreferrer"><img src="{esc(p["figure"], quote=True)}" alt="{esc(p["figure_alt"], quote=True)}" loading="lazy" decoding="async" width="{p["figure_width"]}" height="{p["figure_height"]}"></a>' if p.get('figure') else ''
    papers.append(f'''<article class="paper" id="{p['id']}">
      <div class="paper-index"><span>{p['year']}</span><span class="paper-short">{p['short']}</span>{figure}</div>
      <div class="paper-body">{venue}<h3>{esc(p['title'])}</h3>
      {author_line}{role}{tr(p['en'],p['zh'],'p','class="paper-description"')}
      {f'<div class="paper-links">{links}</div>' if links else ''}</div></article>''')

manuscripts = []
for p in data['manuscripts']:
    manuscripts.append(f'''<article class="manuscript" id="{p['id']}">
      <div class="manuscript-top"><span class="work-name">{p['short']}</span>{tr(p['status'],p['status_zh'],'span','class="submission"')}</div>
      <h3>{esc(p['title'])}</h3><p class="authors">{authors(p['authors'])}</p>
      {tr('* Equal contribution.','* 共同贡献。','p','class="equal"') if p.get('equal') else ''}
      {tr(p['en'],p['zh'],'p','class="paper-description"')}
      <p class="lab">{esc(p['lab'])}</p></article>''')

award_items = []
for a in data['awards']:
    detail = '<small>' + esc(a['detail']) + '</small>' if a['detail'] else ''
    award_items.append(f'<li><span class="award-year">{a["year"]}</span><div>{tr(a["en"],a["zh"])}{detail}</div></li>')
awards = ''.join(award_items)

template = '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Xicheng Gong | Embodied Intelligence</title>
  <meta name="description" content="Xicheng Gong, incoming PhD student at Peking University starting in 2027, advised by Yadong Mu. Research on model architectures for robotic manipulation and generalization across tasks, environments, and embodiments.">
  <meta name="robots" content="index, follow">
  <link rel="canonical" href="@@site_url@@">
  <meta name="theme-color" content="#1a5e9a">
  <link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='10' fill='%231a5e9a'/%3E%3Ctext x='32' y='43' text-anchor='middle' font-family='Georgia,serif' font-size='36' fill='white'%3EG%3C/text%3E%3C/svg%3E">
  <link rel="stylesheet" href="styles.css">
  <script src="app.js" defer></script>
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>
<div class="site-shell">
  <header class="topbar"><a class="wordmark" href="#about">About</a>
    <nav aria-label="Main navigation"><a href="#research">@@research_nav@@</a><a href="#education">@@education_nav@@</a><a href="#contact">@@contact_nav@@</a></nav>
    <button id="language" type="button" aria-label="Switch to Chinese">中文</button>
  </header>
  <main id="main">
    <section class="hero" id="about" aria-labelledby="name">
      <div class="identity"><div class="name-line"><h1 id="name" data-en="@@name_en@@" data-zh="@@name_zh@@">@@name_en@@</h1><span class="name-zh" data-language="en" lang="zh-CN">@@name_zh@@</span></div><p class="role">@@pku@@ · @@role@@</p>
      <div class="identity-links">@@identity_links@@<a href="https://github.com/gxccc123" target="_blank" rel="noopener noreferrer">GitHub</a></div></div>
      <div class="intro">
        <div data-language="en" lang="en">
          <p>I am an incoming PhD student at the <a href="https://www.aais.pku.edu.cn/" target="_blank" rel="noopener noreferrer">Academy for Advanced Interdisciplinary Studies</a>, Peking University, starting in 2027 under the supervision of <a href="http://www.muyadong.com" target="_blank" rel="noopener noreferrer">Prof. Yadong Mu</a>. I am currently completing my undergraduate studies in Intelligent Science and Technology at <a href="https://eecs.pku.edu.cn/" target="_blank" rel="noopener noreferrer">PKU EECS</a>.</p>
          <p>I previously collaborated with <a href="https://linsats.github.io/" target="_blank" rel="noopener noreferrer">Prof. Lin Shao</a> at <a href="https://www.nus.edu.sg/" target="_blank" rel="noopener noreferrer">NUS</a>, and I continue to work closely with <a href="https://songwxuan.github.io/" target="_blank" rel="noopener noreferrer">Wenxuan Song</a>. My research focuses on developing new model architectures for robotic manipulation. I aim to build robots that can learn transferable skills and generalize across tasks, environments, and embodiments.</p>
        </div>
        <div data-language="zh" lang="zh-CN" hidden>
          <p>我将于 2027 年进入北京大学<a href="https://www.aais.pku.edu.cn/" target="_blank" rel="noopener noreferrer">前沿交叉学科研究院</a>攻读博士学位，师从<a href="http://www.muyadong.com" target="_blank" rel="noopener noreferrer">穆亚东老师</a>。目前，我就读于<a href="https://eecs.pku.edu.cn/" target="_blank" rel="noopener noreferrer">北京大学信息科学技术学院（PKU EECS）</a>智能科学与技术专业。</p>
          <p>我曾与 <a href="https://www.nus.edu.sg/" target="_blank" rel="noopener noreferrer">NUS</a> 的 <a href="https://linsats.github.io/" target="_blank" rel="noopener noreferrer">Lin Shao 老师</a>开展研究合作，并与<a href="https://songwxuan.github.io/" target="_blank" rel="noopener noreferrer">宋文轩</a>保持密切合作。我的研究聚焦于机器人操作模型的新架构，致力于让机器人学习可迁移的技能，并实现跨任务、环境与机器人形态的泛化。</p>
        </div>
      </div>
    </section>
    <section class="research section" id="research" aria-labelledby="research-heading"><div class="section-heading"><div><h2 id="research-heading">@@publications@@</h2></div><p class="section-aside">2025 — 2026</p></div>
      <div class="papers">@@papers@@</div>
    </section>
    <section class="section background" id="education" aria-labelledby="education-heading"><div class="education"><h2 id="education-heading">@@education_nav@@</h2>
      <div class="education-entry"><span class="education-date">2023 — 2027</span><h3>@@pku@@</h3><p>@@degree@@</p><p class="education-note">@@graduation@@</p></div>
    </div></section>
    <section class="section contact" id="contact" aria-labelledby="contact-heading"><div><h2 id="contact-heading">@@contact_nav@@</h2><p>@@contact_desc@@</p></div><div class="contact-details">@@contact_links@@<a href="https://github.com/gxccc123" target="_blank" rel="noopener noreferrer">GitHub · gxccc123</a></div></section>
  </main>
  <footer><span data-en="© 2026 @@name_en@@" data-zh="© 2026 @@name_zh@@">© 2026 @@name_en@@</span><span>@@footer@@</span><a href="#about">@@backtop@@</a></footer>
</div>
</body></html>'''
copy = {
'research_nav':('Research','研究'), 'education_nav':('Education','教育背景'), 'contact_nav':('Contact','联系'),
'pku':('Peking University','北京大学'), 'role':('Incoming PhD student · Starting 2027','即将入学的博士生 · 2027 年入学'),
'cv':('CV / PDF','简历 / PDF'), 'intro_kicker':('Embodied intelligence','具身智能'),
'headline':('Learning to perceive, reason, and act.','学习感知、推理与行动。'),
'publications':('Selected papers','代表论文'), 'ongoing':('Ongoing research','在研工作'),
'manuscript_title':('Manuscripts & submissions','稿件与投稿'),
'status_note':('Submission statuses are based on my CV.','投稿状态依据简历记录。'),
'background':('Background','学术背景'), 'degree':('B.E. in Intelligent Science and Technology','智能科学与技术 · 工学学士'),
'graduation':('September 2023 – June 2027 (expected)','2023 年 9 月 — 2027 年 6 月（预计）'),
'honors':('Honors & awards','荣誉与奖励'), 'contact_title':('Get in touch.','学术交流。'),
'contact_desc':('Feel free to reach out for research discussions and collaborations.','欢迎通过邮件交流研究与合作。'),
'copy':('Copy email','复制邮箱'), 'footer':('Embodied intelligence · Peking University','具身智能 · 北京大学'), 'backtop':('Back to top','回到顶部')
}
for key,(en,zh) in copy.items(): template=template.replace('@@'+key+'@@',tr(en,zh))
for key,value in [('papers',''.join(papers)),('manuscripts',''.join(manuscripts)),('awards',awards),('contact_links',''.join(contact_links)),('identity_links',''.join(identity_links)),('site_url',esc(data['site_url'], quote=True))]: template=template.replace('@@'+key+'@@',value)
for key in ['name_en', 'name_zh']:
    template = template.replace('@@' + key + '@@', esc(data['name' if key == 'name_en' else 'name_zh'], quote=True))
assert '@@' not in template
(dist/'index.html').write_text(template)
print(json.dumps({'pages':1,'publications':len(data['publications']),'manuscripts':len(data['manuscripts']),'awards':len(data['awards'])}))
