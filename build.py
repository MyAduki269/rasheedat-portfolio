from pathlib import Path
from html import escape as e
import json
from projects import PROJECTS

ROOT=Path(__file__).parent
OUT=ROOT/'dist'
OUT.mkdir(exist_ok=True)
LABELS={'BA':'Business Analysis','PM':'Project Management','DA':'Data Analytics'}
ARROW='<svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M5 12h14m-6-6 6 6-6 6" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/></svg>'
SEARCH='<svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><circle cx="10.7" cy="10.7" r="6.7" stroke="currentColor" stroke-width="1.7"/><path d="m16 16 4 4" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"/></svg>'
LOCK='<svg viewBox="0 0 20 20" fill="none" aria-hidden="true"><rect x="4.5" y="8.5" width="11" height="8" rx="2" stroke="currentColor"/><path d="M7 8V6a3 3 0 0 1 6 0v2" stroke="currentColor"/><circle cx="10" cy="12.5" r="1" fill="currentColor"/></svg>'

def art(p):
    # Code-native illustrations describe each project's analytical structure.
    v=p['visual']
    defs='<defs><pattern id="grid-'+p['slug']+'" width="24" height="24" patternUnits="userSpaceOnUse"><path d="M24 0H0V24" fill="none" stroke="currentColor" opacity=".12"/></pattern></defs>'
    base=f'<rect width="600" height="300" fill="url(#grid-{p["slug"]})"/><circle cx="490" cy="40" r="140" fill="currentColor" opacity=".035"/>'
    if v=='hr':
        content='<path d="M138 83h95q22 0 22 22v43m-117 77h95q22 0 22-22v-55m210-65h-95q-22 0-22 22v43m117 77h-95q-22 0-22-22v-55" fill="none" stroke="currentColor" opacity=".45"/>'
        for x,y,label in [(65,58,'PEOPLE'),(65,200,'PROCESS'),(418,58,'DATA'),(418,200,'TECHNOLOGY')]:
            content+=f'<rect x="{x}" y="{y}" width="118" height="45" rx="8" fill="#123c49" stroke="currentColor" stroke-opacity=".35"/><text x="{x+59}" y="{y+28}" text-anchor="middle" font-size="11" letter-spacing="1">{label}</text>'
        content+='<rect x="233" y="108" width="134" height="81" rx="12" fill="#214c50" stroke="currentColor"/><circle cx="300" cy="131" r="5" fill="currentColor"/><text x="300" y="157" text-anchor="middle" fill="#f4f4ed" font-size="14" font-weight="600">INTEGRATED HR</text><text x="300" y="175" text-anchor="middle" font-size="9" letter-spacing="1.5">ONE WORKFORCE VIEW</text>'
    elif v=='bank':
        content='<rect x="80" y="45" width="440" height="224" rx="12" fill="#142d39" stroke="currentColor" stroke-opacity=".25"/><path d="M80 83h440" stroke="currentColor" opacity=".2"/><circle cx="100" cy="64" r="3" fill="currentColor"/><text x="115" y="68" font-size="10" letter-spacing="2">BANKING INTELLIGENCE</text>'
        for i,l in enumerate(['CUSTOMERS','ACCOUNTS','TRANSACTIONS']):
            x=101+i*134
            content+=f'<rect x="{x}" y="103" width="122" height="49" rx="5" fill="#233b42"/><text x="{x+10}" y="123" font-size="8" letter-spacing="1">{l}</text><path d="M{x+10} 137h45" stroke="currentColor" stroke-width="3"/>'
        content+='<path d="M104 234h200M104 172v62" stroke="currentColor" opacity=".25"/><path d="m105 223 33-15 31 5 35-27 31 9 35-23 31 5" fill="none" stroke="currentColor" stroke-width="2"/><circle cx="403" cy="204" r="34" stroke="#294650" stroke-width="14" fill="none"/><path d="M403 170a34 34 0 0 1 28 53" stroke="currentColor" stroke-width="14" fill="none"/><text x="403" y="208" text-anchor="middle" font-size="9">BI</text>'
    elif v=='routes':
        content='<path d="M0 223 151 223 224 151 366 151 450 68 600 68M73 0v83l151 68v149M450 300v-81l-84-68V0" fill="none" stroke="currentColor" opacity=".12" stroke-width="17"/><path d="m98 223 126-72h142l84-83" fill="none" stroke="currentColor" stroke-width="2" stroke-dasharray="6 7"/>'
        for x,y,label in [(98,223,'LAGOS'),(224,151,'OYO'),(366,151,'ANAMBRA'),(450,68,'DELIVERY')]:
            content+=f'<circle cx="{x}" cy="{y}" r="16" fill="#1f3b42" stroke="currentColor"/><circle cx="{x}" cy="{y}" r="4" fill="currentColor"/><text x="{x}" y="{y+34}" text-anchor="middle" font-size="10" letter-spacing="1.5">{label}</text>'
    elif v=='fleet':
        content='<path d="M95 150h410" stroke="currentColor" opacity=".4" stroke-dasharray="4 7"/>'
        for i,(label,sub) in enumerate([('REQUEST','Travel portal'),('APPROVE','Controls retained'),('ASSIGN','Fleet platform'),('RECORD','Central visibility')]):
            x=88+i*140
            content+=f'<rect x="{x-43}" y="110" width="86" height="78" rx="10" fill="#173e4c" stroke="currentColor" stroke-opacity=".45"/><circle cx="{x}" cy="137" r="10" fill="none" stroke="currentColor"/><path d="m{x-4} 137 3 3 6-7" stroke="currentColor" fill="none"/><text x="{x}" y="171" text-anchor="middle" font-size="9" letter-spacing="1">{label}</text><text x="{x}" y="213" text-anchor="middle" font-size="9" opacity=".8">{sub}</text>'
    elif v=='survey':
        content='<rect x="104" y="50" width="199" height="214" rx="10" fill="#173e4c" stroke="currentColor" stroke-opacity=".3"/><text x="126" y="82" font-size="10" letter-spacing="2">LISTEN. LEARN. ACT.</text>'
        for i,(t,w) in enumerate([('Awareness',124),('Demographics',98),('Service priorities',145)]):
            y=111+i*48
            content+=f'<text x="126" y="{y}" font-size="9">{t}</text><rect x="126" y="{y+10}" width="153" height="7" rx="3" fill="#284e59"/><rect x="126" y="{y+10}" width="{w}" height="7" rx="3" fill="currentColor" opacity=".7"/>'
        content+='<circle cx="407" cy="149" r="66" fill="none" stroke="#234955" stroke-width="17"/><path d="M407 83a66 66 0 0 1 32 124" fill="none" stroke="currentColor" stroke-width="17"/><text x="407" y="148" text-anchor="middle" font-size="25" fill="#f4f4ed">42%</text><text x="407" y="166" text-anchor="middle" font-size="9">unaware of CAA</text><text x="407" y="246" text-anchor="middle" font-size="9" opacity=".8">PROJECT SURVEY SAMPLE</text>'
    else:
        return '<div class="project-art caa-photo" aria-hidden="true"><span class="photo-label">NEW CANADIANS · NEW POSSIBILITIES</span></div>'
    return f'<div class="project-art {p["color"]}" aria-hidden="true"><svg viewBox="0 0 600 300" fill="currentColor" xmlns="http://www.w3.org/2000/svg">{defs}{base}{content}</svg></div>'

