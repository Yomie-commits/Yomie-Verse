#!/usr/bin/env python3
"""
Naomi Mwangi (parent brand) static site generator.

You don't need to run this to publish — the .html files are already built.
Run it only after changing shared parts (header, footer, SEO, page copy in this file):

    python3 build.py

Contact email, form destination, booking link and analytics live in
assets/js/config.js and need no rebuild (email links are filled in from there).
"""
import json, os, re, datetime

# ------------------------------------------------------------------ SETTINGS
SITE_URL = "https://yomie-commits.github.io/Yomie-Verse"   # no trailing slash
SOCIALFLOW_URL = "https://yomie-commits.github.io/SocialFlowAI/"
EXECUTIVEFLOW_URL = "https://yomie-commits.github.io/ExecutiveFlowAI/"
LEADFLOW_URL = "https://yomie-commits.github.io/LeadFlowAI/"
WHATSAPP = "254792002230"
WHATSAPP_DISPLAY = "+254 792 002 230"
LINKEDIN = "https://www.linkedin.com/in/naomi-njeri-m/"
ASSET_VERSION = "4"
OUT = os.path.dirname(os.path.abspath(__file__))
# ---------------------------------------------------------------------------

ICONS = {
  "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
  "check": '<path d="M5 12.5l4.5 4.5L19 7.5"/>',
  "mail": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/>',
  "bot": '<rect x="4" y="8" width="16" height="12" rx="3"/><path d="M12 8V4M8 4h8"/><circle cx="9" cy="14" r="1.2"/><circle cx="15" cy="14" r="1.2"/>',
  "users": '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87M16 3.13a4 4 0 0 1 0 7.75"/>',
  "cog": '<circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.7 1.7 0 0 0 .3 1.8l.1.1a2 2 0 1 1-2.8 2.8l-.1-.1a1.7 1.7 0 0 0-1.8-.3 1.7 1.7 0 0 0-1 1.5V21a2 2 0 1 1-4 0v-.1a1.7 1.7 0 0 0-1.1-1.5 1.7 1.7 0 0 0-1.8.3l-.1.1a2 2 0 1 1-2.8-2.8l.1-.1a1.7 1.7 0 0 0 .3-1.8 1.7 1.7 0 0 0-1.5-1H3a2 2 0 1 1 0-4h.1a1.7 1.7 0 0 0 1.5-1.1 1.7 1.7 0 0 0-.3-1.8l-.1-.1a2 2 0 1 1 2.8-2.8l.1.1a1.7 1.7 0 0 0 1.8.3H9a1.7 1.7 0 0 0 1-1.5V3a2 2 0 1 1 4 0v.1a1.7 1.7 0 0 0 1 1.5 1.7 1.7 0 0 0 1.8-.3l.1-.1a2 2 0 1 1 2.8 2.8l-.1.1a1.7 1.7 0 0 0-.3 1.8V9a1.7 1.7 0 0 0 1.5 1H21a2 2 0 1 1 0 4h-.1a1.7 1.7 0 0 0-1.5 1z"/>',
  "cal": '<rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/>',
  "puzzle": '<path d="M19.4 13.5a2.5 2.5 0 1 0 0-3H18V7a1 1 0 0 0-1-1h-3.5V4.6a2.5 2.5 0 1 0-3 0V6H7a1 1 0 0 0-1 1v3.5h1.4a2.5 2.5 0 1 1 0 3H6V17a1 1 0 0 0 1 1h3.5v-1.4a2.5 2.5 0 1 1 3 0V18H17a1 1 0 0 0 1-1v-3.5z"/>',
  "sheet": '<rect x="3" y="3" width="18" height="18" rx="2"/><path d="M3 9h18M3 15h18M9 3v18"/>',
  "zap": '<path d="M13 2L3 14h9l-1 8 10-12h-9z"/>',
  "brain": '<path d="M9.5 2A2.5 2.5 0 0 0 7 4.5v.3A3 3 0 0 0 4.5 8a3 3 0 0 0-.5 5.4A3 3 0 0 0 7 18a2.5 2.5 0 0 0 5 .5V4.5A2.5 2.5 0 0 0 9.5 2zM14.5 2A2.5 2.5 0 0 1 17 4.5v.3A3 3 0 0 1 19.5 8a3 3 0 0 1 .5 5.4A3 3 0 0 1 17 18a2.5 2.5 0 0 1-5 .5"/>',
  "hand": '<path d="M18 11V6a2 2 0 0 0-4 0v5M14 10V4a2 2 0 0 0-4 0v6M10 10.5V6a2 2 0 0 0-4 0v8"/><path d="M18 8a2 2 0 1 1 4 0v6a8 8 0 0 1-8 8h-2c-2.8 0-4.5-.9-6-2.4l-3.6-3.6a2 2 0 0 1 2.8-2.8L7 15"/>',
  "clock": '<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>',
  "shield": '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="M9 12l2 2 4-4"/>',
  "eye": '<path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8S1 12 1 12z"/><circle cx="12" cy="12" r="3"/>',
  "trend": '<path d="M23 6l-9.5 9.5-5-5L1 18"/><path d="M17 6h6v6"/>',
  "repeat": '<path d="M17 1l4 4-4 4"/><path d="M3 11V9a4 4 0 0 1 4-4h14M7 23l-4-4 4-4"/><path d="M21 13v2a4 4 0 0 1-4 4H3"/>',
  "inbox": '<path d="M22 12h-6l-2 3h-4l-2-3H2"/><path d="M5.45 5.11L2 12v6a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-6l-3.45-6.89A2 2 0 0 0 16.76 4H7.24a2 2 0 0 0-1.79 1.11z"/>',
  "list": '<path d="M8 6h13M8 12h13M8 18h13M3 6h.01M3 12h.01M3 18h.01"/>',
  "flag": '<path d="M4 22V4m0 0h13l-2 4 2 4H4"/>',
  "pen": '<path d="M12 20h9"/><path d="M16.5 3.5a2.1 2.1 0 0 1 3 3L7 19l-4 1 1-4z"/>',
  "bell": '<path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.7 21a2 2 0 0 1-3.4 0"/>',
  "sun": '<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/>',
  "alert": '<circle cx="12" cy="12" r="10"/><path d="M12 8v4M12 16h.01"/>',
  "spark": '<path d="M12 3l1.9 5.8L20 10l-6.1 1.2L12 17l-1.9-5.8L4 10l6.1-1.2z"/><path d="M19 17l.7 2.3L22 20l-2.3.7L19 23l-.7-2.3L16 20l2.3-.7z"/>',
  "layers": '<path d="M12 2l10 5-10 5L2 7z"/><path d="M2 17l10 5 10-5M2 12l10 5 10-5"/>',
  "briefcase": '<rect x="2" y="7" width="20" height="14" rx="2"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/>',
  "megaphone": '<path d="M3 11l18-8v18L3 13z"/><path d="M11.6 16.8a3 3 0 1 1-5.8-1.6"/>',
  "home": '<path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><path d="M9 22V12h6v10"/>',
  "scale": '<path d="M12 3v18M5 21h14M3 7h18M6 7l-3 7a3 3 0 0 0 6 0zM18 7l-3 7a3 3 0 0 0 6 0z"/>',
  "heart": '<path d="M20.8 4.6a5.5 5.5 0 0 0-7.8 0L12 5.7l-1-1.1a5.5 5.5 0 0 0-7.8 7.8l1 1.1L12 21l7.8-7.5 1-1.1a5.5 5.5 0 0 0 0-7.8z"/>',
  "book": '<path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20V2H6.5A2.5 2.5 0 0 0 4 4.5z"/><path d="M4 19.5A2.5 2.5 0 0 0 6.5 22H20v-5"/>',
  "globe": '<circle cx="12" cy="12" r="10"/><path d="M2 12h20M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/>',
  "cart": '<circle cx="9" cy="21" r="1"/><circle cx="20" cy="21" r="1"/><path d="M1 1h4l2.7 13.4a2 2 0 0 0 2 1.6h9.7a2 2 0 0 0 2-1.6L23 6H6"/>',
  "search": '<circle cx="11" cy="11" r="8"/><path d="M21 21l-4.3-4.3"/>',
  "tool": '<path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.8-3.8a6 6 0 0 1-7.9 7.9l-6.9 6.9a2.1 2.1 0 0 1-3-3l6.9-6.9a6 6 0 0 1 7.9-7.9z"/>',
  "plug": '<path d="M12 22v-5M9 8V2M15 8V2M18 8v5a6 6 0 0 1-12 0V8z"/>',
  "test": '<path d="M9 2v6L4 18a2 2 0 0 0 1.8 3h12.4A2 2 0 0 0 20 18l-5-10V2M8 2h8M7 14h10"/>',
  "grad": '<path d="M22 10L12 5 2 10l10 5z"/><path d="M6 12v5c3 2 9 2 12 0v-5"/>',
  "life": '<circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="4"/><path d="M4.9 4.9l4.3 4.3M14.8 14.8l4.3 4.3M14.8 9.2l4.3-4.3M4.9 19.1l4.3-4.3"/>',
  "map": '<path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/>',
  "linkedin": '<path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-4 0v7h-4v-7a6 6 0 0 1 6-6z"/><rect x="2" y="9" width="4" height="12"/><circle cx="4" cy="4" r="2"/>',
  "play": '<circle cx="12" cy="12" r="10"/><path d="M10 8l6 4-6 4z"/>',
  "menu": '<path d="M3 6h18M3 12h18M3 18h18"/>',
  "lang": '<path d="M5 8l6 6M4 14l6-6 2-3M2 5h12M7 2h1M22 22l-5-10-5 10M14 18h6"/>',
  "target": '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1"/>',
  "tag": '<path d="M20.6 13.4l-7.2 7.2a2 2 0 0 1-2.8 0L2 12V2h10l8.6 8.6a2 2 0 0 1 0 2.8z"/><circle cx="7" cy="7" r="1.5"/>',
  "chev": '<path d="M6 9l6 6 6-6"/>',
  "share": '<circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/><path d="M8.6 13.5l6.8 4M15.4 6.5l-6.8 4"/>',
  "funnel": '<path d="M3 4h18l-7 8v6l-4 2v-8z"/>',
  "inboxes": '<path d="M22 12h-6l-2 3h-4l-2-3H2"/><path d="M5.45 5.11L2 12v6a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-6l-3.45-6.89A2 2 0 0 0 16.76 4H7.24a2 2 0 0 0-1.79 1.11z"/>',
  "chart": '<path d="M3 3v18h18"/><path d="M7 15l4-4 3 3 5-6"/>',
  "school": '<path d="M22 10L12 5 2 10l10 5z"/><path d="M6 12v5c3 2 9 2 12 0v-5"/>',
  "rocket": '<path d="M4.5 16.5c-1.5 1.3-2 5-2 5s3.7-.5 5-2c.7-.8.7-2.1-.1-2.9a2.2 2.2 0 0 0-2.9-.1z"/><path d="M12 15l-3-3a22 22 0 0 1 2-3.9A12.9 12.9 0 0 1 22 2c0 2.7-.8 7.5-6 11a22.4 22.4 0 0 1-4 2z"/><path d="M9 12H4s.6-3 2-4c1.6-1.1 5 0 5 0M12 15v5s3-.6 4-2c1.1-1.6 0-5 0-5"/>',
  "user-check": '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M16 11l2 2 4-4"/>',
  "x-circle": '<circle cx="12" cy="12" r="10"/><path d="M15 9l-6 6M9 9l6 6"/>',
  "ext": '<path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6M15 3h6v6M10 14L21 3"/>',
  "phone": '<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z"/>',
  "info": '<circle cx="12" cy="12" r="10"/><path d="M12 16v-4M12 8h.01"/>',
  "eye-sample": '<rect x="3" y="4" width="18" height="14" rx="2"/><path d="M7 21h10M9 9h6M9 13h3"/>',
}


