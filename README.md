# YomieVerse – AI Automation Services website

Static website (HTML, CSS, JavaScript). No build step, no server, no database. It runs on GitHub Pages, Netlify or any static host.

## Pages

| File | Page |
|---|---|
| `index.html` | Home |
| `services.html` | Services (6 service sections) |
| `ai-executive-assistant.html` | Featured product: AI Executive Assistant System |
| `how-it-works.html` | 7-step client journey |
| `pricing.html` | Starter / Professional / Business packages |
| `about.html` | About Naomi Mwangi |
| `contact.html` | Contact & consultation form, WhatsApp, email, LinkedIn |
| `thank-you.html` | Shown after the form is sent |
| `404.html` | Not-found page |

## Where to change things

- **Contact email** (form destination and email links): `assets/js/config.js`
- **WhatsApp number, LinkedIn, site address**: search the HTML files for `wa.me/254792002230`, `linkedin.com/in/naomi-njeri-m` and `yomie-commits.github.io/Yomie-Verse`
- **Colours and fonts**: the `:root` block at the top of `assets/css/styles.css`
- **Your photo**: replace the "NM" circle in `about.html` with `<img src="assets/img/naomi.jpg" alt="Naomi Mwangi">`

## Deploy on GitHub Pages

1. Sign in at github.com and create a new **public** repository named `Yomie-Verse` (leave "Add a README" unticked).
2. On the empty repository page, click **uploading an existing file**. Drag in **everything inside** the `yomieverse` folder: all the `.html` files, `assets`, `sitemap.xml`, `robots.txt`, `README.md` and `.nojekyll`. Then click **Commit changes**.
3. Go to **Settings → Pages**. Under "Build and deployment" choose **Deploy from a branch**, branch **main**, folder **/ (root)**, then **Save**.
4. After 1–2 minutes the site is live at `https://yomie-commits.github.io/Yomie-Verse/`.

If you use a different repository name or a custom domain, replace `https://yomie-commits.github.io/Yomie-Verse/` in the HTML files, `sitemap.xml` and `robots.txt`.

## Activate the contact form (one time)

The form sends submissions to your email through FormSubmit (free, no account).

1. Open the live site's Contact page and send yourself a test enquiry.
2. FormSubmit emails you an activation link. Click it once.
3. From then on, every enquiry arrives in your inbox as a table, and the visitor sees the Thank You page.

Optional: after activation, FormSubmit gives you a random alias. To hide your email address from the page source, set it as the `email` value in `assets/js/config.js`. The code adds it to `https://formsubmit.co/` the same way.

## Deploy on Netlify instead

Go to app.netlify.com/drop and drag the `yomieverse` folder in. The site goes live immediately. The FormSubmit form works there too.

## Submit to Google

After going live, add the site to Google Search Console and submit `sitemap.xml`.
