#!/usr/bin/env python3
"""Builds the Projexian static site (phase 1) into ./dist."""
import re
import json, os, shutil, html, urllib.parse

ROOT = os.path.dirname(os.path.abspath(__file__))
DIST = os.path.join(ROOT, "dist")
SITE_URL = os.environ.get("SITE_URL", "https://www.projexian.com").rstrip("/")
CSP = ("default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; font-src 'self'; img-src 'self' data:; "
       "connect-src 'self'; form-action https://formsubmit.co; base-uri 'self'; object-src 'none'; frame-src 'none'; upgrade-insecure-requests")
EMAIL = "tyler@projexian.com"
PHONE = "630-888-8182"
FORM_ACTION = f"https://formsubmit.co/{EMAIL}"

NAV = [("index.html", "Home"), ("about.html", "About Us"), ("services.html", "Services"),
       ("industries.html", "Industries"), ("opportunities.html", "Opportunities"), ("lead-generation.html", "Lead Generation"), ("contact.html", "Contact")]

LOGO = ('<span class="wm">Projex<span class="i">ı<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M22 2 15 22l-4-9-9-4 20-7Z" fill="#A58A5B"/></svg></span>an</span>')

CREDITS = json.load(open(os.path.join(ROOT, "credits.json"))) if os.path.exists(os.path.join(ROOT, "credits.json")) else {}


def img(name, alt, cls="", eager=False, cap=None, sizes="(max-width: 820px) 100vw, 60vw"):
    load = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    c = f'<span class="cap">{cap}</span>' if cap else ""
    return (f'<figure class="photo {cls}"><img src="img/{name}-1600.jpg" srcset="img/{name}-900.jpg 900w, img/{name}-1600.jpg 1600w" '
            f'sizes="{sizes}" alt="{html.escape(alt)}" {load}>{c}</figure>')


def page(fn, title, desc, body, extra_head="", extra_js="", sub=False, noindex=False):
    cur = ' aria-current="page"'
    links = "".join(f'<a href="{h}"{cur if h == fn else ""}>{t}</a>' for h, t in NAV[1:])
    canon = SITE_URL + "/" + ("" if fn == "index.html" else fn)
    base = '<base href="../">' if sub else ""
    robots = '<meta name="robots" content="noindex">' if noindex else ""
    ld = {"@context": "https://schema.org", "@type": "Organization", "name": "Projexian LLC", "url": SITE_URL,
          "email": EMAIL, "telephone": "+1-" + PHONE}
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
{base}
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta http-equiv="Content-Security-Policy" content="{CSP}">
<meta name="referrer" content="strict-origin-when-cross-origin">
{robots}
<title>{title}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{canon}">
<meta property="og:type" content="website"><meta property="og:title" content="{html.escape(title)}"><meta property="og:description" content="{html.escape(desc)}"><meta property="og:url" content="{canon}"><meta property="og:image" content="{SITE_URL}/img/hero-1600.jpg">
<meta name="theme-color" content="#142638">
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
<link rel="preload" href="assets/fonts/cormorant-garamond-latin-500-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="assets/fonts/ibm-plex-sans-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="assets/fonts.css">
<link rel="stylesheet" href="assets/site.css">
<script type="application/ld+json">{json.dumps(ld)}</script>
{extra_head}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="hdr" id="hdr"><div class="wrap">
  <a class="logo" href="index.html" aria-label="Projexian home">{LOGO}</a>
  <nav class="nav" id="nav" aria-label="Main">{links}<a class="touch" href="contact.html">Get in Touch</a></nav>
  <button class="menu-btn" id="menuBtn" aria-label="Open menu" aria-expanded="false" aria-controls="nav"><span></span></button>
</div></header>
<main id="main">
{body}
</main>
<footer class="ftr"><div class="wrap">
  <div class="top">
    <div><a class="logo" href="index.html" aria-label="Projexian home">{LOGO}</a><p class="tag">Government contracting, business development and opportunity intelligence.</p></div>
    <div><h4>Firm</h4><ul><li><a href="about.html">About Us</a></li><li><a href="services.html">Services</a></li><li><a href="industries.html">Industries</a></li><li><a href="opportunities.html">Opportunities</a></li><li><a href="lead-generation.html">Lead Generation</a></li><li><a href="partners.html">Partner Network</a></li></ul></div>
    <div><h4>Contact</h4><ul><li><a href="mailto:{EMAIL}">{EMAIL}</a></li><li><a href="tel:+1{PHONE.replace('-', '')}">{PHONE}</a></li></ul></div>
    <div><h4>Registration</h4><ul><li>SAM.gov · Active</li><li>UEI MAVQJ6NPEL59</li><li>CAGE 25TN9</li><li><a href="assets/projexian-capabilities-statement.pdf">Capabilities statement</a></li></ul></div>
  </div>
  <div class="bot"><span>© 2026 Projexian LLC. All rights reserved.</span><span class="disc">Projexian LLC is a private company. It is not affiliated with, and is not endorsed by, any government agency. Photographs are illustrative and do not depict Projexian projects. <a href="terms.html">Terms of Use</a> · <a href="privacy.html">Privacy</a> · <a href="accessibility.html">Accessibility</a> · <a href="credits.html">Photo credits</a></span></div>
