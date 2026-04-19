"""
Generates Elementor v3-compatible template JSON files for all 6 pages of
the Amerigroup International site.

Each page is built from native Elementor widgets (heading, text-editor,
image, button, html) arranged in proper sections + columns so every block
is individually editable inside Elementor.

Usage:
    python3 generate.py
Outputs six .json files in the current directory, ready to import into
WordPress via Elementor > Templates > Saved Templates > Import.
"""
import json, hashlib, os

def uid(*parts):
    h = hashlib.md5("".join(parts).encode()).hexdigest()
    return h[:7]

def widget(wtype, settings, seed):
    return {
        "id": uid(wtype, seed),
        "elType": "widget",
        "widgetType": wtype,
        "settings": settings,
        "elements": []
    }

def heading(text, seed, size="xl", align="left", color=None, tag="h2"):
    s = {"title": text, "size": size, "align": align, "header_size": tag}
    if color: s["title_color"] = color
    return widget("heading", s, seed + text[:20])

def text(html, seed):
    return widget("text-editor", {"editor": html}, seed + html[:20])

def image(url, seed, alt=""):
    return widget("image", {
        "image": {"url": url, "id": ""},
        "image_size": "full",
        "align": "center",
        "caption_source": "none"
    }, seed + url[-20:])

def button(label, link, seed, style="teal"):
    s = {
        "text": label,
        "link": {"url": link, "is_external": "", "nofollow": ""},
        "align": "left",
        "size": "md",
        "background_color": "#0ccfb0" if style == "teal" else "#ffffff",
        "button_text_color": "#0a1628",
        "typography_typography": "custom",
        "typography_font_weight": "700",
        "border_radius": {"unit": "px", "top": "8", "right": "8",
                          "bottom": "8", "left": "8", "isLinked": True}
    }
    return widget("button", s, seed + label)

def html_widget(code, seed):
    return widget("html", {"html": code}, seed + code[:30])

def column(elements, seed, width=100):
    return {
        "id": uid("col", seed),
        "elType": "column",
        "settings": {"_column_size": width, "_inline_size": None},
        "elements": elements,
        "isInner": False
    }

def section(columns, seed, bg=None, padding=None, classes=""):
    s = {}
    if bg:      s["background_background"] = "classic"; s["background_color"] = bg
    if padding: s["padding"] = {"unit": "px", "top": str(padding[0]),
                                 "right": str(padding[1]),
                                 "bottom": str(padding[2]),
                                 "left": str(padding[3]), "isLinked": False}
    if classes: s["css_classes"] = classes
    return {
        "id": uid("sec", seed),
        "elType": "section",
        "settings": s,
        "elements": columns,
        "isInner": False
    }

def template(title, content):
    return {
        "version": "0.4",
        "title": title,
        "type": "page",
        "content": content,
        "page_settings": []
    }

def save(name, data):
    with open(name, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"  ✓ {name}")

# ─────────── Shared elements ────────────────────────────────────────
NAV_HTML = """
<nav style="position:fixed;top:0;left:0;right:0;z-index:1000;display:flex;align-items:center;justify-content:space-between;padding:0 5%;height:70px;background:rgba(10,22,40,0.95);backdrop-filter:blur(12px);border-bottom:1px solid rgba(255,255,255,0.07)">
  <a href="/" style="display:flex;align-items:center;gap:10px;text-decoration:none;color:#fff">
    <svg viewBox="0 0 36 36" width="36" height="36" fill="none"><circle cx="18" cy="18" r="17" stroke="#0ccfb0" stroke-width="2"/><path d="M9 22 L18 10 L27 22" stroke="#0ccfb0" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/><line x1="9" y1="27" x2="27" y2="27" stroke="#0ccfb0" stroke-width="2" stroke-linecap="round"/></svg>
    <div><span style="font-size:1.1rem;font-weight:700">Amerigroup <b style="color:#0ccfb0">Int'l</b></span><small style="display:block;font-size:0.6rem;color:#0ccfb0;letter-spacing:0.12em;text-transform:uppercase">Clean Energy Solutions</small></div>
  </a>
  <ul style="display:flex;gap:28px;list-style:none;margin:0;padding:0">
    <li><a href="/" style="color:rgba(255,255,255,0.8);text-decoration:none;font-size:0.875rem;font-weight:500">Home</a></li>
    <li><a href="/about" style="color:rgba(255,255,255,0.8);text-decoration:none;font-size:0.875rem;font-weight:500">About Us</a></li>
    <li><a href="/technology" style="color:rgba(255,255,255,0.8);text-decoration:none;font-size:0.875rem;font-weight:500">Technology</a></li>
    <li><a href="/projects" style="color:rgba(255,255,255,0.8);text-decoration:none;font-size:0.875rem;font-weight:500">Projects</a></li>
    <li><a href="/team" style="color:rgba(255,255,255,0.8);text-decoration:none;font-size:0.875rem;font-weight:500">Our Team</a></li>
    <li><a href="/partners" style="color:rgba(255,255,255,0.8);text-decoration:none;font-size:0.875rem;font-weight:500">Partners</a></li>
    <li><a href="/#contact" style="background:#0ccfb0;color:#0a1628;padding:8px 20px;border-radius:6px;font-weight:700;text-decoration:none;font-size:0.875rem">Contact</a></li>
  </ul>
</nav>
"""