WA_SVG = '<svg viewBox="0 0 32 32" fill="currentColor" aria-hidden="true"><path d="M16 3C9 3 3.4 8.6 3.4 15.6c0 2.2.6 4.4 1.7 6.3L3.3 29l7.3-1.9c1.8 1 3.9 1.5 6 1.5h.1C23.6 28.6 29.3 23 29.3 16 29.3 9 23.1 3 16 3zm0 23.3c-1.9 0-3.7-.5-5.3-1.4l-.4-.2-4.3 1.1 1.2-4.2-.3-.4c-1-1.6-1.5-3.5-1.5-5.4C5.4 10 10.2 5.3 16 5.3c2.8 0 5.5 1.1 7.5 3.1s3.1 4.7 3.1 7.5c0 5.8-4.8 10.4-10.6 10.4zm5.8-7.8c-.3-.2-1.9-.9-2.2-1-.3-.1-.5-.2-.7.2-.2.3-.8 1-1 1.2-.2.2-.4.2-.7.1-.3-.2-1.3-.5-2.5-1.6-.9-.8-1.6-1.8-1.7-2.1-.2-.3 0-.5.1-.7l.5-.6c.2-.2.2-.3.3-.5.1-.2.1-.4 0-.6l-1-2.4c-.3-.6-.5-.5-.7-.5h-.6c-.2 0-.6.1-.9.4-.3.3-1.2 1.2-1.2 2.9s1.2 3.3 1.4 3.6c.2.2 2.4 3.7 5.8 5.1 2.9 1.1 3.4.9 4.1.9.6-.1 1.9-.8 2.2-1.6.3-.8.3-1.4.2-1.6-.1-.2-.3-.3-.6-.4z"/></svg>'
LOGO_SVG = '<svg viewBox="0 0 40 40" aria-hidden="true"><defs><linearGradient id="lg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#7c5cff"/><stop offset="1" stop-color="#2dd4bf"/></linearGradient></defs><rect width="40" height="40" rx="11" fill="url(#lg)"/><path d="M9.5 28V12.5l9 15V12.5" fill="none" stroke="#fff" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/><path d="M22.5 28V12.5l4.75 8 4.75-8V28" fill="none" stroke="#fff" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></svg>'


def ic(name):
    return f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[name]}</svg>'


def wa(msg="Hello Naomi, I'd like to talk about automating part of my business."):
    from urllib.parse import quote
    return f"https://wa.me/{WHATSAPP}?text={quote(msg)}"


BOOK = "contact.html?type=consultation#enquiry"
EMAIL_LINK = '<a href="contact.html#enquiry" data-email data-email-show>Email me</a>'

NAV_BEFORE = [("index.html", "Home"), ("about.html", "About")]
NAV_AFTER = [("services.html", "Services"), ("contact.html", "Contact")]


def nav_items(cur):
    li = lambda h, t: f'<li><a href="{h}"{" aria-current=" + chr(34) + "page" + chr(34) if h == cur else ""}>{t}</a></li>'
    prods = "".join(f'<li><a href="{p["url"]}" data-track="nav_{p["key"]}"><span class="pi {p["pi"]}">{ic(p["icon"])}</span><span><b>{p["name"]}</b><small>{p["short"]}</small></span></a></li>' for p in PRODUCTS)
    dd = f'''<li class="has-dd"><button class="dd-toggle" type="button" aria-expanded="false" aria-controls="dd-products"{" data-current" if cur == "products.html" else ""}>Our Products {ic("chev")}</button>
      <ul class="dd" id="dd-products">{prods}<li><a class="dd-all" href="products.html">Compare all products</a></li></ul></li>'''
    return "".join(li(h, t) for h, t in NAV_BEFORE) + dd + "".join(li(h, t) for h, t in NAV_AFTER)


def header(current):
    return f'''<a class="skip-link" href="#main">Skip to content</a>
<header class="site-header">
  <nav class="container nav" aria-label="Main">
    <a class="logo" href="index.html" aria-label="Naomi Mwangi home">{LOGO_SVG}<span>Naomi <b>Mwangi</b></span></a>
    <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="menu" aria-label="Open menu">{ic("menu")}</button>
    <ul class="menu" id="menu">{nav_items(current)}<li class="menu-cta"><a href="{BOOK}" data-track="cta_book_consultation">Book a consultation</a></li></ul>
  </nav>
</header>'''


def footer():
    year = datetime.date.today().year
    return f'''<footer class="site-footer">
  <div class="container">
    <div class="foot-grid">
      <div>
        <a class="logo" href="index.html">{LOGO_SVG}<span>Naomi <b>Mwangi</b></span></a>
        <p class="mt-1">Practical AI automation that helps growing businesses reduce repetitive work, stay organised and spend more time on growth. Based in Nairobi, Kenya, working with clients locally and internationally.</p>
      </div>
      <div><h3>Our products</h3><ul>
        <li><a href="{SOCIALFLOW_URL}">SocialFlow AI</a></li>
        <li><a href="{EXECUTIVEFLOW_URL}">ExecutiveFlow AI</a></li>
        <li><a href="{LEADFLOW_URL}">LeadFlow AI</a></li>
        <li><a href="products.html">Compare products</a></li></ul></div>
      <div><h3>Company</h3><ul>
        <li><a href="about.html">About me</a></li>
        <li><a href="services.html">Automation services</a></li>
        <li><a href="how-it-works.html">How it works</a></li>
        <li><a href="pricing.html">Pricing</a></li></ul></div>
      <div><h3>Get started</h3><ul>
        <li><a href="{BOOK}" data-track="cta_book_consultation">Book a consultation</a></li>
        <li><a href="contact.html?type=demo#enquiry" data-track="cta_request_demo">Request a demo</a></li>
        <li><a href="contact.html">Contact me</a></li>
        <li><a href="privacy.html">Privacy notice</a></li></ul></div>
      <div><h3>Contact</h3><ul>
        <li>{EMAIL_LINK}</li>
        <li><a href="{wa()}" target="_blank" rel="noopener" data-track="whatsapp_click">WhatsApp {WHATSAPP_DISPLAY}</a></li>
        <li><a href="{LINKEDIN}" target="_blank" rel="noopener">LinkedIn</a></li>
        <li>Nairobi, Kenya</li></ul></div>
    </div>
    <div class="foot-bottom"><span>&copy; <span data-year>{year}</span> Naomi Mwangi. All rights reserved.</span><span><a href="privacy.html">Privacy</a> · <a href="sitemap.xml">Sitemap</a></span></div>
  </div>
</footer>
<a class="wa-float" href="{wa()}" target="_blank" rel="noopener" aria-label="Chat with Naomi Mwangi on WhatsApp" data-track="whatsapp_click">{WA_SVG}</a>'''


