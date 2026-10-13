import json
import os
import re

with open("uris.json", "r", encoding="utf-8") as f:
    uris = json.load(f)

shield_uri = uris["shield"]
full_uri = uris["full"]

with open("template.html", "r", encoding="utf-8") as f:
    template = f.read()

# 1. ADD CSS FOR REGISTRY PAGE & THREAT BANNER IN CHECK PAGE
registry_css = '''
    /* REGISTRY PAGE STYLES */
    .search-input-group {
      display: flex;
      gap: 10px;
      align-items: stretch;
    }

    .registry-sample-pills {
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      gap: 8px;
      margin-top: 10px;
    }

    .sample-pill-label {
      font-size: 13px;
      font-weight: 700;
      color: var(--text-muted);
    }

    .sample-link-btn {
      background: var(--steel-blue-light);
      border: 1px solid var(--steel-blue-border);
      color: var(--steel-blue);
      padding: 4px 10px;
      border-radius: var(--radius-pill);
      font-size: 13px;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.2s ease;
    }

    .dark .sample-link-btn {
      color: #93c5fd;
    }

    .sample-link-btn:hover {
      background: var(--steel-blue);
      color: #fff;
    }

    .registry-list-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 12px;
    }

    .registry-filter-scroll {
      display: flex;
      gap: 8px;
      overflow-x: auto;
      padding-bottom: 6px;
      margin-bottom: 10px;
      -webkit-overflow-scrolling: touch;
    }

    .filter-pill {
      background: var(--bg-card-subtle);
      border: 1.5px solid var(--border-color);
      color: var(--text-main);
      padding: 7px 14px;
      border-radius: var(--radius-pill);
      font-size: 14px;
      font-weight: 700;
      white-space: nowrap;
      cursor: pointer;
      transition: all 0.2s ease;
    }

    .filter-pill:hover {
      border-color: var(--steel-blue);
    }

    .filter-pill.active {
      background: var(--steel-blue);
      border-color: var(--steel-blue);
      color: #ffffff;
    }

    .registry-threat-card {
      background: var(--bg-card-subtle);
      border: 1.5px solid var(--border-color);
      border-radius: var(--radius-md);
      padding: 14px 16px;
      transition: all 0.2s ease;
    }

    .registry-threat-card:hover {
      border-color: var(--steel-blue);
      box-shadow: var(--shadow-sm);
    }

    .threat-card-top {
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      gap: 10px;
      margin-bottom: 8px;
    }

    .threat-card-title {
      font-size: 17px;
      font-weight: 800;
      color: var(--text-main);
      line-height: 1.35;
    }

    .threat-status-badge {
      font-size: 12px;
      font-weight: 800;
      padding: 3px 8px;
      border-radius: var(--radius-pill);
      text-transform: uppercase;
      letter-spacing: 0.5px;
      flex-shrink: 0;
    }

    .threat-status-active {
      background: var(--verdict-danger);
      color: #ffffff;
    }

    .threat-status-verified {
      background: #dc2626;
      color: #ffffff;
    }

    .threat-status-flagged {
      background: var(--verdict-caution);
      color: #ffffff;
    }

    .threat-card-meta {
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      gap: 10px;
      font-size: 14px;
      color: var(--text-muted);
      margin-top: 6px;
    }

    .threat-reports-count {
      color: var(--verdict-danger);
      font-weight: 800;
      display: flex;
      align-items: center;
      gap: 4px;
    }

    .threat-card-hash {
      font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
      font-size: 11px;
      color: var(--text-muted);
      background: rgba(0, 0, 0, 0.05);
      padding: 4px 8px;
      border-radius: 4px;
      margin-top: 8px;
      word-break: break-all;
    }

    .dark .threat-card-hash {
      background: rgba(255, 255, 255, 0.05);
    }

    .registry-threat-banner {
      background: linear-gradient(135deg, #b91c1c, #991b1b);
      color: #ffffff;
      padding: 14px 16px;
      border-radius: var(--radius-sm);
      margin-bottom: 16px;
      display: flex;
      align-items: center;
      gap: 12px;
      box-shadow: 0 4px 14px rgba(185, 28, 28, 0.35);
      border: 1px solid #ef4444;
      animation: fadeIn 0.3s ease;
    }
'''

if "/* REGISTRY PAGE STYLES */" not in template:
    pos_style_end = template.find("</style>")
    template = template[:pos_style_end] + registry_css + "\n  " + template[pos_style_end:]