FOOTER_HTML = """
<footer style="background:#0a1628;border-top:1px solid rgba(255,255,255,0.07);padding:60px 5% 30px;color:rgba(255,255,255,0.5)">
  <div style="display:grid;grid-template-columns:2fr 1fr 1fr 1fr;gap:48px;margin-bottom:40px">
    <div><h5 style="color:#fff;font-size:0.9rem;font-weight:700;margin-bottom:18px">Amerigroup International</h5><p style="font-size:0.85rem;line-height:1.7;max-width:320px">Leading provider of zero-emission energy solutions — pioneering the transition to sustainable energy integration and advanced clean technology worldwide.</p></div>
    <div><h5 style="color:#fff;font-size:0.9rem;font-weight:700;margin-bottom:18px">Company</h5><a href="/about" style="color:rgba(255,255,255,0.5);font-size:0.85rem;display:block;margin-bottom:8px;text-decoration:none">About Us</a><a href="/team" style="color:rgba(255,255,255,0.5);font-size:0.85rem;display:block;margin-bottom:8px;text-decoration:none">Our Team</a><a href="/partners" style="color:rgba(255,255,255,0.5);font-size:0.85rem;display:block;margin-bottom:8px;text-decoration:none">Partners</a></div>
    <div><h5 style="color:#fff;font-size:0.9rem;font-weight:700;margin-bottom:18px">Solutions</h5><a href="/technology" style="color:rgba(255,255,255,0.5);font-size:0.85rem;display:block;margin-bottom:8px;text-decoration:none">Technology</a><a href="/projects" style="color:rgba(255,255,255,0.5);font-size:0.85rem;display:block;margin-bottom:8px;text-decoration:none">Projects</a></div>
    <div><h5 style="color:#fff;font-size:0.9rem;font-weight:700;margin-bottom:18px">Offices</h5><p style="font-size:0.85rem;line-height:1.7">Hong Kong (SAR)<br>Beijing, China<br>Vancouver, Canada</p></div>
  </div>
  <div style="display:flex;justify-content:space-between;padding-top:30px;border-top:1px solid rgba(255,255,255,0.07);flex-wrap:wrap;gap:16px">
    <div style="font-size:0.8rem;color:rgba(255,255,255,0.35)">© 2024 Amerigroup International. All rights reserved.</div>
    <div style="font-size:0.82rem;color:rgba(255,255,255,0.5)">Leading provider of zero-emission energy solutions.</div>
  </div>
</footer>
"""

def nav_section(page):   return section([column([html_widget(NAV_HTML, "nav"+page)], "ncol"+page)], "navs"+page, padding=(0,0,0,0))
def footer_section(page):return section([column([html_widget(FOOTER_HTML, "ft"+page)], "fcol"+page)], "fts"+page, padding=(0,0,0,0))

def page_hero(title_html, lead, breadcrumb, seed):
    html = f"""
<header style="padding:160px 5% 100px;background:linear-gradient(135deg,rgba(10,22,40,0.92) 0%,rgba(15,52,96,0.85) 60%,rgba(12,207,176,0.12) 100%),url('https://images.unsplash.com/photo-1466611653911-95081537e5b7?w=1800&auto=format&fit=crop&q=80') center/cover no-repeat;color:#fff">
  <div style="font-size:0.8rem;color:#0ccfb0;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:16px">{breadcrumb}</div>
  <h1 style="font-size:clamp(2rem,4.5vw,3.4rem);font-weight:800;line-height:1.15;letter-spacing:-0.02em;max-width:900px;margin-bottom:20px">{title_html}</h1>
  <p style="font-size:1.1rem;color:rgba(255,255,255,0.72);line-height:1.7;max-width:640px">{lead}</p>
</header>"""
    return section([column([html_widget(html, seed)], "hcol"+seed)], "hsec"+seed, padding=(0,0,0,0))