ORG = {"@context": "https://schema.org", "@type": "ProfessionalService", "name": "Naomi Mwangi", "url": SITE_URL + "/",
       "logo": SITE_URL + "/assets/img/favicon.svg",
       "description": "Practical AI automation and digital solutions for entrepreneurs, startups and small to medium-sized businesses.",
       "founder": {"@type": "Person", "name": "Naomi Mwangi", "jobTitle": "AI Automation Specialist", "sameAs": [LINKEDIN]},
       "address": {"@type": "PostalAddress", "addressLocality": "Nairobi", "addressCountry": "KE"},
       "areaServed": ["Kenya", "Worldwide"], "sameAs": [LINKEDIN],
       "brand": [{"@type": "Brand", "name": "SocialFlow AI", "url": SOCIALFLOW_URL}, {"@type": "Brand", "name": "ExecutiveFlow AI", "url": EXECUTIVEFLOW_URL},
                 {"@type": "Brand", "name": "LeadFlow AI", "url": LEADFLOW_URL}]}


def page(fn, title, desc, body, ld=None, noindex=False):
    url = SITE_URL + "/" + ("" if fn == "index.html" else fn)
    lds = "".join('<script type="application/ld+json">' + json.dumps(x, ensure_ascii=False) + "</script>" for x in (ld or []))
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="robots" content="{"noindex, follow" if noindex else "index, follow"}">
<link rel="canonical" href="{url}">
<meta name="theme-color" content="#070c22">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Naomi Mwangi">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE_URL}/assets/img/og-image.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="assets/img/favicon.svg" type="image/svg+xml">
<link rel="icon" href="assets/img/favicon-32.png" type="image/png" sizes="32x32">
<link rel="icon" href="favicon.ico" sizes="any">
<link rel="apple-touch-icon" href="assets/img/apple-touch-icon.png">
<link rel="manifest" href="site.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&amp;display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/site.css?v={ASSET_VERSION}">
<script>document.documentElement.classList.add("js");setTimeout(function(){{if(!window.__yv)document.documentElement.classList.remove("js")}},2500);</script>
{lds}
</head>
<body>
{header(fn)}
<main id="main">
{body}
</main>
{footer()}
<script src="assets/js/config.js?v={ASSET_VERSION}"></script>
<script src="assets/js/main.js?v={ASSET_VERSION}"></script>
</body>
</html>
'''
    open(os.path.join(OUT, fn), "w", encoding="utf-8").write(html)


def page_hero(crumb, eyebrow, h1, text, extra=""):
    crumbs = f'<p class="crumbs"><a href="index.html">Home</a> / {crumb}</p>' if crumb else ""
    return f'''<section class="page-hero"><div class="container">{crumbs}<span class="eyebrow">{eyebrow}</span><h1>{h1}</h1><p>{text}</p>{extra}</div></section>'''


def cta(title="Let's find the first workflow worth automating",
        text="Book a free consultation. I'll look at how your business runs today and show you what can realistically be automated, and what it would take."):
    return f'''<section class="section"><div class="container"><div class="cta reveal">
  <div><h2>{title}</h2><p>{text}</p></div>
  <div class="btn-row"><a class="btn btn--primary" href="{BOOK}" data-track="cta_book_consultation">Book a consultation {ic("arrow")}</a>
  <a class="btn btn--wa" href="{wa()}" target="_blank" rel="noopener" data-track="whatsapp_click">{WA_SVG} WhatsApp me</a></div>
</div></div></section>'''


def faq(items):
    return '<div class="faq">' + "".join(f'<details class="reveal"><summary>{q}</summary><div><p>{a}</p></div></details>' for q, a in items) + "</div>"


def faq_ld(items):
    strip = lambda s: re.sub(r"<[^>]+>", "", s)
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": strip(q), "acceptedAnswer": {"@type": "Answer", "text": strip(a)}} for q, a in items]}


def sample_label(dark=False):
    style = ' style="color:#9aa7c9"' if dark else ""
    return f'<p class="sample-label"{style}>{ic("info")}Illustration with sample data, not a real client account</p>'


# ============================================================== CONTENT
PRODUCTS = [
    {"key": "socialflow", "acc": "acc-sf", "pi": "pi--sf", "short": "Social media content, approvals and reporting", "icon": "share", "name": "SocialFlow AI",
     "tagline": "Plan, create and approve social content in one flow.",
     "desc": "An AI-powered social media workflow that turns your goals into a content calendar, drafts on-brand captions and hashtags, routes posts for approval and summarises how your content performs.",
     "problem": "Posting consistently takes hours of planning, writing and back-and-forth approvals, so content ends up last-minute or stops altogether.",
     "caps": ["AI-assisted content generation", "Social media content calendars", "Caption and hashtag generation", "Content strategy development", "Content approval workflows", "Publishing and scheduling integrations", "Social media performance summaries"],
     "ideal": "Businesses, social media managers, marketing agencies and entrepreneurs.",
     "url": SOCIALFLOW_URL, "external": True, "status": "Available now"},
    {"key": "executiveflow", "acc": "acc-ef", "pi": "pi--ef", "short": "Email, tasks, meetings and daily briefings", "icon": "inboxes", "name": "ExecutiveFlow AI",
     "tagline": "Your inbox, tasks and meetings, organised every morning.",
     "desc": "An AI-powered executive assistant that organises and summarises your email, turns requests into tasks, coordinates meetings, drafts replies for your approval and sends you a daily briefing.",
     "problem": "Important emails get buried, deadlines hide in long threads and follow-ups slip, while hours go into sorting the inbox instead of running the business.",
     "caps": ["Email organisation and summarisation", "Task extraction", "Calendar and meeting coordination", "Administrative workflow automation", "Daily briefings", "Follow-up reminders", "AI-assisted email drafting with human approval"],
     "ideal": "Entrepreneurs, executives, consultants and busy professionals.",
     "url": EXECUTIVEFLOW_URL, "external": True, "status": "Available as a custom setup"},
    {"key": "leadflow", "acc": "acc-lf", "pi": "pi--lf", "short": "Lead capture, qualification and follow-up", "icon": "funnel", "name": "LeadFlow AI",
     "tagline": "Capture every enquiry and follow up on time.",
     "desc": "An intelligent lead management system that captures enquiries from your website and inbox, organises and qualifies them, reminds you to follow up and shows where every lead stands.",
     "problem": "Enquiries arrive through forms, email and WhatsApp. Without a system some are missed, replies are slow and follow-ups depend on memory.",
     "caps": ["Website enquiry capture", "Lead organisation and categorisation", "AI-assisted lead qualification", "CRM and spreadsheet integration", "Automated follow-up reminders", "Lead notifications", "Sales pipeline reporting"],
     "ideal": "Service businesses, real estate companies, consultants, agencies and sales teams.",
     "url": LEADFLOW_URL, "external": True, "status": "Available as a custom setup"}
]


def product_card(p, compact=False):
    caps = p["caps"][:4] if compact else p["caps"]
    more = f'<p class="muted small mb-0">+ {len(p["caps"]) - 4} more capabilities</p>' if compact else ""
    explore = f'<a class="btn btn--acc btn--sm" href="{p["url"]}" data-track="explore_{p["key"]}">Explore {p["name"]} {ic("ext" if p["external"] else "arrow")}</a>'
    demo = f'<a class="link-arrow small" href="{p["url"]}#contact" data-track="cta_request_demo_{p["key"]}">Request a demo {ic("arrow")}</a>'
    return f'''<article class="product {p["acc"]} reveal" id="{p["key"]}">
  <div class="p-head"><span class="p-mark">{ic(p["icon"])}</span><div><h3>{p["name"]}</h3><span class="badge">{p["status"]}</span></div></div>
  <p class="tagline">{p["tagline"]}</p>
  <p>{p["desc"]}</p>
  <dl>
    <div><dt>The problem it solves</dt><dd>{p["problem"]}</dd></div>
    <div><dt>Key capabilities</dt><dd><ul class="checks">{"".join(f"<li>{c}</li>" for c in caps)}</ul>{more}</dd></div>
    <div><dt>Ideal for</dt><dd>{p["ideal"]}</dd></div>
  </dl>
  <div class="p-foot">{explore}{demo}</div>
