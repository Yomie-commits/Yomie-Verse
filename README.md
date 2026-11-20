# YomieVerse

The website for YomieVerse, an AI automation and digital solutions brand. It covers three products:

- **SocialFlow AI**, which has its own site: https://yomie-commits.github.io/SocialFlowAI/
- **LeadFlow AI**, offered as a custom setup
- **ExecutiveFlow AI**, offered as a custom setup

Live site: https://yomie-commits.github.io/Yomie-Verse/

## Structure

| Path | What it is |
|---|---|
| `*.html` | Built pages: home, solutions, leadflow-ai, executiveflow-ai, services, how-it-works, pricing, about, contact, privacy, thank-you, 404 |
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