# 2. REPLACE PAGE 5 REGISTRY HTML
registry_html = '''      <!-- ============================================== -->
      <!-- PAGE 5: REGISTRY (Reported Scams Threat Center)-->
      <!-- ============================================== -->
      <section id="page-registry" class="page-section">
        <div class="section-header">
          <h1 class="section-title">
            <span>🛡️</span> <span data-i18n="registryPageTitle">Reported Scams Registry</span>
          </h1>
          <p class="section-subtitle" data-i18n="registryPageSub">
            Searchable threat database of suspicious numbers, fraudulent loan apps, and malicious links.
          </p>
        </div>

        <!-- Search / Lookup Card -->
        <div class="ui-card">
          <h3 class="card-title" data-i18n="registrySearchTitle">Check a Number, Link, or App</h3>
          <p class="card-text" style="font-size: 15px; margin-bottom: 12px;" data-i18n="registrySearchDesc">
            Enter any suspicious number or link. BlaxGuard will hash it and verify if other citizens have reported it.
          </p>

          <div class="search-input-group">
            <input type="text" id="registrySearchInput" class="text-input" placeholder="e.g. +91 98312 45890, https://sbi-kyc-update.xyz..." data-i18n-placeholder="registrySearchPlaceholder" autocomplete="off" onkeydown="if(event.key==='Enter') lookupRegistryItem()">
            <button type="button" class="btn btn-primary" id="btnRegistryLookup" style="min-width: 120px;" onclick="lookupRegistryItem()">
              <span>🔍</span> <span data-i18n="btnSearchRegistry">Check</span>
            </button>
          </div>

          <!-- Quick Sample Test Pills -->
          <div class="registry-sample-pills">
            <span class="sample-pill-label" data-i18n="registryTrySamples">Try sample:</span>
            <button type="button" class="sample-link-btn" onclick="tryRegistrySample('+91 98312 45890')">+91 98312 45890</button>
            <button type="button" class="sample-link-btn" onclick="tryRegistrySample('https://sbi-kyc-update.xyz')">sbi-kyc-update.xyz</button>
            <button type="button" class="sample-link-btn" onclick="tryRegistrySample('quickcashrupeeloan')">QuickCash Loan</button>
            <button type="button" class="sample-link-btn" onclick="tryRegistrySample('+91 99999 00000')">Clean Number</button>
          </div>

          <!-- Live Lookup Result Box -->
          <div id="registryLookupResultBox" style="display: none; margin-top: 16px;"></div>
        </div>

        <!-- Filterable Reported Scams Directory Card -->
        <div class="ui-card">
          <div class="registry-list-header">
            <div>
              <h3 class="card-title" data-i18n="registryListTitle">Verified Community Threat Registry</h3>
              <p class="card-text" style="font-size: 14px;" id="registryItemCountLabel">Showing active community threats</p>
            </div>
            <button type="button" class="btn btn-outline" style="min-height: 40px; padding: 6px 14px; font-size: 14px; width: auto;" onclick="renderRegistryList('all')">
              <span>🔄</span> <span data-i18n="btnRefreshRegistry">Refresh</span>
            </button>
          </div>

          <!-- Category Filter Pills -->
          <div class="registry-filter-scroll" id="registryFilterBar">
            <button type="button" class="filter-pill active" data-category="all" onclick="filterRegistryCategory('all')">
              <span data-i18n="filterAll">All Threats</span>
            </button>
            <button type="button" class="filter-pill" data-category="loan_app" onclick="filterRegistryCategory('loan_app')">
              <span data-i18n="filterLoan">Loan Apps</span>
            </button>
            <button type="button" class="filter-pill" data-category="phishing_link" onclick="filterRegistryCategory('phishing_link')">
              <span data-i18n="filterLink">Phishing Links</span>
            </button>
            <button type="button" class="filter-pill" data-category="fake_care" onclick="filterRegistryCategory('fake_care')">
              <span data-i18n="filterCare">Customer Care</span>
            </button>
            <button type="button" class="filter-pill" data-category="digital_arrest" onclick="filterRegistryCategory('digital_arrest')">
              <span data-i18n="filterArrest">Digital Arrest</span>
            </button>
            <button type="button" class="filter-pill" data-category="kyc_bill" onclick="filterRegistryCategory('kyc_bill')">
              <span data-i18n="filterBill">Electricity / Bills</span>
            </button>
            <button type="button" class="filter-pill" data-category="job_scam" onclick="filterRegistryCategory('job_scam')">
              <span data-i18n="filterJob">Job Scams</span>
            </button>
          </div>

          <!-- Dynamic Registry Cards Container -->
          <div id="registryCardsContainer" style="margin-top: 14px; display: flex; flex-direction: column; gap: 12px;"></div>
        </div>
      </section>'''

pos_reg_start = template.find('<section id="page-registry"')
pos_learn_start = template.find('<section id="page-learn"')
template = template[:pos_reg_start] + registry_html + "\n\n      " + template[pos_learn_start:]

# 3. UPDATE TRANSLATIONS FOR REGISTRY & CHECK INTEGRATION
en_reg_trans = '''/* Registry Page */
        registryPageTitle: "Reported Scams Registry",
        registryPageSub: "Searchable threat database of suspicious numbers, fraudulent loan apps, and malicious links.",
        registrySearchTitle: "Check a Number, Link, or App",
        registrySearchDesc: "Enter any suspicious number or link. BlaxGuard will hash it and verify if other citizens have reported it.",
        registrySearchPlaceholder: "Enter phone number, link, or app name (e.g. +91 98312 45890)...",
        btnSearchRegistry: "Check",
        registryTrySamples: "Try sample:",
        registryListTitle: "Verified Community Threat Registry",
        registryItemCountLabel: "Showing {count} active community threats",
        btnRefreshRegistry: "Refresh",
        filterAll: "All Threats",
        filterLoan: "Loan Apps",
        filterLink: "Phishing Links",
        filterCare: "Customer Care",
        filterArrest: "Digital Arrest",
        filterBill: "Electricity / Bills",
        filterJob: "Job Scams",
        registryStatusActive: "ACTIVE THREAT",
        registryStatusVerified: "VERIFIED SCAM",
        registryStatusFlagged: "FLAGGED",
        registryReportedBy: "Reported by {count} users",
        registryFirstReported: "First reported:",
        registryNoReportsTitle: "No reports found",
        registryNoReportsDesc: "This number or link has not been reported in the BlaxGuard community registry yet.",
        registryNoReportsTip: "⚠️ Stay cautious! Even unlisted numbers can be fresh scams. Never share OTP or PIN.",
        registryFoundTitle: "Reported by {count} users",
        registryFoundDesc: "🚨 ACTIVE THREAT: This identifier has been reported by multiple citizens in the community registry. Do not interact!",
        registryHashTitle: "SHA-256 Threat Hash:",
        checkRegistryBannerTitle: "COMMUNITY THREAT INTERCEPTED",
        checkRegistryBannerDesc: "Found in BlaxGuard Registry! Reported by {count} users as a {type}.",'''

