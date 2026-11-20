# YomieVerse ecosystem: repository structure

YomieVerse is the parent brand. It presents three independent products. Each product has its own repository, website, identity, pricing and enquiry form, and deploys on its own.

```
YomieVerse (parent brand)                     github.com/Yomie-commits/Yomie-Verse
│   https://yomie-commits.github.io/Yomie-Verse/
│
├── SocialFlow AI    social media automation  github.com/Yomie-commits/SocialFlowAI
│   https://yomie-commits.github.io/SocialFlowAI/
│
├── ExecutiveFlow AI executive assistance     github.com/Yomie-commits/ExecutiveFlowAI
│   https://yomie-commits.github.io/ExecutiveFlowAI/
│
└── LeadFlow AI      lead management          github.com/Yomie-commits/LeadFlowAI
    https://yomie-commits.github.io/LeadFlowAI/

Not part of the product family (kept as is until its role is decided):
automationservices   general automation site  github.com/Yomie-commits/automationservices
    https://yomie-commits.github.io/automationservices/
    └── /app/  AI Executive Assistant demo workspace, used as ExecutiveFlow AI's live demo
```

## How the sites connect

| From | To | Where |
|---|---|---|
| YomieVerse | each product | "Our Products" menu, home page product cards, products.html, footer, pricing.html |
| YomieVerse (old URLs) | ExecutiveFlow / LeadFlow | `executiveflow-ai.html`, `ai-executive-assistant.html` and `leadflow-ai.html` redirect to the product sites; `solutions.html` redirects to `products.html` |
| Each product | YomieVerse | "Part of YomieVerse" bar at the top, "A YomieVerse product" badge and a YomieVerse column in the footer |
| Each product | sister products | Top bar (desktop) and footer |
| ExecutiveFlow AI | automationservices/app/ | "Open the live demo" button |

If a product site's URL ever changes, update it in:
- YomieVerse `build.py` (`SOCIALFLOW_URL`, `EXECUTIVEFLOW_URL`, `LEADFLOW_URL`), then rebuild
- each product's `build.py` → `P["siblings"]`
- SocialFlowAI's `index.html` (the attribution bar and footer)

## Brand system

| Site | Accent | Logo mark |
|---|---|---|
| YomieVerse | Violet `#7c5cff` → teal gradient | "Y" mark |
| SocialFlow AI | Purple `#6D28D9` | Rising-line mark, its own design |
| ExecutiveFlow AI | Teal `#0d9488` | Briefing-list mark |
| LeadFlow AI | Electric blue `#2f64ec` → cyan | Funnel mark |

All the sites share the midnight-navy base, the Plus Jakarta Sans typeface and the same layout system.

ExecutiveFlow AI and LeadFlow AI use a **themed copy** of the YomieVerse stylesheet (`assets/css/site.css`, design system v3). There are no cross-repository file links, so each site deploys and works on its own. When the YomieVerse stylesheet changes in a way the products should get, copy it across and re-apply that product's colour substitutions. They are listed at the top of each product's README.

## What lives where

| Repository | Build | Settings without rebuilding | Enquiries |
|---|---|---|---|
| Yomie-Verse | `python3 build.py` | `assets/js/config.js` | FormSubmit, subject "New YomieVerse enquiry…" |
| ExecutiveFlowAI | `python3 build.py` | `assets/js/config.js` | FormSubmit, subject "New ExecutiveFlow AI enquiry…" |
| LeadFlowAI | `python3 build.py` | `assets/js/config.js` | FormSubmit, subject "New LeadFlow AI enquiry…" |
| SocialFlowAI | none (single `index.html`) | `CONFIG` block at the bottom of `index.html` | WhatsApp or email (no form endpoint set) |

All four sites are hosted on GitHub Pages from the `main` branch, root folder. None of them contains API keys or tokens.