def badges(p): return ''.join(f'<span class="badge {c.lower()}">{c if c!="DA" else "DATA"}</span>' for c in p['categories'])
def tags(items): return ''.join(f'<span class="tag">{e(x)}</span>' for x in items)
def link(p): return f'/projects/{p["slug"]}/'
def card(p,i=0):
 return f'''<article class="project-card" data-slug="{p['slug']}" data-category="{' '.join(p['categories'])}" data-tools='{e(json.dumps(p['tools']),quote=True)}' data-skills='{e(json.dumps(p['skills']),quote=True)}' data-search="{e(' '.join([p['company'],p['subtitle'],p['summary'],p['sector']]+p['tools']+p['skills']),quote=True)}">
 <a class="art-link" href="{link(p)}" aria-label="Read {e(p['company'])}: {e(p['subtitle'])}">{art(p)}<span class="art-open">{ARROW}</span></a>
 <div class="card-body"><div class="card-topline"><span class="sector">{e(p['sector'])}</span><div class="badges">{badges(p)}</div></div>
 <h3><a href="{link(p)}">{e(p['company'])}</a></h3><p class="card-subtitle">{e(p['subtitle'])}</p><p class="card-summary">{e(p['summary'])}</p><div class="card-tools">{tags(p['tools'])}</div>
 <div class="card-actions"><a class="text-link" href="{link(p)}">Explore case study {ARROW}</a><button class="summary-button" data-summary="{p['slug']}" aria-label="Quick summary of {e(p['company'])}: {e(p['subtitle'])}"><span>Quick view</span><span aria-hidden="true">＋</span></button></div></div></article>'''