hi_reg_trans = '''/* Registry Page */
        registryPageTitle: "रिपोर्ट किए गए स्कैम की रजिस्ट्री",
        registryPageSub: "संदिग्ध फोन नंबरों, अवैध लोन ऐप्स और फर्जी लिंक का खोज योग्य डेटाबेस।",
        registrySearchTitle: "नंबर, लिंक या ऐप की जांच करें",
        registrySearchDesc: "कोई भी संदिग्ध नंबर या लिंक दर्ज करें। BlaxGuard इसका हैश बनाकर जांचेगा कि क्या अन्य नागरिकों ने इसकी रिपोर्ट की है।",
        registrySearchPlaceholder: "फोन नंबर, लिंक या ऐप दर्ज करें (उदा. +91 98312 45890)...",
        btnSearchRegistry: "जांचें",
        registryTrySamples: "नमूना जांचें:",
        registryListTitle: "सत्यापित सामुदायिक खतरा रजिस्ट्री",
        registryItemCountLabel: "{count} सक्रिय खतरे प्रदर्शित",
        btnRefreshRegistry: "रीफ्रेश",
        filterAll: "सभी खतरे",
        filterLoan: "लोन ऐप्स",
        filterLink: "फर्जी लिंक",
        filterCare: "कस्टमर केयर",
        filterArrest: "डिजिटल अरेस्ट",
        filterBill: "बिजली बिल / KYC",
        filterJob: "फर्जी नौकरी",
        registryStatusActive: "सक्रिय खतरा",
        registryStatusVerified: "सत्यापित स्कैम",
        registryStatusFlagged: "चिह्नित खतरा",
        registryReportedBy: "{count} नागरिकों द्वारा रिपोर्टेड",
        registryFirstReported: "प्रथम रिपोर्ट:",
        registryNoReportsTitle: "कोई रिपोर्ट नहीं मिली",
        registryNoReportsDesc: "यह नंबर या लिंक अभी तक BlaxGuard रजिस्ट्री में रिपोर्ट नहीं किया गया है।",
        registryNoReportsTip: "⚠️ सतर्क रहें! नए नंबर भी धोखाधड़ी हो सकते हैं। कभी भी ओटीपी या पिन साझा न करें।",
        registryFoundTitle: "{count} उपयोगकर्ताओं द्वारा रिपोर्टेड",
        registryFoundDesc: "🚨 सक्रिय खतरा: इस पहचानकर्ता को कई नागरिकों द्वारा रिपोर्ट किया गया है। कोई बातचीत न करें!",
        registryHashTitle: "SHA-256 हैश:",
        checkRegistryBannerTitle: "सामुदायिक रजिस्ट्री में दर्ज खतरा पकड़ा गया",
        checkRegistryBannerDesc: "BlaxGuard रजिस्ट्री में मिला! {count} नागरिकों द्वारा {type} के रूप में रिपोर्ट किया गया है।",'''

te_reg_trans = '''/* Registry Page */
        registryPageTitle: "రిపోర్ట్ చేయబడిన స్కామ్‌ల రిజిస్ట్రీ",
        registryPageSub: "అనుమానాస్పద ఫోన్ నంబర్లు, లోన్ యాప్‌లు మరియు ఫిషింగ్ లింక్‌ల శోధించదగిన డేటాబేస్.",
        registrySearchTitle: "నంబర్, లింక్ లేదా యాప్‌ను తనిఖీ చేయండి",
        registrySearchDesc: "అనుమానాస్పద నంబర్ లేదా లింక్ నమోదు చేయండి. BlaxGuard దీనిని హ్యాష్ చేసి ఇతర పౌరులు రిపోర్ట్ చేశారో లేదో చూస్తుంది.",
        registrySearchPlaceholder: "ఫోన్ నంబర్, లింక్ లేదా యాప్ పేరు రాయండి (ఉదా. +91 98312 45890)...",
        btnSearchRegistry: "తనిఖీ చేయండి",
        registryTrySamples: "నమూనా ప్రయత్నించండి:",
        registryListTitle: "ధృవీకరించబడిన ప్రజా రక్షణ రిజిస్ట్రీ",
        registryItemCountLabel: "{count} క్రియాశీల బెదిరింపులు చూపబడుతున్నాయి",
        btnRefreshRegistry: "రిఫ్రెష్",
        filterAll: "అన్ని బెదిరింపులు",
        filterLoan: "లోన్ యాప్‌లు",
        filterLink: "ఫిషింగ్ లింకులు",
        filterCare: "కస్టమర్ కేర్",
        filterArrest: "డిజిటల్ అరెస్ట్",
        filterBill: "విద్యుత్ / KYC",
        filterJob: "జాబ్ స్కామ్‌లు",
        registryStatusActive: "యాక్టివ్ ప్రమాదం",
        registryStatusVerified: "ధృవీకరించిన స్కామ్",
        registryStatusFlagged: "గుర్తించిన ముప్పు",
        registryReportedBy: "{count} మంది వినియోగదారులచే రిపోర్ట్ చేయబడింది",
        registryFirstReported: "మొదట నివేదించిన తేదీ:",
        registryNoReportsTitle: "ఎలాంటి నివేదికలు లేవు",
        registryNoReportsDesc: "ఈ నంబర్ లేదా లింక్ ఇంకా BlaxGuard రిజిస్ట్రీలో నివేదించబడలేదు.",
        registryNoReportsTip: "⚠️ జాగ్రత్తగా ఉండండి! కొత్త నంబర్లు కూడా మోసాలు కావచ్చు. ఎప్పుడూ OTP లేదా పిన్ చెప్పకండి.",
        registryFoundTitle: "{count} మంది వినియోగదారులచే రిపోర్ట్ చేయబడింది",
        registryFoundDesc: "🚨 యాక్టివ్ ప్రమాదం: ఈ వివరాలను అనేక మంది పౌరులు రిపోర్ట్ చేశారు. ఎలాంటి లావాదేవీలు చేయవద్దు!",
        registryHashTitle: "SHA-256 క్రిప్టోగ్రాఫిక్ హ్యాష్:",
        checkRegistryBannerTitle: "కమ్యూనిటీ రిజిస్ట్రీలో ముప్పు గుర్తించబడింది",
        checkRegistryBannerDesc: "BlaxGuard రిజిస్ట్రీలో దొరికింది! {count} మంది పౌరులచే {type}గా రిపోర్ట్ చేయబడింది.",'''

# Replace EN registry translation
idx_en_reg = template.find('/* Registry Page */')
idx_en_learn = template.find('/* Learn Page */', idx_en_reg)
template = template[:idx_en_reg] + en_reg_trans + "\n\n        " + template[idx_en_learn:]

