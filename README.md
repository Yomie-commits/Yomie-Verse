# Naomi Mwangi: main website

The main website for Naomi Mwangi, AI automation specialist. It is written in the first person and is hosted in the `Yomie-Verse` repository (the brand's former name, kept so existing links keep working). It presents three independent products, each with its own website:

- **SocialFlow AI**: https://yomie-commits.github.io/SocialFlowAI/
- **ExecutiveFlow AI**: https://yomie-commits.github.io/ExecutiveFlowAI/
- **LeadFlow AI**: https://yomie-commits.github.io/LeadFlowAI/

See **[ECOSYSTEM.md](ECOSYSTEM.md)** for how the four repositories fit together.

Live site: https://yomie-commits.github.io/Yomie-Verse/

## Structure

| Path | What it is |
|---|---|
| `*.html` | Built pages: home, products, services, how-it-works, pricing (by product), about, contact, privacy, thank-you, 404. `solutions.html`, `leadflow-ai.html`, `executiveflow-ai.html` and `ai-executive-assistant.html` are redirects |
| `build.py` | Generates every page, the sitemap and robots.txt. Page copy, header and footer live here |
| `assets/css/site.css` | Design system: navy, violet and electric blue |
| `assets/js/config.js` | **Settings you can change without rebuilding**: email, WhatsApp, booking link, analytics |
| `assets/js/main.js` | Menu, animations, the enquiry form, analytics events |
| `assets/img/` | Favicon and social share image (`og-image.png`) |

After editing `build.py`, run `python3 build.py` and commit the regenerated HTML. Edits to `config.js` need no rebuild.

## Contact form

The form posts through [FormSubmit](https://formsubmit.co), which is free and needs no account, to the email in `config.js`.

**One-time activation:** the first real submission triggers an "Activate Form" email from FormSubmit. Click the link in it. Until you do, the form shows visitors a friendly WhatsApp and email fallback. To activate early, submit a test enquiry yourself.

## Optional settings (`assets/js/config.js`)

- `bookingUrl`: a Calendly or Google Calendar booking link. When set, a "Pick a time online" button appears on the Contact page.
- `cloudflareAnalyticsToken` or `ga4MeasurementId`: switches on analytics. Cloudflare Web Analytics is free and cookie-free. Clicks on elements with `data-track` are sent as events.

## Placeholders to fill in

- Founder photo: save it as `assets/img/naomi.jpg`, then uncomment the `<img>` line in `build_about()`.
- Privacy notice: add the "last updated" date, and update the analytics section if you turn analytics on.

No testimonials, client logos or results figures are shown, because none have been supplied. Product illustrations are labelled as sample data.
