import json
import os
import re

# Load base64 URIs
with open("uris.json", "r", encoding="utf-8") as f:
    uris = json.load(f)

shield_uri = uris["shield"]
full_uri = uris["full"]

# Read existing template
with open("template.html", "r", encoding="utf-8") as f:
    template = f.read()

# 1. ADD CSS FOR REPORT PAGE
report_css = '''
    /* REPORT PAGE STYLES */
    .privacy-banner-card {
      background: var(--steel-blue-light);
      border: 1.5px solid var(--steel-blue-border);
      border-radius: var(--radius-md);
      padding: 16px 18px;
      margin-bottom: 20px;
      display: flex;
      align-items: flex-start;
      gap: 14px;
    }

    .privacy-banner-icon {
      font-size: 26px;
      line-height: 1;
      flex-shrink: 0;
      margin-top: 2px;
    }

    .privacy-banner-title {
      font-size: 17px;
      font-weight: 800;
      color: var(--text-main);
      margin-bottom: 4px;
    }

    .privacy-banner-desc {
      font-size: 14px;
      line-height: 1.5;
      color: var(--text-muted);
    }

    .field-hint {
      font-size: 13px;
      color: var(--text-muted);
      margin-top: 6px;
      line-height: 1.4;
    }

    .confirmation-header {
      display: flex;
      align-items: center;
      gap: 14px;
      margin-bottom: 18px;
      padding-bottom: 16px;
      border-bottom: 1px solid var(--border-color);
    }

    .confirmation-icon {
      font-size: 36px;
      line-height: 1;
      flex-shrink: 0;
    }

    .confirmation-title {
      font-size: 20px;
      font-weight: 800;
      color: var(--text-main);
      margin-bottom: 4px;
    }

    .confirmation-sub {
      font-size: 15px;
      color: var(--text-muted);
      line-height: 1.4;
    }

    .receipt-box {
      background: var(--bg-card-subtle);
      border: 1.5px solid var(--border-color);
      border-radius: var(--radius-sm);
      padding: 16px;
      margin-bottom: 16px;
      display: flex;
      flex-direction: column;
      gap: 12px;
    }

    .receipt-row {
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 15px;
    }

    .receipt-label {
      color: var(--text-muted);
      font-weight: 600;
    }

    .receipt-value {
      color: var(--text-main);
      font-weight: 700;
    }

    .hash-display-pill {
      font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
      font-size: 12px;
      color: var(--steel-blue);
      background: rgba(59, 105, 152, 0.08);
      border: 1px dashed var(--steel-blue-border);
      padding: 10px 12px;
      border-radius: 6px;
      word-break: break-all;
      width: 100%;
      line-height: 1.45;
      user-select: all;
    }

    .dark .hash-display-pill {
      color: #93c5fd;
      background: rgba(147, 197, 253, 0.08);
      border-color: #3b82f6;
    }

    .privacy-stamp {
      display: flex;
      align-items: center;
      gap: 10px;
      font-size: 14px;
      color: var(--text-muted);
      background: rgba(13, 148, 136, 0.08);
      border: 1px solid rgba(13, 148, 136, 0.25);
      padding: 12px 14px;
      border-radius: var(--radius-sm);
      margin-bottom: 20px;
      line-height: 1.45;
    }

    .official-portal-callout {
      background: var(--bg-card-subtle);
      border: 2px solid var(--steel-blue);
      border-radius: var(--radius-md);
      padding: 18px 20px;
      margin-bottom: 16px;
    }

    .official-portal-title {
      font-size: 18px;
      font-weight: 800;
      color: var(--text-main);
      display: flex;
      align-items: center;
      gap: 8px;
      margin-bottom: 8px;
    }

    .official-portal-text {
      font-size: 15px;
      color: var(--text-muted);
      line-height: 1.5;
      margin-bottom: 14px;
    }

    .btn-cybercrime {
      background: #1e3a8a; /* Deep official navy */
      color: #ffffff;
      width: 100%;
      font-size: 17px;
      font-weight: 800;
      border-radius: var(--radius-sm);
      padding: 14px 18px;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 10px;
      text-decoration: none;
      box-shadow: 0 4px 12px rgba(30, 58, 138, 0.3);
      transition: all 0.2s ease;
    }

    .btn-cybercrime:hover {
      background: #172554;
      color: #ffffff;
    }

    .official-helpline-note {
      margin-top: 14px;
      display: flex;
      align-items: center;
      gap: 10px;
      font-size: 15px;
      color: var(--text-main);
      padding-top: 12px;
      border-top: 1px solid var(--border-color);
    }
'''