# ─────────── HOME ──────────────────────────────────────────────────
def build_home():
    hero = html_widget("""
<section style="min-height:100vh;display:flex;align-items:center;background:linear-gradient(135deg,rgba(10,22,40,0.92),rgba(15,52,96,0.85) 60%,rgba(12,207,176,0.12)),url('https://images.unsplash.com/photo-1466611653911-95081537e5b7?w=1800&auto=format&fit=crop&q=80') center/cover;padding:120px 5% 80px;color:#fff">
  <div style="max-width:820px">
    <div style="display:inline-flex;gap:8px;background:rgba(12,207,176,0.15);border:1px solid rgba(12,207,176,0.4);color:#0ccfb0;padding:6px 16px;border-radius:100px;font-size:0.78rem;font-weight:600;letter-spacing:0.08em;text-transform:uppercase;margin-bottom:28px">Net-Zero by 2050 Initiative</div>
    <h1 style="font-size:clamp(2rem,4.5vw,3.6rem);font-weight:800;line-height:1.15;margin-bottom:24px">Pioneering <span style="color:#0ccfb0">Sustainable Energy</span><br>Integration &amp; Advanced<br>Clean Technology Solutions</h1>
    <p style="font-size:clamp(1rem,1.6vw,1.2rem);color:rgba(255,255,255,0.72);line-height:1.7;max-width:620px;margin-bottom:44px">Innovative solutions for sustainable energy projects and infrastructure — leading the global transition toward carbon neutrality through science-driven innovation.</p>
    <div style="display:flex;gap:16px;flex-wrap:wrap">
      <a href="/technology" style="background:#0ccfb0;color:#0a1628;padding:14px 32px;border-radius:8px;font-weight:700;text-decoration:none">Explore Technology →</a>
      <a href="/#contact" style="border:1.5px solid rgba(255,255,255,0.35);color:#fff;padding:14px 32px;border-radius:8px;font-weight:600;text-decoration:none">Get In Touch</a>
    </div>
    <div style="display:flex;gap:48px;margin-top:64px;flex-wrap:wrap">
      <div><div style="font-size:2.4rem;font-weight:800;color:#0ccfb0">100+</div><div style="color:rgba(255,255,255,0.55);font-size:0.8rem">Years Experience</div></div>
      <div><div style="font-size:2.4rem;font-weight:800;color:#0ccfb0">30+</div><div style="color:rgba(255,255,255,0.55);font-size:0.8rem">Global Clients</div></div>
      <div><div style="font-size:2.4rem;font-weight:800;color:#0ccfb0">8</div><div style="color:rgba(255,255,255,0.55);font-size:0.8rem">Energy Domains</div></div>
      <div><div style="font-size:2.4rem;font-weight:800;color:#0ccfb0">3</div><div style="color:rgba(255,255,255,0.55);font-size:0.8rem">Global Offices</div></div>
    </div>
  </div>
</section>""", "herohome")

    who = section([
        column([
            heading("Who We Are", "whoh", size="small", color="#09a38c"),
            heading("Leading the Global Energy Transition with Scalable, Science-Driven Innovation", "whot", tag="h2"),
            text("<p>Amerigroup International stands at the forefront of the clean energy revolution, delivering unparalleled expertise and turnkey solutions in hydrogen production and dispensing, methanol fuel cell power generation and range extenders, and renewable energy generation with solar, wind turbines, and innovative water solar solutions.</p><p>We also specialize in liquefied natural gas (LNG) infrastructure — including onshore regasification terminals, offshore Floating Storage and Regasification Units (FSRU), and international LNG supply logistics — as well as power grid modernization and power plant integration with new energy technologies around the globe.</p>", "whop")
        ], "whoc1", 50),
        column([
            html_widget("""<div style="display:grid;grid-template-columns:1fr 1fr;gap:16px">
<div style="background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.1);border-radius:14px;padding:24px"><div style="font-size:1.8rem;margin-bottom:10px">⚡</div><h4 style="color:#fff;font-size:0.95rem;font-weight:700;margin-bottom:8px">Grid Modernization</h4><p style="color:rgba(255,255,255,0.6);font-size:0.85rem;line-height:1.6">Smart power grid integration with next-gen clean technologies across global markets.</p></div>
<div style="background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.1);border-radius:14px;padding:24px"><div style="font-size:1.8rem;margin-bottom:10px">💧</div><h4 style="color:#fff;font-size:0.95rem;font-weight:700;margin-bottom:8px">Hydrogen Systems</h4><p style="color:rgba(255,255,255,0.6);font-size:0.85rem;line-height:1.6">End-to-end hydrogen production, storage, and dispensing infrastructure.</p></div>
<div style="background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.1);border-radius:14px;padding:24px"><div style="font-size:1.8rem;margin-bottom:10px">☀️</div><h4 style="color:#fff;font-size:0.95rem;font-weight:700;margin-bottom:8px">Renewables</h4><p style="color:rgba(255,255,255,0.6);font-size:0.85rem;line-height:1.6">Solar, wind, and innovative water solar solutions for scalable clean generation.</p></div>
<div style="background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.1);border-radius:14px;padding:24px"><div style="font-size:1.8rem;margin-bottom:10px">🚢</div><h4 style="color:#fff;font-size:0.95rem;font-weight:700;margin-bottom:8px">LNG Infrastructure</h4><p style="color:rgba(255,255,255,0.6);font-size:0.85rem;line-height:1.6">Onshore terminals, FSRU units, and international LNG supply chain management.</p></div>
</div>""", "whocards")
        ], "whoc2", 50)
    ], "whosec", bg="#0a1628", padding=(100,80,100,80))

    climate = html_widget("""
<div style="background:linear-gradient(135deg,#0f3460,#1a4a8a);padding:80px 5%;text-align:center;color:#fff">
  <div style="max-width:860px;margin:0 auto">
    <div style="font-size:clamp(3rem,7vw,6rem);font-weight:900;color:#0ccfb0;margin-bottom:16px">70%+</div>
    <p style="font-size:clamp(1rem,2vw,1.35rem);color:rgba(255,255,255,0.85);line-height:1.7;margin-bottom:12px">of global warming emissions come from the energy sector</p>
    <p style="font-size:0.95rem;color:rgba(255,255,255,0.55)">Annually, nearly 40 billion tons of carbon dioxide are released into the atmosphere by our global energy systems.</p>
    <div style="display:inline-block;margin-top:20px;background:rgba(255,255,255,0.1);border-radius:8px;padding:12px 20px;font-size:0.85rem;color:rgba(255,255,255,0.65);max-width:600px">As the urgency of the climate crisis becomes clearer, we support the development of technology innovations, emissions regulations, and policy pathways designed to enable a net-zero emissions future by 2050.</div>
  </div>
</div>""", "climateband")

    solutions = html_widget("""
<section style="padding:100px 5%;background:#fff">
  <div style="text-align:center;margin-bottom:56px">
    <span style="display:inline-block;color:#09a38c;font-size:0.78rem;font-weight:700;letter-spacing:0.12em;text-transform:uppercase;margin-bottom:14px">What We Do</span>
    <h2 style="font-size:clamp(1.7rem,3vw,2.6rem);font-weight:800;color:#0a1628;margin-bottom:20px">Comprehensive Clean Energy Solutions</h2>
    <p style="font-size:1.05rem;color:#64748b;line-height:1.75;max-width:640px;margin:0 auto">Eight integrated domains designed to accelerate the global transition to sustainable, zero-emission energy systems.</p>
  </div>
  <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:24px">
""" + "".join(f'<div style="border:1px solid #dce4ef;border-radius:16px;padding:32px;background:#fff"><div style="font-size:2rem;margin-bottom:16px">{icon}</div><h3 style="font-size:1rem;font-weight:700;color:#0a1628;margin-bottom:10px">{t}</h3><p style="font-size:0.86rem;color:#64748b;line-height:1.65">{d}</p></div>' for icon, t, d in [
    ("🏗️","Power Grid Modernization &amp; Power Plant Integration in Mexico","Advanced grid infrastructure upgrades and integration of clean generation technologies across Mexico's energy network."),
    ("☀️","Renewable Energy Generation: Solar, Wind &amp; Water Solar","Scalable renewable generation combining photovoltaic, onshore/offshore wind, and novel water-based solar technologies."),
    ("⚗️","Hydrogen Production &amp; Dispensing Systems","End-to-end green and blue hydrogen production, compression, storage, and public/commercial dispensing infrastructure."),
    ("🔋","Methanol Fuel Cell Power &amp; Range Extenders","High-efficiency methanol fuel cell systems for stationary power and range-extending applications in commercial fleets."),
    ("🏭","LNG Onshore Regasification &amp; Infrastructure","Full-cycle onshore LNG regasification terminal design, procurement, construction, and operations management."),
    ("🚢","Offshore Floating Storage &amp; Regasification (FSRU)","Offshore FSRU deployment and operations enabling rapid LNG import capacity expansion without onshore construction."),
    ("🌐","Overseas LNG Supply Chain Management","Integrated international LNG sourcing, shipping logistics, scheduling, and supply chain optimization services."),
    ("🚗","E-Mobility Integration &amp; Commercial EVs","Fleet electrification strategy, EV infrastructure deployment, and commercial electric vehicle integration programs."),
]) + "</div></section>", "solgrid")

    contact = html_widget("""
<section id="contact" style="padding:100px 5%;background:linear-gradient(135deg,#0a1628,#0f3460);color:#fff">
  <div style="max-width:640px;margin:0 auto;text-align:center">
    <span style="display:inline-block;color:#0ccfb0;font-size:0.78rem;font-weight:700;letter-spacing:0.12em;text-transform:uppercase;margin-bottom:14px">Get In Touch</span>
    <h2 style="font-size:clamp(1.7rem,3vw,2.6rem);font-weight:800;color:#fff;margin-bottom:20px">Join Us in Building the Energy Systems of Tomorrow</h2>
    <p style="font-size:1.05rem;color:rgba(255,255,255,0.65);line-height:1.75;margin-bottom:48px">Contact us for energy solutions, partnerships, and project inquiries. Our team will respond within 24 hours.</p>
    <form style="display:flex;flex-direction:column;gap:16px;text-align:left">
      <input type="text" placeholder="Your name" style="background:rgba(255,255,255,0.08);border:1px solid rgba(255,255,255,0.18);border-radius:8px;padding:12px 16px;color:#fff;font-size:0.95rem" />
      <input type="email" placeholder="you@company.com" style="background:rgba(255,255,255,0.08);border:1px solid rgba(255,255,255,0.18);border-radius:8px;padding:12px 16px;color:#fff;font-size:0.95rem" />
      <textarea placeholder="Describe your project or inquiry…" style="background:rgba(255,255,255,0.08);border:1px solid rgba(255,255,255,0.18);border-radius:8px;padding:12px 16px;color:#fff;font-size:0.95rem;min-height:120px"></textarea>
      <button type="submit" style="background:#0ccfb0;color:#0a1628;border:none;padding:15px 40px;border-radius:8px;font-weight:700;font-size:1rem;cursor:pointer;align-self:center">Submit Enquiry →</button>
    </form>
  </div>
</section>""", "contacthome")

    content = [
        nav_section("home"),
        section([column([hero], "hc")], "hs", padding=(0,0,0,0)),
        who,
        section([column([climate], "cc")], "cs", padding=(0,0,0,0)),
        section([column([solutions], "solc")], "sols", padding=(0,0,0,0)),
        section([column([contact], "cnc")], "cns", padding=(0,0,0,0)),
        footer_section("home"),
    ]
    return template("Home — Amerigroup International", content)