# Replace HI registry translation
idx_hi_reg = template.find('registryPageTitle:')
idx_hi_learn = template.find('learnPageTitle:', idx_hi_reg)
template = template[:idx_hi_reg] + hi_reg_trans + "\n\n        " + template[idx_hi_learn:]

# Replace TE registry translation
idx_te_reg = template.find('registryPageTitle:', idx_hi_learn)
idx_te_learn = template.find('learnPageTitle:', idx_te_reg)
template = template[:idx_te_reg] + te_reg_trans + "\n\n        " + template[idx_te_learn:]

# 4. ADD registryMatched REASON TRANSLATION IN ruleReasonTranslations
rule_reg_add = '''    registryMatched: {
      en: "🚨 MATCHED IN BLAXGUARD REGISTRY: This phone number or link has already been reported by multiple citizens in the community database.",
      hi: "🚨 BlaxGuard रजिस्ट्री में दर्ज: यह नंबर या लिंक पहले ही कई नागरिकों द्वारा सामुदायिक डेटाबेस में रिपोर्ट किया जा चुका है।",
      te: "🚨 BlaxGuard రిజిస్ట్రీలో మ్యాచ్ అయ్యింది: ఈ నంబర్ లేదా లింక్ ఇప్పటికే ప్రజా డేటాబేస్‌లో అనేక మంది పౌరులచే రిపోర్ట్ చేయబడింది."
    },
'''

if "registryMatched:" not in template:
    template = template.replace(
        "const ruleReasonTranslations = {",
        "const ruleReasonTranslations = {\n  " + rule_reg_add
    )

# 5. ENHANCE BlaxGuardDataLayer WITH ENRICHED SEED DATA & QUERY METHODS
new_datalayer_js = '''    var BlaxGuardDataLayer = (function() {
      // In-memory threat database: stores ONLY hashes and metadata counters
      // Map<string, { hash: string, count: number, scamType: string, date: string, firstReported: string, status: string, display: string, timestamp: string }>
      const _memoryStore = new Map();

      // Normalize identifier according to requirement:
      // lowercase, strip spaces, remove +91
      function normalize(identifier) {
        if (!identifier) return "";
        let clean = String(identifier).trim().toLowerCase();
        // Strip all whitespace characters
        clean = clean.replace(/\\s+/g, "");
        // Remove leading +91
        if (clean.startsWith("+91")) {
          clean = clean.slice(3);
        }
        return clean;
      }

      // Compute SHA-256 hash using Web Crypto API
      async function hashSha256(normalizedStr) {
        if (typeof window !== "undefined" && window.crypto && window.crypto.subtle) {
          const encoder = new TextEncoder();
          const data = encoder.encode(normalizedStr);
          const hashBuffer = await window.crypto.subtle.digest("SHA-256", data);
          const hashArray = Array.from(new Uint8Array(hashBuffer));
          return hashArray.map(b => b.toString(16).padStart(2, "0")).join("");
        }
        // Fallback for environments lacking subtle crypto
        let h = 0;
        for (let i = 0; i < normalizedStr.length; i++) {
          h = ((h << 5) - h) + normalizedStr.charCodeAt(i);
          h |= 0;
        }
        return "sha256_" + Math.abs(h).toString(16).padStart(16, "0");
      }

      // Enriched seed data for community threat intelligence demo
      const _demoSeeds = [
        { raw: "9831245890", type: "fake_care", count: 14, date: "2026-10-01", status: "active", display: "+91 98312 45890 (Fake SBI Support)" },
        { raw: "https://sbi-kyc-update.xyz", type: "phishing_link", count: 29, date: "2026-10-02", status: "verified", display: "sbi-kyc-update.xyz (Phishing Portal)" },
        { raw: "quickcashrupeeloan", type: "loan_app", count: 42, date: "2026-09-28", status: "active", display: "QuickCash Rupee Loan (Harassment APK)" },
        { raw: "http://bill-tsspdcl-pay.site", type: "kyc_bill", count: 19, date: "2026-10-03", status: "flagged", display: "bill-tsspdcl-pay.site (Power Cut Bait)" },
        { raw: "9820019283", type: "digital_arrest", count: 8, date: "2026-10-04", status: "active", display: "+91 98200 19283 (Police/CBI Impersonator)" },
        { raw: "https://telegram-youtube-like.top", type: "job_scam", count: 33, date: "2026-10-02", status: "verified", display: "telegram-youtube-like.top (Task Scam)" },
        { raw: "9940128472", type: "lottery_parcel", count: 11, date: "2026-10-05", status: "flagged", display: "+91 99401 28472 (Customs Parcel Scam)" },
        { raw: "fastcreditrupee", type: "loan_app", count: 56, date: "2026-09-25", status: "active", display: "FastCredit Rupee Harassment APK" }
      ];

      async function _initSeeds() {
        for (const item of _demoSeeds) {
          try {
            const norm = normalize(item.raw);
            const h = await hashSha256(norm);
            _memoryStore.set(h, {
              hash: h,
              count: item.count,
              scamType: item.type,
              firstReported: item.date,
              date: item.date,
              status: item.status,
              display: item.display,
              timestamp: new Date().toISOString()
            });
          } catch(e) {}
        }
      }

      _initSeeds();

      return {
        normalizeIdentifier(raw) {
          return normalize(raw);
        },

        async hashIdentifier(normalized) {
          return hashSha256(normalized);
        },

        /**
         * Search by raw phone number, link, or keyword
         */
        async searchByIdentifier(raw) {
          const norm = normalize(raw);
          if (!norm) return null;
          const hash = await hashSha256(norm);
          return _memoryStore.get(hash) || null;
        },

        /**
         * Submit a scam report.
         * STRICT PRIVACY GUARANTEE:
         * - Raw input and message descriptions are NEVER stored in memory or persistence.
         * - STORES ONLY: SHA-256 hash, counter, category, optional date.
         */
        async recordReport({ rawIdentifier, scamType, incidentDate }) {
          const normalized = normalize(rawIdentifier);
          if (!normalized) {
            throw new Error("EMPTY_IDENTIFIER");
          }

          const hash = await hashSha256(normalized);
          const existing = _memoryStore.get(hash);
          const newCount = (existing ? existing.count : 0) + 1;

          const record = {
            hash: hash,
            count: newCount,
            scamType: scamType || "other",
            firstReported: existing ? existing.firstReported : (incidentDate || new Date().toISOString().split("T")[0]),
            date: incidentDate || new Date().toISOString().split("T")[0],
            status: existing ? (existing.count >= 20 ? "verified" : "active") : "flagged",
            display: existing ? existing.display : (scamType === "loan_app" ? "Reported Loan App" : (scamType === "phishing_link" ? "Reported Phishing Link" : "Reported Number/Contact")),
            timestamp: new Date().toISOString()
          };

          _memoryStore.set(hash, record);

          return {
            success: true,
            hash: hash,
            count: newCount,
            scamType: record.scamType,
            incidentDate: record.date
          };
        },

        getReport(hash) {
          return _memoryStore.get(hash) || null;
        },

        getReportCount(hash) {
          const entry = _memoryStore.get(hash);
          return entry ? entry.count : 0;
        },

        getAllReports() {
          return Array.from(_memoryStore.values());
        },

        getSummaryStats() {
          let total = 0;
          _memoryStore.forEach(e => total += e.count);
          return {
            uniqueHashes: _memoryStore.size,
            totalReports: total
          };
        }
      };
    })();
    if (typeof window !== 'undefined') window.BlaxGuardDataLayer = BlaxGuardDataLayer;'''