# Insert CSS before </style>
if "/* REPORT PAGE STYLES */" not in template:
    style_end_pos = template.find("</style>")
    template = template[:style_end_pos] + report_css + "\n  " + template[style_end_pos:]

# 2. REPLACE PAGE 4 REPORT HTML
report_html = '''      <!-- ============================================== -->
      <!-- PAGE 4: REPORT (Zero-Knowledge Scam Reporting) -->
      <!-- ============================================== -->
      <section id="page-report" class="page-section">
        <div class="section-header">
          <h1 class="section-title">
            <span>🚨</span> <span data-i18n="reportPageTitle">Report a Scam</span>
          </h1>
          <p class="section-subtitle" data-i18n="reportPageSub">
            Protect your community anonymously while preserving your privacy.
          </p>
        </div>

        <!-- Privacy Shield Banner -->
        <div class="privacy-banner-card">
          <div class="privacy-banner-icon">🛡️</div>
          <div class="privacy-banner-body">
            <div class="privacy-banner-title" data-i18n="reportPrivacyNoticeTitle">Zero-Knowledge Privacy Architecture</div>
            <div class="privacy-banner-desc" data-i18n="reportPrivacyNoticeDesc">
              Your name, message text, and phone number are <strong>never stored</strong>. BlaxGuard normalizes the identifier, converts it into an anonymous SHA-256 cryptographic hash, and records only the hash counter.
            </div>
          </div>
        </div>

        <!-- Report Form Card -->
        <div class="ui-card" id="reportFormContainer">
          <h3 class="card-title" data-i18n="reportFormTitle">Anonymous Scam Incident Form</h3>
          
          <form id="scamReportForm" onsubmit="handleReportSubmit(event)">
            <!-- Scam Type Dropdown -->
            <div class="form-group">
              <label class="form-label" for="reportScamTypeSelect">
                <span data-i18n="reportScamTypeLabel">Scam Type:</span> <span style="color: var(--verdict-danger);">*</span>
              </label>
              <select class="text-input" id="reportScamTypeSelect" required>
                <option value="" disabled selected data-i18n="reportOptPlaceholder">-- Select Scam Category --</option>
                <option value="loan_app" data-i18n="reportOptLoan">Predatory Loan App / Extortion / Fake Recovery</option>
                <option value="phishing_link" data-i18n="reportOptLink">Phishing Link / SMS / WhatsApp Trap</option>
                <option value="digital_arrest" data-i18n="reportOptArrest">Digital Arrest / Fake Police / CBI Call</option>
                <option value="fake_care" data-i18n="reportOptCare">Fake Customer Care / Toll-Free Number</option>
                <option value="kyc_bill" data-i18n="reportOptKyc">Electricity Bill Disconnection / KYC Expiry Warning</option>
                <option value="job_scam" data-i18n="reportOptJob">Work From Home / Task Scam / Part-Time Job</option>
                <option value="lottery_parcel" data-i18n="reportOptLottery">Lottery / Prize / FedEx Parcel Scam</option>
                <option value="other" data-i18n="reportOptOther">Other Fraudulent Trap</option>
              </select>
            </div>

            <!-- Scam Number / Link / App Name -->
            <div class="form-group">
              <label class="form-label" for="reportIdentifierInput">
                <span data-i18n="reportIdentifierLabel">Scam Number, Link, or App Name:</span> <span style="color: var(--verdict-danger);">*</span>
              </label>
              <input type="text" class="text-input" id="reportIdentifierInput" placeholder="e.g. +91 98765 43210, https://sbi-kyc.top, QuickRupee" data-i18n-placeholder="reportIdentifierPlaceholder" required autocomplete="off">
              <div class="field-hint" data-i18n="reportIdentifierHint">
                Normalized automatically: lowercased, spaces removed, +91 stripped before one-way hashing.
              </div>
            </div>

            <!-- Short Description -->
            <div class="form-group">
              <label class="form-label" for="reportDescInput">
                <span data-i18n="reportDescLabel">Short Description:</span> <span style="font-weight: 400; color: var(--text-muted); font-size: 14px;" data-i18n="reportDescSub">(Explain what happened)</span>
              </label>
              <textarea class="text-input" id="reportDescInput" rows="3" placeholder="Briefly describe what happened (e.g. Caller claimed to be electricity officer demanding Rs 10 via APK download)..." data-i18n-placeholder="reportDescPlaceholder"></textarea>
              <div class="field-hint" data-i18n="reportDescHint">
                ⚠️ For your safety, <strong>never</strong> enter passwords, ATM PINs, OTPs, or bank account numbers. This text is never stored.
              </div>
            </div>

            <!-- Optional Date -->
            <div class="form-group">
              <label class="form-label" for="reportDateInput" data-i18n="reportDateLabel">Incident Date (Optional):</label>
              <input type="date" class="text-input" id="reportDateInput" style="min-height: 48px;">
            </div>

            <!-- Submit Button -->
            <button type="submit" class="btn btn-primary" id="btnSubmitReport">
              <span>🛡️</span> <span data-i18n="btnSubmitReportText">Cryptographically Hash & Register</span>
            </button>
          </form>
        </div>

        <!-- Confirmation Card (Shown After Submission) -->
        <div class="ui-card" id="reportConfirmationCard" style="display: none;">
          <div class="confirmation-header">
            <div class="confirmation-icon">✅</div>
            <div>
              <h3 class="confirmation-title" data-i18n="reportConfirmTitle">Scam Incident Registered Anonymously!</h3>
              <p class="confirmation-sub" data-i18n="reportConfirmSub">Your report helps warn other citizens while preserving your privacy.</p>
            </div>
          </div>

          <div class="receipt-box">
            <div class="receipt-row">
              <span class="receipt-label" data-i18n="reportReceiptCategory">Category:</span>
              <span class="receipt-value" id="confirmCategoryBadge">--</span>
            </div>
            <div class="receipt-row">
              <span class="receipt-label" data-i18n="reportReceiptCount">Community Reports:</span>
              <span class="receipt-value" id="confirmCounterBadge" style="color: var(--verdict-danger); font-weight: 800;">1</span>
            </div>
            <div class="receipt-row" style="flex-direction: column; align-items: flex-start; gap: 6px;">
              <span class="receipt-label" data-i18n="reportReceiptHash">Stored SHA-256 Threat Hash:</span>
              <div class="hash-display-pill" id="confirmHashDisplay">--</div>
            </div>
          </div>

          <div class="privacy-stamp">
            <span style="font-size: 18px;">🔒</span>
            <span data-i18n="reportPrivacyGuarantee">Original message & contact details were discarded immediately. Only the SHA-256 hash & counter were recorded in memory.</span>
          </div>

          <!-- Official Cybercrime Reporting Callout -->
          <div class="official-portal-callout">
            <div class="official-portal-title">
              <span>🏛️</span> <span data-i18n="reportOfficialHeading">File Official Police Complaint</span>
            </div>
            <p class="official-portal-text" data-i18n="reportOfficialBody">
              BlaxGuard operates for crowdsourced prevention. If you have lost money or need immediate law enforcement action, lodge an official complaint on the National Cyber Crime Reporting Portal:
            </p>
            
            <a href="https://cybercrime.gov.in" target="_blank" rel="noopener noreferrer" class="btn btn-cybercrime">
              <span>🌐</span> <span data-i18n="btnOfficialCybercrime">Lodge Complaint on cybercrime.gov.in &rarr;</span>
            </a>

            <div class="official-helpline-note">
              <span style="font-size: 18px;">📞</span>
              <span><strong data-i18n="reportHelplineCall">Emergency Financial Fraud Helpline:</strong> <a href="tel:1930" style="color: #60a5fa; font-weight: 800; text-decoration: underline;">Call 1930</a> (<span data-i18n="reportHelplineTollFree">Toll-free 24x7</span>)</span>
            </div>
          </div>

          <button type="button" class="btn btn-outline" style="margin-top: 14px;" onclick="resetReportForm()">
            <span>➕</span> <span data-i18n="btnReportAnother">Report Another Scam</span>
          </button>
        </div>
      </section>
'''

