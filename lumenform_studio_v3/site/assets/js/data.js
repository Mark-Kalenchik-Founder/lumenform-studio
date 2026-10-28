/* Lumen&Form — single source of truth for prices, projects and contacts.
   Read at runtime by main.js (currency switching, contact preselection) and by
   tools/build.py (static, no-JS fallback markup). Keep the object below valid JSON
   (double quotes, no trailing commas) so build.py can parse it. */
window.LF_DATA = {
  "contacts": {
    "personalEmail": "mark@lumenform.studio",
    "studioEmail": "hello@lumenform.studio",
    "linkedin": "https://www.linkedin.com/in/lumenform",
    "facebook": "https://www.facebook.com/MarkKalenchik/",
    "x": "https://x.com/lumenandform",
    "xHandle": "@lumenandform",
    "telegram": "https://t.me/mark_lumenform",
    "telegramHandle": "@mark_lumenform"
  },
  "currencies": [
    { "code": "USD", "label": "USD", "name": "US dollars" },
    { "code": "GBP", "label": "GBP", "name": "British pounds" },
    { "code": "AUD", "label": "AUD", "name": "Australian dollars" }
  ],
  "defaultCurrency": "USD",
  "packages": [
    {
      "id": "one-page",
      "name": "One page",
      "from": false,
      "prices": { "USD": "$290", "GBP": "£290", "AUD": "A$490" },
      "summary": "One landing page or single-page business website.",
      "payment": "Paid after final approval.",
      "features": [
        "One landing page or single-page business website",
        "Contact form",
        "Mobile-first implementation",
        "First-year hosting",
        "One pre-approval revision round",
        "Thirty days of small edits"
      ]
    },
    {
      "id": "business",
      "name": "Business site",
      "from": false,
      "label": "For service businesses",
      "prices": { "USD": "$490", "GBP": "£490", "AUD": "A$790" },
      "summary": "Up to six pages. Typically Home, Services, About, Contact and up to two more.",
      "payment": "Paid after final approval.",
      "features": [
        "Up to six pages",
        "Typical structure: Home, Services, About, Contact and up to two additional pages",
        "Contact forms",
        "Integration of an existing booking tool where agreed",
        "First-year hosting",
        "One pre-approval revision round",
        "Thirty days of small edits"
      ]
    },
    {
      "id": "extended",
      "name": "Extended",
      "from": true,
      "prices": { "USD": "$790", "GBP": "£690", "AUD": "A$1,290" },
      "summary": "Expanded scope: more pages, a small shop, a bilingual site or extra galleries and booking needs.",
      "payment": "30% after homepage approval, balance after final approval.",
      "features": [
        "7–15 pages",
        "A small shop with up to 20 products",
        "A bilingual website",
        "Additional galleries or booking requirements"
      ],
      "featuresNote": "Possible project types, not all included together at the starting price. Scope and final price are agreed before the paid stage begins."
    }
  ],
  "careFromUSD": "US$9/month",
  "agencyFromUSD": "US$100",
  "projects": [
    {
      "id": "mobilenotary",
      "group": "business",
      "name": "Mobile Notary Now",
      "category": "Local services",
      "url": "https://mobilenotarynow-preview-lf.netlify.app/",
      "description": "A service-focused website with local-area pages and clear routes to appointment information.",
      "label": "Independent preview"
    },
    {
      "id": "leading4life",
      "group": "business",
      "name": "Leading4Life",
      "category": "Coaching & speaking",
      "url": "https://leading4life-preview-lf.netlify.app/",
      "description": "A leadership website organizing services, speaking information and call requests.",
      "label": "Independent preview"
    },
    {
      "id": "alexboylan",
      "group": "business",
      "name": "Alex Boylan",
      "category": "Personal brand",
      "url": "https://alexboylan-preview-lf.netlify.app/",
      "description": "A multi-offer personal website connecting speaking, a book, a workshop and coaching.",
      "label": "Independent preview"
    },
    {
      "id": "soulentanglement",
      "group": "business",
      "name": "Soul Entanglement",
      "category": "Music & bookings",
      "url": "https://soulentanglement-preview-lf.netlify.app/",
      "description": "A band website bringing music, show information and a dedicated booking-request interface together.",
      "label": "Independent preview"
    },
    {
      "id": "ashby",
      "group": "fictional",
      "name": "Ashby Renovations",
      "category": "Trades & renovation",
      "url": "https://ashby-preview.netlify.app/",
      "description": "A fictional renovation-business concept focused on services and site-visit enquiries.",
      "label": "Fictional business concept"
    },
    {
      "id": "haldenrowe",
      "group": "fictional",
      "name": "Halden & Rowe Dental",
      "category": "Dental practice",
      "url": "https://haldenrowe-preview.netlify.app/",
      "description": "A fictional dental-practice concept with clear treatment and appointment information.",
      "label": "Fictional business concept"
    },
    {
      "id": "sophia",
      "group": "experimental",
      "name": "Sophia",
      "category": "Product website",
      "url": "https://sophia-preview-lf.netlify.app/",
      "description": "A product-website concept for manufacturing back-office software.",
      "label": "Unofficial product concept"
    },
    {
      "id": "vaultlings",
      "group": "experimental",
      "name": "vaultlings",
      "category": "Editorial concept",
      "url": "https://vaultlings-preview-lf.netlify.app/",
      "description": "An experimental editorial concept for a digital character project.",
      "label": "Unofficial concept"
    }
  ]
};