</div></footer>
<script src="assets/site.js" defer></script>
{extra_js}
</body>
</html>
"""


def form_hidden(subject, next_page="thanks.html"):
    return (f'<input type="hidden" name="_subject" value="{subject}">'
            f'<input type="hidden" name="_template" value="table">'
            f'<input type="hidden" name="_next" value="{SITE_URL}/{next_page}" data-next="{next_page}">'
            f'<div class="hp" aria-hidden="true"><label>Leave this field empty<input type="text" name="_honey" tabindex="-1" autocomplete="off"></label></div>')


INDUSTRIES = [
    ("construction", "Construction and Infrastructure", "road", "Construction worker drilling foundation piles on a building site",
     "Agencies at every level fund new buildings, roads, utilities and site work. Much of it is packaged for small and mid-size contractors, often through set-asides and subcontracting plans.",
     ["NAICS 236220 · Commercial building", "NAICS 237310 · Highway, street & bridge", "PSC Y · Construction of structures"]),
    ("facility-maintenance", "Facility Maintenance", "mechanical", "Technician checking refrigerant gauges on an HVAC unit",
     "Federal buildings, bases, clinics and field offices need ongoing operations and maintenance: mechanical, electrical, plumbing and preventive maintenance under multi-year service contracts.",
     ["NAICS 561210 · Facilities support", "PSC J · Maintenance & repair of equipment", "PSC Z · Maintenance of real property"]),
    ("janitorial", "Janitorial Services", "janitorial", "Crew pressure-washing a building entrance and sidewalk",
     "Custodial work is one of the most frequently solicited service categories in the federal market, from single ranger stations to large office complexes.",
     ["NAICS 561720 · Janitorial services", "PSC S201 · Custodial janitorial", "NAICS 561790 · Other building services"]),
    ("information-technology", "Information Technology", "servers", "Network cabling inside a server rack",
     "IT services, infrastructure and equipment are bought continuously, through open-market solicitations and through contract vehicles that prime contractors hold.",
     ["NAICS 541512 · Computer systems design", "NAICS 541519 · Other computer services", "PSC D · IT & telecommunications"]),
    ("transportation-logistics", "Transportation and Logistics", "truck", "Refrigerated semi truck on an interstate highway",
     "Freight, moving, warehousing and vehicle rentals support agency operations across the country, including recurring and emergency requirements.",
     ["NAICS 484110 · General freight, local", "NAICS 484220 · Specialized freight", "PSC V · Transportation & travel"]),
    ("engineering", "Engineering Services", "blueprint", "Historic engineering drawing of a warehouse structure",
     "Design, studies, inspections and technical support are acquired under architect-engineer procedures and professional services contracts.",
     ["NAICS 541330 · Engineering services", "PSC C · Architect & engineering", "NAICS 541350 · Building inspection"]),
    ("professional-services", "Professional Services", "boardroom", "Empty meeting room with a long wooden table",
     "Program support, administrative services, research and advisory work make up a large share of what agencies purchase each year.",
     ["NAICS 541611 · Management consulting", "NAICS 561110 · Office administration", "PSC R · Professional support"]),
    ("equipment-supply", "Equipment and Supply Procurement", "port", "Aerial view of container cranes and shipping containers at a port",
     "Agencies buy and rent equipment, vehicles, generators and supplies, often on short timelines that reward responsive, well-prepared vendors.",
     ["NAICS 532490 · Equipment rental", "NAICS 532120 · Truck rental", "NAICS 423 · Merchant wholesalers"]),
    ("building-renovations", "Building Renovations", "renovation", "Scaffolding wrapped around a building during renovation",
     "Repair and alteration projects keep public buildings in service: interiors, roofing, windows, accessibility upgrades and systems replacement.",
     ["PSC Z2 · Repair or alteration of real property", "NAICS 236220 · Commercial building", "NAICS 238990 · Specialty trades"]),
    ("security", "Security and Facility Support", "camera", "Surveillance camera mounted on a building wall",
     "Guard services, access control, surveillance systems and site support protect federal property and the people who work there.",
     ["NAICS 561612 · Security guards", "NAICS 561621 · Security systems services", "NAICS 561210 · Facilities support"]),
]


D3 = '<script src="assets/vendor/d3.min.js" defer></script><script src="assets/vendor/topojson-client.min.js" defer></script><script src="assets/live.js" defer></script>'
LIVE = '<script src="assets/live.js" defer></script>'

OPP_BODY = '\n<div class="wrap"><div class="phead">\n  <div class="label rv">Opportunities</div>\n  <h1 class="display rv">Government Contracting <em>Opportunities.</em></h1>\n  <p class="body rv">Public agencies publish their requirements openly. The challenge is finding the right ones in time. Below are the federal opportunities open today in the categories we track, across all 50 states and U.S. territories, refreshed every morning.</p>\n</div></div>\n<section id="opp" style="padding-bottom:clamp(80px,9vw,130px)"><div class="wrap">\n  <div class="ofilters rv" role="search">\n    <div class="fld q"><label for="fQ">Search</label><input id="fQ" type="search" placeholder="Keyword, agency or city"></div>\n    <div class="fld"><label for="fInd">Industry</label><select id="fInd"></select></div>\n    <div class="fld"><label for="fSt">Location</label><select id="fSt"></select></div>\n    <div class="fld"><label for="fAg">Agency</label><select id="fAg"></select></div>\n    <div class="fld"><label for="fCat">Contract category</label><select id="fCat"></select></div>\n    <div class="fld"><label for="fType">Opportunity type</label><select id="fType"></select></div>\n    <button type="button" id="fReset">Reset</button>\n  </div>\n  <div class="oshell">\n    <div class="omap rv"><svg id="oppmap" role="group" aria-label="Map of open opportunities by state. Select a state to filter."></svg><div class="terr" id="terrRow"></div><div class="otip" id="otip"></div></div>\n    <aside class="oside rv">\n      <div class="lens" role="tablist" aria-label="Map view"><button role="tab" data-lens="contracts" aria-selected="true">Contracts</button><button role="tab" data-lens="partners" aria-selected="false">Partner needs</button><button role="tab" data-lens="leads" aria-selected="false">Lead generation</button></div>\n      <p class="note" id="lensNote"></p>\n      <div class="tot" id="oTotal">—</div><div class="label" style="margin-top:8px">Open opportunities tracked today</div>\n      <p class="src" id="oUpd"></p>\n      <div class="pairing" id="pairing" hidden></div>\n    </aside>\n  </div>\n  <div class="ohead"><div id="oCount"></div><button type="button" id="oClear" hidden>Clear filters</button></div>\n  <div class="olist" id="oList" aria-live="polite"></div>\n  <div class="offmsg"><p class="lead" style="margin-top:20px">Live opportunity data is temporarily unavailable.</p><p class="body" style="margin-top:12px">Please check back shortly, or <a class="link" href="contact.html?topic=research">ask us about a specific market <span class="ar"></span></a></p></div>\n</div></section>\n\n<section class="sec white"><div class="wrap">\n  <div class="head-row"><div class="label rv"><span class="n">02</span>The Marketplace</div><h2 class="h2 rv">How the government <em>buys.</em></h2></div>\n  <div class="mkt rv">\n    <div><span class="n">i.</span><h3>Federal contracting</h3><p>Federal agencies publish solicitations, sources sought notices and awards on SAM.gov. Many service contracts are set aside for small businesses and run for a base year plus options.</p></div>\n    <div><span class="n">ii.</span><h3>State government procurement</h3><p>Each state runs its own purchasing system, vendor registration and bid portal, with rules and preferences that differ from the federal process.</p></div>\n    <div><span class="n">iii.</span><h3>Local government contracts</h3><p>Cities, counties, school districts and transit agencies post work on their own sites and regional portals, often with shorter timelines.</p></div>\n    <div><span class="n">iv.</span><h3>Subcontracting opportunities</h3><p>Large primes need capable small businesses to perform portions of their contracts and meet subcontracting goals.</p></div>\n    <div><span class="n">v.</span><h3>Prime contractor relationships</h3><p>Long-term relationships with primes create access to work that is never openly advertised to small firms.</p></div>\n    <div><span class="n">vi.</span><h3>Procurement research &amp; discovery</h3><p>Spending history, agency forecasts and recompete timing show where opportunities will appear before they post.</p></div>\n  </div>\n  <div style="margin-top:44px;display:flex;gap:24px;flex-wrap:wrap;align-items:center" class="rv"><a class="btn" href="contact.html?topic=research">Identify Your Next Opportunity</a><a class="link" href="services.html#opportunity-intelligence">Opportunity intelligence services <span class="ar"></span></a></div>\n</div></section>\n'


import re as _re, hashlib as _hl
from datetime import date as _date
DATA = os.path.join(ROOT, "data")
ST_NAMES = {"AL":"Alabama","AK":"Alaska","AZ":"Arizona","AR":"Arkansas","CA":"California","CO":"Colorado","CT":"Connecticut","DE":"Delaware","DC":"Washington, DC","FL":"Florida","GA":"Georgia","HI":"Hawaii","ID":"Idaho","IL":"Illinois","IN":"Indiana","IA":"Iowa","KS":"Kansas","KY":"Kentucky","LA":"Louisiana","ME":"Maine","MD":"Maryland","MA":"Massachusetts","MI":"Michigan","MN":"Minnesota","MS":"Mississippi","MO":"Missouri","MT":"Montana","NE":"Nebraska","NV":"Nevada","NH":"New Hampshire","NJ":"New Jersey","NM":"New Mexico","NY":"New York","NC":"North Carolina","ND":"North Dakota","OH":"Ohio","OK":"Oklahoma","OR":"Oregon","PA":"Pennsylvania","RI":"Rhode Island","SC":"South Carolina","SD":"South Dakota","TN":"Tennessee","TX":"Texas","UT":"Utah","VT":"Vermont","VA":"Virginia","WA":"Washington","WV":"West Virginia","WI":"Wisconsin","WY":"Wyoming","PR":"Puerto Rico","GU":"Guam","VI":"U.S. Virgin Islands","MP":"Northern Mariana Islands","AS":"American Samoa"}
CAT_NAMES = {"541611": "Management consulting", "115310": "Forestry support", "236118": "Residential remodeling", "236220": "Commercial building construction", "237110": "Water and sewer line construction", "237310": "Highway, street and bridge", "237990": "Heavy and civil construction", "238140": "Masonry", "238160": "Roofing", "238210": "Electrical", "238220": "Plumbing, heating and air conditioning", "238320": "Painting and wall covering", "238330": "Flooring", "238910": "Site preparation", "238990": "Specialty trades", "332410": "Boilers and heat exchangers", "332722": "Fasteners", "334513": "Industrial instruments", "335910": "Batteries", "337126": "Furniture manufacturing", "339940": "Office supplies manufacturing", "423210": "Furniture supply", "423420": "Office equipment supply", "423430": "Computer equipment supply", "423450": "Medical supplies", "423610": "Electrical supplies", "484110": "Local freight", "484121": "Long-distance freight", "484210": "Moving services", "484220": "Specialized freight", "484230": "Specialized freight, long-distance", "488510": "Freight arrangement", "492110": "Couriers and delivery", "493110": "Warehousing and storage", "524298": "Insurance services", "532120": "Truck and trailer rental", "532283": "Home health equipment rental", "532412": "Construction equipment rental", "532490": "Equipment rental", "541330": "Engineering services", "541350": "Building inspection", "541512": "IT systems design", "541519": "IT services", "541614": "Logistics consulting", "541618": "Management consulting", "541620": "Environmental consulting", "541910": "Market research", "541990": "Professional services", "561110": "Office administration", "561210": "Facilities support", "561320": "Temporary staffing", "561410": "Document preparation", "561612": "Security guards", "561621": "Security systems", "561710": "Pest control", "561720": "Janitorial", "561730": "Landscaping and grounds", "561740": "Carpet cleaning", "561790": "Building services", "561920": "Events and trade shows", "561990": "Support services", "562111": "Solid waste", "562112": "Hazardous waste collection", "562119": "Other waste collection", "562910": "Remediation", "562920": "Recycling", "562991": "Portable restrooms and septic", "562998": "Waste management", "611430": "Training", "722310": "Food service", "811192": "Vehicle washing", "811210": "Electronic equipment repair", "811310": "Machinery repair", "812332": "Industrial laundry", "812930": "Parking management"}
TRADES = ["Janitorial & custodial", "Landscaping & grounds", "Snow & ice removal", "Pest control", "Waste & recycling hauling", "Moving & freight", "Equipment & truck rental", "Building maintenance & repairs", "HVAC / mechanical", "Security services", "Other"]
e = html.escape


def slugify(t, nid):
    base = _re.sub(r"[^a-z0-9]+", "-", (t or "").lower()).strip("-")[:70].strip("-")
    return f"{base}-{_hl.sha1(str(nid).encode()).hexdigest()[:6]}"


def money(v):
    return "$" + format(int(v or 0), ",")


EMAIL_RE = re.compile(r"[A-Za-z0-9._%+\-]+\s*(?:@|\(at\)|\[at\])\s*[A-Za-z0-9\-]+(?:\s*[.,]+\s*[A-Za-z0-9\-]+)*\.[A-Za-z]{2,}\b", re.I)
PHONE_RE = re.compile(r"(?<!\d)(?:\+?1[\s.\-]?)?\(?\d{3}\)?[\s.\-]\d{3}[\s.\-]\d{4}(?:\s*(?:x|ext\.?)\s*\d+)?(?!\d)", re.I)


def scrub(text):
    """Remove email addresses and phone numbers (contact details stay on SAM.gov)."""
    text = EMAIL_RE.sub("[contact on SAM.gov]", text or "")
    text = PHONE_RE.sub("[contact on SAM.gov]", text)
    return re.sub(r"(\[contact on SAM\.gov\][\s,;/]*){2,}", "[contact on SAM.gov] ", text)


def load_data():
    feed = {"items": [], "stats": {}, "updated": ""}
    awards = {"past": {}, "recompetes": []}
    if os.path.exists(os.path.join(DATA, "feed.json")):
        feed = json.load(open(os.path.join(DATA, "feed.json")))
    if os.path.exists(os.path.join(DATA, "awards.json")):
        awards = json.load(open(os.path.join(DATA, "awards.json")))
    today = _date.today().isoformat()
    feed["items"] = [i for i in feed["items"] if i.get("due", "") >= today]
    for i in feed["items"]:
        for k, v in list(i.items()):
            if isinstance(v, str):
                i[k] = scrub(v.replace("\ufffd", "'")) if k == "d" else v.replace("\ufffd", "'")
        i["u"] = slugify(i["t"], i.get("id") or i["t"] + i["due"])
    return feed, awards


def fmt_date(d):
    try:
        y, m, dd = d[:10].split("-")
        return _date(int(y), int(m), int(dd)).strftime("%b %-d, %Y")
    except Exception:
        return d or "—"


def opp_page(i, feed, awards):
    stn = ST_NAMES.get(i["s"], i["s"])
    where = f'{i["c"]}, {stn}' if i.get("c") else stn
    cat = CAT_NAMES.get(i["n"], i["n"])
    typ = i.get("ty") or ("Sources Sought" if i.get("k") == "ss" else "Solicitation")
    inquire = "contact.html?topic=contracting&opp=" + urllib.parse.quote(f'{i["t"]} ({where}, due {i["due"]})')
    partner = "partners.html?opp=" + urllib.parse.quote(f'{i["t"]} ({where})')
    sam = f'https://sam.gov/opp/{i["id"]}/view' if i.get("id") else "https://sam.gov"
    rows = [("Agency", i.get("a") or "Federal agency"), ("Place of performance", where), ("Category", cat),
            ("Notice type", typ), ("Set-aside", i.get("sa") or "None stated"), ("Posted", fmt_date(i.get("posted", ""))),
            ("Response due", fmt_date(i["due"])), ("Solicitation no.", i.get("sol") or "See notice")]
    spec = "".join(f'<div class="r"><span>{e(k)}</span><span>{e(v)}</span></div>' for k, v in rows)
    desc = (i.get("d") or "").strip()
    desc_html = (f'<section class="sec tight" style="padding-top:0"><div class="wrap grid12"><div class="label" style="grid-column:1/4;padding-top:6px"><span class="n">02</span>From the notice</div>'
                 f'<div style="grid-column:4/12"><blockquote class="quote">{e(desc[:800])}{"…" if len(desc) > 800 else ""}</blockquote>'
                 f'<p class="src">Excerpt from the public notice. Read the full solicitation and all attachments on SAM.gov.</p></div></div></section>') if len(desc) > 40 else ""
    past = awards.get("past", {}).get(f'{i["s"]}|{i["n"]}', [])
    if past:
        trs = "".join(f'<tr><td>{e(a["r"])}</td><td>{e(a["ag"])}</td><td class="num">{money(a["amt"])}</td><td>{fmt_date(a["start"])} – {fmt_date(a["end"])}</td></tr>' for a in past[:6])
        past_html = (f'<section class="sec white"><div class="wrap"><div class="head-row"><div class="label"><span class="n">03</span>Market history</div>'
                     f'<h2 class="h2">Who has won similar work <em>in {e(stn)}.</em></h2></div>'
                     f'<div class="tbl-wrap"><table class="tbl"><thead><tr><th>Recipient</th><th>Awarding agency</th><th class="num">Award value</th><th>Period</th></tr></thead><tbody>{trs}</tbody></table></div>'
                     f'<p class="src">Largest federal contract awards in {e(cat.lower())} performed in {e(stn)}, with contract activity in the past three years. Source: USAspending.gov. Shown for market context; not necessarily the incumbent for this requirement.</p></div></section>')
    else:
        past_html = ""
    rel = [x for x in feed["items"] if x is not i and x["s"] == i["s"]][:3]
    rel += [x for x in feed["items"] if x is not i and x["n"] == i["n"] and x not in rel][:4 - len(rel)]
    rel_html = "".join(f'<a class="path" href="opp/{x["u"]}.html"><span class="n">{k+1:02d}</span><div><h3 style="font-size:24px">{e(x["t"])}</h3><p>{e(x.get("a") or "")} · {e((x["c"] + ", ") if x.get("c") else "")}{e(x["s"])} · due {fmt_date(x["due"])}</p></div><span class="go" aria-hidden="true">→</span></a>' for k, x in enumerate(rel[:4]))
    body = f"""