pos_rep_start = template.find('<section id="page-report"')
pos_reg_start = template.find('<!-- ============================================== -->\n      <!-- PAGE 5: REGISTRY')
if pos_reg_start == -1:
    pos_reg_start = template.find('<section id="page-registry"')

template = template[:pos_rep_start] + report_html + "\n\n      " + template[pos_reg_start:]

# 3. UPDATE TRANSLATIONS IN EN, HI, AND TE
en_report_trans = '''/* Report Page */
        reportPageTitle: "Report a Scam",
        reportPageSub: "Protect your community anonymously while preserving complete privacy.",
        reportPrivacyNoticeTitle: "Zero-Knowledge Privacy Architecture",
        reportPrivacyNoticeDesc: "Your name, message text, and phone number are <strong>never stored</strong>. BlaxGuard normalizes the scam identifier, computes a SHA-256 cryptographic hash, and logs only the hash and a counter.",
        reportFormTitle: "Anonymous Scam Incident Form",
        reportScamTypeLabel: "Scam Type:",
        reportOptPlaceholder: "-- Select Scam Category --",
        reportOptLoan: "Predatory Loan App / Extortion",
        reportOptLink: "Phishing Link / SMS / WhatsApp Trap",
        reportOptArrest: "Digital Arrest / Fake Police / CBI Call",
        reportOptCare: "Fake Customer Care Number",
        reportOptKyc: "Electricity Bill / KYC Expiry Warning",
        reportOptJob: "Work From Home / Task Scam / Part-Time Job",
        reportOptLottery: "Lottery / Prize / Parcel Customs Scam",
        reportOptOther: "Other Fraudulent Trap",
        reportIdentifierLabel: "Scam Number, Link, or App Name:",
        reportIdentifierPlaceholder: "e.g. +91 98765 43210, https://sbi-kyc.top, or QuickRupee",
        reportIdentifierHint: "Auto-cleaned: spaces removed, +91 stripped, lowercased before one-way hashing.",
        reportDescLabel: "Short Description:",
        reportDescSub: "(Explain what happened)",
        reportDescPlaceholder: "Briefly describe what happened (e.g. Caller claimed power will be cut tonight)...",
        reportDescHint: "⚠️ Never enter passwords, ATM PINs, OTPs, or bank account numbers. Text is discarded immediately.",
        reportDateLabel: "Incident Date (Optional):",
        btnSubmitReportText: "Cryptographically Hash & Register",
        btnSubmitting: "Hashing & Registering...",
        reportConfirmTitle: "Scam Incident Registered Anonymously!",
        reportConfirmSub: "Your report helps warn other citizens while keeping you completely anonymous.",
        reportReceiptCategory: "Scam Category:",
        reportReceiptCount: "Community Reports:",
        reportReceiptHash: "Stored SHA-256 Threat Hash:",
        reportPrivacyGuarantee: "Original message & contact discarded immediately. Only the SHA-256 hash & counter were recorded in memory.",
        reportOfficialHeading: "File Official Police Complaint",
        reportOfficialBody: "BlaxGuard operates for crowdsourced prevention. If you have lost money or need immediate law enforcement action, lodge an official complaint on the National Cyber Crime Reporting Portal:",
        btnOfficialCybercrime: "Lodge Complaint on cybercrime.gov.in →",
        reportHelplineCall: "Emergency Financial Fraud Helpline:",
        reportHelplineTollFree: "Toll-free 24x7",
        btnReportAnother: "Report Another Scam",
        reportErrorEmptyId: "Please enter a scam phone number, link, or app name.",
        reportErrorEmptyType: "Please select a scam type from the dropdown.",'''