def header(detail=False):
 return f'''<a class="skip-link" href="#main">Skip to content</a><header class="site-header"><div class="header-inner"><a class="brand" href="/" aria-label="Rasheedat Animashaun home"><span class="monogram">ra<span>.</span></span><span class="brand-name">Rasheedat Animashaun<small>DATA · BUSINESS · PROJECTS</small></span></a><nav aria-label="Main navigation"><a href="{'/' if detail else ''}#work" class="{'current' if not detail else ''}">Selected work</a><a href="{'/' if detail else ''}#approach">My approach</a><a href="{'/' if detail else ''}#about">About</a></nav><span class="private-label" title="This website is privately hosted">{LOCK} Private portfolio</span></div></header>'''
def footer():
 return f'''<footer class="site-footer"><div class="wrap"><a class="footer-name" href="/">Rasheedat Animashaun<span>Data. Business. Projects. Impact.</span></a><div class="footer-right"><span>{LOCK} Privately hosted</span><a href="#top">Back to top ↑</a></div></div></footer>'''
def shell(title,desc,body,detail=False):
 return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#0B3041"><meta name="robots" content="noindex,nofollow"><meta name="description" content="{e(desc,quote=True)}"><title>{e(title)} | Rasheedat Animashaun</title><link rel="icon" href="/assets/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="/style.css"><script src="/app.js" defer></script></head><body id="top">{header(detail)}{body}{footer()}</body></html>'''