</article>'''


CHALLENGES = [
    ("inbox", "Hours lost in the inbox", "Sorting, reading and replying to email eats the time you meant to spend on clients and growth."),
    ("funnel", "Enquiries that go cold", "Leads arrive in different places, replies are slow and follow-ups depend on someone remembering."),
    ("share", "Content that's always last-minute", "Planning, writing and approving social posts takes so long that consistency suffers."),
    ("repeat", "Admin that never ends", "Copying data between emails, forms and spreadsheets, and preparing the same reports every week."),
    ("plug", "Tools that don't talk to each other", "Your apps hold the information, but moving it between them is still manual work."),
    ("eye", "No clear view of what's due", "Tasks, deadlines and promises are scattered across threads, so things slip through the cracks."),
]

STEPS = [
    ("Discover", "Understand your business and challenges.",
     ["A conversation about how your business runs today", "Where time is lost and what frustrates your team", "Your goals, tools, budget and any constraints"]),
    ("Analyse", "Identify repetitive tasks and automation opportunities.",
     ["Map the tasks that repeat every day or week", "Estimate which automations will save the most time", "Flag anything that should stay manual"]),
    ("Design", "Plan a suitable workflow.",
     ["A written workflow plan you can understand", "Clear scope, timeline and quote before work starts", "Agreement on data, access and human approval points"]),
    ("Implement", "Build, integrate and test the solution.",
     ["Built in your own accounts (e.g. Google Workspace, Make.com)", "Tested with realistic examples before going live", "Handover with simple documentation and training"]),
    ("Optimise", "Monitor performance and improve the workflow.",
     ["Check results and fix anything that needs adjusting", "Improve prompts, rules and reports as you learn", "Add the next workflow when you're ready"]),
]

INDUSTRIES = [
    ("rocket", "Entrepreneurs & founders", "Get time back from email, admin and follow-ups."),
    ("briefcase", "Startups & SMEs", "Put simple, reliable systems in place as you grow."),
    ("user-check", "Consultants & independent professionals", "Stay on top of clients, meetings and proposals."),
    ("megaphone", "Marketing agencies", "Plan, approve and report on content for many clients."),
    ("school", "Schools & educational institutions", "Handle enquiries, admissions communication and admin."),
    ("home", "Real estate", "Capture property enquiries and follow up quickly."),
    ("scale", "Professional services", "Organise correspondence, documents and deadlines."),
    ("globe", "NGOs & organisations", "Coordinate partners, reporting and internal tasks."),
]

WHY = [
    ("target", "Practical, not experimental", "I automate real, everyday tasks — email, enquiries, content and admin — with results you notice in your working week."),
    ("layers", "Start small, grow at your pace", "Begin with the workflow that matters most, then add more as your needs grow. Nothing is locked in."),
    ("hand", "You stay in control", "Human approval is built in wherever it matters: replies, posts and meetings don't go out without you."),
    ("shield", "Your accounts, your data", "Systems run in tools you own, such as Google Workspace and Make.com, with only the access each workflow needs."),
    ("book", "Clear handover", "You get plain-language documentation and training, so you understand exactly how your system works."),
    ("tag", "Transparent pricing", "Starting prices are published in KES, you receive a written quote before work begins, and third-party tool costs are explained upfront."),
]

HOME_FAQ = [
    ("What do you do?", "I help businesses reduce repetitive work by setting up practical AI automation: organising email and tasks, capturing and following up on leads, planning and approving social media content, and connecting the tools you already use."),
    ("Are your products apps I sign up for?", "No. SocialFlow AI, ExecutiveFlow AI and LeadFlow AI are done-for-you systems that I design and set up for your business, mostly in tools you already own such as Google Workspace, together with Make.com and AI. There is nothing to install."),
    ("Will anything be sent or posted without my approval?", "Not unless you want it to be. By default, email replies stay as drafts, social posts wait for approval and meetings are only added to your calendar once you confirm them."),
    ("Which tools do you work with?", "Mainly Gmail, Google Sheets, Google Calendar, Google Forms and Make.com, with AI for summaries, classification and drafting. Other tools can often be connected; I confirm this during the consultation."),
    ("How much does it cost?", "Each product has its own pricing: ExecutiveFlow AI setups start at KES 15,000, SocialFlow AI lists its plans on its own site, and LeadFlow AI and custom projects are quoted after a consultation. You always get a written quote before work starts, and third-party tool costs such as Make.com are explained upfront. See <a href=\"pricing.html\">pricing</a>."),
    ("Do you work with businesses outside Kenya?", "Yes. I work remotely with clients in Kenya and internationally, and can quote in KES or another currency."),
]


# ============================================================== PAGES
def build_home():
    nodes = [("SocialFlow AI", "Social content planned, drafted and approved", "share", "pi--sf", SOCIALFLOW_URL, "50%", "15%"),
             ("ExecutiveFlow AI", "Inbox, tasks and meetings organised", "inboxes", "pi--ef", EXECUTIVEFLOW_URL, "24%", "80%"),
             ("LeadFlow AI", "Every enquiry captured and followed up", "funnel", "pi--lf", LEADFLOW_URL, "76%", "80%")]
    eco_nodes = "".join(f'<a class="eco-node" href="{u}" style="left:{x};top:{y}" data-track="hero_{n.split()[0].lower()}"><span class="pi {c}">{ic(i)}</span><b>{n}</b><small>{d}</small></a>' for n, d, i, c, u, x, y in nodes)
    challenges = "".join(f'<div class="card card--flat problem reveal"><span class="ico">{ic(i)}</span><div><h3>{t}</h3><p class="mb-0">{d}</p></div></div>' for i, t, d in CHALLENGES)
    products = "".join(product_card(p, compact=True) for p in PRODUCTS)
    steps = "".join(f'<div class="step reveal"><span class="n">{n}</span><h3>{t}</h3><p>{d}</p></div>' for n, (t, d, _) in enumerate(STEPS, 1))
    inds = "".join(f'<div class="industry reveal"><span class="ico">{ic(i)}</span><div><h3>{t}</h3><p>{d}</p></div></div>' for i, t, d in INDUSTRIES)
    why = "".join(f'<div class="card reveal"><span class="ico">{ic(i)}</span><h3>{t}</h3><p>{d}</p></div>' for i, t, d in WHY)
    body = f'''
<section class="hero">
  <div class="container hero-grid">
    <div>
      <span class="eyebrow">AI automation &amp; digital solutions</span>
      <h1>Work Smarter. Automate Better. <span class="grad">Grow Faster.</span></h1>
      <p class="hero-copy">I'm Naomi Mwangi, an AI automation specialist. I build practical systems that take repetitive work off your team's plate, so your business runs smoother and has more time to grow.</p>
      <div class="btn-row">
        <a class="btn btn--primary" href="{BOOK}" data-track="cta_book_consultation">Book a Consultation {ic("arrow")}</a>
        <a class="btn btn--ghost" href="#products" data-track="cta_explore_products">Explore Our Products</a>
      </div>
      <ul class="hero-notes">
        <li>{ic("hand")} You approve what goes out</li>
        <li>{ic("plug")} Built in tools you already use</li>
        <li>{ic("globe")} Kenya &amp; international clients</li>
      </ul>
    </div>
    <div class="eco" role="group" aria-label="My three products connected to your business">
      <svg class="eco-lines" viewBox="0 0 100 92" preserveAspectRatio="none" aria-hidden="true">
        <path d="M50 22 C50 32, 50 36, 50 38"/><path d="M30 70 C35 64, 39 59, 43 55"/><path d="M70 70 C65 64, 61 59, 57 55"/>
      </svg>
      <div class="eco-hub">Your business<small>one connected workflow</small></div>
      {eco_nodes}
      <div class="eco-tools" aria-label="Tools I connect"><span>Gmail</span><span>Google Sheets</span><span>Calendar</span><span>Make.com</span><span>AI models</span></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container split">
    <div class="reveal">
      <span class="eyebrow">What I do</span>
      <h2>AI that solves everyday business problems</h2>
      <p class="lead">I'm an AI automation specialist working with entrepreneurs, startups and growing businesses.</p>
      <p>I help businesses reduce repetitive tasks, organise their work and spend more time growing. Instead of experimenting with AI for its own sake, I build practical systems around the work you already do: answering enquiries, managing email, planning content and keeping track of what's due.</p>
      <a class="link-arrow" href="about.html">More about me {ic("arrow")}</a>
    </div>
    <div class="grid reveal" style="gap:1rem">
      <div class="card card--flat problem"><span class="ico" style="background:var(--violet-100);color:var(--violet-700)">{ic("target")}</span><div><h3>Outcome-first</h3><p class="mb-0">I start with the result you want, such as faster replies or consistent posting, then choose the tools.</p></div></div>
      <div class="card card--flat problem"><span class="ico" style="background:var(--blue-100);color:var(--blue-700)">{ic("cog")}</span><div><h3>Built around your process</h3><p class="mb-0">Every workflow is designed for how your business actually runs, not a generic template.</p></div></div>
      <div class="card card--flat problem"><span class="ico" style="background:var(--teal-100);color:var(--teal-700)">{ic("hand")}</span><div><h3>People stay in charge</h3><p class="mb-0">Automation handles the repetitive steps; you make the decisions that matter.</p></div></div>
    </div>
  </div>