<div class="wrap"><div class="phead">
  <div class="label"><a href="opportunities.html" class="crumb">Opportunities</a> · {e(stn)}</div>
  <h1 class="h2" style="grid-column:4/13">{e(i["t"])}</h1>
  <p class="body">{e(i.get("a") or "Federal agency")} · {e(where)} · {e(typ)}</p>
</div></div>
<section class="sec tight" style="padding-top:0"><div class="wrap oppd">
  <div class="spec2">{spec}</div>
  <aside class="ctabox"><div class="label" style="color:var(--brass)">Response due</div><div class="due">{fmt_date(i["due"])}</div>
    <p>Interested in pursuing this opportunity, or in performing the work as a local partner?</p>
    <a class="btn brass" href="{inquire}">Discuss this opportunity</a>
    <a class="link" href="{partner}" style="color:var(--ivory);margin-top:18px">Perform this work as a partner <span class="ar"></span></a>
    <a class="link ext" href="{sam}" rel="noopener noreferrer" target="_blank" style="color:#b5bcc2;margin-top:12px;font-size:13px">Official notice on SAM.gov ↗</a>
  </aside>
</div></section>
{desc_html}
{past_html}
<section class="sec"><div class="wrap"><div class="head-row"><div class="label"><span class="n">04</span>Related</div><h2 class="h2">Related <em>opportunities.</em></h2></div><div class="paths">{rel_html}</div>
<p class="src" style="margin-top:28px">Opportunity information comes from public federal sources and may change. Always confirm requirements, amendments and deadlines in the official notice. Projexian is not affiliated with the issuing agency.</p></div></section>
"""
    return page(f'opp/{i["u"]}.html', f'{i["t"]} · {where} | Projexian', f'Open federal opportunity: {i["t"]} in {where}, due {fmt_date(i["due"])}. Category: {cat}.', body, sub=True)


def recompete_table(awards):
    rec = awards.get("recompetes", [])[:30]
    if not rec:
        return ""
    trs = "".join(f'<tr><td>{e(a["r"])}</td><td>{e(a["ag"])}</td><td>{e(ST_NAMES.get(a["st"], a["st"]) or "—")}</td><td>{e(CAT_NAMES.get(str(a["n"]), str(a["n"])))}</td><td class="num">{money(a["amt"])}</td><td>{fmt_date(a["end"])}</td></tr>' for a in rec)
    return f"""<section class="sec"><div class="wrap">
  <div class="head-row"><div class="label rv"><span class="n">03</span>Upcoming recompetes</div><h2 class="h2 rv">Contracts ending <em>in the next twelve months.</em></h2></div>
  <div class="tbl-wrap rv"><table class="tbl"><thead><tr><th>Current contractor</th><th>Agency</th><th>Location</th><th>Category</th><th class="num">Award value</th><th>Period ends</th></tr></thead><tbody>{trs}</tbody></table></div>
  <p class="src">Federal contracts in the categories we track whose current period of performance ends within a year, from USAspending.gov. Option years or extensions may change timing. <a class="link" href="contact.html?topic=research" style="margin-left:6px">Ask us about a recompete <span class="ar"></span></a></p>
</div></section>"""


def _harden(h):
    # every external link opens safely; inputs get length limits
    h = _re.sub(r'<a ([^>]*href="https?://(?!www\.projexian\.com)[^"]+"[^>]*)>', lambda m: m.group(0) if "rel=" in m.group(1) else f'<a {m.group(1)} rel="noopener noreferrer">', h)
    h = _re.sub(r'<input(?![^>]*maxlength)(?![^>]*type="(?:hidden|checkbox)")', '<input maxlength="200"', h)
    h = _re.sub(r'<textarea(?![^>]*maxlength)', '<textarea maxlength="4000"', h)
    return h


def build():
    if os.path.exists(DIST):
        shutil.rmtree(DIST)
    shutil.copytree(os.path.join(ROOT, "assets"), os.path.join(DIST, "assets"))
    shutil.copytree(os.path.join(ROOT, "img_out"), os.path.join(DIST, "img"))
    feed, awards = load_data()
    os.makedirs(os.path.join(DIST, "data"), exist_ok=True)
    json.dump(feed, open(os.path.join(DIST, "data", "feed.json"), "w"), separators=(",", ":"))
    pages = {}

    # ---------------- HOME ----------------
    pages["index.html"] = page("index.html", "Projexian | Government Contracting, Business Development & Opportunity Intelligence",
        "Projexian LLC helps businesses identify government opportunities, strengthen their market position and pursue growth through contracting support, business development and lead generation.",
        f"""
<section class="hero">
  <div class="txt">
    <div>
      <div class="label rv">Government Contracting · Business Development · Opportunity Intelligence</div>
      <h1 class="display rv">Creating Opportunity. <em>Building Lasting Business.</em></h1>
      <p class="sub rv">Strategic government contracting, business development, and opportunity intelligence designed to help businesses navigate and grow within the government marketplace.</p>
      <div class="ctas rv"><a class="btn" href="services.html">Explore Our Services <span aria-hidden="true">→</span></a><a class="link" href="contact.html">Start a Conversation <span class="ar" aria-hidden="true"></span></a></div>
    </div>
    <div class="meta rv"><span><b>SAM.gov</b> Active</span><span><b>UEI</b> MAVQJ6NPEL59</span><span><b>CAGE</b> 25TN9</span></div>
  </div>
  {img("hero", "Worker in a hard hat and safety vest pressure-washing the stone wall of a large public building", eager=True, cap="Illustrative · Building renewal, Washington, D.C.", sizes="(max-width: 1080px) 100vw, 58vw")}
</section>
<div class="ticker" hidden data-live><div class="wrap"><span class="lbl">Open now · SAM.gov</span><div class="tk-view"><div class="tk-track" id="tickerTrack"></div></div><a class="link" href="opportunities.html" style="color:var(--ivory);flex:none">All opportunities <span class="ar"></span></a></div></div>

<section class="sec"><div class="wrap grid12 intro">
  <div class="label rv"><span class="n">01</span>The Firm</div>
  <p class="lead rv">Navigating the government marketplace requires strategy, research, and the right business relationships. We help businesses identify opportunities, strengthen their market position, and pursue meaningful growth.</p>
  <div class="facts rv">
    <div class="fact"><div class="k">Coverage</div><div class="v">Nationwide</div><div class="d">All 50 states and U.S. territories</div></div>
    <div class="fact"><div class="k">Services</div><div class="v">Facility &amp; site support</div><div class="d">Janitorial, grounds, snow, pest, waste and rentals</div></div>
    <div class="fact"><div class="k">Structure</div><div class="v">Small business</div><div class="d">Active SAM.gov entity registration</div></div>
  </div>
</div></section>

<section class="sec dark"><div class="wrap">
  <div class="head-row"><div class="label rv"><span class="n">02</span>Services</div><h2 class="h2 rv">Four disciplines, <em>one standard of work.</em></h2></div>
  <div class="svc-list">
    <a class="svc-row rv" href="services.html#government-contracting"><span class="num">01</span><h3>Government Contracting</h3><p>Procurement support, opportunity research, bids, proposals and contract administration.</p><span class="peek">{img("courthouse", "")[len('<figure class="photo ">'):-len('</figure>')]}</span><span class="ar" aria-hidden="true"></span></a>
    <a class="svc-row rv" href="services.html#business-development"><span class="num">02</span><h3>Business Development</h3><p>Partnerships, prime and subcontractor relationships, market and industry research.</p><span class="peek">{img("boardroom", "")[len('<figure class="photo ">'):-len('</figure>')]}</span><span class="ar" aria-hidden="true"></span></a>
    <a class="svc-row rv" href="services.html#lead-generation"><span class="num">03</span><h3>Lead Generation</h3><p>Targeted B2B prospecting, contact research and qualified business leads.</p><span class="peek">{img("binders", "")[len('<figure class="photo ">'):-len('</figure>')]}</span><span class="ar" aria-hidden="true"></span></a>
    <a class="svc-row rv" href="services.html#opportunity-intelligence"><span class="num">04</span><h3>Opportunity Intelligence</h3><p>Contract research, procurement discovery, market and competitor analysis.</p><span class="peek">{img("archive", "")[len('<figure class="photo ">'):-len('</figure>')]}</span><span class="ar" aria-hidden="true"></span></a>
  </div>
</div></section>

<section class="band">
  <img src="img/hall-1600.jpg" srcset="img/hall-900.jpg 900w, img/hall-1600.jpg 1600w" sizes="100vw" alt="Marble interior hall of a federal building" loading="lazy">
  <span class="cap">Illustrative · Federal building interior</span>
  <div class="over"><div class="wrap"><div class="box rv"><div class="label"><span class="n">03</span>The Market</div><p class="lead" style="font-size:clamp(24px,2.3vw,32px);margin-top:14px">Federal, state and local governments buy nearly everything a business sells, from janitorial services to engineering studies.</p></div></div></div>
</section>