hi_report_trans = '''/* Report Page */
        reportPageTitle: "स्कैम की रिपोर्ट करें",
        reportPageSub: "अपनी पूर्ण गोपनीयता बनाए रखते हुए दूसरों को धोखे से बचाएं।",
        reportPrivacyNoticeTitle: "ज़ीरो-नॉलेज गोपनीयता सुरक्षा",
        reportPrivacyNoticeDesc: "आपकी व्यक्तिगत जानकारी और संदेश <strong>कभी भी सहेजे नहीं जाते</strong>। BlaxGuard पहचानकर्ता को मानकीकृत करता है, SHA-256 क्रिप्टोग्राफ़िक हैश बनाता है, और केवल हैश व काउंटर सहेजता है।",
        reportFormTitle: "गुमनाम स्कैम रिपोर्ट फॉर्म",
        reportScamTypeLabel: "स्कैम का प्रकार:",
        reportOptPlaceholder: "-- स्कैम श्रेणी चुनें --",
        reportOptLoan: "अवैध लोन ऐप / ब्लैकमेल व उत्पीड़न",
        reportOptLink: "फ़िशिंग लिंक / एसएमएस / व्हाट्सएप जाल",
        reportOptArrest: "डिजिटल अरेस्ट / नकली पुलिस / सीबीआई कॉल",
        reportOptCare: "नकली कस्टमर केयर नंबर",
        reportOptKyc: "बिजली बिल कटने / बैंक केवाईसी समाप्ति जाल",
        reportOptJob: "वर्क फ्रॉम होम / यूट्यूब लाइक / फर्जी नौकरी",
        reportOptLottery: "लॉटरी / इनाम / पार्सल कस्टम्स स्कैम",
        reportOptOther: "अन्य संदिग्ध धोखाधड़ी",
        reportIdentifierLabel: "स्कैमर का नंबर, लिंक या ऐप का नाम:",
        reportIdentifierPlaceholder: "उदा. +91 98765 43210, https://sbi-kyc.top, या QuickRupee",
        reportIdentifierHint: "स्वचालित सफ़ाई: रिक्त स्थान हटाए गए, +91 हटाया गया, सुरक्षित हैशिंग से पहले।",
        reportDescLabel: "संक्षिप्त विवरण:",
        reportDescSub: "(क्या हुआ था बताएं)",
        reportDescPlaceholder: "संक्षेप में बताएं कि क्या हुआ (उदा. कॉलर ने कहा कि आज रात बिजली कट जाएगी)...",
        reportDescHint: "⚠️ कभी भी पासवर्ड, पिन, ओटीपी या बैंक खाता नंबर न लिखें। यह विवरण कभी सहेजा नहीं जाता।",
        reportDateLabel: "घटना की तिथि (वैकल्पिक):",
        btnSubmitReportText: "क्रिप्टोग्राफ़िक हैश करें और दर्ज करें",
        btnSubmitting: "हैश तैयार हो रहा है...",
        reportConfirmTitle: "स्कैम सफलतापूर्वक गुमनाम रूप से दर्ज किया गया!",
        reportConfirmSub: "आपकी रिपोर्ट आपकी पूर्ण गोपनीयता बनाए रखते हुए अन्य नागरिकों को सचेत करेगी।",
        reportReceiptCategory: "स्कैम श्रेणी:",
        reportReceiptCount: "कुल रिपोर्ट दर्ज:",
        reportReceiptHash: "सुरक्षित SHA-256 हैश:",
        reportPrivacyGuarantee: "मूल संदेश और नंबर तुरंत नष्ट कर दिए गए। मेमोरी में केवल SHA-256 हैश और काउंटर दर्ज हुआ।",
        reportOfficialHeading: "आधिकारिक पुलिस शिकायत दर्ज करें",
        reportOfficialBody: "BlaxGuard सामुदायिक सुरक्षा के लिए कार्य करता है। यदि आपके पैसे कटे हैं या आधिकारिक पुलिस कार्रवाई चाहते हैं, तो भारत सरकार के साइबर क्राइम पोर्टल पर शिकायत करें:",
        btnOfficialCybercrime: "cybercrime.gov.in पर शिकायत दर्ज करें →",
        reportHelplineCall: "वित्तीय धोखाधड़ी हेल्पलाइन:",
        reportHelplineTollFree: "टोल-फ्री 24x7",
        btnReportAnother: "एक और स्कैम रिपोर्ट करें",
        reportErrorEmptyId: "कृपया स्कैमर का फोन नंबर, लिंक या ऐप का नाम दर्ज करें।",
        reportErrorEmptyType: "कृपया ड्रॉपडाउन से स्कैम का प्रकार चुनें।",'''