def hub():
 tools=sorted({t for p in PROJECTS for t in p['tools']})
 skills=sorted({s for p in PROJECTS for s in p['skills']})
 options=lambda values:''.join(f'<option value="{e(x,quote=True)}">{e(x)}</option>' for x in values)
 tabs=''.join(f'<button class="filter-tab" data-discipline="{c}" aria-pressed="false">{LABELS[c]} <span>{sum(c in p["categories"] for p in PROJECTS)}</span></button>' for c in ['BA','PM','DA'])
 body=f'''<main id="main"><section class="hero wrap" aria-labelledby="hero-title"><div class="hero-copy"><p class="eyebrow"><span></span> THE PORTFOLIO OF RASHEEDAT ANIMASHAUN</p><h1 id="hero-title">Turning complexity<br>into <em>clear direction.</em></h1><p class="hero-description">I connect data, people and business needs to shape practical solutions and purposeful project delivery.</p><div class="hero-actions"><a class="button primary" href="#work">Explore my work {ARROW}</a><a class="quiet-link" href="#about">A little about me <span aria-hidden="true">↗</span></a></div><div class="hero-disciplines"><span>Business Analysis</span><span>Project Management</span><span>Data Analytics</span></div></div>
 <div class="hero-canvas" aria-label="From business questions to insight and action"><div class="canvas-top"><span>FROM QUESTION TO CLARITY</span><span class="canvas-dot"></span></div><div class="canvas-orbit orbit-one"></div><div class="canvas-orbit orbit-two"></div><div class="canvas-axis"></div><div class="canvas-core"><span class="core-symbol">↗</span><span>INSIGHT<br><strong>INTO ACTION</strong></span></div><div class="canvas-note note-data"><span class="note-icon">▥</span><div>Find the signal<small>Data & evidence</small></div></div><div class="canvas-note note-people"><span class="note-icon">◎</span><div>Understand the need<small>People & processes</small></div></div><div class="canvas-note note-delivery"><span class="note-icon">✓</span><div>Shape the next step<small>Strategy & delivery</small></div></div><div class="canvas-bottom"><span>CURIOUS BY NATURE.</span><span>STRUCTURED BY PRACTICE.</span></div></div></section>
 <div class="portfolio-strip"><div class="wrap"><span>One portfolio. <strong>Three connected perspectives.</strong></span><span><b>05</b> organizations</span><span><b>06</b> case studies</span><span><b>03</b> disciplines</span></div></div>
 <section class="work-section wrap" id="work" aria-labelledby="work-title"><div class="section-heading"><div><p class="eyebrow">SELECTED WORK / 01</p><h2 id="work-title">Explore the work.</h2></div><p>Different challenges. A consistent thread:<br>understand deeply, then make it useful.</p></div>
 <div class="filter-panel" aria-label="Project filters"><div class="filter-tabs" role="group" aria-label="Filter by discipline"><button class="filter-tab active" data-discipline="all" aria-pressed="true">All work <span>6</span></button>{tabs}</div><form id="project-filters" role="search"><div class="search-field">{SEARCH}<label class="sr-only" for="project-search">Search projects, tools or skills</label><input id="project-search" type="search" placeholder="Search projects, tools or skills…" autocomplete="off" name="q"></div><div class="select-field"><label for="tool-filter">Tool</label><select id="tool-filter" name="tool"><option value="">All tools</option>{options(tools)}</select></div><div class="select-field"><label for="skill-filter">Skill</label><select id="skill-filter" name="skill"><option value="">All skills</option>{options(skills)}</select></div></form></div>
 <div class="results-meta"><p id="result-count" role="status" aria-live="polite" aria-atomic="true">Showing all 6 case studies</p><button id="clear-filters" class="clear-button" hidden>Clear filters <span aria-hidden="true">×</span></button><span class="results-note">BUILT ON EVIDENCE. DRIVEN BY PURPOSE.</span></div><div class="project-grid" id="project-grid">{''.join(card(p,i) for i,p in enumerate(PROJECTS))}</div><div class="empty-state" id="empty-state" hidden><span aria-hidden="true">⌕</span><h3>No projects match this combination.</h3><p>Try a different search, tool or skill to explore more of the work.</p><button class="button secondary" id="empty-reset">Reset filters {ARROW}</button></div><noscript><p class="noscript-note">All case studies are available below. Enable JavaScript to use filters and quick summaries.</p></noscript></section>
 <section class="approach-section" id="approach" aria-labelledby="approach-title"><div class="wrap"><div class="section-heading"><div><p class="eyebrow">HOW I WORK / 02</p><h2 id="approach-title">Clarity before complexity.</h2></div><p>My work starts with the right questions<br>and ends with a practical way forward.</p></div><div class="approach-grid"><article><span class="step-num">01 / UNDERSTAND</span><h3>Start with the real need.</h3><p>Listen to stakeholders, examine the context and define the problem worth solving.</p><span class="method">Research · Stakeholders · Discovery</span></article><article><span class="step-num">02 / CONNECT</span><h3>Make the evidence useful.</h3><p>Connect data, map processes and turn scattered information into a clear picture.</p><span class="method">Analysis · Requirements · Insights</span></article><article><span class="step-num">03 / SHAPE</span><h3>Create a way forward.</h3><p>Translate findings into recommendations, future states and a plan people can act on.</p><span class="method">Strategy · Roadmaps · Delivery</span></article></div></div></section>
 <section class="about-section wrap" id="about" aria-labelledby="about-title"><div class="about-mark" aria-hidden="true">ra<span>.</span><small>DATA | BUSINESS | PROJECTS | IMPACT</small></div><div class="about-copy"><p class="eyebrow">THE PERSON BEHIND THE WORK / 03</p><h2 id="about-title">Analytical mind.<br><em>People-first perspective.</em></h2><p>I’m Rasheedat Animashaun, a Business Intelligence and Data Analyst, Business Analyst and Project Management Professional based in Saint John, New Brunswick.</p><p>I bring a collaborative approach to understanding business challenges, translating stakeholder needs and connecting analysis with practical decisions.</p><div class="credentials"><span>MBA · UNB</span><span>MSc · Information Systems Management</span><span>PMP</span><span>CBAP</span></div><blockquote>“No knowledge is wasted.”</blockquote></div></section></main>
 <dialog id="project-dialog" aria-labelledby="dialog-title"><div class="dialog-inner"><button class="dialog-close" aria-label="Close project summary">×</button><p class="eyebrow" id="dialog-sector"></p><div class="badges" id="dialog-badges"></div><h2 id="dialog-title"></h2><p class="dialog-subtitle" id="dialog-subtitle"></p><p id="dialog-description"></p><div class="dialog-metrics" id="dialog-metrics"></div><h3>Demonstrated skills</h3><div class="tag-list" id="dialog-skills"></div><p class="evidence-note" id="dialog-status"></p><a class="button primary" id="dialog-link" href="/">Read full case study {ARROW}</a></div></dialog>'''
 return shell('Project Hub','Explore business analysis, project management and data analytics case studies by Rasheedat Animashaun.',body)