<section class="sec white" id="intel"><div class="wrap">
  <div class="head-row"><div class="label rv"><span class="n">04</span>Opportunity Intelligence</div><h2 class="h2 rv">What the market looks like <em>this morning.</em></h2></div>
  <div class="grid12"><div class="intel">
    <div class="rv"><div class="bignum" id="iOpen">—</div><p class="body" style="margin-top:14px">open federal opportunities in the service categories Projexian tracks, refreshed every morning from SAM.gov.</p><p class="src iUpd"></p><a class="link" style="margin-top:22px" href="opportunities.html">Explore the opportunity map <span class="ar"></span></a></div>
    <div class="rv"><div class="label" style="margin-bottom:14px">Where they are · top states</div><div class="bars" id="iBars"></div></div>
  </div></div>
  <div class="night rv" data-live>
    <div id="nightmap"></div>
    <div><div class="label">Every business day</div><div class="clock" id="nightClock">5:00 AM ET</div><p class="body" style="margin-top:16px">Before the business day starts, each new solicitation in our categories has been collected and reviewed, coast to coast and across U.S. territories.</p></div>
  </div>
</div></section>

<section class="sec"><div class="wrap">
  <div class="head-row"><div class="label rv"><span class="n">05</span>Industries</div><h2 class="h2 rv">Industries we <em>support.</em></h2></div>
  <div class="mosaic">
    {img("vamc", "Veterans Affairs medical center building on a city street", "a rv")}
    {img("warehouse", "Warehouse aisle with stacked pallets on tall racks", "b rv")}
  </div>
  <div class="ind-index rv">{"".join(f'<a href="industries.html#{s}">{n}<span>{i+1:02d}</span></a>' for i, (s, n, *_ ) in enumerate(INDUSTRIES))}</div>
</div></section>

<section class="sec dark"><div class="wrap">
  <div class="head-row"><div class="label rv"><span class="n">06</span>Credentials</div><h2 class="h2 rv">Registered and <em>ready to perform.</em></h2></div>
  <div class="creds rv">
    <div class="cred"><div class="k">SAM.gov</div><div class="v">Active</div></div>
    <div class="cred"><div class="k">UEI</div><div class="v">MAVQJ6NPEL59</div></div>
    <div class="cred"><div class="k">CAGE</div><div class="v">25TN9</div></div>
    <div class="cred"><div class="k">Business size</div><div class="v">Small business</div></div>
    <div class="cred"><div class="k">Founded</div><div class="v">2026</div></div>
  </div>
  <div style="margin-top:36px" class="rv"><a class="btn brass" href="assets/projexian-capabilities-statement.pdf">Download Capabilities Statement <span aria-hidden="true">↓</span></a></div>
</div></section>

<section class="sec"><div class="wrap">
  <div class="head-row"><div class="label rv"><span class="n">07</span>Start Here</div><h2 class="h2 rv">Identify your <em>next opportunity.</em></h2></div>
  <div class="paths rv">
    <a class="path" href="contact.html?topic=contracting"><span class="n">A</span><div><h3>Government contracting support</h3><p>Discuss your contracting needs, from registration to a submitted bid.</p></div><span class="go" aria-hidden="true">→</span></a>
    <a class="path" href="lead-generation.html#inquiry"><span class="n">B</span><div><h3>Lead generation</h3><p>Request lead generation information for your market.</p></div><span class="go" aria-hidden="true">→</span></a>
    <a class="path" href="partners.html"><span class="n">C</span><div><h3>Subcontracting and partnerships</h3><p>Join our partner network, or explore teaming and prime relationships.</p></div><span class="go" aria-hidden="true">→</span></a>
    <a class="path" href="contact.html?topic=research"><span class="n">D</span><div><h3>Procurement research</h3><p>Commission research on an agency, market or competitor set.</p></div><span class="go" aria-hidden="true">→</span></a>
  </div>
</div></section>
""", extra_js=D3)

    # ---------------- SERVICES ----------------
    def svc(id_, n, title, em, body, items, photo, alt, flip, extra=""):
        p = img(photo, alt, "rv")
        txt = f'''<div class="rv"><div class="num">{n}</div><h2 class="h2">{title} <em>{em}</em></h2><p class="body">{body}</p>
<ul class="items">{"".join(f"<li>{i}</li>" for i in items)}</ul>{extra}</div>'''
        a, b = (f'<div style="grid-column:1/6">{p}</div>', f'<div style="grid-column:7/13">{txt}</div>') if not flip else \
               (f'<div style="grid-column:1/7">{txt}</div>', f'<div style="grid-column:8/13">{p}</div>')
        return f'<section class="svc-block" id="{id_}"><div class="wrap split">{a}{b}</div></section>'

    pages["services.html"] = page("services.html", "Services | Projexian",
        "Government contracting support, business development, lead generation and opportunity intelligence for businesses pursuing public-sector work.",
        f"""
<div class="wrap"><div class="phead">
  <div class="label rv">Services</div>
  <h1 class="display rv">Strategy for the <em>government marketplace.</em></h1>
  <p class="body rv">Each engagement starts with the same question: where can this business realistically win, and what will it take? Our services are built to answer that question and act on it.</p>
</div></div>
{svc("government-contracting", "01", "Government", "Contracting.",
     "Federal, state and local procurement follows rules that reward preparation. We help businesses find the right solicitations, understand what is being asked, and respond with complete, compliant submissions.",
     ["Government procurement support", "Contract opportunity research", "Bid and proposal support", "Contract administration", "Federal procurement navigation", "State and local procurement", "Contract strategy"],
     "courthouse", "Columned facade of a federal building and U.S. courthouse", False,
     '<a class="link" style="margin-top:30px" href="contact.html?topic=contracting">Discuss Your Contracting Needs <span class="ar"></span></a>')}
<section class="svc-block" id="solicitation-to-bid" style="padding-top:clamp(50px,6vw,90px)"><div class="wrap split">
  <div style="grid-column:1/5" class="rv"><div class="label"><span class="n">01·b</span>From solicitation to submission</div><h2 class="h3" style="margin-top:18px">Eighty pages in. <em>One clean bid out.</em></h2><p class="body" style="margin-top:16px">Every solicitation is read in full. The items that decide a bid are pulled out first: scope, deadlines, wage determinations, insurance and site requirements. Then the response is built around them.</p></div>
  <div style="grid-column:6/13" class="rv"><div class="docanim" id="docanim" aria-label="Animation: solicitation pages are reviewed, key requirements highlighted, and condensed into a bid package">
    <div class="dpage" style="--i:0;--x:calc(-2.5 * min(96px,12vw));--y:20px;--r:-12.5deg"><i class="hd"></i><i style="width:67%"></i><i style="width:71%"></i><i style="width:58%"></i><i style="width:98%"></i><i style="width:77%"></i><i style="width:82%"></i><i style="width:61%"></i><i style="width:57%"></i><i style="width:56%"></i><i style="width:53%"></i><i style="width:77%"></i><i style="width:87%"></i><i style="width:70%"></i><i style="width:100%"></i><span class="pn">p. 1</span></div><div class="dpage" style="--i:1;--x:calc(-1.5 * min(96px,12vw));--y:12px;--r:-7.5deg"><i class="hd"></i><i style="width:55%"></i><i style="width:66%"></i><i style="width:85%"></i><i class="hl" style="--d:1.3s;width:94%"></i><i style="width:86%"></i><i style="width:75%"></i><i style="width:69%"></i><i style="width:63%"></i><i style="width:58%"></i><i style="width:68%"></i><i style="width:65%"></i><i style="width:53%"></i><i style="width:93%"></i><i style="width:68%"></i><span class="pn">p. 9</span></div><div class="dpage" style="--i:2;--x:calc(-0.5 * min(96px,12vw));--y:4px;--r:-2.5deg"><i class="hd"></i><i style="width:69%"></i><i style="width:64%"></i><i style="width:62%"></i><i style="width:71%"></i><i style="width:70%"></i><i style="width:92%"></i><i class="hl" style="--d:1.8s;width:94%"></i><i style="width:98%"></i><i style="width:75%"></i><i style="width:57%"></i><i style="width:90%"></i><i style="width:73%"></i><i style="width:94%"></i><i style="width:76%"></i><span class="pn">p. 17</span></div><div class="dpage" style="--i:3;--x:calc(0.5 * min(96px,12vw));--y:4px;--r:2.5deg"><i class="hd"></i><i style="width:84%"></i><i style="width:67%"></i><i style="width:63%"></i><i style="width:67%"></i><i class="hl" style="--d:2.3s;width:94%"></i><i style="width:82%"></i><i style="width:69%"></i><i style="width:57%"></i><i style="width:87%"></i><i style="width:71%"></i><i style="width:52%"></i><i style="width:70%"></i><i style="width:88%"></i><i style="width:97%"></i><span class="pn">p. 34</span></div><div class="dpage" style="--i:4;--x:calc(1.5 * min(96px,12vw));--y:12px;--r:7.5deg"><i class="hd"></i><i style="width:71%"></i><i style="width:100%"></i><i style="width:84%"></i><i style="width:64%"></i><i style="width:78%"></i><i style="width:79%"></i><i style="width:90%"></i><i style="width:70%"></i><i class="hl" style="--d:2.8s;width:94%"></i><i style="width:79%"></i><i style="width:80%"></i><i style="width:62%"></i><i style="width:66%"></i><i style="width:71%"></i><span class="pn">p. 52</span></div><div class="dpage" style="--i:5;--x:calc(2.5 * min(96px,12vw));--y:20px;--r:12.5deg"><i class="hd"></i><i style="width:68%"></i><i style="width:54%"></i><i style="width:57%"></i><i style="width:54%"></i><i style="width:81%"></i><i class="hl" style="--d:3.3s;width:94%"></i><i style="width:92%"></i><i style="width:69%"></i><i style="width:85%"></i><i style="width:86%"></i><i style="width:93%"></i><i style="width:82%"></i><i style="width:96%"></i><i style="width:73%"></i><span class="pn">p. 80</span></div>
    <div class="co" style="--d:1.3s;left:4%;top:9%"><small>Scope</small>Custodial services, 3 buildings</div>
    <div class="co" style="--d:1.8s;right:4%;top:15%"><small>Response due</small>14 days from posting</div>
    <div class="co" style="--d:2.3s;left:3%;top:64%"><small>Wage rates</small>Service Contract Act applies</div>
    <div class="co" style="--d:2.8s;right:5%;top:70%"><small>Insurance</small>General liability required</div>
    <div class="co" style="--d:3.3s;left:34%;top:86%"><small>Site visit</small>Optional, scheduled</div>
    <div class="dsum"><div class="label" style="color:var(--brass)">Bid package</div><h4>Ready to submit</h4><ul>
      <li style="animation-delay:5.2s">Requirements confirmed</li><li style="animation-delay:5.35s">Partner pricing in hand</li><li style="animation-delay:5.5s">Forms, reps and certifications</li><li style="animation-delay:5.65s">Wage rates applied</li><li style="animation-delay:5.8s">Submitted ahead of deadline</li></ul></div>
    <span class="ex">Illustrative example</span>
  </div></div>