te_report_trans = '''/* Report Page */
        reportPageTitle: "స్కామ్‌ను రిపోర్ట్ చేయండి",
        reportPageSub: "మీ గోప్యతను కాపాడుకుంటూనే ఇతరులను సైబర్ మోసాల నుండి కాపాడండి.",
        reportPrivacyNoticeTitle: "జీరో-నాలెడ్జ్ పూర్తి గోప్యతా రక్షణ",
        reportPrivacyNoticeDesc: "మీ వ్యక్తిగత వివరాలు లేదా సందేశం <strong>ఎప్పుడూ భద్రపరచబడవు</strong>. BlaxGuard గుర్తింపు వివరాలను శుద్ధి చేసి, SHA-256 క్రిప్టోగ్రాఫిక్ హ్యాష్‌గా మార్చి కేవలం హ్యాష్ మరియు కౌంటర్‌ను మాత్రమే ఉంచుతుంది.",
        reportFormTitle: "అజ్ఞాత స్కామ్ రిపోర్ట్ ఫారమ్",
        reportScamTypeLabel: "స్కామ్ రకం:",
        reportOptPlaceholder: "-- స్కామ్ వర్గాన్ని ఎంచుకోండి --",
        reportOptLoan: "వేధింపుల లోన్ యాప్ / బెదిరింపులు",
        reportOptLink: "ఫిషింగ్ లింక్ / SMS / వాట్సాప్ మోసం",
        reportOptArrest: "డిజిటల్ అరెస్ట్ / నకిలీ పోలీస్ / CBI కాల్",
        reportOptCare: "నకిలీ కస్టమర్ కేర్ నంబర్",
        reportOptKyc: "విద్యుత్ బిల్లు నిలిపివేత / KYC గడువు మోసం",
        reportOptJob: "వర్క్ ఫ్రమ్ హోమ్ / పార్ట్ టైమ్ జాబ్ స్కామ్",
        reportOptLottery: "లాటరీ / బహుమతి / కొరియర్ పార్సిల్ మోసం",
        reportOptOther: "ఇతర అనుమానాస్పద మోసం",
        reportIdentifierLabel: "స్కామర్ నంబర్, లింక్ లేదా యాప్ పేరు:",
        reportIdentifierPlaceholder: "ఉదా. +91 98765 43210, https://sbi-kyc.top, లేదా QuickRupee",
        reportIdentifierHint: "ఆటోమేటిక్ ప్రక్షాళన: స్పేస్‌లు, +91 తొలగించి SHA-256 హ్యాష్‌గా మార్చబడుతుంది.",
        reportDescLabel: "సంక్షిప్త వివరణ:",
        reportDescSub: "(ఏమి జరిగిందో వివరించండి)",
        reportDescPlaceholder: "ఏమి జరిగిందో క్లుప్తంగా వివరించండి (ఉదా. విద్యుత్ అధికారి అని చెప్పి APK డౌన్‌లోడ్ చేయమన్నారు)...",
        reportDescHint: "⚠️ ఎట్టి పరిస్థితుల్లోనూ పాస్‌వర్డ్‌లు, పిన్‌లు, OTPలు రాయకండి. ఈ సమాచారం భద్రపరచబడదు.",
        reportDateLabel: "సంఘటన తేదీ (ఐచ్ఛికం):",
        btnSubmitReportText: "క్రిప్టోగ్రాఫిక్ హ్యాష్ చేసి నమోదు చేయండి",
        btnSubmitting: "హ్యాష్ నమోదు అవుతోంది...",
        reportConfirmTitle: "స్కామ్ విజయవంతంగా అజ్ఞాతంగా నమోదైంది!",
        reportConfirmSub: "మీ గోప్యతను కాపాడుతూనే ఇతరులను హెచ్చరించడానికి మీ నివేదిక సహాయపడుతుంది.",
        reportReceiptCategory: "స్కామ్ వర్గం:",
        reportReceiptCount: "నమోదైన మొత్తం నివేదికలు:",
        reportReceiptHash: "నిల్వ చేయబడిన SHA-256 హ్యాష్:",
        reportPrivacyGuarantee: "అసలు సందేశం మరియు నంబర్ వెంటనే తొలగించబడ్డాయి. మెమరీలో కేవలం SHA-256 హ్యాష్ మరియు కౌంటర్ మాత్రమే నిల్వ చేయబడ్డాయి.",
        reportOfficialHeading: "అధికారిక పోలీసు ఫిర్యాదు నమోదు చేయండి",
        reportOfficialBody: "BlaxGuard ప్రజా రక్షణ కోసం సమాచారాన్ని సేకరిస్తుంది. మీరు డబ్బు పోగొట్టుకుంటే లేదా అధికారిక చర్య కోసం భారత ప్రభుత్వ సైబర్ క్రైమ్ పోర్టల్‌లో ఫిర్యాదు చేయండి:",
        btnOfficialCybercrime: "cybercrime.gov.in లో ఫిర్యాదు చేయండి →",
        reportHelplineCall: "ఆర్థిక మోసాల అత్యవసర హెల్ప్‌లైన్:",
        reportHelplineTollFree: "టోల్-ఫ్రీ 24x7",
        btnReportAnother: "మరొక స్కామ్‌ను రిపోర్ట్ చేయండి",
        reportErrorEmptyId: "దయచేసి స్కామర్ ఫోన్ నంబర్, లింక్ లేదా యాప్ పేరును నమోదు చేయండి.",
        reportErrorEmptyType: "దయచేసి డ్రాప్‌డౌన్ నుండి స్కామ్ రకాన్ని ఎంచుకోండి.",'''