# ─────────── ABOUT ─────────────────────────────────────────────────
def build_about():
    hero = page_hero("Leading the Way Through <span style='color:#0ccfb0'>Innovative Policies</span><br>and Sustainable Practices",
                    "From a regional LNG transporter to a global clean energy leader — discover the story, vision, and values behind Amerigroup International.",
                    "Home → About Us", "ab")

    mission = section([
        column([image("https://images.unsplash.com/photo-1497366216548-37526070297c?w=900&auto=format&fit=crop&q=80", "amis")], "abc1", 50),
        column([
            heading("Our Mission", "abmh", size="small", color="#09a38c"),
            heading("Dedicated to Zero-Emission Energy Solutions", "abm", tag="h2"),
            text("<p><strong>At Amerigroup, we are dedicated to leading the transition to clean energy by providing zero-emission solutions for transportation and energy production.</strong></p><p>Our organization aims to reduce greenhouse gas emissions, improve energy supply quality, and support sustainable regional development — serving governments, industries, and communities across three continents.</p>", "abmp")
        ], "abc2", 50)
    ], "absec", padding=(100,80,100,80))

    stats_html = html_widget("""
<section style="padding:100px 5%;background:#0a1628;color:#fff">
  <div style="text-align:center;margin-bottom:56px">
    <span style="color:#0ccfb0;font-size:0.78rem;font-weight:700;letter-spacing:0.12em;text-transform:uppercase">By the Numbers</span>
    <h2 style="font-size:clamp(1.7rem,3vw,2.6rem);font-weight:800;margin:14px 0 20px">A Legacy of Impact</h2>
  </div>
  <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:24px;text-align:center">
    <div><div style="font-size:3.5rem;font-weight:800;color:#0ccfb0">100+</div><div style="color:rgba(255,255,255,0.55);font-size:0.9rem">Years Combined Experience</div></div>
    <div><div style="font-size:3.5rem;font-weight:800;color:#0ccfb0">30+</div><div style="color:rgba(255,255,255,0.55);font-size:0.9rem">Global Clients</div></div>
    <div><div style="font-size:3.5rem;font-weight:800;color:#0ccfb0">3</div><div style="color:rgba(255,255,255,0.55);font-size:0.9rem">Continents</div></div>
    <div><div style="font-size:3.5rem;font-weight:800;color:#0ccfb0">8</div><div style="color:rgba(255,255,255,0.55);font-size:0.9rem">Technology Domains</div></div>
  </div>
</section>""", "abstats")

    history = section([
        column([
            heading("Our History", "abhh", size="small", color="#09a38c"),
            heading("From LNG Transport to Global Clean Energy", "abht", tag="h2"),
            text("<p>Amerigroup evolved from a regional LNG transporter into a global clean energy leader. Over decades, the company expanded its expertise across hydrogen production, power grid modernization, and advanced clean energy infrastructure.</p><p>Today, we operate integrated teams across Hong Kong, Beijing, and Vancouver — connecting North American innovation with Asian manufacturing capacity and Latin American energy markets.</p>", "abhp")
        ], "abhc1", 50),
        column([image("https://images.unsplash.com/photo-1518709268805-4e9042af2176?w=900&auto=format&fit=crop&q=80", "abhi")], "abhc2", 50)
    ], "abhsec", padding=(100,80,100,80))

    values_html = html_widget("""
<section style="padding:100px 5%;background:#f0f4f8">
  <div style="text-align:center;margin-bottom:56px">
    <span style="color:#09a38c;font-size:0.78rem;font-weight:700;letter-spacing:0.12em;text-transform:uppercase">Core Values</span>
    <h2 style="font-size:clamp(1.7rem,3vw,2.6rem);font-weight:800;color:#0a1628;margin:14px 0 20px">What Drives Us Forward</h2>
    <p style="color:#64748b;max-width:640px;margin:0 auto;font-size:1.05rem">Four guiding principles define how we build, partner, and deliver.</p>
  </div>
  <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:20px">
""" + "".join(f'<div style="background:#fff;border:1px solid #dce4ef;border-radius:16px;padding:32px"><div style="font-size:2rem;margin-bottom:16px">{i}</div><h3 style="font-size:1rem;font-weight:700;color:#0a1628;margin-bottom:10px">{t}</h3><p style="font-size:0.86rem;color:#64748b;line-height:1.65">{d}</p></div>' for i,t,d in [
    ("💡","Innovation","Continuously pursuing new technologies and solutions to stay ahead of the energy transition curve."),
    ("🌱","Sustainability","Committed to reducing environmental impact and promoting clean energy across every project we undertake."),
    ("🌍","Regional Development","Enhancing local economies through sustainable energy projects and resilient infrastructure."),
    ("⭐","Excellence","Striving for the highest standards in every operation, from engineering to partnerships."),
]) + "</div></section>", "abvalues")

    offices_html = html_widget("""
<section style="padding:100px 5%;background:#0a1628;color:#fff">
  <div style="text-align:center;margin-bottom:56px">
    <span style="color:#0ccfb0;font-size:0.78rem;font-weight:700;letter-spacing:0.12em;text-transform:uppercase">Our Offices</span>
    <h2 style="font-size:clamp(1.7rem,3vw,2.6rem);font-weight:800;margin:14px 0 20px">Global Presence, Local Expertise</h2>
  </div>
  <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:24px">
    <div style="background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.1);border-radius:14px;padding:32px"><div style="font-size:2rem;margin-bottom:12px">🇭🇰</div><h4 style="color:#fff;font-size:1rem;font-weight:700;margin-bottom:8px">Hong Kong (SAR)</h4><p style="color:rgba(255,255,255,0.6);font-size:0.88rem;line-height:1.7">Unit 1201, Beverley Commercial Centre<br>87–105 Chatham Rd. S.<br>Tsim Sha Tsui, Kowloon</p></div>
    <div style="background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.1);border-radius:14px;padding:32px"><div style="font-size:2rem;margin-bottom:12px">🇨🇳</div><h4 style="color:#fff;font-size:1rem;font-weight:700;margin-bottom:8px">Beijing, China</h4><p style="color:rgba(255,255,255,0.6);font-size:0.88rem;line-height:1.7">Building A1, Zone B<br>Daxing International Hydrogen Energy Demonstration Zone<br>Daxing District</p></div>
    <div style="background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.1);border-radius:14px;padding:32px"><div style="font-size:2rem;margin-bottom:12px">🇨🇦</div><h4 style="color:#fff;font-size:1rem;font-weight:700;margin-bottom:8px">Vancouver, Canada</h4><p style="color:rgba(255,255,255,0.6);font-size:0.88rem;line-height:1.7">170 – 422 Richard St<br>Vancouver, BC V6B 2Z4</p></div>
  </div>
</section>""", "aboff")

    content = [
        nav_section("about"),
        hero,
        mission,
        section([column([stats_html], "asc")], "ass", padding=(0,0,0,0)),
        history,
        section([column([values_html], "avc")], "avs", padding=(0,0,0,0)),
        section([column([offices_html], "aoc")], "aos", padding=(0,0,0,0)),
        footer_section("about"),
    ]
    return template("About Us — Amerigroup International", content)