def detail(p,index):
    overview=[('Company background',p['context']),('Industry context',p['sector']),('Project background',p['question']),('Scope of the analysis',p['scope']),('Tools & technologies',', '.join(p['tools'])),('Business value',p['value']),('Portfolio project summary',p['summary'])]
    sections=[('overview','Project overview'),('challenge','Business challenges'),('analysis','Business analysis'),('objectives','Project objectives'),('evidence','Evidence & preparation'),('exploration','Exploratory analysis' if 'DA' in p['categories'] else 'Analysis & solution design'),('insights','Insight generation'),('deliverables','Reporting & deliverables'),('recommendations','Recommendations'),('strategy','Strategic recommendation'),('skills','Skills demonstrated')]
    overview_html=''.join(f'<div class="overview-item"><h3>{e(k)}</h3><p>{e(v)}</p></div>' for k,v in overview)
    ul=lambda values:'<ul class="detail-list">'+''.join(f'<li>{e(v)}</li>' for v in values)+'</ul>'
    def section(sid,content,extra=''):
        n=next(i+1 for i,(s,t) in enumerate(sections) if s==sid)
        name=dict(sections)[sid]
        return f'<section class="case-section {extra}" id="{sid}" aria-labelledby="title-{sid}"><div class="case-section-title"><span>{n:02d}</span><h2 id="title-{sid}">{name}</h2></div>{content}</section>'
    metrics=''.join(f'<div><strong>{e(n)}</strong><span>{e(l)}</span></div>' for n,l in p['metrics'])
    tracks=''
    if p.get('tracks'):
        names=list(p['tracks'])
        tracks='<div class="track-switch" role="tablist" aria-label="Project perspective">'+''.join(f'<button role="tab" id="tab-{i}" aria-selected="{str(i==0).lower()}" aria-controls="panel-{i}" tabindex="{0 if i==0 else -1}">{name}</button>' for i,name in enumerate(names))+'</div>'
        tracks+=''.join(f'<div class="track-panel" role="tabpanel" id="panel-{i}" aria-labelledby="tab-{i}" tabindex="0" {"hidden" if i else ""}>{ul(p["tracks"][name])}</div>' for i,name in enumerate(names))
    else:
        tracks=f'<p class="section-lead">{e(p["question"])}</p><p>{e(p["scope"])}</p>'
    approach='<div class="analysis-steps">'+''.join(f'<article><span>{i+1:02d}</span><div><h3>{e(t)}</h3><p>{e(d)}</p></div></article>' for i,(t,d) in enumerate(p['approach']))+'</div>'
    artifacts='<div class="artifact-grid">'+''.join(f'<article><span aria-hidden="true">↗</span><h3>{e(t)}</h3><p>{e(d)}</p></article>' for t,d in p['artifacts'])+'</div>'
    if p.get('artwork'):
        artifacts+=f'<details class="artwork-details"><summary>View existing portfolio artwork <span aria-hidden="true">＋</span></summary><figure><img loading="lazy" src="/assets/{p["artwork"]}" alt="Existing {e(p["company"])} portfolio artwork for {e(p["subtitle"])}"><figcaption>{e(p["artworkCaption"])}</figcaption></figure></details>'
    related=''
    if p.get('sibling'):
        sib=next(x for x in PROJECTS if x['slug']==p['sibling'])
        related=f'<a class="sibling-link" href="{link(sib)}"><small>COMPANION CASE STUDY</small><strong>{e(sib["subtitle"])} {ARROW}</strong></a>'
    content=section('overview','<div class="overview-grid">'+overview_html+'</div>')+section('challenge',ul(p['challenges']))+section('analysis',tracks)+section('objectives',f'<p class="section-lead">{e(p["objective"])}</p>')+section('evidence',f'<p>{e(p["evidence"])}</p>')+section('exploration',approach)+section('insights',ul(p['insights']))+section('deliverables',artifacts)+section('recommendations',ul(p['recommendations']))+section('strategy',f'<p class="strategy-statement">{e(p["strategy"])}</p><h3 class="measures-label">How success would be measured</h3>{ul(p["measures"])}<div class="evidence-note"><strong>Evidence & outcome status</strong><p>{e(p["status"])}</p></div>')+section('skills',f'<div class="skill-links">'+''.join(f'<a class="tag" href="/?skill={e(s,quote=True)}#work">{e(s)} ↗</a>' for s in p['skills'])+f'</div><p class="source-note">Source: {e(p["source"])}</p>{related}')
    nextp=PROJECTS[(index+1)%len(PROJECTS)]
    body=f'''<main id="main" class="detail-main"><div class="wrap"><nav class="breadcrumb" aria-label="Breadcrumb"><a href="/#work">All work</a><span aria-hidden="true">/</span><span>{e(p['company'])}</span></nav><section class="case-hero" aria-labelledby="case-title"><div><p class="eyebrow">{e(p['kind'])}</p><div class="badges">{badges(p)}</div><h1 id="case-title">{e(p['company'])}<span>{e(p['title'])}</span></h1><p class="case-intro">{e(p['summary'])}</p><div class="tag-list">{tags(p['tools'])}</div></div><div class="case-hero-art">{art(p)}<span>{e(p['subtitle'])}</span></div></section><div class="case-metrics">{metrics}</div><div class="case-layout"><aside class="case-contents"><p>IN THIS CASE STUDY</p><nav aria-label="Case study contents">{''.join(f'<a href="#{sid}"><span>{i+1:02d}</span>{title}</a>' for i,(sid,title) in enumerate(sections))}</nav><a class="back-work" href="/#work">← Back to all work</a></aside><div class="case-content">{content}</div></div><a class="next-project" href="{link(nextp)}"><div><small>CONTINUE EXPLORING</small><h2>{e(nextp['company'])}</h2><p>{e(nextp['subtitle'])}</p></div><span>{ARROW}</span></a></div></main>'''
    return shell(p['company']+' — '+p['subtitle'],p['summary'],body,True)

(OUT/'index.html').write_text(hub())
for i,p in enumerate(PROJECTS):
    folder=OUT/'projects'/p['slug'];folder.mkdir(parents=True,exist_ok=True)
    (folder/'index.html').write_text(detail(p,i))
(OUT/'projects.json').write_text(json.dumps(PROJECTS,ensure_ascii=False))
(OUT/'assets'/'favicon.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="#0B3041"/><text x="8" y="43" font-family="Georgia" font-style="italic" font-size="42" fill="#FF6A3D">ra</text></svg>')
(OUT/'404.html').write_text(shell('Page not found','Return to the portfolio hub.','<main id="main" class="wrap not-found"><p class="eyebrow">404 / PAGE NOT FOUND</p><h1>Let’s find your way back.</h1><a class="button primary" href="/#work">Explore all projects '+ARROW+'</a></main>',True))
print('Built hub, 6 case-study pages and 404 page.')