# Replace old BlaxGuardDataLayer
pos_dl_start = template.find('var BlaxGuardDataLayer = (function() {')
pos_dl_end = template.find('/* REPORT FORM SUBMISSION CONTROLLER */', pos_dl_start)
template = template[:pos_dl_start] + new_datalayer_js + "\n\n    " + template[pos_dl_end:]

# 6. ENHANCE evaluateTextSafety AND renderVerdictUI AND runRuleEngine
enhanced_eval_js = '''/* HEURISTIC RULE ENGINE (0-100) WITH REGISTRY INTEGRATION */
    async function evaluateTextSafety(rawText) {
      const text = (rawText || "").trim();
      const lower = text.toLowerCase();

      let score = 0;
      const matchedRules = [];
      let matchedRegistryEntry = null;

      // 1. LOOKUP CANDIDATE IDENTIFIERS IN BLAXGUARD REGISTRY
      // Extract links, phone numbers, and domains from scanned message
      if (typeof BlaxGuardDataLayer !== "undefined") {
        const candidates = [];
        
        // URLs
        const urlMatches = text.match(/https?:\\/\\/[^\\s]+/gi) || [];
        urlMatches.forEach(u => candidates.push(u));

        // Phone numbers (10 digits with or without +91)
        const phoneMatches = text.match(/(?:\\+?91[\\-\\s]?)?([6-9]\\d{9})\\b/g) || [];
        phoneMatches.forEach(p => candidates.push(p));

        // Risky domains without protocol
        const domainMatches = text.match(/\\b([a-zA-Z0-9\\-]+\\.(?:xyz|top|site|online|live|cam|loan|guru|cf|tk|ml))\\b/gi) || [];
        domainMatches.forEach(d => candidates.push(d));

        // If the whole input is short, test it directly as an identifier
        if (text.length <= 80) {
          candidates.push(text);
        }

        // Test each candidate against BlaxGuardDataLayer
        for (const cand of candidates) {
          const entry = await BlaxGuardDataLayer.searchByIdentifier(cand);
          if (entry) {
            matchedRegistryEntry = entry;
            break;
          }
        }
      }

      // Check standard heuristic rules
      const urgencyRegex = /\\b(immediately|urgent|urgently|within 24 hours|within 2 hours|within \\d+ hours|tonight|today only|last chance|at 9:30 pm|at 9 pm|before 9 pm|expire in \\d+|hurry|action required|suspended today|disconnected tonight|cut tonight|block today|account suspended)\\b/i;
      if (urgencyRegex.test(lower)) {
        score += 20;
        matchedRules.push("urgency");
      }

      const otpRegex = /\\b(otp|upi pin|4-digit pin|6-digit pin|share pin|enter pin|provide otp|send otp|verify otp|share code|enter upi|password)\\b/i;
      if (otpRegex.test(lower)) {
        score += 35;
        matchedRules.push("otpPin");
      }

      const kycRegex = /\\b(kyc expired|update kyc|kyc pending|pan aadhaar link|pan blocked|pan card block|account blocked|kyc verification|sim kyc|aadhaar update|kyc suspension)\\b/i;
      if (kycRegex.test(lower)) {
        score += 25;
        matchedRules.push("kycExpiry");
      }

      const prizeRegex = /\\b(congratulations|you won|won lottery|lucky draw|kbc|cashback of rs|prize money|reward points|claim ₹|claim rs|gift voucher|winner draw)\\b/i;
      if (prizeRegex.test(lower)) {
        score += 25;
        matchedRules.push("prizes");
      }

      const feeRegex = /\\b(processing fee|registration fee|refundable fee|pay deposit|advance payment|pay ₹\\d+|pay rs \\d+ to claim|security deposit|transfer fee)\\b/i;
      if (feeRegex.test(lower)) {
        score += 25;
        matchedRules.push("advanceFee");
      }

      const loanRegex = /\\b(pre-approved loan|instant loan|instant cash|no cibil|without cibil|loan in 5 mins|0% interest loan|instant ₹|instant rs|quick cash loan)\\b/i;
      if (loanRegex.test(lower)) {
        score += 25;
        matchedRules.push("loanBait");
      }

      const remoteApkRegex = /(\\.apk|\\.apk\\.zip|download apk|download app|install app to update|anydesk|teamviewer|rustdesk|quicksupport|screen share|alpemix|airmirror)/i;
      if (remoteApkRegex.test(lower)) {
        score += 35;
        matchedRules.push("remoteApk");
      }

      const careKeyword = /(customer care|helpline|support|helpdesk|call us at|toll free|contact)/i.test(lower);
      const mobileNumberMatch = /(?:\\+?91[\\-\\s]?)?([6-9]\\d{9})\\b/.exec(lower);
      const isOfficialHelpline = /\\b(1800\\d{4,8}|1912|1930|112)\\b/.test(lower);

      if (careKeyword && mobileNumberMatch && !isOfficialHelpline) {
        score += 25;
        matchedRules.push("fakeCareNum");
      } else if (!careKeyword && mobileNumberMatch && text.length <= 15) {
        score += 15;
        matchedRules.push("fakeCareNum");
      }

      const shortLinkRegex = /(bit\\.ly|tinyurl\\.com|t\\.co|is\\.gd|cutt\\.ly|rb\\.gy|shorturl\\.at|ow\\.ly|buff\\.ly|goo\\.gl)/i;
      if (shortLinkRegex.test(lower)) {
        score += 20;
        matchedRules.push("shortLink");
      }

      const riskyTldRegex = /\\.(xyz|top|online|club|buzz|work|live|loan|vip|icu|tk|ml|ga|cf|gq|site|space|guru|cam|rest)(?:[\\/\\?\\s]|$)/i;
      const rawIpRegex = /https?:\\/\\/\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}/i;
      if (riskyTldRegex.test(lower) || rawIpRegex.test(lower)) {
        score += 25;
        matchedRules.push("riskyTld");
      }

      const httpRegex = /http:\\/\\/[a-z0-9\\-\\._~:\\/\\?#\\[\\]@!\\$&'\\(\\)\\*\\+,;=]+/i;
      if (httpRegex.test(text) && !text.includes("https://")) {
        score += 15;
        matchedRules.push("missingHttps");
      }

      const brandKeywords = /(sbi|hdfc|icici|axis|pnb|rbi|gov|pmkisan|epfo|discom|electricity|bescom|bsnl|jio|airtel|incometax)/i;
      const genuineDomains = [
        "onlinesbi.sbi", "sbi.co.in", "hdfcbank.com", "icicibank.com", "axisbank.com",
        "pnbindia.in", "rbi.org.in", "cybercrime.gov.in", "gov.in", "nic.in",
        "pmkisan.gov.in", "epfindia.gov.in", "incometax.gov.in", "jio.com", "airtel.in", "bsnl.co.in"
      ];

      const urlMatches = text.match(/https?:\\/\\/[^\\s]+/gi) || [];
      let isSpoofed = false;
      let hasGenuineWhitelist = false;

      for (let u of urlMatches) {
        try {
          const urlObj = new URL(u);
          const hostname = urlObj.hostname.toLowerCase();
          const isOfficial = genuineDomains.some(d => hostname === d || hostname.endsWith("." + d));

          if (isOfficial) {
            hasGenuineWhitelist = true;
          } else if (brandKeywords.test(hostname)) {
            isSpoofed = true;
          }
        } catch (e) {
          if (brandKeywords.test(u) && !genuineDomains.some(d => u.toLowerCase().includes(d))) {
            isSpoofed = true;
          }
        }
      }

      if (isSpoofed) {
        score += 35;
        matchedRules.push("brandSpoof");
      }

      if (hasGenuineWhitelist && score <= 20) {
        score = 0;
      }

      // IF MATCHED IN REGISTRY: SUBSTANTIALLY RAISE RISK SCORE (Immediate Danger)
      if (matchedRegistryEntry) {
        score = Math.min(100, Math.max(score + 45, 80));
        matchedRules.unshift("registryMatched");
      }

      let finalScore = Math.min(100, Math.max(0, score));

      let verdict = "safe";
      if (finalScore >= 60 || matchedRegistryEntry) {
        verdict = "danger";
      } else if (finalScore >= 25) {
        verdict = "caution";
      } else {
        verdict = "safe";
      }

      if (matchedRules.length === 0) {
        matchedRules.push("cleanText");
      }

      return {
        score: finalScore,
        verdict: verdict,
        matchedRules: matchedRules,
        rawText: text,
        matchedRegistry: matchedRegistryEntry
      };
    }

    function renderVerdictUI(data) {
      const container = document.getElementById("checkVerdictContainer");
      if (!container) return;

      const dict = translations[currentLang] || translations.en;
      const isDanger = data.verdict === "danger";
      const isCaution = data.verdict === "caution";
      const isSafe = data.verdict === "safe";

      let verdictClass = isDanger ? "verdict-danger" : (isCaution ? "verdict-caution" : "verdict-safe");
      let verdictBadgeText = isDanger ? dict.verdictBadgeDanger : (isCaution ? dict.verdictBadgeCaution : dict.verdictBadgeSafe);
      let verdictTitleText = isDanger ? dict.verdictTitleDanger : (isCaution ? dict.verdictTitleCaution : dict.verdictTitleSafe);

      let reasonsHtml = "";
      data.matchedRules.forEach(ruleKey => {
        if (ruleKey === "registryMatched" && data.matchedRegistry) {
          const typeName = getScamTypeName(data.matchedRegistry.scamType);
          let reasonText = "";
          if (currentLang === "hi") {
            reasonText = `🚨 BlaxGuard रजिस्ट्री में दर्ज: यह नंबर/लिंक ${data.matchedRegistry.count} नागरिकों द्वारा ${typeName} के रूप में रिपोर्ट किया जा चुका है।`;
          } else if (currentLang === "te") {
            reasonText = `🚨 BlaxGuard రిజిస్ట్రీలో మ్యాచ్ అయ్యింది: ఈ నంబర్/లింక్ ఇప్పటికే ${data.matchedRegistry.count} మంది పౌరులచే ${typeName}గా రిపోర్ట్ చేయబడింది.`;
          } else {
            reasonText = `🚨 MATCHED IN BLAXGUARD REGISTRY: This phone number or link has already been reported by ${data.matchedRegistry.count} citizens as a ${typeName}!`;
          }
          reasonsHtml += `<li style="font-weight: 700; color: var(--verdict-danger);">${reasonText}</li>`;
        } else {
          const trans = ruleReasonTranslations[ruleKey];
          const reasonText = (trans && trans[currentLang]) ? trans[currentLang] : (trans ? trans.en : ruleKey);
          reasonsHtml += `<li>${reasonText}</li>`;
        }
      });

      let registryAlertBannerHtml = "";
      if (data.matchedRegistry) {
        const typeName = getScamTypeName(data.matchedRegistry.scamType);
        registryAlertBannerHtml = `
          <div class="registry-threat-banner">
            <span style="font-size: 26px;">🚨</span>
            <div>
              <div style="font-weight: 800; font-size: 15px;">${dict.checkRegistryBannerTitle || "COMMUNITY THREAT INTERCEPTED"}</div>
              <div style="font-size: 13.5px; opacity: 0.95; margin-top: 2px;">
                ${(dict.checkRegistryBannerDesc || "Found in BlaxGuard Registry! Reported by {count} users as a {type}.").replace("{count}", data.matchedRegistry.count).replace("{type}", typeName)}
              </div>
            </div>
          </div>
        `;
      }

      container.style.display = "block";
      container.className = `verdict-box ${verdictClass}`;
      container.innerHTML = `
        ${registryAlertBannerHtml}
        <div class="verdict-header">
          <span class="verdict-badge">${verdictBadgeText}</span>
          <span style="font-size: 24px;">${isDanger ? "⚠️" : (isCaution ? "🔍" : "✅")}</span>
        </div>

        <div class="verdict-title">${verdictTitleText}</div>

        <div class="score-meter-wrap">
          <div class="score-text-label">
            <span>${dict.riskScoreLabel}:</span>
            <span style="font-size: 19px;">${data.score} / 100</span>
          </div>
          <div class="score-bar-bg">
            <div class="score-fill" style="width: ${Math.max(5, data.score)}%;"></div>
          </div>
        </div>

        <div class="reasons-box">
          <div class="reasons-title">
            <span>📋</span> <span>${dict.reasonsTitle}</span>
          </div>
          <ul class="reasons-list">
            ${reasonsHtml}
          </ul>
        </div>

        <div class="next-steps-card">
          <div class="next-steps-header">
            <span>🛡️</span> <span>${dict.nextStepsTitle}</span>
          </div>
          <ul class="next-steps-list">
            <li>
              <span class="step-badge">1</span>
              <div>${dict.stepBlock}</div>
            </li>
            <li>
              <span class="step-badge">2</span>
              <div>${dict.stepCallBank}</div>
            </li>
            <li>
              <span class="step-badge">3</span>
              <div>${dict.stepCall1930}</div>
            </li>
            <li>
              <span class="step-badge">4</span>
              <div>${dict.stepCyberCrime}</div>
            </li>
          </ul>
        </div>

        <button class="senior-voice-btn" onclick="speakRuleEngineAlert()">
          <span>🔊</span> <span>${dict.btnListenAlert}</span>
        </button>

        <div class="disclaimer-text">
          ${dict.disclaimerText}
        </div>
      `;
    }

    async function runRuleEngine() {
      const input = document.getElementById("checkMessageInput");
      const val = input ? input.value.trim() : "";

      if (!val) {
        const alertMsg = currentLang === "hi" 
          ? "कृपया पहले कोई संदेश, लिंक या फोन नंबर दर्ज करें" 
          : (currentLang === "te" 
            ? "దయచేసి ముందుగా సందేశం, లింక్ లేదా ఫోన్ నంబర్ నమోదు చేయండి" 
            : "Please paste a message, link, or phone number first");
        alert(alertMsg);
        return;
      }

      const scanBtn = document.getElementById("btnRunCheck");
      if (scanBtn) {
        scanBtn.disabled = true;
      }

      try {
        const result = await evaluateTextSafety(val);
        lastAnalysisData = result;
        renderVerdictUI(result);

        const container = document.getElementById("checkVerdictContainer");
        if (container) {
          container.scrollIntoView({ behavior: "smooth", block: "nearest" });
        }
      } finally {
        if (scanBtn) {
          scanBtn.disabled = false;
        }
      }
    }'''