# ─────────── TECHNOLOGY ────────────────────────────────────────────
TECH_ROWS = [
    ("Renewables","Solar, Wind Turbines &amp; Water Solar Solutions",
     "<p>Amerigroup integrates cutting-edge solar photovoltaic systems, utility-scale wind turbines, and innovative water solar solutions such as floating solar arrays to maximize clean energy production.</p><p>These renewables are designed to complement our portfolio — providing scalable, flexible power generation that supports grid stability and complements hydrogen and methanol fuel cell systems for a balanced, sustainable energy mix.</p>",
     "https://images.unsplash.com/photo-1509391366360-2e959784a276?w=900&auto=format&fit=crop&q=80"),
    ("Hydrogen","Hydrogen Production &amp; Dispensing Systems",
     "<p>Harnessing cutting-edge electrolysis and blue hydrogen technologies with carbon capture, Amerigroup designs and deploys modular, scalable hydrogen production facilities.</p><p>Our hydrogen refueling stations are engineered for industrial, transportation, and power generation applications — empowering the shift toward a zero-carbon hydrogen economy.</p>",
     "https://images.unsplash.com/photo-1581092918484-8313ec0d4d0f?w=900&auto=format&fit=crop&q=80"),
    ("Fuel Cells","Methanol Fuel Cell Power &amp; Range Extenders",
     "<p>We deliver industry-leading methanol fuel cell generators and range extender systems, providing clean, reliable power for off-grid locations, emergency backup, and electric mobility.</p><p>Our innovative methanol solutions combine efficiency, portability, and environmental performance.</p>",
     "https://images.unsplash.com/photo-1473341304170-971dccb5ac1e?w=900&auto=format&fit=crop&q=80"),
    ("Grid Modernization","Power Grid Modernization &amp; Power Plant Integration in Mexico",
     "<p>With extensive experience in Mexico's energy sector, Amerigroup spearheads power grid modernization projects that incorporate advanced clean energy technologies.</p><p>Our services include integration of hydrogen and methanol fuel cells, renewables, and energy storage solutions into existing and new power plants.</p>",
     "https://images.unsplash.com/photo-1473341304170-971dccb5ac1e?w=900&auto=format&fit=crop&q=80"),
    ("E-Mobility","E-Mobility Integration &amp; Commercial Electric Vehicles",
     "<p>Amerigroup champions the electrification of transport through comprehensive e-mobility solutions — advanced EV fleets, commercial electric trucks, and hydrogen fuel cell vehicles.</p><p>Class 5 and 8 diesel-to-electric truck conversions with travel range up to 1,300 miles. Notable clients: Staples, UPS, FedEx, Kenworth.</p>",
     "https://images.unsplash.com/photo-1593941707882-a5bac6861d75?w=900&auto=format&fit=crop&q=80"),
    ("Innovation","Advanced Linear Generator Technology",
     "<p>Converts mechanical energy directly into electrical power with minimal moving parts. By employing a linear motion mechanism rather than traditional rotating components, this generator offers enhanced efficiency, longer operational lifespans, and greater reliability.</p>",
     "https://images.unsplash.com/photo-1581092160607-ee22621dd758?w=900&auto=format&fit=crop&q=80"),
    ("Innovation","Hydrogen Injection Reactor",
     "<p>A cutting-edge system designed to enhance fuel efficiency and reduce emissions in transport units by using only water as the source for hydrogen production. The reactor utilizes electrolysis to generate hydrogen on-demand, which is directly injected into the engine's combustion chamber.</p>",
     "https://images.unsplash.com/photo-1507668077129-56e32842fceb?w=900&auto=format&fit=crop&q=80"),
    ("LNG Onshore","LNG Onshore Regasification &amp; Infrastructure",
     "<p>Amerigroup operates state-of-the-art onshore LNG regasification terminals designed for optimal throughput, safety, and integration with downstream gas networks.</p><p>DOE approval: AmerigroupLNG authorized to export approximately 4.6 billion cubic feet (Bcf) of LNG from the United States.</p>",
     "https://images.unsplash.com/photo-1542331608-b7ff9666c40f?w=900&auto=format&fit=crop&q=80"),
    ("LNG Offshore","Offshore Floating Storage &amp; Regasification Units (FSRU)",
     "<p>Our advanced offshore FSRU solutions offer agile, cost-effective alternatives to traditional land-based terminals. Strategically deployed in ports and coastal hubs worldwide with minimal environmental footprint and rapid commissioning timelines.</p>",
     "https://images.unsplash.com/photo-1605281317010-fe5ffe798166?w=900&auto=format&fit=crop&q=80"),
    ("LNG Supply Chain","Overseas LNG Supply Chain Management",
     "<p>Amerigroup ensures end-to-end LNG supply chain excellence — from international procurement, marine transportation, and cargo handling to distribution and delivery. Global reach and strategic partnerships guarantee dependable LNG sourcing tailored to market needs.</p>",
     "https://images.unsplash.com/photo-1494412651409-8963ce7935a7?w=900&auto=format&fit=crop&q=80"),
]