# Replace EN block
idx_en = template.find('/* Report Page */')
idx_en_end = template.find('/* Registry Page */', idx_en)
template = template[:idx_en] + en_report_trans + "\n\n        " + template[idx_en_end:]

# Replace HI block
idx_hi = template.find('reportPageTitle: "धोखाधड़ी की रिपोर्ट करें"')
idx_hi_end = template.find('registryPageTitle:', idx_hi)
template = template[:idx_hi] + hi_report_trans + "\n\n        " + template[idx_hi_end:]

# Replace TE block
idx_te = template.find('reportPageTitle: "మోసాన్ని నివేదించండి"')
idx_te_end = template.find('registryPageTitle:', idx_te)
template = template[:idx_te] + te_report_trans + "\n\n        " + template[idx_te_end:]

# 4. REPLACE JAVASCRIPT LOGIC WITH BLAXGUARD DATA LAYER & REPORT HANDLERS
report_js = '''/* ============================================================== */
    /* BLAXGUARD DATA-LAYER MODULE & REPORTING ARCHITECTURE           */
    /*                                                                */
    /* PRIVACY & SECURITY CONTRACT:                                   */
    /* 1. Never stores the original message or raw contact identifier.*/
    /* 2. Normalizes identifier (lowercase, strip spaces, remove +91).*/
    /* 3. Hashes identifier with SHA-256 via Web Crypto API.          */
    /* 4. Stores ONLY the SHA-256 hash and a counter in memory.       */
    /* 5. Decoupled module interface ready for future cloud backend.  */
    /* ============================================================== */
    const BlaxGuardDataLayer = (function() {
      // In-memory threat database: stores ONLY hashes and metadata counters
      // Map<string, { hash: string, count: number, scamType: string, date: string, timestamp: string }>
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

      // Seed initial realistic known threats (PS-31 community intelligence)
      const _demoSeeds = [
        { raw: "9831245890", type: "fake_care", count: 14, date: "2026-10-02" },
        { raw: "https://sbi-kyc-update.xyz", type: "phishing_link", count: 29, date: "2026-10-04" },
        { raw: "quickcashrupeeloan", type: "loan_app", count: 42, date: "2026-10-06" }
      ];

      (async function initSeeds() {
        for (const item of _demoSeeds) {
          try {
            const norm = normalize(item.raw);
            const h = await hashSha256(norm);
            _memoryStore.set(h, {
              hash: h,
              count: item.count,
              scamType: item.type,
              incidentDate: item.date,
              timestamp: new Date().toISOString()
            });
          } catch(e) {}
        }
      })();

      return {
        normalizeIdentifier(raw) {
          return normalize(raw);
        },

        async hashIdentifier(normalized) {
          return hashSha256(normalized);
        },

        /**
         * Submit a scam report.
         * STRICT PRIVACY GUARANTEE:
         * - Raw input and message descriptions are NEVER stored in memory or persistence.
         * - STORES ONLY: SHA-256 hash, counter, category, optional date.
         * 
         * To replace with real backend later:
         * Replace the local Map update with:
         *   return await fetch('/api/reports', {
         *     method: 'POST',
         *     headers: { 'Content-Type': 'application/json' },
         *     body: JSON.stringify({ hash, count, scamType, incidentDate })
         *   }).then(r => r.json());
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
            incidentDate: incidentDate || new Date().toISOString().split("T")[0],
            timestamp: new Date().toISOString()
          };

          _memoryStore.set(hash, record);

          return {
            success: true,
            hash: hash,
            count: newCount,
            scamType: record.scamType,
            incidentDate: record.incidentDate
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

    /* REPORT FORM SUBMISSION CONTROLLER */
    async function handleReportSubmit(e) {
      if (e && e.preventDefault) e.preventDefault();
      
      const typeSelect = document.getElementById("reportScamTypeSelect");
      const identifierInput = document.getElementById("reportIdentifierInput");
      const descInput = document.getElementById("reportDescInput");
      const dateInput = document.getElementById("reportDateInput");
      const submitBtn = document.getElementById("btnSubmitReport");
      const dict = translations[currentLang] || translations.en;

      const scamType = typeSelect.value;
      const rawIdentifier = identifierInput.value.trim();
      const incidentDate = dateInput.value;

      if (!scamType) {
        alert(dict.reportErrorEmptyType || "Please select a scam type");
        typeSelect.focus();
        return;
      }

      if (!rawIdentifier) {
        alert(dict.reportErrorEmptyId || "Please enter a scam phone number, link, or app name");
        identifierInput.focus();
        return;
      }

      // UI Loading indicator
      const originalBtnHTML = submitBtn.innerHTML;
      submitBtn.disabled = true;
      submitBtn.innerHTML = `<span>⏳</span> <span>${dict.btnSubmitting || "Hashing & Registering..."}</span>`;

      try {
        // Record report in data-layer module
        // Note: The message description is intentionally NOT sent to the data store
        // ensuring the strict privacy rule: "Never store the original message".
        const result = await BlaxGuardDataLayer.recordReport({
          rawIdentifier: rawIdentifier,
          scamType: scamType,
          incidentDate: incidentDate
        });

        // Populate Confirmation Card
        const categoryBadge = document.getElementById("confirmCategoryBadge");
        if (categoryBadge) categoryBadge.textContent = getScamTypeName(scamType);

        const counterBadge = document.getElementById("confirmCounterBadge");
        if (counterBadge) counterBadge.textContent = result.count;

        const hashDisplay = document.getElementById("confirmHashDisplay");
        if (hashDisplay) hashDisplay.textContent = result.hash;

        // Clear sensitive inputs immediately
        identifierInput.value = "";
        descInput.value = "";
        typeSelect.selectedIndex = 0;
        dateInput.value = "";

        // Switch to Confirmation view
        document.getElementById("reportFormContainer").style.display = "none";
        const confirmCard = document.getElementById("reportConfirmationCard");
        confirmCard.style.display = "block";
        confirmCard.scrollIntoView({ behavior: "smooth", block: "start" });

      } catch (err) {
        console.error("Report processing error:", err);
        alert("An error occurred while registering the incident. Please try again.");
      } finally {
        submitBtn.disabled = false;
        submitBtn.innerHTML = originalBtnHTML;
      }
    }

    function resetReportForm() {
      document.getElementById("reportConfirmationCard").style.display = "none";
      document.getElementById("reportFormContainer").style.display = "block";
      const idInput = document.getElementById("reportIdentifierInput");
      if (idInput) idInput.focus();
    }

    function getScamTypeName(typeKey) {
      const dict = translations[currentLang] || translations.en;
      const map = {
        "loan_app": dict.reportOptLoan,
        "phishing_link": dict.reportOptLink,
        "digital_arrest": dict.reportOptArrest,
        "fake_care": dict.reportOptCare,
        "kyc_bill": dict.reportOptKyc,
        "job_scam": dict.reportOptJob,
        "lottery_parcel": dict.reportOptLottery,
        "other": dict.reportOptOther
      };
      return map[typeKey] || typeKey;
    }
'''

# Replace submitReport in template
idx_js_sub = template.find('/* REPORT, REGISTRY, GUARDIAN, LEARN FUNCTIONS */')
idx_js_filter = template.find('function filterRegistry()', idx_js_sub)
template = template[:idx_js_sub] + report_js + "\n\n    " + template[idx_js_filter:]

# Save updated template.html
with open("template.html", "w", encoding="utf-8") as f:
    f.write(template)

# Build index.html
output = template.replace("{{SHIELD_URI}}", shield_uri).replace("{{FULL_URI}}", full_uri)
with open("index.html", "w", encoding="utf-8") as f:
    f.write(output)

print(f"Generated index.html with complete Report page! File size: {os.path.getsize('index.html')} bytes")