</div></section>
{svc("business-development", "02", "Business", "Development.",
     "Most government work is won through relationships formed long before a solicitation is released. We help businesses build the partnerships and market position that lead to sustained growth.",
     ["Strategic partnerships", "Prime contractor relationships", "Subcontracting opportunities", "Business growth strategies", "Market research", "Industry research", "Business opportunity identification"],
     "boardroom", "Meeting room with a long wooden table and chairs", True,
     '<a class="link" style="margin-top:30px" href="contact.html?topic=partnerships">Explore Business Development Services <span class="ar"></span></a>')}
<section class="svc-block white" id="teaming"><div class="wrap split">
  <div style="grid-column:1/6" class="rv"><div class="label"><span class="n">02·b</span>For prime contractors</div><h2 class="h2" style="margin-top:18px">Teaming with <em>prime contractors.</em></h2>
    <p class="body">Large primes need dependable small businesses to perform parts of their contracts and meet their small business subcontracting goals. Projexian can join your team as a registered small business subcontractor.</p>
    <p class="src" style="margin-top:22px">UEI MAVQJ6NPEL59 · CAGE 25TN9</p>
    <a class="btn" style="margin-top:28px" href="contact.html?topic=teaming">Discuss teaming</a></div>
  <div style="grid-column:7/13" class="rv">
    <div class="label">What we bring</div>
    <ul class="items" style="grid-template-columns:1fr;margin-top:14px"><li>Facility services across all 50 states and U.S. territories: janitorial, grounds, snow, pest control, refuse and site support</li><li>A network of vetted local crews near the place of performance, managed through one point of contact</li><li>Compliance handled up front: wage determinations, insurance and site access requirements</li><li>Daily tracking of federal solicitations, so we can help you spot and prepare for upcoming bids</li></ul>
    <div class="label" style="margin-top:34px">How we work with primes</div>
    <ul class="items" style="grid-template-columns:1fr;margin-top:14px"><li>Teaming agreements before you bid, or subcontracts after you win</li><li>We price our scope, provide our registration and capability details, and support your proposal</li><li>One accountable contact for your program manager</li></ul>
  </div>
</div></section>
<section class="svc-block dark" id="lead-generation"><div class="wrap split">
  <div style="grid-column:1/6">{img("binders", "Row of colored binders on an office shelf", "rv")}</div>
  <div style="grid-column:7/13" class="rv"><div class="num">03</div><h2 class="h2">Lead <em>Generation.</em></h2>
    <p class="body">We research and qualify the businesses and decision-makers most likely to buy what you sell, then deliver them in a form your team can act on.</p>
    <ul class="items"><li>Targeted B2B lead generation</li><li>Business prospect research</li><li>Industry-specific prospecting</li><li>Government contractor prospect identification</li><li>Qualified business leads</li><li>Contact research</li><li>Business development campaigns</li></ul>
    <div style="margin-top:34px;display:flex;gap:18px;flex-wrap:wrap;align-items:center"><a class="btn brass" href="lead-generation.html#inquiry">Request Lead Generation Information</a><a class="link" href="lead-generation.html">How it works <span class="ar"></span></a></div>
  </div>
</div></section>
<section class="svc-block" id="opportunity-intelligence"><div class="wrap split">
  <div style="grid-column:1/7" class="rv"><div class="num">04</div><h2 class="h2">Opportunity <em>Intelligence.</em></h2>
    <p class="body">Good decisions start with good information. We track the public procurement market every day and turn it into research a business can use: what is being bought, by whom, and how often.</p>
    <ul class="items"><li>Government contract research</li><li>Procurement opportunity discovery</li><li>Market analysis</li><li>Competitor research</li><li>Industry tracking</li><li>Subcontracting opportunity research</li><li>Business intelligence</li></ul>
    <a class="link" style="margin-top:30px" href="contact.html?topic=research">Identify Your Next Opportunity <span class="ar"></span></a>
  </div>
  <div style="grid-column:8/13" class="rv" data-live>
    <div class="label" style="margin-bottom:6px">Live sample · open opportunities by category</div>
    <div class="bignum" id="iOpen" style="font-size:clamp(70px,7vw,110px)">—</div>
    <div class="bars" id="iCats" style="margin-top:22px"></div>
    <p class="src iUpd"></p>
    <a class="link" style="margin-top:18px" href="opportunities.html">Open the opportunity map <span class="ar"></span></a>
  </div>
</div></section>
<section class="sec" id="capabilities"><div class="wrap">
  <div class="head-row"><div class="label rv"><span class="n">05</span>Capabilities</div><h2 class="h2 rv">What we can <em>deliver.</em></h2></div>
  <p class="body rv" style="margin:-30px 0 40px;max-width:640px">Through Projexian and our network of local partners, we support government buyers and prime contractors across these categories.</p>
  <div class="capgrid rv"><div class="capg"><h3>Facility services</h3><ul><li>Janitorial and custodial</li><li>Carpet and upholstery cleaning</li><li>Landscaping and grounds</li><li>Snow and ice removal</li><li>Pest control</li><li>Facilities support and operations</li><li>Building services</li><li>Industrial laundry</li><li>Food service and dining facilities</li></ul></div><div class="capg"><h3>Construction and trades</h3><ul><li>Commercial and institutional building</li><li>Residential remodeling</li><li>Highway, street and bridge</li><li>Heavy and civil construction</li><li>Water and sewer lines</li><li>Masonry</li><li>Roofing</li><li>Electrical</li><li>Plumbing, heating and air conditioning</li><li>Painting and wall covering</li><li>Windows, glass and glazing</li><li>Flooring</li><li>Site preparation</li><li>Specialty trades</li></ul></div><div class="capg"><h3>Environmental and waste</h3><ul><li>Solid waste collection</li><li>Recycling and scrap</li><li>Hazardous waste collection</li><li>Remediation</li><li>Waste management</li><li>Portable restrooms and septic services</li><li>Tree clearing and vegetation management</li></ul></div><div class="capg"><h3>Transportation and logistics</h3><ul><li>Local and long-distance freight</li><li>Specialized freight</li><li>Moving services</li><li>Courier and express delivery</li><li>Freight arrangement</li><li>Warehousing and storage</li></ul></div><div class="capg"><h3>Equipment rental and repair</h3><ul><li>Truck and trailer rental</li><li>Construction equipment rental</li><li>Commercial and industrial equipment rental</li><li>Medical equipment rental</li><li>Vehicle washing</li><li>Commercial machinery repair</li><li>Electronic and precision equipment repair</li></ul></div><div class="capg"><h3>Security and site services</h3><ul><li>Security guards and patrol</li><li>Security systems and access control</li><li>Parking management</li></ul></div><div class="capg"><h3>Products and supply</h3><ul><li>Office equipment and supplies</li><li>Furniture</li><li>Computers and peripherals</li><li>Medical and hospital supplies</li><li>Electrical equipment and wiring supplies</li><li>Industrial and manufactured goods</li></ul></div><div class="capg"><h3>Professional and technical</h3><ul><li>Engineering services</li><li>Building inspection</li><li>Environmental consulting</li><li>Management and logistics consulting</li><li>Office administration</li><li>Document preparation</li><li>Events and trade shows</li><li>Market research</li><li>Temporary staffing</li><li>Professional training</li><li>IT systems design and support</li></ul></div></div>
</div></section>
<section class="sec dark tight"><div class="wrap cta-strip">
  <h2 class="h2 rv">Not sure where to start? <em>Speak with our team.</em></h2>
  <div class="rv" style="display:flex;gap:16px;flex-wrap:wrap;justify-content:flex-end"><a class="btn brass" href="contact.html">Start a Conversation</a><a class="btn ghost" href="assets/projexian-capabilities-statement.pdf">Capabilities Statement</a></div>
</div></section>
""", extra_js='<script src="assets/live.js" defer></script>')

    # ---------------- OPPORTUNITIES ----------------
    pages["opportunities.html"] = page("opportunities.html", "Government Contracting Opportunities | Projexian",
        "Explore open federal contracting opportunities across all 50 states and U.S. territories, filtered by industry, location, agency, category and type.",
        OPP_BODY.replace('<section class="sec white"><div class="wrap">\n  <div class="head-row"><div class="label rv"><span class="n">02</span>The Marketplace', recompete_table(awards) + '<section class="sec white"><div class="wrap">\n  <div class="head-row"><div class="label rv"><span class="n">02</span>The Marketplace'), extra_js='<script src="assets/vendor/d3.min.js" defer></script><script src="assets/vendor/topojson-client.min.js" defer></script><script src="assets/live.js" defer></script>')

    # ---------------- INDUSTRIES ----------------
    rows = []
    for i, (slug, name, ph, alt, text, cats) in enumerate(INDUSTRIES):
        flip = i % 2 == 1
        pic = f'<div style="grid-column:{"7/13" if flip else "1/7"};grid-row:1">{img(ph, alt, "rv")}</div>'
        txt = f'''<div style="grid-column:{"1/6" if flip else "8/13"};grid-row:1" class="rv"><div class="no">{i+1:02d}</div><h2>{name}</h2><p class="body">{text}</p>
<a class="link" href="contact.html?topic=contracting&amp;industry={slug}">Inquire about {name.lower()} <span class="ar"></span></a></div>'''
        rows.append(f'<section class="ind" id="{slug}">{pic}{txt}</section>')
    pages["industries.html"] = page("industries.html", "Industries We Serve | Projexian",
        "Industries Projexian supports in the government marketplace, from construction and facility maintenance to IT, logistics and security.",
        f"""
<div class="wrap"><div class="phead">
  <div class="label rv">Industries We Serve</div>
  <h1 class="display rv">Where public money <em>meets private capability.</em></h1>
  <p class="body rv">Government agencies buy across hundreds of categories. These are the industries we are positioned to support, with examples of how agencies classify the work. They describe where we can help, not completed projects.</p>
</div>
{"".join(rows)}
</div>
<section class="sec dark tight"><div class="wrap cta-strip">
  <h2 class="h2 rv">Don't see your industry? <em>Ask us.</em></h2>
  <div class="rv" style="display:flex;justify-content:flex-end"><a class="btn brass" href="contact.html">Speak With Our Team</a></div>
</div></section>
""")

    # ---------------- ABOUT ----------------
    pages["about.html"] = page("about.html", "About Us | Projexian",
        "Projexian LLC is an American small business focused on government contracting, business development, market intelligence and lead generation.",
        f"""
<section class="hero" style="min-height:0">
  <div class="txt" style="justify-content:center">
    <div><div class="label rv">About Us</div>
    <h1 class="display rv" style="margin-top:26px">Built Around Opportunity. <em>Driven by Strategy.</em></h1>
    <p class="sub rv">Projexian is an American small business that helps companies find, pursue and win work in the government marketplace, and build the relationships that keep it coming.</p></div>
  </div>
  {img("eeob", "Ornate facade of a historic government office building in Washington, D.C.", eager=True, cap="Illustrative · Washington, D.C.", sizes="(max-width: 1080px) 100vw, 58vw")}
</section>