</section>

<section class="section section--soft">
  <div class="container">
    <div class="head reveal"><span class="eyebrow">Challenges I solve</span><h2>Does this sound familiar?</h2><p class="lead">These are the everyday problems that slow growing businesses down, and the ones automation handles well.</p></div>
    <div class="grid g3">{challenges}</div>
  </div>
</section>

<section class="section" id="products">
  <div class="container">
    <div class="head reveal"><span class="eyebrow">Our products</span><h2>Three independent AI products, one goal: less busywork</h2><p class="lead">Each product has its own focus, its own website and its own offering. Start with the one you need most, then add more as you grow.</p></div>
    <div class="grid g3">{products}</div>
    <p class="center mt-2 reveal"><a class="btn btn--outline" href="products.html" data-track="cta_compare_products">Compare all products {ic("arrow")}</a></p>
  </div>
</section>

<section class="section section--dark">
  <div class="container">
    <div class="head reveal"><span class="eyebrow">How it works</span><h2>A simple, five-step process</h2><p class="lead">Every project starts with understanding your business. Nothing is built until we agree on what will genuinely save you time.</p></div>
    <div class="steps">{steps}</div>
    <p class="center mt-2 reveal"><a class="btn btn--ghost" href="how-it-works.html">See the process in detail {ic("arrow")}</a></p>
  </div>
</section>

<section class="section section--soft">
  <div class="container">
    <div class="head reveal"><span class="eyebrow">Who I help</span><h2>Built for busy teams of every kind</h2><p class="lead">If your business runs on email, enquiries, content and deadlines, there's likely work that can be automated.</p></div>
    <div class="grid g4">{inds}</div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="head reveal"><span class="eyebrow">Why work with me</span><h2>Why businesses choose to work with me</h2></div>
    <div class="grid g3">{why}</div>
  </div>
</section>

<section class="section section--soft" id="faq">
  <div class="container">
    <div class="head reveal"><span class="eyebrow">FAQ</span><h2>Questions businesses ask me</h2></div>
    {faq(HOME_FAQ)}
  </div>
</section>
{cta()}
'''
    page("index.html", "Naomi Mwangi | AI Automation &amp; Digital Solutions for Growing Businesses",
         "Naomi Mwangi helps entrepreneurs, startups and SMEs reduce repetitive work with practical AI automation: SocialFlow AI, LeadFlow AI and ExecutiveFlow AI. Book a consultation.",
         body, ld=[ORG, faq_ld(HOME_FAQ)])


def build_products():
    cards = "".join(product_card(p) for p in PRODUCTS)
    body = f'''
{page_hero("Our products", "Our products", "Three AI products for the work that slows you down",
  "SocialFlow AI, ExecutiveFlow AI and LeadFlow AI are independent products, each with its own website, features and offering. Choose one to start, and add the others as your needs grow.",
  f'<div class="btn-row mt-2"><a class="btn btn--primary" href="{BOOK}" data-track="cta_book_consultation">Book a consultation</a><a class="btn btn--ghost" href="contact.html?type=demo#enquiry" data-track="cta_request_demo">Request a demo</a></div>')}
<section class="section section--soft">
  <div class="container">
    <div class="notice reveal" style="margin-bottom:2rem">{ic("info")}<div><p><strong>How my products are delivered.</strong> Each product has its own website where you can explore it in depth. Each product is a done-for-you system that I design and set up for your business, mostly inside tools you already own (such as Google Workspace), connected with Make.com and AI. There's no app to download, and you receive training and documentation at handover.</p></div></div>
    <div class="grid g3">{cards}</div>
  </div>
</section>
<section class="section">
  <div class="container split">
    <div class="reveal">
      <span class="eyebrow">Not sure where to start?</span>
      <h2>Start with one workflow, then grow</h2>
      <p class="lead">Most clients begin with the problem that costs them the most time each week.</p>
      <ul class="checks">
        <li><strong>Drowning in email?</strong> Start with <a href="{EXECUTIVEFLOW_URL}">ExecutiveFlow AI</a>.</li>
        <li><strong>Losing enquiries?</strong> Start with <a href="{LEADFLOW_URL}">LeadFlow AI</a>.</li>
        <li><strong>Struggling to post consistently?</strong> Start with <a href="{SOCIALFLOW_URL}">SocialFlow AI</a>.</li>
        <li><strong>Something else entirely?</strong> I build <a href="services.html">custom automations</a> too.</li>
      </ul>
    </div>
    <div class="card card--flat reveal">
      <h3>Request a walkthrough</h3>
      <p class="muted">Tell me which product interests you. I'll show you how it would work with your tools and your type of work, on a call or over WhatsApp.</p>
      <div class="btn-row"><a class="btn btn--primary" href="contact.html?type=demo#enquiry" data-track="cta_request_demo">Request a demo {ic("arrow")}</a><a class="btn btn--wa" href="{wa("Hello Naomi, I'd like a walkthrough of one of your AI products.")}" target="_blank" rel="noopener" data-track="whatsapp_click">{WA_SVG} WhatsApp</a></div>
    </div>
  </div>