def build_technology():
    hero = page_hero("Advanced <span style='color:#0ccfb0'>Clean Technology</span> Solutions",
                    "Enhancing fuel efficiency, reducing emissions, and pioneering sustainable energy generation across ten integrated technology domains.",
                    "Home → Technology", "tech")
    content = [nav_section("tech"), hero]
    for i, (tag, t, d, img) in enumerate(TECH_ROWS):
        cols = [
            column([heading(tag, f"tr{i}l", size="small", color="#09a38c"),
                    heading(t, f"tr{i}t", tag="h2"),
                    text(d, f"tr{i}p")], f"trc1{i}", 50),
            column([image(img, f"tr{i}img")], f"trc2{i}", 50)
        ]
        if i % 2 == 1: cols = list(reversed(cols))
        bg = "#ffffff" if i % 2 == 0 else "#f0f4f8"
        content.append(section(cols, f"trs{i}", bg=bg, padding=(80,80,80,80)))
    content.append(footer_section("tech"))
    return template("Technology — Amerigroup International", content)

# ─────────── PROJECTS ──────────────────────────────────────────────
PROJECTS = [
    ("Solar","Sonora, Mexico","Utility-Scale Solar Power Plant","Developing and managing large-scale solar facilities that convert sunlight into electricity, delivering clean power to Mexico's national grid.","Capacity: 250 MW","Status: Operational","https://images.unsplash.com/photo-1509391366360-2e959784a276?w=900&auto=format&fit=crop&q=80"),
    ("Wind","Oaxaca, Mexico","Onshore Wind Farm Development","Establishing and operating wind farms that capture wind energy and convert it into electrical power for regional industrial users.","Capacity: 180 MW","Status: Commissioning","https://images.unsplash.com/photo-1466611653911-95081537e5b7?w=900&auto=format&fit=crop&q=80"),
    ("Hydrogen","Daxing, Beijing","Hydrogen Electrolysis &amp; Production Hub","Leading in zero-emission hydrogen generation using renewable electricity to split water into hydrogen and oxygen.","Output: 10,000 kg/day","Status: Operational","https://images.unsplash.com/photo-1581092918484-8313ec0d4d0f?w=900&auto=format&fit=crop&q=80"),
    ("Ammonia","Vancouver, Canada","Green Ammonia Production Facility","Utilizing hydrogen produced from renewable sources to create ammonia — a key component for energy storage and agricultural applications.","Output: 50,000 tpa","Status: In Development","https://images.unsplash.com/photo-1532601224476-15c79f2f7a51?w=900&auto=format&fit=crop&q=80"),
    ("Grid","Nationwide, Mexico","CFE Power Grid Modernization","Enhancing Mexico's national power grid with innovative engineering — integrating fuel cells, renewables, and energy storage.","Client: CFE","Status: Multi-Phase","https://images.unsplash.com/photo-1473341304170-971dccb5ac1e?w=900&auto=format&fit=crop&q=80"),
    ("EV","North America","Class 5 &amp; 8 Diesel-to-Electric Truck Conversion","Converting commercial diesel trucks to fully electric with travel range up to 1,300 miles. Serving premier logistics and retail fleets.","Clients: Staples, UPS, FedEx, Kenworth","Range: Up to 1,300 mi","https://images.unsplash.com/photo-1593941707882-a5bac6861d75?w=900&auto=format&fit=crop&q=80"),
    ("LNG Export","United States","AmerigroupLNG — US Export Authorization","DOE-approved license for AmerigroupLNG to export approximately 4.6 billion cubic feet (Bcf) of liquefied natural gas from the United States.","Volume: 4.6 Bcf","Authority: US DOE","https://images.unsplash.com/photo-1605281317010-fe5ffe798166?w=900&auto=format&fit=crop&q=80"),
    ("FSRU","Pacific Coast, Mexico","Offshore FSRU Deployment","Offshore Floating Storage and Regasification Unit providing rapid LNG import capacity with minimal environmental footprint.","Capacity: 170,000 m³","Status: Operational","https://images.unsplash.com/photo-1542331608-b7ff9666c40f?w=900&auto=format&fit=crop&q=80"),
    ("Logistics","Trans-Pacific","Overseas LNG Supply Chain &amp; Bunkering","End-to-end LNG sourcing and logistics — transportation, onshore regasification, FSRU operations, marine bunkering, and small-scale distribution.","Scope: Global","Status: Ongoing","https://images.unsplash.com/photo-1494412651409-8963ce7935a7?w=900&auto=format&fit=crop&q=80"),
]

