# Lumen&Form — studio website (v3, English)

A new, separate version of the studio website for lumenform.studio. It is plain static
HTML, CSS and JavaScript. **There is no build step and no framework.**
The live site and every linked portfolio site were left untouched.

```
site/                    ← DEPLOY THIS FOLDER (publish directory)
  index.html             Home
  work/ pricing/ about/ contact/ thank-you/ privacy/   (each has index.html)
  404.html  robots.txt  sitemap.xml  netlify.toml
  assets/css/styles.css  all styles (tokens at the top)
  assets/js/data.js      ★ prices, projects, contacts — single source of truth
  assets/js/main.js      currency switch, contact preselection, form checks, motion
  assets/fonts/          self-hosted Instrument Serif + Golos Text (SIL OFL, see LICENSE.txt)
  assets/img/work/       real captures of the 8 portfolio sites (desktop + mobile)
  assets/img/og.jpg      Open Graph image (built from a real capture)
tools/build.py           optional page generator (see "Editing content")
tools/og.html            source of og.jpg
handoff/                 real screenshots of the new homepage (desktop + mobile)
```

## 1. Deploy (Netlify)

1. Create a **new** Netlify site (do not overwrite the live one yet).
   Netlify Drop: drag the `site/` folder. Or a repo with base/publish directory `site`, build command empty.
2. **Forms:** Site configuration → Forms → *Enable form detection*, then **redeploy**
   (detection only runs on deploys made after it is enabled).
   The form is named `preview-request`.
3. **Notifications:** Forms → Form notifications → add an email notification to
   `mark@lumenform.studio`. The HTML alone does not send any email.
4. Test the form once on the Netlify URL, then check that the submission appears in the
   Forms dashboard and the email arrives.
5. When approved, attach the domain `lumenform.studio` to this site.

## 2. Contact form

The form posts natively (`method="POST"`, `data-netlify="true"`, hidden `form-name`,
`netlify-honeypot="bot-field"`) to the real page `/thank-you/`. JavaScript only checks
required fields before sending. **It never shows success without a real submission**: the
thank-you page appears only after Netlify accepts the POST. Without JavaScript the browser
`required` attributes still apply.

Submitted fields: `name`, `business`, `website`, `email`, `message`, `package`, `currency`.
Pricing buttons link to `/contact/?package=business&currency=GBP#enquiry`; the form shows
the selection, and the visitor can change or clear it.

## 3. Editing content

All prices, projects and contacts are in **`site/assets/js/data.js`**. The browser reads it
for currency switching and form preselection.

The HTML pages also contain the same values as static text (for SEO and no-JS visitors).
After editing `data.js` or the copy, regenerate the pages:

```
python3 tools/build.py      # needs Python 3 only, no packages
```

Copy lives in `tools/build.py` (one function per page). If you would rather edit HTML
directly, that works too; just keep the prices in `data.js` the same.

- Care price stays **US$9/month** in every currency view (on purpose).
- White-label price: `agencyFromUSD` in `data.js` plus the text on the Pricing page.

## 4. Adding a founder photo later

No portrait was supplied, so Home and About use a typographic identity block.
To add a photo:

1. Save `site/assets/img/mark.webp` (portrait 4:5, for example 800×1000).
2. In `tools/build.py`, in `identity_block()`, follow the comment: add
   `<img class="identity__portrait" src="/assets/img/mark.webp" width="800" height="1000" alt="Mark Kalenchik">`
   as the first child and remove `aria-hidden="true"` from the block. Run `build.py`.
   The CSS already handles the cover fit.

## 5. Screenshots and asset permissions

- All 8 project images are **real captures** of the published preview sites, taken
  2026-10-28 with headless Chromium. Desktop: 1440×900 @2x. Mobile: 390×844 @3x,
  mobile emulation. Nothing was generated or retouched. They are resized to WebP only.
- The old archive's captures were not reused: most were of projects that are no longer
  shown, and fresh captures are more accurate.
- **Unconfirmed:** permission to show the four real-business previews (Mobile Notary Now,
  Leading4Life, Alex Boylan, Soul Entanglement) and the photographs and logos visible in
  their screenshots. The same applies to the Sophia and vaultlings concepts. Public
  availability does not grant asset rights. Confirm before launch, or remove items in `data.js`.
- Fonts: Instrument Serif and Golos Text, SIL Open Font License, self-hosted (no Google requests).
- Logo/monogram: taken from the supplied archive.

## 6. Still to confirm (owner)

- **Payment provider and methods.** The site only says *"Payment instructions and invoice
  details are confirmed before you approve."* No badges, logos or payment links are shown.
- Privacy page: no legal entity, address, retention period or jurisdiction is stated,
  because none were supplied. Add them if your situation requires it.
- Permissions for portfolio publication (see 5).
- X profile URL assumed to be `https://x.com/lumenandform` (from the handle).

## 7. Tested vs untested

Tested locally (headless Chromium):
- All 8 pages render. One `<h1>` per page. No broken local links, no `href="#"`.
- External links open in a new tab with `rel="noopener noreferrer"` and a visually hidden
  "(opens in a new tab)" label.
- All 8 portfolio URLs are exact and respond with HTTP 200.
- Currency switching on Home and Pricing (mouse and keyboard arrows) works, with checked
  state and a live announcement. USD is the default. An explicit choice is kept for the
  browser session only, with no geolocation.
- Package CTAs to Contact preselect package and currency. Change and clear both work.
  The Extended staged-payment note appears in the banner.
- Form validation: errors are announced, focus moves to the first invalid field, values are kept.
- No horizontal overflow at 360, 390, 768, 1024 and 1440 px, or at a 200%-zoom equivalent.
- Reduced motion and JavaScript disabled: no hidden content.
- No console errors.

**Not tested:**
- An actual Netlify form submission and notification email. This needs deployment and the
  dashboard setup in section 1.
- Real devices and Safari/Firefox (only Chromium was used).
- Lighthouse or other performance and accessibility audits. No scores are claimed.
- Forms, bookings and checkouts on the portfolio sites were not tested or changed.

## 8. Indexing

Production pages are `index, follow` with canonical URLs on `https://lumenform.studio/`.
`/thank-you/` and `404.html` are `noindex`. `robots.txt` and `sitemap.xml` are included.
There is no staging noindex mode, so this build can be indexed as-is. While it sits on a
temporary `*.netlify.app` URL, the canonicals already point to the production domain.
There are no analytics or tracking pixels, so no cookie banner is needed.

## 9. Launch checklist

- [ ] Review all pages on the Netlify preview URL (phone and desktop).
- [ ] Confirm portfolio publication permissions (section 5).
- [ ] Confirm the payment provider. Wording stays generic until then.
- [ ] Enable form detection, redeploy, and set up email notifications.
- [ ] Send a test enquiry and confirm it arrives. Delete it from the dashboard.
- [ ] Optional: add a founder photo (section 4).
- [ ] Attach `lumenform.studio` to the new site. Check HTTPS and the `www` redirect.
- [ ] Submit `https://lumenform.studio/sitemap.xml` in Google Search Console.
- [ ] Keep the old site's archive in case you need to roll back.