</section>
{cta()}
'''
    ld = {"@context": "https://schema.org", "@type": "ItemList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "item": {"@type": "Service", "name": p["name"], "description": p["desc"],
         "provider": {"@type": "Person", "name": "Naomi Mwangi"}, "url": p["url"]}} for i, p in enumerate(PRODUCTS)]}
    page("products.html", "Our Products: SocialFlow AI, ExecutiveFlow AI &amp; LeadFlow AI | Naomi Mwangi",
         "Explore Naomi Mwangi's AI products: SocialFlow AI for social media workflows, ExecutiveFlow AI for email, tasks and meetings, and LeadFlow AI for lead capture and follow-up.",
         body, ld=[ld])


def redirect(fn, target, name):
    html = f'''<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><title>{name} | Naomi Mwangi</title><meta name="robots" content="noindex, follow"><link rel="canonical" href="{target}"><meta http-equiv="refresh" content="0; url={target}"><script>location.replace("{target}"+location.hash);</script></head><body><p>{name} now has its own website: <a href="{target}">{target}</a></p></body></html>\n'''
    open(os.path.join(OUT, fn), "w").write(html)


def build_redirects():
    redirect("solutions.html", "products.html", "Our products")
    redirect("leadflow-ai.html", LEADFLOW_URL, "LeadFlow AI")
    redirect("executiveflow-ai.html", EXECUTIVEFLOW_URL, "ExecutiveFlow AI")
    redirect("ai-executive-assistant.html", EXECUTIVEFLOW_URL, "ExecutiveFlow AI")


def chips(items):
    return '<div class="chips">' + "".join(f'<span class="chip">{ic(i)}{t}</span>' for i, t in items) + "</div>"


SERVICES = [
    ("process", "cog", "Business process automation",
     "Copying information between emails, forms and spreadsheets, preparing routine reports and chasing updates takes hours of manual effort every week.",
     "Automated workflows that move information between your tools, keep records up to date and produce routine summaries.",
     "I map your current process, then use Make.com to connect your apps (such as Gmail, Google Sheets, Forms and Drive). A trigger, like a new email, form or row, starts a sequence of steps that records, formats and reports the information.",
     ["Less manual data entry and fewer errors", "Up-to-date records without chasing", "Routine reports produced automatically"], None),
    ("ai-integration", "spark", "AI workflow integration",
     "You already have processes that work, but they rely on people reading, sorting and summarising text by hand.",
     "I add AI steps to the workflows you already use, so information is summarised, classified, extracted or drafted automatically.",
     "AI reads incoming text such as emails, form answers or documents and returns structured information (category, priority, key details or a draft). The results flow into your existing tools, with human review where it matters.",
     ["Faster handling of incoming information", "Consistent categories and summaries", "People focus on decisions, not reading"], None),
    ("social", "share", "Social media workflow automation",
     "Planning, writing and approving posts takes so long that social media becomes inconsistent or rushed.",
     "A structured content workflow: AI-assisted planning and drafting, a shared calendar, approvals and simple performance summaries.",
     "Your goals and brand voice become a monthly plan. Drafts, captions and hashtags are prepared for review, approved posts move to scheduling, and results are summarised each month.",
     ["Consistent posting without the scramble", "Clear approvals before anything goes live", "Decisions based on what actually works"], ("SocialFlow AI", SOCIALFLOW_URL)),
    ("leads", "funnel", "Lead management automation",
     "Enquiries arrive in different places, some are missed and follow-ups depend on memory.",
     "An automated enquiry pipeline that captures every lead, organises and qualifies it, and reminds you to follow up.",
     "Form submissions and enquiry emails are captured automatically, details are extracted and logged to a lead tracker, you're notified, and follow-up reminders are scheduled.",
     ["Every enquiry captured and tracked", "Faster first responses", "Follow-ups that happen on time"], ("LeadFlow AI", LEADFLOW_URL)),
    ("executive", "inboxes", "Executive and administrative automation",
     "Email, meeting requests and to-dos pile up, and important items get lost in the noise.",
     "An AI assistant system that organises email, extracts tasks, coordinates meetings, drafts replies for approval and sends a daily briefing.",
     "Make.com checks Gmail on a schedule. AI summarises and prioritises each email, tasks and follow-ups go to Google Sheets, meeting requests are checked against Google Calendar, and drafts wait in Gmail for you.",
     ["Less time sorting email", "Urgent issues surfaced straight away", "A clear plan every morning"], ("ExecutiveFlow AI", EXECUTIVEFLOW_URL)),
    ("custom", "puzzle", "Custom AI-assisted business solutions",
     "Some processes don't fit any off-the-shelf product, so they stay manual and slow.",
     "A tailored solution designed around your process, combining automation and AI only where it adds real value.",
     "I follow my five-step process: understand the process, identify what can be automated, design the workflow, build and test it, then monitor and improve it.",
     ["Automation that fits how you actually work", "Connected tools instead of copy-paste", "Reliable, documented workflows"], None),
]


def build_services():
    blocks = ""
    for n, (sid, icon, name, prob, sol, how, ben, prod) in enumerate(SERVICES, 1):
        link = f'<p class="mt-1 mb-0"><a class="link-arrow" href="{prod[1]}">Explore {prod[0]} {ic("arrow")}</a></p>' if prod else ""
        blocks += f'''
    <article class="service" id="{sid}">
      <div class="reveal"><span class="ico">{ic(icon)}</span><span class="num">SERVICE {n:02d}</span><h2 style="font-size:1.6rem">{name}</h2>{link}
        <p class="mt-1"><a class="btn btn--outline btn--sm" href="contact.html?type=consultation#enquiry" data-track="cta_service_enquiry">Discuss this service</a></p></div>
      <div class="sb reveal">
        <div class="problem-box"><h4>The problem</h4><p class="mb-0">{prob}</p></div>
        <div><h4>The solution</h4><p class="mb-0">{sol}</p></div>
        <div><h4>How it works</h4><p class="mb-0">{how}</p></div>
        <div><h4>What you gain</h4><ul class="checks mb-0">{"".join(f"<li>{b}</li>" for b in ben)}</ul></div>
      </div>
    </article>'''
    path = [("1", "Start with one workflow", "Pick the process that costs you the most time each week, and I automate that first."),
            ("2", "See the results", "Use it in your real work, notice the time saved and adjust what needs tuning."),
            ("3", "Expand as you grow", "Add the next workflow when you're ready, building on what already works.")]
    body = f'''
{page_hero("Services", "Automation services", "Custom automation for the way your business works",
  "Beyond my three products, I design automations around your specific processes, from simple data workflows to AI-assisted solutions.")}
<section class="section"><div class="container">{blocks}</div></section>
<section class="section section--soft">
  <div class="container">
    <div class="head reveal"><span class="eyebrow">Start small</span><h2>Start with one workflow and expand as your needs grow</h2><p class="lead">You don't need to automate everything at once. Most successful projects start with one well-chosen workflow.</p></div>
    <div class="grid g3">{"".join(f'<div class="card reveal"><span class="ico" style="font-weight:800">{n}</span><h3>{t}</h3><p>{d}</p></div>' for n, t, d in path)}</div>
    <div class="mt-3 reveal" style="text-align:center"><p class="muted small">Tools I commonly connect</p>{chips([("mail", "Gmail"), ("sheet", "Google Sheets"), ("cal", "Google Calendar"), ("list", "Google Forms"), ("layers", "Google Drive"), ("zap", "Make.com"), ("spark", "AI models")]).replace('class="chips"', 'class="chips" style="justify-content:center"')}</div>
  </div>
</section>
{cta("Not sure which service fits?", "Tell me what's taking up your time. I'll recommend where to start, or tell you honestly if automation isn't the right answer.")}
'''
    page("services.html", "Automation Services: Process, AI, Social, Leads &amp; Admin | Naomi Mwangi",
         "Business process automation, AI workflow integration, social media, lead management, executive and administrative automation, and custom AI-assisted solutions from Naomi Mwangi.",
         body)


def build_process():
    tl = "".join(f'''<div class="tl reveal"><span class="n">{n}</span><div class="body"><h3>{t}</h3><p class="q">{d}</p><ul>{"".join(f"<li>{x}</li>" for x in xs)}</ul></div></div>''' for n, (t, d, xs) in enumerate(STEPS, 1))
    body = f'''
{page_hero("How it works", "How it works", "Five clear steps from first conversation to a working system",
  "A transparent process that starts with your business, not the technology. You'll know what's being built, why, and what it will cost before any work begins.",
  f'<div class="btn-row mt-2"><a class="btn btn--primary" href="{BOOK}" data-track="cta_book_consultation">Start with a consultation {ic("arrow")}</a></div>')}
<section class="section section--soft"><div class="container"><div class="timeline">{tl}</div></div></section>
<section class="section">
  <div class="container split split--top">
    <div class="reveal"><span class="eyebrow">What I need from you</span><h2>Easy to get started</h2>
      <ul class="checks"><li>A 30–60 minute conversation about your work</li><li>Examples of the emails, enquiries or tasks you want automated</li><li>Access to the relevant accounts, granted securely when I build</li><li>Your feedback during testing</li></ul></div>
    <div class="reveal"><span class="eyebrow">How I work</span><h2>My principles</h2>
      <ul class="checks"><li><strong>Practical first:</strong> automate what genuinely saves time</li><li><strong>Human in the loop:</strong> approvals wherever decisions matter</li><li><strong>Transparent costs:</strong> including third-party tool costs</li><li><strong>Your accounts, your data:</strong> systems run in tools you own</li><li><strong>Documented:</strong> you understand what was built</li></ul></div>
  </div>
</section>
{cta()}
'''
    ld = {"@context": "https://schema.org", "@type": "HowTo", "name": "How an automation project with Naomi Mwangi works",
          "step": [{"@type": "HowToStep", "position": n, "name": t, "text": d} for n, (t, d, _) in enumerate(STEPS, 1)]}
    page("how-it-works.html", "How It Works: Discover, Analyse, Design, Implement, Optimise | Naomi Mwangi",
         "My five-step automation process: discover your business, analyse automation opportunities, design the workflow, implement and test it, then optimise it over time.",
         body, ld=[ld])


def build_pricing():
    cards = [
        ("acc-sf", "share", "SocialFlow AI", "Plans for social media content workflows are listed on the SocialFlow AI website.", SOCIALFLOW_URL + "#pricing", "See SocialFlow AI pricing"),
        ("acc-ef", "inboxes", "ExecutiveFlow AI", "One-off setup packages from KES 15,000 (Starter), KES 30,000 (Professional) and KES 50,000+ (Business).", EXECUTIVEFLOW_URL + "#pricing", "See ExecutiveFlow AI packages"),
        ("acc-lf", "funnel", "LeadFlow AI", "Quoted after a short consultation, based on your lead sources, tools and volumes.", LEADFLOW_URL + "#pricing", "See how LeadFlow AI is priced"),
    ]
    html = "".join(f'''<div class="card reveal {acc}"><span class="ico" style="background:var(--acc-bg);color:var(--acc)">{ic(i)}</span><h3>{n}</h3><p>{d}</p><a class="link-arrow" href="{u}">{l} {ic("ext")}</a></div>''' for acc, i, n, d, u, l in cards)
    pfaq = [("Why is pricing on each product's website?", "Each product is independent and priced for the work it does, so its packages live with its features and FAQs. This page brings them together."),
            ("What other costs should I expect?", "Tools such as Make.com charge based on how much an automation runs, and some AI features have usage costs. I estimate these with you before building. Usage is never unlimited."),
            ("How are custom projects priced?", "Custom automation, workflow integration and process automation are quoted after a consultation. You receive a written quote before anything starts."),
            ("Is maintenance included?", "Setup prices are one-off. Optional monthly maintenance (monitoring, adjustments and support) is quoted separately, based on the size of your system."),
            ("Do you accept international clients?", "Yes. I can quote in KES or an equivalent amount in your currency.")]
    body = f'''
{page_hero("Pricing", "Pricing", "Pricing by product",
  "Each of my products has its own pricing on its own website. Custom automation work is quoted after a consultation, and you always receive a written quote before work starts.")}