def build_projects():
    hero = page_hero("Sustainability Projects <span style='color:#0ccfb0'>Delivered Worldwide</span>",
                    "Innovative solutions for zero-emission energy, efficient infrastructure, advanced water treatment, hydrogen and ammonia production, and power grid enhancements for environmental protection.",
                    "Home → Projects", "proj")

    cards_html = '<section style="padding:100px 5%;background:#fff"><div style="text-align:center;margin-bottom:48px"><span style="color:#09a38c;font-size:0.78rem;font-weight:700;letter-spacing:0.12em;text-transform:uppercase">Portfolio</span><h2 style="font-size:clamp(1.7rem,3vw,2.6rem);font-weight:800;color:#0a1628;margin:14px 0">Featured Projects</h2></div><div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(340px,1fr));gap:28px">'
    for tag, loc, t, d, m1, m2, img in PROJECTS:
        cards_html += f'''<article style="border-radius:18px;overflow:hidden;background:#fff;border:1px solid #dce4ef">
<div style="aspect-ratio:16/10;overflow:hidden;position:relative"><img src="{img}" style="width:100%;height:100%;object-fit:cover"/><div style="position:absolute;top:16px;left:16px;background:#0ccfb0;color:#0a1628;padding:6px 14px;border-radius:100px;font-size:0.72rem;font-weight:700;letter-spacing:0.05em;text-transform:uppercase">{tag}</div></div>
<div style="padding:28px"><div style="font-size:0.78rem;font-weight:600;color:#09a38c;letter-spacing:0.08em;text-transform:uppercase;margin-bottom:8px">{loc}</div><div style="font-size:1.15rem;font-weight:800;color:#0a1628;margin-bottom:12px;line-height:1.35">{t}</div><div style="font-size:0.88rem;color:#64748b;line-height:1.65;margin-bottom:18px">{d}</div><div style="display:flex;gap:20px;padding-top:18px;border-top:1px solid #dce4ef;font-size:0.78rem;color:#64748b"><span>{m1}</span><span>{m2}</span></div></div></article>'''
    cards_html += '</div></section>'

    content = [
        nav_section("proj"), hero,
        section([column([html_widget(cards_html, "pcards")], "pcc")], "pcs", padding=(0,0,0,0)),
        footer_section("proj"),
    ]
    return template("Projects — Amerigroup International", content)

# ─────────── TEAM ──────────────────────────────────────────────────
TEAM = [
    ("Mr. Gerardo Payán Ramos","President, Amerigroup International · Founder, AmerigroupLNG &amp; AmeriGas Propane S.A. de C.V.","Over 15 years in the energy industry. Former consultant for Coca-Cola bottling companies across Latin America, specializing in electromechanical systems and quality control. Expert in government relations and strategic partnerships between Mexico and the USA. Authority in LNG, hydrogen, solar, wind, and EV conversion. Holds patents for an emergency alert system and a 911 location-sharing app.","https://images.unsplash.com/photo-1560250097-0b93528c311a?w=700&auto=format&fit=crop&q=80"),
    ("Mr. Ken Wong","Corporate Vice President &amp; Co-Founder, Amerigroup International","Canadian-Chinese entrepreneur directing global strategy and operations. Background in commodity trading and mining across Canada, USA, and Mexico. First Canadian-Chinese exporter of iron ore from Mexico to China (2012). Active in mergers, capital investment, new energy, real estate, agriculture, supply chain, and industrial park development. Belt and Road projects since 2016. Educated in Computer Engineering and International Trade Business.","https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=700&auto=format&fit=crop&q=80"),
    ("Mr. James Wang","CEO (China), Amerigroup International","Over 15 years at Fortune 500 companies and leading Chinese corporations. Expertise in government relations and state-owned enterprise partnerships. Oversaw transactions exceeding $10 billion. Key role in Belt and Road projects across African countries. Graduate in economics and management from Moscow State University.","https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=700&auto=format&fit=crop&q=80"),
    ("Mr. Roberto Compeán Woodworth","CFO (Mexico), Amerigroup International · CFO &amp; Co-founder, AmerigroupLNG","Strong background in private and public sectors. Former Chief Sales Officer at Mexico's National Lottery. Previous CFO for Bestel and Cablevision Monterrey (Televisa subsidiaries). BBVA Bank experience with advanced training in Madrid. Bachelor's Degree in Business Administration from ITAM University, Mexico.","https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?w=700&auto=format&fit=crop&q=80"),
    ("Mr. Peter Pang","CFO (CGA/CFA) Global, Amerigroup International","Over 30 years of industry experience. Former partner at KPMG Vancouver. Chartered Professional Accountant in Canada. Expertise in auditing, financial management, and mergers &amp; acquisitions. Instrumental in major corporate mergers and complex financial restructuring.","https://images.unsplash.com/photo-1568602471122-7832951cc4c5?w=700&auto=format&fit=crop&q=80"),
    ("Mr. Victor Manuel Villanueva Rivera","Managing Director, Amerigroup International","Over 40 years in the automotive industry. Former Managing Director at Jetour Motors and FIAT Mexico. Previous Sales Director at Hertz-AVASA. Former CEO &amp; Managing Director of Mitsubishi Motors Mexico. Master's in Quality Engineering; Bachelor's in Industrial Engineering.","https://images.unsplash.com/photo-1542909168-82c3e7fdca5c?w=700&auto=format&fit=crop&q=80"),
    ("Ms. Vanessa Muñoz","Business Development Director","Successfully owned and operated businesses in Mexico and the USA with top client satisfaction and awards. Former Real Estate Commercial and Leasing Manager for Liverpool. Previously at Alsea facilitating new business development. Bachelor's Degree in International Relations from Tecnológico de Monterrey, Mexico.","https://images.unsplash.com/photo-1580489944761-15a19d654956?w=700&auto=format&fit=crop&q=80"),
    ("Ms. Liviere Galván","Commercial Director","Transitioned from Sales Manager to Commercial Director at Amerigroup. Drives sales strategy, spearheads new business development, and expands the international client base. Former Director of Sales and Marketing at Dronamex (5+ years). Master of Science and Bachelor's degree in Marketing.","https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=700&auto=format&fit=crop&q=80"),
]