<section class="sec"><div class="wrap grid12 intro">
  <div class="label rv"><span class="n">01</span>Company Overview</div>
  <p class="lead rv">We combine daily market research with hands-on contracting work. That means we see what agencies are buying, understand how they buy it, and know which businesses are positioned to deliver.</p>
  <div class="facts rv">
    <div class="fact"><div class="k">Legal name</div><div class="v">Projexian LLC</div><div class="d">Limited liability company</div></div>
    <div class="fact"><div class="k">Coverage</div><div class="v">Nationwide</div><div class="d">All 50 states and U.S. territories</div></div>
    <div class="fact"><div class="k">Registration</div><div class="v">SAM.gov · Active</div><div class="d">UEI MAVQJ6NPEL59 · CAGE 25TN9</div></div>
  </div>
</div></section>

<section class="sec white"><div class="wrap">
  <div class="head-row"><div class="label rv"><span class="n">02</span>Our Approach</div><h2 class="h2 rv">Six commitments that <em>shape every engagement.</em></h2></div>
  <div class="principles rv">
    <div class="principle"><span class="n">i.</span><h3>Government contracting</h3><p>We pursue work a business can realistically win and deliver, and we read every requirement before recommending a bid.</p></div>
    <div class="principle"><span class="n">ii.</span><h3>Business development</h3><p>Growth in this market is built on relationships with agencies, primes and partners. We invest in them before they are needed.</p></div>
    <div class="principle"><span class="n">iii.</span><h3>Market intelligence</h3><p>We track the procurement market every day so recommendations rest on current data, not assumptions.</p></div>
    <div class="principle"><span class="n">iv.</span><h3>Strategic relationships</h3><p>We connect businesses with the right partners: local firms that perform and larger firms that need capable subcontractors.</p></div>
    <div class="principle"><span class="n">v.</span><h3>Lead generation</h3><p>Prospects are researched and qualified before they reach you, so your team spends its time on real conversations.</p></div>
    <div class="principle"><span class="n">vi.</span><h3>Long-term growth</h3><p>One contract should lead to the next. We plan for past performance, references and repeat business from the start.</p></div>
  </div>
</div></section>

<section class="sec dark"><div class="wrap">
  <div class="head-row"><div class="label rv"><span class="n">03</span>Mission &amp; Values</div><h2 class="h2 rv">Our mission is to make the government marketplace <em>accessible to capable businesses.</em></h2></div>
  <div class="values rv">
    <div class="value"><h3>Accuracy</h3><p>We say what a solicitation requires and what it will take, even when the answer is not to bid.</p></div>
    <div class="value"><h3>Accountability</h3><p>One point of contact, clear commitments and follow-through from first call to final invoice.</p></div>
    <div class="value"><h3>Integrity</h3><p>We follow procurement rules closely and represent our capabilities and our partners honestly.</p></div>
    <div class="value"><h3>Partnership</h3><p>Our success depends on the businesses we work with. We build arrangements that are fair to both sides.</p></div>
  </div>
</div></section>

<section class="sec"><div class="wrap">
  <div class="head-row"><div class="label rv"><span class="n">04</span>Leadership</div><h2 class="h2 rv">Leadership</h2></div>
  <div class="leader solo rv">
    <div><h3 class="h3">Tyler Montgomery</h3><div class="label" style="margin-top:10px">Founder</div>
      <p class="body" style="margin-top:22px">Tyler founded Projexian to help businesses compete for government work with better information and stronger relationships. He leads the firm's contracting, business development and research work, and is the point of contact for clients, partners and contracting officers.</p>
      <div style="margin-top:30px;display:flex;gap:24px;flex-wrap:wrap"><a class="link" href="mailto:{EMAIL}">{EMAIL} <span class="ar"></span></a><a class="link" href="tel:+1{PHONE.replace('-', '')}">{PHONE} <span class="ar"></span></a></div>
    </div>
  </div>
</div></section>

<section class="sec white light"><div class="wrap">
  <div class="head-row"><div class="label rv"><span class="n">05</span>Credentials</div><h2 class="h2 rv">Registration <em>&amp; capabilities.</em></h2></div>
  <div class="creds rv">
    <div class="cred"><div class="k">SAM.gov</div><div class="v">Active</div></div>
    <div class="cred"><div class="k">UEI</div><div class="v">MAVQJ6NPEL59</div></div>
    <div class="cred"><div class="k">CAGE</div><div class="v">25TN9</div></div>
    <div class="cred"><div class="k">Business size</div><div class="v">Small business</div></div>
    <div class="cred"><div class="k">Founded</div><div class="v">2026</div></div>
  </div>
  <div style="margin-top:36px;display:flex;gap:24px;flex-wrap:wrap;align-items:center" class="rv"><a class="btn" href="assets/projexian-capabilities-statement.pdf">Download Capabilities Statement <span aria-hidden="true">↓</span></a><a class="link" href="industries.html">Industries we serve <span class="ar"></span></a></div>
</div></section>
""")

    # ---------------- LEAD GENERATION ----------------
    pages["lead-generation.html"] = page("lead-generation.html", "Lead Generation | Projexian",
        "Targeted B2B lead generation, prospect research and government contractor prospecting from Projexian.",
        f"""
<div class="wrap"><div class="phead">
  <div class="label rv">Lead Generation</div>
  <h1 class="display rv">Better Intelligence. <em>More Meaningful Connections.</em></h1>
  <p class="body rv">We help businesses find the customers most likely to buy, from commercial buyers to the prime contractors and agencies active in their market, and we deliver those prospects researched, qualified and ready for outreach.</p>
</div></div>
<section class="band" style="height:min(62vh,600px)">
  <img src="img/archive-1600.jpg" srcset="img/archive-900.jpg 900w, img/archive-1600.jpg 1600w" sizes="100vw" alt="Rows of document boxes in an archive" loading="lazy">
  <span class="cap">Illustrative</span>
</section>
<section class="sec"><div class="wrap">
  <div class="head-row"><div class="label rv"><span class="n">01</span>Process</div><h2 class="h2 rv">From target market <em>to first conversation.</em></h2></div>
  <div class="process rv">
    <div class="step"><div class="n">01</div><h3>Define</h3><p>We agree on your ideal customer: industry, size, geography, buying signals and the roles that make decisions.</p></div>
    <div class="step"><div class="n">02</div><h3>Research</h3><p>We build the prospect list from public records, procurement data, permits and industry sources.</p></div>
    <div class="step"><div class="n">03</div><h3>Qualify</h3><p>Each prospect is checked for fit and current activity, and verified contacts are added.</p></div>
    <div class="step"><div class="n">04</div><h3>Deliver</h3><p>You receive organized leads with the context your team needs, on a schedule that fits your pipeline.</p></div>
  </div>
</div></section>
<section class="sec white"><div class="wrap split">
  <div style="grid-column:1/6" class="rv"><div class="label"><span class="n">02</span>What we provide</div><h2 class="h2" style="margin-top:18px">Leads built for <em>your market.</em></h2></div>
  <div style="grid-column:7/13" class="rv"><ul class="items" style="margin-top:0"><li>B2B prospecting</li><li>Industry-specific research</li><li>Target market identification</li><li>Business contact research</li><li>Government contractor prospecting</li><li>Qualified lead generation</li><li>Business development support</li><li>Public bid and project monitoring</li></ul></div>
</div></section>
<section class="sec" id="inquiry"><div class="wrap formwrap">
  <div class="rv"><div class="label"><span class="n">03</span>Inquiry</div><h2 class="h2" style="margin-top:18px">Request lead generation <em>information.</em></h2><p class="body" style="margin-top:18px">Tell us about your business and the customers you want to reach. We will reply within one business day.</p>
    <div class="side-info" style="margin-top:34px"><div><div class="k">Email</div><div class="v"><a href="mailto:{EMAIL}">{EMAIL}</a></div></div><div><div class="k">Phone</div><div class="v"><a href="tel:+1{PHONE.replace('-', '')}">{PHONE}</a></div></div></div></div>
  <form class="f rv" action="{FORM_ACTION}" method="POST">
    {form_hidden("Lead generation inquiry · projexian.com")}
    <div class="fld"><label for="lg-name">Full name <i>*</i></label><input id="lg-name" name="Full name" autocomplete="name" required></div>
    <div class="fld"><label for="lg-co">Company <i>*</i></label><input id="lg-co" name="Company" autocomplete="organization" required></div>
    <div class="fld"><label for="lg-email">Business email <i>*</i></label><input id="lg-email" type="email" name="email" autocomplete="email" required></div>
    <div class="fld"><label for="lg-phone">Phone number</label><input id="lg-phone" type="tel" name="Phone" autocomplete="tel"></div>
    <div class="fld"><label for="lg-ind">Industry <i>*</i></label><input id="lg-ind" name="Industry" required></div>
    <div class="fld"><label for="lg-target">Target market <i>*</i></label><input id="lg-target" name="Target market" placeholder="e.g. general contractors in Texas" required></div>
    <div class="fld"><label for="lg-type">Type of leads needed <i>*</i></label><select id="lg-type" name="Type of leads" required><option value="">Select</option><option>Commercial businesses (B2B)</option><option>Government contractors / primes</option><option>Government agencies</option><option>Construction projects &amp; build-outs</option><option>Public bids in my trade</option><option>Other</option></select></div>
    <div class="fld"><label for="lg-vol">Estimated monthly leads</label><select id="lg-vol" name="Monthly leads"><option value="">Select</option><option>Fewer than 50</option><option>50–150</option><option>150–500</option><option>500+</option><option>Not sure yet</option></select></div>
    <div class="fld full"><label for="lg-more">Additional information</label><textarea id="lg-more" name="Additional information"></textarea></div>
    <label class="consent"><input type="checkbox" name="Consent" value="Yes" required><span>I agree to the <a href="terms.html">Terms of Use</a> and <a href="privacy.html">Privacy Notice</a>, and that Projexian may use the information I provide to respond to this inquiry. <i style="color:var(--brass);font-style:normal">*</i></span></label>
    <label class="consent"><input type="checkbox" name="Updates" value="Yes"><span>Send me occasional updates about Projexian services. Optional; you can unsubscribe at any time.</span></label>
    <div class="fld full"><button class="btn" type="submit">Submit Inquiry <span aria-hidden="true">→</span></button></div>
    <p class="privacy">We use your information only to respond to your inquiry. We do not sell or share it for marketing. Submissions are delivered by our form provider, FormSubmit. See our <a href="privacy.html">privacy notice</a>.</p>
  </form>
</div></section>
""")

    # ---------------- CONTACT ----------------
    pages["contact.html"] = page("contact.html", "Contact | Projexian",
        "Contact Projexian about government contracting support, lead generation, partnerships or procurement research.",
        f"""
<div class="wrap"><div class="phead">
  <div class="label rv">Contact</div>
  <h1 class="display rv">Let's Discuss Your <em>Next Opportunity.</em></h1>
  <p class="body rv">Whether you are preparing a first bid, looking for partners or need research on a market, start here. We reply within one business day.</p>