<section class="section section--soft">
  <div class="container">
    <div class="grid g3">{html}</div>
    <div class="grid g2 mt-3">
      <div class="card reveal"><span class="ico">{ic("puzzle")}</span><h3>Custom automation projects</h3><p>Business process automation, AI workflow integration and custom AI-assisted solutions are quoted after a consultation.</p><a class="link-arrow" href="contact.html?service=custom&amp;type=consultation#enquiry">Request a quote {ic("arrow")}</a></div>
      <div class="card reveal"><span class="ico">{ic("tool")}</span><h3>Optional monthly maintenance</h3><p>Monitoring, adjustments, prompt tuning and support after handover, priced by the size of your system.</p><a class="link-arrow" href="contact.html?type=general#enquiry">Ask about maintenance {ic("arrow")}</a></div>
    </div>
    <div class="notice mt-3 reveal">{ic("info")}<div><p><strong>Third-party tool costs</strong> (for example Make.com, which charges by usage) are separate and paid directly by you. I help you choose the right plan.</p></div></div>
  </div>
</section>
<section class="section"><div class="container"><div class="head reveal"><span class="eyebrow">Pricing FAQ</span><h2>Pricing questions</h2></div>{faq(pfaq)}</div></section>
{cta("Get a quote for your business", "Share a little about your processes and I'll recommend the right starting point.")}
'''
    page("pricing.html", "Pricing by Product | Naomi Mwangi",
         "Pricing for Naomi Mwangi's products: SocialFlow AI plans, ExecutiveFlow AI setup packages from KES 15,000, and LeadFlow AI and custom automation quoted on request.",
         body, ld=[faq_ld(pfaq)])


def build_about():
    bg = [("grad", "Information & Communication Technology", "Diploma in ICT"),
          ("tool", "Web development", "HTML, CSS, JavaScript and Bootstrap"),
          ("users", "Virtual assistance", "Administrative and executive support"),
          ("megaphone", "Digital marketing", "Including social media management"),
          ("spark", "AI data training", "Data annotation and validation"),
          ("cog", "Business process automation", "Make.com and Google Workspace")]
    facts = "".join(f'<li><span class="ico">{ic(i)}</span><div><b>{t}</b><span>{d}</span></div></li>' for i, t, d in bg)
    body = f'''
{page_hero("About", "About me", "Making practical AI automation accessible to growing businesses",
  "I believe AI shouldn't be reserved for large companies with big technology budgets. It should help every business work smarter, save time and grow.")}
<section class="section">
  <div class="container split split--top">
    <div class="reveal"><span class="eyebrow">My mission</span><h2>Why I do this work</h2>
      <p class="lead">My mission is to make practical AI automation accessible to growing businesses, so their people spend less time on repetitive work and more time on growth.</p>
      <p>Many entrepreneurs and small teams spend hours each week on work that follows the same pattern: answering similar emails, chasing enquiries, preparing posts and updating spreadsheets. AI and automation can now handle much of that, but the tools can feel complicated and out of reach.</p>
      <p>I close that gap. I turn practical AI into simple, reliable systems built around how each business already works, so people spend less time on repetitive tasks and more time on the work that grows the business.</p></div>
    <div class="reveal"><span class="eyebrow">My vision</span><h2>Where I'm going</h2>
      <p>A future where every growing business, whatever its size, can use AI as an everyday tool rather than an experiment.</p>
      <ul class="checks"><li>Solutions that are useful from the first week</li><li>Technology explained in plain language</li><li>People in control of the decisions that matter</li><li>Systems clients own and understand</li></ul></div>
  </div>
</section>
<section class="section section--soft" id="founder">
  <div class="container split split--top">
    <div class="reveal" style="max-width:420px;width:100%">
      <figure class="portrait" style="margin:0">
        <!-- To add a photo: save it as assets/img/naomi.jpg and uncomment the next line -->
        <!-- <img src="assets/img/naomi.jpg" alt="Naomi Mwangi, AI automation specialist" width="800" height="1000" loading="lazy"> -->
        <span class="ini" aria-hidden="true">NM</span>
        <figcaption><b>Naomi Mwangi</b>AI Automation Specialist</figcaption>
      </figure>
    </div>
    <div class="reveal"><span class="eyebrow">About me</span><h2>Naomi Mwangi</h2>
      <p class="lead">AI Automation Specialist, based in Nairobi, Kenya.</p>
      <p>I started this work to help businesses use technology to simplify their operations. My background brings together the technical, administrative and marketing sides of a business, which shapes how I design automation around real day-to-day work.</p>
      <ul class="facts mt-2">{facts}</ul>
      <p class="mt-2">I work remotely with clients in Kenya and internationally, in English and Kiswahili.</p>
      <div class="btn-row"><a class="btn btn--primary" href="{BOOK}" data-track="cta_book_consultation">Book a consultation</a><a class="btn btn--outline" href="{LINKEDIN}" target="_blank" rel="noopener">{ic("linkedin")} Connect on LinkedIn</a></div>
    </div>
  </div>