def build_team():
    hero = page_hero("Our Team Thrives on <span style='color:#0ccfb0'>Individuality &amp; Innovation</span>",
                    "Firsthand experience from collaborations with industry-leading clients and premier business partners.",
                    "Home → Our Team", "team")
    cards_html = '<section style="padding:100px 5%;background:#fff"><div style="text-align:center;margin-bottom:56px"><span style="color:#09a38c;font-size:0.78rem;font-weight:700;letter-spacing:0.12em;text-transform:uppercase">Leadership</span><h2 style="font-size:clamp(1.7rem,3vw,2.6rem);font-weight:800;color:#0a1628;margin:14px 0">Executives &amp; Directors</h2></div><div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:32px">'
    for n, r, b, img in TEAM:
        cards_html += f'''<div style="background:#fff;border-radius:20px;overflow:hidden;border:1px solid #dce4ef">
<div style="aspect-ratio:1/1.1;overflow:hidden;background:#f0f4f8"><img src="{img}" style="width:100%;height:100%;object-fit:cover"/></div>
<div style="padding:24px 28px 28px"><div style="font-size:1.15rem;font-weight:800;color:#0a1628;margin-bottom:4px">{n}</div><div style="font-size:0.8rem;font-weight:600;color:#09a38c;letter-spacing:0.04em;margin-bottom:14px;line-height:1.4">{r}</div><p style="font-size:0.82rem;color:#64748b;line-height:1.65">{b}</p></div></div>'''
    cards_html += '</div></section>'
    content = [
        nav_section("team"), hero,
        section([column([html_widget(cards_html, "tcards")], "tcc")], "tcs", padding=(0,0,0,0)),
        footer_section("team"),
    ]
    return template("Our Team — Amerigroup International", content)

# ─────────── PARTNERS ──────────────────────────────────────────────
PARTNER_NAMES = ["CFE","Bayotech","Mainspring","Power China","CPECC","Hybot","Hypower","HBA","Amerigas","Nikola","Pan America","Sauber Water","CEEC GEDI","Tian Tang","AG Intal","Conacen","H2B2","Technical America","CSCEC","Vastgold","Sangfor","GRB","A-SSA","Mexmot","Evenflo","Cryotainer","Big River Energy","SUMEC","SUMEC International Tech","Jishang Fortune","AY-C"]

def build_partners():
    hero = page_hero("Our <span style='color:#0ccfb0'>Collaboration</span> Network",
                    "Our team proudly reflects on its rich history of professional experience. The logos below represent the respected organizations where our team members have contributed expertise.",
                    "Home → Our Partners", "part")
    grid_html = '<section style="padding:100px 5%;background:#fff"><div style="text-align:center;margin-bottom:48px"><span style="color:#09a38c;font-size:0.78rem;font-weight:700;letter-spacing:0.12em;text-transform:uppercase">Professional History</span><h2 style="font-size:clamp(1.7rem,3vw,2.6rem);font-weight:800;color:#0a1628;margin:14px 0">Trusted Relationships Across Industries</h2><p style="color:#64748b;max-width:640px;margin:0 auto;font-size:1.05rem">These logos are the registered trademarks of their respective companies and are displayed solely to showcase our team\'s collective background.</p></div><div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:18px">'
    for n in PARTNER_NAMES:
        grid_html += f'<div style="aspect-ratio:3/2;background:#fff;border:1px solid #dce4ef;border-radius:12px;display:flex;align-items:center;justify-content:center;padding:20px;text-align:center;font-weight:700;color:#0f3460;font-size:1rem">{n}</div>'
    grid_html += '</div></section>'
    content = [
        nav_section("part"), hero,
        section([column([html_widget(grid_html, "pgrid")], "pgc")], "pgs", padding=(0,0,0,0)),
        footer_section("part"),
    ]
    return template("Partners — Amerigroup International", content)

# ─────────── GENERATE ──────────────────────────────────────────────
if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    print("Generating Elementor template JSON files...")
    save("01-home.json",       build_home())
    save("02-about.json",      build_about())
    save("03-technology.json", build_technology())
    save("04-projects.json",   build_projects())
    save("05-team.json",       build_team())
    save("06-partners.json",   build_partners())
    print("\nDone. Import these .json files into WordPress via:")
    print("  Elementor → Templates → Saved Templates → Import Templates")