</div></div>
<section class="sec" style="padding-top:0"><div class="wrap formwrap">
  <div class="rv">
    <div class="side-info">
      <div><div class="k">Email</div><div class="v"><a href="mailto:{EMAIL}">{EMAIL}</a></div></div>
      <div><div class="k">Phone</div><div class="v"><a href="tel:+1{PHONE.replace('-', '')}">{PHONE}</a></div></div>
      <div><div class="k">Registration</div><div class="v" style="font-size:20px">UEI MAVQJ6NPEL59 · CAGE 25TN9</div></div>
    </div>
    <a class="link" style="margin-top:28px" href="assets/projexian-capabilities-statement.pdf">Download capabilities statement <span aria-hidden="true">↓</span></a>
  </div>
  <form class="f rv" action="{FORM_ACTION}" method="POST" id="contactForm">
    {form_hidden("New inquiry · projexian.com")}
    <div class="fld"><label for="c-name">Name <i>*</i></label><input id="c-name" name="Name" autocomplete="name" required></div>
    <div class="fld"><label for="c-co">Company name <i>*</i></label><input id="c-co" name="Company" autocomplete="organization" required></div>
    <div class="fld"><label for="c-email">Business email <i>*</i></label><input id="c-email" type="email" name="email" autocomplete="email" required></div>
    <div class="fld"><label for="c-phone">Phone number</label><input id="c-phone" type="tel" name="Phone" autocomplete="tel"></div>
    <div class="fld"><label for="c-svc">Service requested <i>*</i></label><select id="c-svc" name="Service requested" required><option value="">Select</option><option value="Government contracting support" data-topic="contracting">Government contracting support</option><option value="Lead generation" data-topic="leads">Lead generation</option><option value="Subcontracting and partnerships" data-topic="partnerships">Subcontracting and partnerships</option><option value="Teaming with a prime" data-topic="teaming">Teaming with a prime</option><option value="Procurement research" data-topic="research">Procurement research</option><option value="Business development" data-topic="bd">Business development</option><option value="Other">Other</option></select></div>
    <div class="fld"><label for="c-ind">Industry</label><select id="c-ind" name="Industry"><option value="">Select</option>{"".join(f'<option value="{n}" data-slug="{s}">{n}</option>' for s, n, *_ in INDUSTRIES)}<option>Other</option></select></div>
    <div class="fld full"><label for="c-desc">Project description <i>*</i></label><textarea id="c-desc" name="Project description" required></textarea></div>
    <div class="fld full"><label for="c-more">Additional comments</label><textarea id="c-more" name="Additional comments" style="min-height:80px"></textarea></div>
    <label class="consent"><input type="checkbox" name="Consent" value="Yes" required><span>I agree to the <a href="terms.html">Terms of Use</a> and <a href="privacy.html">Privacy Notice</a>, and that Projexian may use the information I provide to respond to this inquiry. <i style="color:var(--brass);font-style:normal">*</i></span></label>
    <div class="fld full"><button class="btn" type="submit">Send Inquiry <span aria-hidden="true">→</span></button></div>
    <p class="privacy">We use your information only to respond to your inquiry. We do not sell or share it. Submissions are delivered by our form provider, FormSubmit. See our <a href="privacy.html">privacy notice</a>.</p>
  </form>
</div></section>
""")

    # ---------------- THANKS / PRIVACY / CREDITS ----------------
    pages["thanks.html"] = page("thanks.html", "Thank You | Projexian", "Your inquiry has been received.", """
<div class="wrap"><div class="phead" style="min-height:60vh">
  <div class="label">Received</div>
  <h1 class="display">Thank you. <em>We'll be in touch.</em></h1>
  <p class="body">Your inquiry reached our team. We reply within one business day. If it's urgent, call 630-888-8182.</p>
  <div style="grid-column:4/12;margin-top:34px"><a class="link" href="index.html">Return home <span class="ar"></span></a></div>
</div></div>""").replace('<meta name="theme-color"', '<meta name="robots" content="noindex"><meta name="theme-color"')

    pages["privacy.html"] = page("privacy.html", "Privacy Notice | Projexian", "How Projexian handles information submitted through this website.", f"""
<div class="wrap"><div class="phead"><div class="label">Privacy Notice</div><h1 class="display">Privacy <em>notice.</em></h1>
<div class="body" style="grid-column:4/11">
<p style="margin-top:28px"><b>What we collect.</b> When you submit a form, we receive the information you enter: your name, company, contact details and the details of your inquiry. We do not use advertising trackers on this site.</p>
<p style="margin-top:18px"><b>How we use it.</b> We use your information to respond to your inquiry and, if you ask us to, to send occasional updates about our services. We do not sell your information or share it with third parties for their marketing.</p>
<p style="margin-top:18px"><b>Form delivery.</b> Forms are delivered to us by FormSubmit (formsubmit.co), which processes submissions in order to email them to us.</p>
<p style="margin-top:18px"><b>Your choices.</b> To access, correct or delete information you sent us, or to unsubscribe, email <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
<p style="margin-top:18px"><b>Live data.</b> Opportunity figures on this site come from public U.S. government procurement data (SAM.gov).</p>
<p style="margin-top:18px;color:var(--slate)">Last updated November 2026.</p></div></div></div>""")

    cred_rows = "".join(
        f'<li style="padding:14px 0;border-bottom:1px solid var(--line)"><b style="font-family:var(--serif);font-size:20px;color:var(--navy)">{html.escape(k.title())}</b><br>'
        f'<span style="font-size:14px;color:#4a535a">{html.escape(v.get("title","").replace("File:",""))} · {html.escape(v.get("artist") or "Unknown")} · {html.escape(v.get("license",""))} · '
        f'<a style="text-decoration:underline" href="{html.escape(v.get("page",""))}">Source</a></span></li>'
        for k, v in sorted(CREDITS.items()))
    pages["credits.html"] = page("credits.html", "Photo Credits | Projexian", "Photo credits and licenses.", f"""
<div class="wrap"><div class="phead"><div class="label">Photo Credits</div><h1 class="display">Photo <em>credits.</em></h1>
<div class="body" style="grid-column:4/12"><p style="margin-top:28px">Photographs on this site are illustrative and do not depict Projexian projects. They are used under public-domain or Creative Commons licenses from Wikimedia Commons and the Library of Congress.</p>
<ul style="list-style:none;margin-top:28px;border-top:1px solid var(--line)">{cred_rows}</ul></div></div></div>""")

    # ---------------- PARTNERS ----------------
    st_opts = "".join(f'<option value="{e(v)}">{e(v)}</option>' for v in sorted(ST_NAMES.values()))
    trades = "".join(f'<label class="chk"><input type="checkbox" name="Trades" value="{e(t)}"><span>{e(t)}</span></label>' for t in TRADES)
    pages["partners.html"] = page("partners.html", "Partner Network | Projexian",
        "Local service companies: join the Projexian partner network to perform federal facility service contracts in your area.",
        f"""
<div class="wrap"><div class="phead">
  <div class="label rv">Partner Network</div>
  <h1 class="display rv">Your crew. <em>Our contracts.</em></h1>
  <p class="body rv">Cleaning, grounds, snow, pest control, hauling and facility companies across the country: we bring you federal work you would rarely see, and we handle the government side so your team can focus on doing the job well.</p>
</div></div>
<section class="sec tight" style="padding-top:0"><div class="wrap">
  <div class="process rv">
    <div class="step"><div class="n">01</div><h3>Register</h3><p>Tell us what you do and where. It takes about three minutes.</p></div>
    <div class="step"><div class="n">02</div><h3>Get matched</h3><p>When a contract fits your trade and area, we send you the full package to review.</p></div>
    <div class="step"><div class="n">03</div><h3>Price the work</h3><p>You quote the work you already do well. We build and submit the bid.</p></div>
    <div class="step"><div class="n">04</div><h3>Perform</h3><p>We manage the contract, paperwork and invoicing. You get steady, multi-year work.</p></div>
  </div>
</div></section>
<section class="sec white"><div class="wrap split">
  <div style="grid-column:1/6" class="rv"><div class="label"><span class="n">02</span>What we look for</div><h2 class="h2" style="margin-top:18px">Reliable crews <em>that show up.</em></h2></div>
  <div style="grid-column:7/13" class="rv"><ul class="items" style="margin-top:0"><li>Licensed where your trade requires it</li><li>General liability insurance, or able to obtain it</li><li>A dependable crew and supervisor</li><li>Willing to follow federal wage requirements</li><li>Staff able to pass site background checks</li><li>References from commercial customers</li></ul></div>
</div></section>
<section class="sec" id="apply"><div class="wrap formwrap">
  <div class="rv"><div class="label"><span class="n">03</span>Apply</div><h2 class="h2" style="margin-top:18px">Join the <em>partner network.</em></h2><p class="body" style="margin-top:18px">There is no cost to join. We will reach out when an opportunity matches your trade and service area.</p>
    <p class="src" style="margin-top:24px">Joining does not guarantee work or create a contract. Any engagement is made under a separate written subcontract agreement.</p></div>
  <form class="f rv" action="{FORM_ACTION}" method="POST" id="partnerForm">
    {form_hidden("Partner network application · projexian.com")}
    <div class="fld"><label for="p-co">Company name <i>*</i></label><input id="p-co" name="Company" autocomplete="organization" required maxlength="150"></div>
    <div class="fld"><label for="p-name">Contact name <i>*</i></label><input id="p-name" name="Contact name" autocomplete="name" required maxlength="120"></div>
    <div class="fld"><label for="p-email">Email <i>*</i></label><input id="p-email" type="email" name="email" autocomplete="email" required maxlength="150"></div>
    <div class="fld"><label for="p-phone">Phone <i>*</i></label><input id="p-phone" type="tel" name="Phone" autocomplete="tel" required maxlength="30"></div>
    <div class="fld full"><label>Services you provide <i>*</i></label><div class="chks">{trades}</div></div>
    <div class="fld"><label for="p-st">Primary state <i>*</i></label><select id="p-st" name="Primary state" required><option value="">Select</option>{st_opts}</select></div>
    <div class="fld"><label for="p-area">Service area <i>*</i></label><input id="p-area" name="Service area" required maxlength="200" placeholder="Cities, counties or miles from base"></div>
    <div class="fld"><label for="p-yrs">Years in business</label><select id="p-yrs" name="Years in business"><option value="">Select</option><option>Less than 1</option><option>1–3</option><option>3–10</option><option>10+</option></select></div>
    <div class="fld"><label for="p-crew">Crew size</label><select id="p-crew" name="Crew size"><option value="">Select</option><option>1–5</option><option>6–15</option><option>16–50</option><option>50+</option></select></div>
    <div class="fld"><label for="p-ins">General liability insurance</label><select id="p-ins" name="Insurance"><option value="">Select</option><option>Yes</option><option>No</option><option>In progress</option></select></div>
    <div class="fld"><label for="p-gov">Prior government work</label><select id="p-gov" name="Prior government work"><option value="">Select</option><option>Yes, federal</option><option>Yes, state or local</option><option>No</option></select></div>
    <div class="fld"><label for="p-web">Website</label><input id="p-web" type="url" name="Website" maxlength="200" placeholder="https://"></div>
    <div class="fld"><label for="p-sam">Registered in SAM.gov</label><select id="p-sam" name="SAM registered"><option value="">Select</option><option>Yes</option><option>No</option><option>Not sure</option></select></div>
    <div class="fld full"><label for="p-notes">Anything else</label><textarea id="p-notes" name="Notes" maxlength="3000"></textarea></div>
    <label class="consent"><input type="checkbox" name="Consent" value="Yes" required><span>I agree to the <a href="terms.html">Terms of Use</a> and <a href="privacy.html">Privacy Notice</a>, and I understand joining the network does not guarantee work. <i style="color:var(--brass);font-style:normal">*</i></span></label>
    <div class="fld full"><button class="btn" type="submit">Submit Application <span aria-hidden="true">→</span></button></div>
    <p class="privacy">Do not include Social Security numbers, bank details or other sensitive personal information in this form.</p>
  </form>