pos_old_eval = template.find('function evaluateTextSafety(rawText)')
pos_old_clear = template.find('function clearCheckInput()')
template = template[:pos_old_eval] + enhanced_eval_js + "\n\n    " + template[pos_old_clear:]

# 7. ADD REGISTRY CONTROLLERS IN JAVASCRIPT
registry_controllers_js = '''    /* REGISTRY PAGE CONTROLLERS */
    let currentRegistryCategory = "all";

    function getRegistryStatusText(statusKey) {
      const dict = translations[currentLang] || translations.en;
      if (statusKey === "verified") return dict.registryStatusVerified || "VERIFIED SCAM";
      if (statusKey === "flagged") return dict.registryStatusFlagged || "FLAGGED";
      return dict.registryStatusActive || "ACTIVE THREAT";
    }

    async function lookupRegistryItem() {
      const input = document.getElementById("registrySearchInput");
      const raw = input ? input.value.trim() : "";
      const resultBox = document.getElementById("registryLookupResultBox");
      if (!resultBox) return;

      if (!raw) {
        const alertMsg = currentLang === "hi" 
          ? "कृपया पहले फोन नंबर या लिंक दर्ज करें" 
          : (currentLang === "te" 
            ? "దయచేసి ముందుగా ఫోన్ నంబర్ లేదా లింక్ నమోదు చేయండి" 
            : "Please enter a phone number or link to search");
        alert(alertMsg);
        if (input) input.focus();
        return;
      }

      const dict = translations[currentLang] || translations.en;
      resultBox.style.display = "block";
      resultBox.innerHTML = `
        <div style="text-align: center; padding: 12px; color: var(--text-muted); font-size: 15px;">
          <span>⏳</span> <span>Hashing and querying BlaxGuard Registry...</span>
        </div>
      `;

      try {
        const entry = await BlaxGuardDataLayer.searchByIdentifier(raw);
        const norm = BlaxGuardDataLayer.normalizeIdentifier(raw);
        const hash = await BlaxGuardDataLayer.hashIdentifier(norm);

        if (entry) {
          const typeName = getScamTypeName(entry.scamType);
          const statusClass = entry.status === "verified" ? "threat-status-verified" : (entry.status === "active" ? "threat-status-active" : "threat-status-flagged");
          const statusText = getRegistryStatusText(entry.status);
          const reportedText = (dict.registryFoundTitle || "Reported by {count} users").replace("{count}", entry.count);

          resultBox.innerHTML = `
            <div class="verdict-box verdict-danger" style="margin: 0;">
              <div class="verdict-header">
                <span class="verdict-badge">⚠️ ${reportedText}</span>
                <span class="threat-status-badge ${statusClass}">${statusText}</span>
              </div>
              <div class="verdict-title" style="margin-top: 8px;">
                🚨 ${reportedText}
              </div>
              <p class="verdict-desc" style="margin-bottom: 12px;">
                ${dict.registryFoundDesc || "ACTIVE THREAT: This identifier has been reported by multiple citizens in the community registry. Do not interact!"}
              </p>
              <div style="font-size: 14px; background: rgba(0,0,0,0.15); padding: 10px 14px; border-radius: var(--radius-sm); display: flex; flex-direction: column; gap: 4px;">
                <div><strong>Category:</strong> ${typeName}</div>
                <div><strong>First Reported:</strong> ${entry.firstReported || entry.date || "Recent"}</div>
                <div><strong>SHA-256 Threat Hash:</strong> <code style="font-size: 11px; word-break: break-all;">${hash}</code></div>
              </div>
            </div>
          `;
        } else {
          resultBox.innerHTML = `
            <div class="verdict-box verdict-safe" style="margin: 0;">
              <div class="verdict-header">
                <span class="verdict-badge">🟢 ${dict.registryNoReportsTitle || "No reports found"}</span>
              </div>
              <div class="verdict-title" style="margin-top: 8px;">
                ✅ ${dict.registryNoReportsTitle || "No reports found"}
              </div>
              <p class="verdict-desc">
                ${dict.registryNoReportsDesc || "This number or link has not been reported in the BlaxGuard community registry yet."}
              </p>
              <div style="font-size: 13.5px; color: var(--text-muted); margin-top: 8px;">
                ${dict.registryNoReportsTip || "⚠️ Stay cautious! Even unlisted numbers can be fresh scams. Never share OTP or PIN."}
              </div>
            </div>
          `;
        }
      } catch (err) {
        console.error("Registry lookup error:", err);
      }
    }

    function tryRegistrySample(sampleText) {
      const input = document.getElementById("registrySearchInput");
      if (input) {
        input.value = sampleText;
        lookupRegistryItem();
      }
    }

    function filterRegistryCategory(category) {
      currentRegistryCategory = category;

      // Update active pill
      const pills = document.querySelectorAll("#registryFilterBar .filter-pill");
      pills.forEach(p => {
        if (p.getAttribute("data-category") === category) {
          p.classList.add("active");
        } else {
          p.classList.remove("active");
        }
      });

      renderRegistryList(category);
    }

    function renderRegistryList(category = currentRegistryCategory) {
      const container = document.getElementById("registryCardsContainer");
      const countLabel = document.getElementById("registryItemCountLabel");
      if (!container) return;

      const allRecords = BlaxGuardDataLayer.getAllReports();
      const dict = translations[currentLang] || translations.en;

      let filtered = allRecords;
      if (category && category !== 'all') {
        filtered = allRecords.filter(r => r.scamType === category);
      }

      if (countLabel) {
        countLabel.textContent = (dict.registryItemCountLabel || "Showing {count} active community threats").replace("{count}", filtered.length);
      }

      if (filtered.length === 0) {
        container.innerHTML = `
          <div style="text-align: center; padding: 24px; color: var(--text-muted); font-size: 15px;">
            ${dict.registryNoReportsTitle || "No reports found in this category"}
          </div>
        `;
        return;
      }

      let html = "";
      filtered.forEach(item => {
        const typeName = getScamTypeName(item.scamType);
        const statusClass = item.status === "verified" ? "threat-status-verified" : (item.status === "active" ? "threat-status-active" : "threat-status-flagged");
        const statusText = getRegistryStatusText(item.status);
        const reportedText = (dict.registryReportedBy || "Reported by {count} users").replace("{count}", item.count);
        const displayTitle = item.display || typeName;

        html += `
          <div class="registry-threat-card" data-category="${item.scamType}">
            <div class="threat-card-top">
              <div class="threat-card-title">${displayTitle}</div>
              <span class="threat-status-badge ${statusClass}">${statusText}</span>
            </div>
            <div class="threat-card-meta">
              <span class="threat-reports-count">
                <span>🚨</span> <strong>${reportedText}</strong>
              </span>
              <span>&bull;</span>
              <span>${dict.registryFirstReported || "First reported:"} ${item.firstReported || item.date || "Recent"}</span>
              <span>&bull;</span>
              <span>${typeName}</span>
            </div>
            <div class="threat-card-hash">
              <span>SHA-256: </span><code>${item.hash.substring(0, 24)}...</code>
            </div>
          </div>
        `;
      });

      container.innerHTML = html;
    }
'''

# Replace old filterRegistry function
pos_old_filt = template.find('function filterRegistry() {')
pos_next_func = template.find('function saveGuardian()', pos_old_filt)
template = template[:pos_old_filt] + registry_controllers_js + "\n\n    " + template[pos_next_func:]

# Make sure renderRegistryList is called in setLanguage and handleRouting
if "renderRegistryList();" not in template:
    template = template.replace(
        "recalculateCallDangerMeter();",
        "recalculateCallDangerMeter();\n      renderRegistryList();"
    )
    template = template.replace(
        'if (targetSection) targetSection.classList.add("active");',
        'if (targetSection) targetSection.classList.add("active");\n      if (route === "registry") renderRegistryList();'
    )

# Save template.html
with open("template.html", "w", encoding="utf-8") as f:
    f.write(template)

# Build index.html
output = template.replace("{{SHIELD_URI}}", shield_uri).replace("{{FULL_URI}}", full_uri)
with open("index.html", "w", encoding="utf-8") as f:
    f.write(output)

print(f"Generated index.html with complete Registry page & Check page connection! File size: {os.path.getsize('index.html')} bytes")