</section>
{cta("Let's talk about your business", "Tell me what's taking up your time, and I'll show you what can realistically be automated.")}
'''
    person = {"@context": "https://schema.org", "@type": "Person", "name": "Naomi Mwangi", "jobTitle": "AI Automation Specialist",
              "address": {"@type": "PostalAddress", "addressLocality": "Nairobi", "addressCountry": "KE"},
              "knowsLanguage": ["English", "Swahili"], "sameAs": [LINKEDIN]}
    page("about.html", "About Naomi Mwangi | AI Automation Specialist in Nairobi, Kenya",
         "Naomi Mwangi makes practical AI automation accessible to growing businesses. An AI Automation Specialist in Nairobi with a background in ICT, web development, virtual assistance, digital marketing and AI data training.",
         body, ld=[ORG, person])


def build_contact():
    services = [("socialflow", "SocialFlow AI (social media workflows)"), ("leadflow", "LeadFlow AI (lead capture & follow-up)"),
                ("executiveflow", "ExecutiveFlow AI (email, tasks & meetings)"), ("process", "Business process automation"),
                ("ai-integration", "AI workflow integration"), ("custom", "Custom AI-assisted solution"), ("unsure", "Not sure yet")]
    opts = "".join(f'<option value="{t.replace("&", "&amp;")}" data-key="{k}">{t.replace("&", "&amp;")}</option>' for k, t in services)
    types = [("consultation", "Book a consultation", True), ("demo", "Request a demo", False), ("general", "General question", False)]
    type_html = "".join(f'<label><input type="radio" name="Request type" value="{t}" data-key="{k}"{" checked" if c else ""}> {t}</label>' for k, t, c in types)
    methods = "".join(f'<label><input type="radio" name="Preferred contact method" value="{m}" required data-msg="Please choose how you&#39;d like me to contact you."> {m}</label>' for m in ["Email", "WhatsApp", "Phone call"])
    body = f'''
{page_hero("Contact", "Contact &amp; consultations", "Book a consultation", "Tell me about your business and the work you'd like to simplify. I'll reply with next steps, usually within one working day.")}
<section class="section section--soft">
  <div class="container split split--top split--contact">
    <div class="form-card" id="enquiry">
      <form id="enquiry-form" action="thank-you.html" method="POST" novalidate>
        <h2 style="font-size:1.6rem">Send me your enquiry</h2>
        <p class="muted small">Fields marked <span style="color:var(--violet-700)">*</span> are required.</p>
        <noscript><p class="form-msg form-msg--err">This form needs JavaScript. Please contact me on WhatsApp ({WHATSAPP_DISPLAY}) instead.</p></noscript>
        <input type="hidden" name="_next" value="{SITE_URL}/thank-you.html">
        <input type="hidden" name="_captcha" value="false">
        <input type="hidden" name="_template" value="table">
        <div class="hp" aria-hidden="true"><label>Leave this field empty<input type="text" name="_honey" tabindex="-1" autocomplete="off"></label></div>
        <div class="form-grid">
          <fieldset class="field full"><legend>What would you like to do?</legend><div class="seg">{type_html}</div></fieldset>
          <div class="field"><label for="f-name">Full name <span class="req">*</span></label><input id="f-name" name="Full name" autocomplete="name" required maxlength="100" data-msg="Please enter your full name."><p class="err" id="e-name"></p></div>
          <div class="field"><label for="f-biz">Business name <span class="opt">(optional)</span></label><input id="f-biz" name="Business name" autocomplete="organization" maxlength="120"><p class="err" id="e-biz"></p></div>
          <div class="field"><label for="f-email">Email address <span class="req">*</span></label><input id="f-email" type="email" name="email" autocomplete="email" required maxlength="160" data-msg="Please enter your email address."><p class="err" id="e-email"></p></div>
          <div class="field"><label for="f-phone">Phone number <span class="opt">(optional)</span></label><input id="f-phone" type="tel" name="Phone" autocomplete="tel" maxlength="20" placeholder="+254 7XX XXX XXX"><p class="err" id="e-phone"></p></div>
          <div class="field full"><label for="f-service">Service of interest <span class="req">*</span></label><select id="f-service" name="Service of interest" required data-msg="Please choose a service, or “Not sure yet”."><option value="">Select a service…</option>{opts}</select><p class="err" id="e-service"></p></div>
          <div class="field full"><label for="f-msg">Describe your challenge <span class="req">*</span></label><textarea id="f-msg" name="Challenge" required minlength="20" maxlength="3000" data-msg="Please tell me a little about the challenge." placeholder="What takes up your time today? Which tools do you use? Any deadlines?"></textarea><p class="hint">A few sentences is plenty.</p><p class="err" id="e-msg"></p></div>
          <fieldset class="field full"><legend>Preferred contact method <span class="req">*</span></legend><div class="seg">{methods}</div><p class="err" id="e-method"></p></fieldset>
          <div class="field full"><label class="consent"><input type="checkbox" name="Consent" value="Yes" required data-msg="Please confirm so I can reply to you."> I agree that Naomi Mwangi may use these details to respond to my enquiry, as described in the <a href="privacy.html">privacy notice</a>.</label><p class="err" id="e-consent"></p></div>
          <div class="full"><button class="btn btn--primary btn--block" type="submit">Send enquiry {ic("arrow")}</button></div>
        </div>
        <div id="form-msg" class="form-msg" hidden></div>
      </form>
      <div id="form-done" class="form-success" hidden tabindex="-1">
        <div class="tick">{ic("check")}</div>
        <h2 style="font-size:1.6rem">Thank you<span id="done-name"></span>. Your enquiry has been sent.</h2>
        <p class="muted">Here's what happens next:</p>
        <ol><li>I read your enquiry and look at the challenge you described.</li><li>I'll contact you by <strong id="done-how">email</strong>, usually within one working day.</li><li>If it's a good fit, I'll arrange a short consultation or demo.</li></ol>
        <div class="btn-row" style="justify-content:center"><a class="btn btn--outline" href="products.html">Explore the products</a><a class="btn btn--wa" href="{wa("Hello Naomi, I've just sent an enquiry on your website.")}" target="_blank" rel="noopener" data-track="whatsapp_click">{WA_SVG} Message me on WhatsApp</a></div>
      </div>
    </div>
    <aside>
      <div class="card card--flat">
        <h2 style="font-size:1.3rem">Prefer to chat?</h2>
        <p class="muted">For quick questions, WhatsApp is the fastest way to reach me.</p>
        <a class="btn btn--wa btn--block" href="{wa()}" target="_blank" rel="noopener" data-track="whatsapp_click">{WA_SVG} Chat on WhatsApp</a>
        <a class="btn btn--outline btn--block mt-1" href="#enquiry" data-booking hidden target="_blank" rel="noopener" data-track="cta_booking_page">{ic("cal")} Pick a time online</a>
        <ul class="contact-list mt-2">
          <li><span class="ico">{ic("mail")}</span><div><b>Email</b>{EMAIL_LINK}</div></li>
          <li><span class="ico" style="background:#dcfce7;color:#15803d">{ic("phone")}</span><div><b>WhatsApp</b><a href="{wa()}" target="_blank" rel="noopener">{WHATSAPP_DISPLAY}</a></div></li>
          <li><span class="ico">{ic("linkedin")}</span><div><b>LinkedIn</b><a href="{LINKEDIN}" target="_blank" rel="noopener">Naomi Mwangi</a></div></li>
          <li><span class="ico">{ic("map")}</span><div><b>Location</b><span>Nairobi, Kenya · serving clients locally and remotely (EAT, UTC+3)</span></div></li>
        </ul>
      </div>
      <div class="notice mt-1">{ic("shield")}<p class="small">Please don't include passwords or confidential client data in this form. Your details are used only to respond to your enquiry.</p></div>
    </aside>
  </div>
</section>
'''
    page("contact.html", "Contact Naomi Mwangi | Book a Consultation or Request a Demo",
         "Book a consultation, request a demo or ask a question about SocialFlow AI, LeadFlow AI, ExecutiveFlow AI or custom automation. Contact Naomi Mwangi by form, WhatsApp or email.",
         body, ld=[{"@context": "https://schema.org", "@type": "ContactPage", "name": "Contact Naomi Mwangi", "url": SITE_URL + "/contact.html"}])


def build_misc():
    page("thank-you.html", "Thank You | Naomi Mwangi", "Thank you for contacting Naomi Mwangi.", f'''
<section class="page-hero" style="text-align:center"><div class="container">
  <span class="eyebrow">Enquiry received</span><h1 style="margin-inline:auto">Thank you, I've received your enquiry</h1>
  <p style="margin-inline:auto">I'll reply using your preferred contact method, usually within one working day. For anything urgent, message me on WhatsApp.</p>
  <div class="btn-row mt-2" style="justify-content:center"><a class="btn btn--wa" href="{wa()}" target="_blank" rel="noopener">{WA_SVG} WhatsApp</a><a class="btn btn--ghost" href="products.html">Explore the products</a><a class="btn btn--ghost" href="index.html">Back to home</a></div>
</div></section>''', noindex=True)
    page("404.html", "Page Not Found | Naomi Mwangi", "Page not found.", f'''
<section class="page-hero" style="text-align:center"><div class="container">
  <span class="eyebrow">Error 404</span><h1 style="margin-inline:auto">This page couldn't be found</h1>
  <p style="margin-inline:auto">The link may be out of date. Try one of these instead.</p>
  <div class="btn-row mt-2" style="justify-content:center"><a class="btn btn--primary" href="index.html">Home</a><a class="btn btn--ghost" href="products.html">Our products</a><a class="btn btn--ghost" href="contact.html">Contact</a></div>
</div></section>''', noindex=True)
    page("privacy.html", "Privacy Notice | Naomi Mwangi", "How Naomi Mwangi handles the information you share through this website.", f'''
{page_hero("Privacy notice", "Privacy", "Privacy notice", "How I handle the information you share with me through this website.")}
<section class="section"><div class="container narrow">
  <p class="small muted">Last updated: <span class="placeholder">[add date]</span></p>
  <h2 style="font-size:1.4rem">Who I am</h2><p>This website is operated by Naomi Mwangi, based in Nairobi, Kenya. You can contact me by <a href="contact.html#enquiry" data-email>email</a> or on WhatsApp ({WHATSAPP_DISPLAY}).</p>
  <h2 style="font-size:1.4rem">What I collect</h2><p>When you send an enquiry, I receive the details you enter: your name, business name, email address, phone number, the service you're interested in, your description of the challenge and your preferred contact method.</p>
  <h2 style="font-size:1.4rem">How I use it</h2><p>Only to respond to your enquiry, arrange consultations or demos, and prepare proposals. I don't sell your information or use it for unrelated marketing.</p>
  <h2 style="font-size:1.4rem">How it is delivered and stored</h2><p>Form submissions are delivered to my email inbox through FormSubmit (formsubmit.co). I keep enquiries only as long as needed to respond and for reasonable business records.</p>
  <h2 style="font-size:1.4rem">Analytics</h2><p>If website analytics are switched on, I use aggregated statistics to understand which pages are useful.</p>
  <h2 style="font-size:1.4rem">Your rights</h2><p>Under Kenya's Data Protection Act, 2019, you can ask to access, correct or delete your personal data at any time by contacting me.</p>
  <h2 style="font-size:1.4rem">Client automation projects</h2><p>Automations I build for clients run in the client's own accounts. What data is processed, what access is granted and how long data is kept are agreed with each client before work begins.</p>
</div></section>''')


def build_seo():
    today = datetime.date.today().isoformat()
    pages = [("", "1.0"), ("products.html", "0.9"), ("services.html", "0.8"),
             ("how-it-works.html", "0.7"), ("pricing.html", "0.8"), ("about.html", "0.7"), ("contact.html", "0.9"), ("privacy.html", "0.3")]
    urls = "".join(f"  <url><loc>{SITE_URL}/{p}</loc><lastmod>{today}</lastmod><priority>{pr}</priority></url>\n" for p, pr in pages)
    open(os.path.join(OUT, "sitemap.xml"), "w").write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n')
    open(os.path.join(OUT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\nDisallow: /thank-you.html\n\nSitemap: {SITE_URL}/sitemap.xml\n")


if __name__ == "__main__":
    build_home(); build_products(); build_redirects(); build_services()
    build_process(); build_pricing(); build_about(); build_contact(); build_misc(); build_seo()
    print("Built Naomi Mwangi site in", OUT)