</div></section>
""")

    # ---------------- LEGAL ----------------
    def legal(fn, title, h1, sections, intro=""):
        secs = "".join(f'<div class="lg"><h2>{n:02d}. {e(h)}</h2>{b}</div>' for n, (h, b) in enumerate(sections, 1))
        return page(fn, f"{title} | Projexian", f"{title} for projexian.com.", f"""
<div class="wrap"><div class="phead"><div class="label">Legal</div><h1 class="display">{h1}</h1>
<div class="body" style="grid-column:4/12;margin-top:24px"><p>{intro}</p><p class="src" style="margin-top:10px">Effective November 7, 2026</p></div></div>
<div class="legal">{secs}</div></div>""")

    C = f'<a href="mailto:{EMAIL}">{EMAIL}</a>'
    pages["terms.html"] = legal("terms.html", "Terms of Use", "Terms of <em>Use.</em>", [
        ("Agreement", "<p>These Terms of Use govern your use of projexian.com (the “Site”), operated by Projexian LLC (“Projexian,” “we,” “us”). By using the Site you agree to these terms. If you do not agree, please do not use the Site.</p>"),
        ("No government affiliation", "<p>Projexian is a private company. We are not a government agency and are not affiliated with, endorsed by or acting on behalf of any federal, state or local government. References to agencies describe public procurement activity only.</p>"),
        ("Information only", "<p>Content on the Site is general information. It is not legal, financial, tax or procurement advice, and it does not create a client, agency or partnership relationship. Decisions about bidding, pricing or compliance should be made with the official solicitation documents and, where appropriate, qualified professional advice.</p>"),
        ("Opportunity and award data", "<p>Opportunity listings, award history and market figures are compiled automatically from public sources such as SAM.gov and USAspending.gov. They are provided “as is” and may be incomplete, delayed or out of date. Deadlines, amendments and requirements must always be confirmed in the official notice. We do not guarantee the accuracy of third-party data or that any opportunity will remain open.</p>"),
        ("No guarantee of work or results", "<p>Submitting an inquiry, joining the partner network or using our services does not guarantee a contract award, revenue, leads or any particular result. Any work we perform together is governed by a separate written agreement.</p>"),
        ("Information you submit", "<p>You agree that information you submit is accurate and that you have the right to share it. Do not submit Social Security numbers, bank or payment card details, passwords, or classified or controlled information through the Site. Our handling of your information is described in our <a href=\"privacy.html\">Privacy Notice</a>.</p>"),
        ("Acceptable use", "<p>You agree not to: use the Site for any unlawful purpose; submit false, misleading or spam content; attempt to gain unauthorized access to the Site or related systems; introduce malware or interfere with the Site’s operation or security; scrape or harvest the Site in a way that places an unreasonable load on it; or use the Site to harass anyone or to collect information about other users.</p>"),
        ("Intellectual property", "<p>The Projexian name, logo, design, text and original graphics are owned by Projexian LLC and may not be copied or reused without permission, except for brief quotations with attribution. Government data is public. Photographs are used under their respective licenses, listed on our <a href=\"credits.html\">Photo Credits</a> page.</p>"),
        ("Third-party links and services", "<p>The Site links to third-party websites, including government sites, and uses a third-party service to deliver form submissions. We are not responsible for the content, availability or practices of third parties.</p>"),
        ("Disclaimer of warranties", "<p>The Site and its content are provided “as is” and “as available,” without warranties of any kind, express or implied, including warranties of accuracy, merchantability, fitness for a particular purpose and non-infringement.</p>"),
        ("Limitation of liability", "<p>To the fullest extent permitted by law, Projexian LLC will not be liable for any indirect, incidental, special, consequential or punitive damages, or for lost profits, revenue, data or business opportunities, arising from your use of or reliance on the Site. Our total liability for any claim relating to the Site will not exceed one hundred U.S. dollars.</p>"),
        ("Indemnification", "<p>You agree to indemnify and hold Projexian LLC harmless from claims arising from your misuse of the Site or your violation of these terms.</p>"),
        ("Governing law", "<p>These terms are governed by the laws of the State of Illinois, without regard to conflict-of-law rules. Any dispute will be brought in the state or federal courts located in Cook County, Illinois.</p>"),
        ("Changes", "<p>We may update these terms from time to time. The effective date above shows when they last changed. Continued use of the Site means you accept the updated terms.</p>"),
        ("Contact", f"<p>Questions about these terms: {C}, Projexian LLC.</p>"),
    ], "Please read these terms carefully before using this website.")

    pages["privacy.html"] = legal("privacy.html", "Privacy Notice", "Privacy <em>Notice.</em>", [
        ("Who we are", f"<p>Projexian LLC operates projexian.com. This notice explains what information we collect through the Site and how we use it. Contact: {C}.</p>"),
        ("Information you provide", "<p>When you submit a contact, lead generation or partner form, we receive the information you enter, such as your name, company, email, phone number, trade, service area and the details of your request.</p>"),
        ("Information collected automatically", "<p>We do not use cookies, advertising trackers, analytics scripts or social media pixels. Fonts, scripts and data are served from our own site, so loading a page does not send your information to third-party font or script providers. Our hosting provider, GitHub, may record standard technical information such as IP addresses in server logs for security and operations, under its own privacy statement.</p>"),
        ("How we use information", "<p>We use the information you submit to respond to your request, evaluate partner applications, match partners with relevant opportunities, provide services you ask for, and, if you opt in, send occasional updates. We do not sell or rent personal information, and we do not share it for third parties’ marketing.</p>"),
        ("Service providers", "<p>Form submissions are delivered to us by FormSubmit (formsubmit.co), which processes them in order to email them to us. We use email and business software to store and manage inquiries. These providers process information on our behalf. We may also disclose information when required by law or to protect our rights and the security of the Site.</p>"),
        ("Retention", "<p>We keep inquiry and partner information for as long as needed for the purpose it was provided, typically up to three years after our last contact, unless you ask us to delete it sooner or the law requires us to keep it longer.</p>"),
        ("Security", "<p>The Site is served only over encrypted HTTPS connections, loads no third-party scripts, and uses a strict content security policy. Forms include spam protection and ask you not to send sensitive information. No method of transmission or storage is perfectly secure, but we take reasonable measures to protect the information you share with us.</p>"),
        ("Your choices and rights", f"<p>You can ask us to access, correct or delete your information, or to stop sending updates, by emailing {C}. Depending on where you live, you may have additional rights under state privacy laws, including the right to know, correct, delete and opt out of the sale or sharing of personal information. We do not sell or share personal information as those terms are defined in such laws. We will not discriminate against you for exercising your rights.</p>"),
        ("Email communications", "<p>If you opt in to updates, every message will include a way to unsubscribe. Messages about an inquiry you sent are not marketing.</p>"),
        ("Children", "<p>The Site is intended for businesses and is not directed to children. We do not knowingly collect information from anyone under 16.</p>"),
        ("Changes", "<p>We may update this notice. The effective date above shows when it last changed.</p>"),
    ], "Your privacy matters. This site is built to collect as little as possible.")

    pages["accessibility.html"] = legal("accessibility.html", "Accessibility", "Accessibility <em>statement.</em>", [
        ("Our commitment", "<p>Projexian wants this site to be usable by everyone. We aim to meet the Web Content Accessibility Guidelines (WCAG) 2.1, Level AA.</p>"),
        ("What we have done", "<p>Pages use a logical heading structure, descriptive text for images, visible keyboard focus, a skip-to-content link, form labels, and sufficient color contrast. Animations are minimal and are turned off when your device requests reduced motion. The opportunity map can be operated by keyboard, and every map result is also available as a text list with filters.</p>"),
        ("Known limitations", "<p>Some content comes from third-party government data and may contain abbreviations or formatting we do not control. Downloadable PDFs may not be fully accessible; contact us for an alternative format.</p>"),
        ("Feedback", f"<p>If you have trouble using any part of this site, email {C} or call 630-888-8182. We will work with you to provide the information in a format that works for you.</p>"),
    ], "We want everyone to be able to use this site.")

    for fn, h in pages.items():
        open(os.path.join(DIST, fn), "w").write(_harden(h))
    os.makedirs(os.path.join(DIST, "opp"), exist_ok=True)
    opp_fns = []
    for it in feed["items"]:
        fn = f'opp/{it["u"]}.html'
        open(os.path.join(DIST, fn), "w").write(_harden(opp_page(it, feed, awards)))
        opp_fns.append(fn)
    os.makedirs(os.path.join(DIST, ".well-known"), exist_ok=True)
    sec = f"Contact: mailto:{EMAIL}\nExpires: 2027-11-07T00:00:00.000Z\nPreferred-Languages: en\nCanonical: {SITE_URL}/.well-known/security.txt\n"
    open(os.path.join(DIST, ".well-known", "security.txt"), "w").write(sec)
    open(os.path.join(DIST, ".nojekyll"), "w").write("")
    urls = "".join(f"<url><loc>{SITE_URL}/{'' if fn == 'index.html' else fn}</loc></url>" for fn in list(pages) + opp_fns if fn != "thanks.html")
    open(os.path.join(DIST, "sitemap.xml"), "w").write(f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>')
    open(os.path.join(DIST, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\nSitemap: {SITE_URL}/sitemap.xml\n")
    open(os.path.join(DIST, "404.html"), "w").write(page("404.html", "Page Not Found | Projexian", "Page not found.", """
<div class="wrap"><div class="phead" style="min-height:60vh"><div class="label">404</div><h1 class="display">This page <em>isn't here.</em></h1>
<div style="grid-column:4/12;margin-top:34px"><a class="link" href="index.html">Return home <span class="ar"></span></a></div></div></div>"""))
    print("built", len(pages), "pages")


if __name__ == "__main__":
    build()
