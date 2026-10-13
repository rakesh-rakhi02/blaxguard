import json
import os
import re

with open("uris.json", "r", encoding="utf-8") as f:
    uris = json.load(f)

shield_uri = uris["shield"]
full_uri = uris["full"]

with open("template.html", "r", encoding="utf-8") as f:
    template = f.read()

# 1. ADD CSS FOR HELP PAGE (LARGE & CALM LAYOUT)
help_css = '''
    /* HELP PAGE STYLES: LARGE & CALM LAYOUT */
    .calm-hero-card {
      background: var(--steel-blue-light);
      border: 1.5px solid var(--steel-blue-border);
      border-radius: var(--radius-md);
      padding: 18px 20px;
      margin-bottom: 20px;
      display: flex;
      align-items: flex-start;
      gap: 14px;
    }
    .calm-hero-icon {
      font-size: 32px;
      line-height: 1;
      flex-shrink: 0;
      margin-top: 2px;
    }
    .calm-hero-title {
      font-size: 18px;
      font-weight: 800;
      color: var(--text-main);
      margin-bottom: 4px;
    }
    .calm-hero-text {
      font-size: 15px;
      line-height: 1.5;
      color: var(--text-muted);
    }
    .tap-call-btn {
      width: 100%;
      min-height: 60px;
      padding: 16px 20px;
      border-radius: var(--radius-md);
      display: flex;
      align-items: center;
      justify-content: space-between;
      text-decoration: none;
      transition: all 0.2s ease;
      margin-bottom: 12px;
      box-shadow: var(--shadow-sm);
    }
    .tap-call-btn-1930 {
      background: #1e3a8a;
      color: #ffffff;
      border: 2px solid #3b82f6;
    }
    .tap-call-btn-1930:hover {
      background: #1e40af;
      color: #ffffff;
    }
    .tap-call-btn-112 {
      background: #0f766e;
      color: #ffffff;
      border: 2px solid #14b8a6;
    }
    .tap-call-btn-112:hover {
      background: #115e59;
      color: #ffffff;
    }
    .tap-call-badge {
      font-size: 12px;
      font-weight: 700;
      background: rgba(255, 255, 255, 0.2);
      color: #ffffff;
      padding: 4px 10px;
      border-radius: var(--radius-pill);
      letter-spacing: 0.5px;
    }
    .bank-reminder-card {
      background: rgba(245, 158, 11, 0.08);
      border: 1.5px solid rgba(245, 158, 11, 0.35);
      border-radius: var(--radius-sm);
      padding: 14px 16px;
      margin-top: 14px;
      display: flex;
      align-items: flex-start;
      gap: 12px;
    }
    .bank-reminder-title {
      font-size: 16px;
      font-weight: 800;
      color: var(--text-main);
      margin-bottom: 4px;
    }
    .bank-reminder-desc {
      font-size: 14.5px;
      line-height: 1.5;
      color: var(--text-muted);
    }
    .golden-hour-list {
      list-style: none;
      padding: 0;
      margin: 16px 0 0 0;
      display: flex;
      flex-direction: column;
      gap: 14px;
    }
    .golden-hour-item {
      display: flex;
      align-items: flex-start;
      gap: 14px;
      font-size: 15.5px;
      line-height: 1.5;
      color: var(--text-main);
    }
    .golden-step-badge {
      width: 32px;
      height: 32px;
      border-radius: 50%;
      background: var(--steel-blue);
      color: #ffffff;
      font-weight: 800;
      font-size: 15px;
      display: flex;
      align-items: center;
      justify-content: center;
      flex-shrink: 0;
      margin-top: 2px;
    }
    .freeze-guide-box {
      background: var(--bg-card-subtle);
      border: 2px solid var(--steel-blue-border);
      border-radius: var(--radius-md);
      padding: 18px 20px;
      margin-top: 16px;
    }
    .freeze-steps-grid {
      display: flex;
      flex-direction: column;
      gap: 10px;
      margin-top: 12px;
    }
    .freeze-step-chip {
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: var(--radius-sm);
      padding: 10px 14px;
      font-size: 14.5px;
      display: flex;
      align-items: center;
      gap: 10px;
      line-height: 1.4;
      color: var(--text-main);
    }
'''

if "/* HELP PAGE STYLES: LARGE & CALM LAYOUT */" not in template:
    pos_style_end = template.find("</style>")
    template = template[:pos_style_end] + help_css + "\n  " + template[pos_style_end:]

# 2. REPLACE PAGE 7 HELP HTML
help_html = '''      <!-- ============================================== -->
      <!-- PAGE 7: HELP (Emergency Response & Assistance) -->
      <!-- ============================================== -->
      <section id="page-help" class="page-section">
        <div class="section-header">
          <h1 class="section-title">
            <span>🆘</span> <span data-i18n="helpPageTitle">Emergency Help & Scam Response</span>
          </h1>
          <p class="section-subtitle" data-i18n="helpPageSub">
            Stay calm and act quickly. Immediate steps to freeze debits, lock accounts, and report to authorities.
          </p>
        </div>

        <!-- Calming Reassurance Card -->
        <div class="calm-hero-card">
          <div class="calm-hero-icon">🧘</div>
          <div>
            <div class="calm-hero-title" data-i18n="helpCalmTitle">Stay Calm — You Can Take Action Now</div>
            <div class="calm-hero-text" data-i18n="helpCalmText">
              Cyber fraud happens to thousands of citizens every day. Acting swiftly within the first hour gives banks and authorities the highest probability of freezing fraudulent transactions before money is withdrawn.
            </div>
          </div>
        </div>

        <!-- Tap-To-Call Emergency Numbers Card -->
        <div class="ui-card">
          <h3 class="card-title" data-i18n="helpTapCallTitle">Immediate Tap-to-Call Helplines</h3>
          <p class="card-text" style="font-size: 15px; margin-bottom: 14px;" data-i18n="helpTapCallSub">
            Tap directly on your mobile screen to connect with emergency cyber defense services:
          </p>

          <!-- Button: 1930 Cyber Fraud Helpline -->
          <a href="tel:1930" class="tap-call-btn tap-call-btn-1930">
            <div style="display: flex; align-items: center; gap: 12px;">
              <span style="font-size: 24px;">📞</span>
              <div>
                <div style="font-size: 19px; font-weight: 800;" data-i18n="btnDial1930">Call 1930 (Cyber Fraud Helpline)</div>
                <div style="font-size: 13px; opacity: 0.9; font-weight: 600;" data-i18n="descDial1930">National Cyber Crime Reporting Helpline &bull; Toll-Free 24x7</div>
              </div>
            </div>
            <span class="tap-call-badge" data-i18n="badgeTollFree">TOLL FREE</span>
          </a>

          <!-- Button: 112 National Emergency Services -->
          <a href="tel:112" class="tap-call-btn tap-call-btn-112">
            <div style="display: flex; align-items: center; gap: 12px;">
              <span style="font-size: 24px;">🚨</span>
              <div>
                <div style="font-size: 19px; font-weight: 800;" data-i18n="btnDial112">Call 112 (National Emergency)</div>
                <div style="font-size: 13px; opacity: 0.9; font-weight: 600;" data-i18n="descDial112">Police &bull; Immediate In-Person Help &bull; Coercion / Blackmail</div>
              </div>
            </div>
            <span class="tap-call-badge" data-i18n="badge24x7">24x7 EMERGENCY</span>
          </a>

          <!-- Bank Official Number Reminder Box -->
          <div class="bank-reminder-card">
            <span style="font-size: 22px;">💳</span>
            <div>
              <div class="bank-reminder-title" data-i18n="bankReminderTitle">Crucial Reminder: Use Only Bank's Official Number</div>
              <div class="bank-reminder-desc" data-i18n="bankReminderDesc">
                <strong>Never search for your bank's customer care on Google Search or Google Maps</strong> — scammers post fake mobile numbers there. Look <strong>only on the back of your physical ATM/Debit card</strong> or inside your printed passbook.
              </div>
            </div>
          </div>
        </div>

        <!-- The First Hour Guide Card -->
        <div class="ui-card">
          <h3 class="card-title">
            <span>⏱️</span> <span data-i18n="firstHourTitle">First 60 Minutes After Losing Money (The Golden Hour)</span>
          </h3>
          <p class="card-text" style="font-size: 15px;" data-i18n="firstHourSub">
            Banks and 1930 nodal officers can trigger an emergency freeze on beneficiary accounts if reported immediately. Follow these 5 steps in order:
          </p>

          <ul class="golden-hour-list">
            <li class="golden-hour-item">
              <span class="golden-step-badge">1</span>
              <div>
                <strong data-i18n="step1Bold">Dial 1930 Immediately:</strong>
                <span data-i18n="step1Text"> Provide your account number, bank name, transaction time, and amount. The 1930 operator triggers a CFCFRMS ticket to freeze the scammer's bank account before they withdraw cash.</span>
              </div>
            </li>
            <li class="golden-hour-item">
              <span class="golden-step-badge">2</span>
              <div>
                <strong data-i18n="step2Bold">Freeze Card &amp; UPI in Bank App:</strong>
                <span data-i18n="step2Text"> Open your official mobile banking app right now. Go to Card Controls and lock your Debit card. Turn off online and international transactions.</span>
              </div>
            </li>
            <li class="golden-hour-item">
              <span class="golden-step-badge">3</span>
              <div>
                <strong data-i18n="step3Bold">Save 12-Digit UTR &amp; Transaction Details:</strong>
                <span data-i18n="step3Text"> Take screenshots of debit SMS and UPI receipts. Note down the 12-digit UTR/UPI reference number, scammer's UPI ID/number, and exact timestamp.</span>
              </div>
            </li>
            <li class="golden-hour-item">
              <span class="golden-step-badge">4</span>
              <div>
                <strong data-i18n="step4Bold">Lodge Complaint on cybercrime.gov.in:</strong>
                <span data-i18n="step4Text"> Visit the official National Cyber Crime Reporting Portal to log an official police complaint and receive an acknowledgement number for your bank dispute.</span>
              </div>
            </li>
            <li class="golden-hour-item">
              <span class="golden-step-badge">5</span>
              <div>
                <strong data-i18n="step5Bold">Notify Bank in Writing within 3 Days:</strong>
                <span data-i18n="step5Text"> Submit a formal written dispute letter to your home bank branch manager with the 1930 complaint number. Under RBI guidelines, notifying the bank promptly protects your entitlement to refund compensation.</span>
              </div>
            </li>
          </ul>
        </div>

        <!-- Note to Freeze Card / UPI through Bank App -->
        <div class="freeze-guide-box">
          <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 8px;">
            <span style="font-size: 24px;">🔒</span>
            <h3 style="font-size: 18px; font-weight: 800; color: var(--text-main);" data-i18n="freezeNoteTitle">How to Freeze Your Card &amp; UPI in Bank App (30 Seconds)</h3>
          </div>
          <p style="font-size: 14.5px; color: var(--text-muted); line-height: 1.5;" data-i18n="freezeNoteSub">
            Even if a scammer stole your card number or PIN, they cannot deduct another rupee once you switch off card usage in your official bank app:
          </p>

          <div class="freeze-steps-grid">
            <div class="freeze-step-chip">
              <span>1️⃣</span>
              <span data-i18n="freezeChip1">Open your genuine bank app (e.g. YONO SBI, HDFC MobileBanking, iMobile, Baroda M-Connect).</span>
            </div>
            <div class="freeze-step-chip">
              <span>2️⃣</span>
              <span data-i18n="freezeChip2">Go to <strong>"Cards"</strong> &rarr; <strong>"Manage Debit Card"</strong> &rarr; Toggle <strong>"Temporary Lock / Block Card"</strong>.</span>
            </div>
            <div class="freeze-step-chip">
              <span>3️⃣</span>
              <span data-i18n="freezeChip3">Turn OFF <strong>"Domestic Online / E-Commerce"</strong> and <strong>"ATM Cash Withdrawal"</strong> toggles.</span>
            </div>
            <div class="freeze-step-chip">
              <span>4️⃣</span>
              <span data-i18n="freezeChip4">Under <strong>"UPI Settings"</strong> &rarr; Select <strong>"Deregister UPI Profile"</strong> or reduce your daily limit to ₹1.</span>
            </div>
          </div>
        </div>

        <!-- Official Cybercrime Portal Callout -->
        <div class="ui-card" style="margin-top: 16px;">
          <h3 class="card-title">
            <span>🏛️</span> <span data-i18n="officialPortalTitle">National Cyber Crime Reporting Portal</span>
          </h3>
          <p class="card-text" style="font-size: 15px; margin-bottom: 14px;" data-i18n="officialPortalSub">
            Official Government of India portal operated by the Ministry of Home Affairs (MHA) for reporting cyber financial crimes and filing police complaints:
          </p>
          <a href="https://cybercrime.gov.in" target="_blank" rel="noopener noreferrer" class="btn btn-cybercrime">
            <span>🌐</span> <span data-i18n="btnOfficialCybercrimeLink">Lodge Complaint on cybercrime.gov.in &rarr;</span>
          </a>
        </div>

        <!-- Family Guardian Alert Mode -->
        <div class="ui-card" style="margin-top: 16px;">
          <h3 class="card-title">
            <span>🛡️</span> <span data-i18n="guardianTitle">Family Guardian Alert Contact</span>
          </h3>
          <p class="card-text" style="font-size: 15px;" data-i18n="guardianDesc">
            Save your son, daughter, or trusted relative's phone number. BlaxGuard keeps this in your phone so you can alert them with one tap during suspicious calls or messages.
          </p>
          <div class="form-group" style="margin-top: 12px;">
            <label class="form-label" data-i18n="guardianPhoneLabel">Guardian's Mobile Number:</label>
            <input type="tel" id="guardianPhoneInput" class="text-input" placeholder="+91 98765 00000" data-i18n-placeholder="guardianPhonePlaceholder">
          </div>
          <button type="button" class="btn btn-secondary" onclick="saveGuardian()">
            <span>💾</span> <span data-i18n="btnSaveGuardian">Save Guardian Contact</span>
          </button>
        </div>
      </section>'''

pos_help_start = template.find('<section id="page-help"')
pos_admin_start = template.find('<section id="page-admin"')
template = template[:pos_help_start] + help_html + "\n\n      " + template[pos_admin_start:]

# 3. TRANSLATIONS FOR HELP PAGE ACROSS EN, HI, TE
en_help_trans = '''/* Help Page */
        helpPageTitle: "Emergency Help & Scam Response",
        helpPageSub: "Stay calm and act quickly. Immediate steps to freeze debits, lock accounts, and report to authorities.",
        helpCalmTitle: "Stay Calm — You Can Take Action Now",
        helpCalmText: "Cyber fraud happens to thousands of citizens every day. Acting swiftly within the first hour gives banks and authorities the highest probability of freezing fraudulent transactions before money is withdrawn.",
        helpTapCallTitle: "Immediate Tap-to-Call Helplines",
        helpTapCallSub: "Tap directly on your mobile screen to connect with emergency cyber defense services:",
        btnDial1930: "Call 1930 (Cyber Fraud Helpline)",
        descDial1930: "National Cyber Crime Reporting Helpline &bull; Toll-Free 24x7",
        badgeTollFree: "TOLL FREE",
        btnDial112: "Call 112 (National Emergency)",
        descDial112: "Police &bull; Immediate In-Person Help &bull; Coercion / Blackmail",
        badge24x7: "24x7 EMERGENCY",
        bankReminderTitle: "Crucial Reminder: Use Only Bank's Official Number",
        bankReminderDesc: "<strong>Never search for your bank's customer care on Google Search or Google Maps</strong> — scammers post fake mobile numbers there. Look <strong>only on the back of your physical ATM/Debit card</strong> or inside your printed passbook.",
        firstHourTitle: "First 60 Minutes After Losing Money (The Golden Hour)",
        firstHourSub: "Banks and 1930 nodal officers can trigger an emergency freeze on beneficiary accounts if reported immediately. Follow these 5 steps in order:",
        step1Bold: "Dial 1930 Immediately:",
        step1Text: "Provide your account number, bank name, transaction time, and amount. The 1930 operator triggers a CFCFRMS ticket to freeze the scammer's bank account before they withdraw cash.",
        step2Bold: "Freeze Card & UPI in Bank App:",
        step2Text: "Open your official mobile banking app right now. Go to Card Controls and lock your Debit card. Turn off online and international transactions.",
        step3Bold: "Save 12-Digit UTR & Transaction Details:",
        step3Text: "Take screenshots of debit SMS and UPI receipts. Note down the 12-digit UTR/UPI reference number, scammer's UPI ID/number, and exact timestamp.",
        step4Bold: "Lodge Complaint on cybercrime.gov.in:",
        step4Text: "Visit the official National Cyber Crime Reporting Portal to log an official police complaint and receive an acknowledgement number for your bank dispute.",
        step5Bold: "Notify Bank in Writing within 3 Days:",
        step5Text: "Submit a formal written dispute letter to your home bank branch manager with the 1930 complaint number. Under RBI guidelines, notifying the bank promptly protects your entitlement to refund compensation.",
        freezeNoteTitle: "How to Freeze Your Card & UPI in Bank App (30 Seconds)",
        freezeNoteSub: "Even if a scammer stole your card number or PIN, they cannot deduct another rupee once you switch off card usage in your official bank app:",
        freezeChip1: "Open your genuine bank app (e.g. YONO SBI, HDFC MobileBanking, iMobile, Baroda M-Connect).",
        freezeChip2: "Go to <strong>'Cards'</strong> &rarr; <strong>'Manage Debit Card'</strong> &rarr; Toggle <strong>'Temporary Lock / Block Card'</strong>.",
        freezeChip3: "Turn OFF <strong>'Domestic Online / E-Commerce'</strong> and <strong>'ATM Cash Withdrawal'</strong> toggles.",
        freezeChip4: "Under <strong>'UPI Settings'</strong> &rarr; Select <strong>'Deregister UPI Profile'</strong> or reduce your daily limit to ₹1.",
        officialPortalTitle: "National Cyber Crime Reporting Portal",
        officialPortalSub: "Official Government of India portal operated by the Ministry of Home Affairs (MHA) for reporting cyber financial crimes and filing police complaints:",
        btnOfficialCybercrimeLink: "Lodge Complaint on cybercrime.gov.in →",
        guardianTitle: "Family Guardian Alert Contact",
        guardianDesc: "Save your son, daughter, or trusted relative's phone number. BlaxGuard keeps this in your phone so you can alert them with one tap during suspicious calls or messages.",
        guardianPhoneLabel: "Guardian's Mobile Number:",
        guardianPhonePlaceholder: "+91 98765 00000",
        btnSaveGuardian: "Save Guardian Contact",'''

hi_help_trans = '''/* Help Page */
        helpPageTitle: "आपातकालीन सहायता व स्कैम प्रतिक्रिया",
        helpPageSub: "शांत रहें और तुरंत कदम उठाएं। लेन-देन रोकने, खाते लॉक करने और पुलिस रिपोर्ट के तत्काल चरण।",
        helpCalmTitle: "शांत रहें — आप तुरंत कदम उठा सकते हैं",
        helpCalmText: "साइबर धोखाधड़ी हर दिन हजारों नागरिकों के साथ होती है। पहले घंटे के भीतर त्वरित कार्रवाई करने से बैंकों और अधिकारियों द्वारा धोखाधड़ी वाले लेन-देन को फ्रीज करने की सबसे अधिक संभावना होती है।",
        helpTapCallTitle: "तत्काल कॉल करने के लिए हेल्पलाइन",
        helpTapCallSub: "आपातकालीन साइबर सुरक्षा सेवाओं से जुड़ने के लिए स्क्रीन पर सीधे टैप करें:",
        btnDial1930: "1930 पर कॉल करें (साइबर फ्रॉड हेल्पलाइन)",
        descDial1930: "राष्ट्रीय साइबर अपराध रिपोर्टिंग हेल्पलाइन &bull; टोल-फ्री 24x7",
        badgeTollFree: "टोल फ्री",
        btnDial112: "112 पर कॉल करें (राष्ट्रीय आपातकालीन)",
        descDial112: "पुलिस &bull; तत्काल व्यक्तिगत सहायता &bull; धमकी / ब्लैकमेल",
        badge24x7: "24x7 आपातकाल",
        bankReminderTitle: "अत्यंत महत्वपूर्ण: केवल बैंक के आधिकारिक नंबर का उपयोग करें",
        bankReminderDesc: "<strong>गूगल सर्च या मैप्स पर कभी भी अपने बैंक का कस्टमर केयर न खोजें</strong> — धोखेबाज वहां फर्जी मोबाइल नंबर डाल देते हैं। केवल <strong>अपने एटीएम/डेबिट कार्ड के पीछे</strong> या बैंक पासबुक में छपे नंबर पर ही कॉल करें।",
        firstHourTitle: "पैसे कटने के बाद पहले 60 मिनट (स्वर्ण काल / गोल्डन ऑवर)",
        firstHourSub: "तुरंत सूचना देने पर बैंक नोडल अधिकारी और 1930 धोखेबाज के खाते में पैसे फ्रीज कर सकते हैं। इन 5 चरणों का क्रमवार पालन करें:",
        step1Bold: "तुरंत 1930 डायल करें:",
        step1Text: "अपना खाता नंबर, बैंक का नाम, लेन-देन का समय और राशि बताएं। 1930 ऑपरेटर धोखेबाज के खाते को फ्रीज करने के लिए तुरंत टिकट जारी करता है।",
        step2Bold: "बैंक ऐप में कार्ड और यूपीआई तुरंत फ्रीज करें:",
        step2Text: "अभी अपना आधिकारिक मोबाइल बैंकिंग ऐप खोलें। कार्ड सेटिंग्स में जाकर डेबिट कार्ड को लॉक करें और ऑनलाइन लेन-देन बंद कर दें।",
        step3Bold: "12 अंकों का यूटीआर और लेन-देन विवरण सुरक्षित करें:",
        step3Text: "पैसे कटने के एसएमएस और यूपीआई रसीद का स्क्रीनशॉट लें। 12 अंकों का यूटीआर/यूपीआई नंबर, धोखेबाज की यूपीआई आईडी और सटीक समय नोट करें।",
        step4Bold: "cybercrime.gov.in पर औपचारिक शिकायत दर्ज करें:",
        step4Text: "आधिकारिक राष्ट्रीय साइबर अपराध पोर्टल पर शिकायत दर्ज करें ताकि बैंक विवाद के लिए आधिकारिक पावती नंबर प्राप्त हो सके।",
        step5Bold: "3 दिनों के भीतर बैंक शाखा को लिखित रूप में सूचित करें:",
        step5Text: "1930 शिकायत संख्या के साथ अपनी बैंक शाखा में लिखित विवाद पत्र जमा करें। आरबीआई नियमों के अनुसार तुरंत सूचना देने पर रिफंड का अधिकार सुरक्षित रहता है।",
        freezeNoteTitle: "बैंक ऐप में 30 सेकंड में कार्ड और यूपीआई कैसे फ्रीज करें",
        freezeNoteSub: "यदि धोखेबाज के पास आपका कार्ड नंबर या पिन भी है, तो भी बैंक ऐप में कार्ड बंद करने के बाद एक रुपया भी नहीं कट सकता:",
        freezeChip1: "अपना प्रामाणिक बैंक ऐप खोलें (उदा. YONO SBI, HDFC MobileBanking, iMobile, Baroda M-Connect)।",
        freezeChip2: "<strong>'Cards'</strong> &rarr; <strong>'Manage Debit Card'</strong> में जाएं &rarr; <strong>'Temporary Lock / Block'</strong> चालू करें।",
        freezeChip3: "<strong>'Domestic Online / E-Commerce'</strong> और <strong>'ATM Withdrawal'</strong> को बंद (OFF) कर दें।",
        freezeChip4: "<strong>'UPI Settings'</strong> में जाकर <strong>'Deregister UPI Profile'</strong> चुनें या दैनिक सीमा ₹1 कर दें।",
        officialPortalTitle: "राष्ट्रीय साइबर अपराध रिपोर्टिंग पोर्टल",
        officialPortalSub: "गृह मंत्रालय (एमएचए) द्वारा संचालित आधिकारिक भारत सरकार पोर्टल, जहां साइबर वित्तीय अपराधों की रिपोर्ट दर्ज की जाती है:",
        btnOfficialCybercrimeLink: "cybercrime.gov.in पर शिकायत दर्ज करें →",
        guardianTitle: "पारिवारिक अभिभावक संपर्क",
        guardianDesc: "अपने पुत्र, पुत्री या विश्वसनीय रिश्तेदार का मोबाइल नंबर सुरक्षित करें। BlaxGuard इसे सुरक्षित रखता है ताकि संकट के समय आप एक टैप में उन्हें सचेत कर सकें।",
        guardianPhoneLabel: "अभिभावक का मोबाइल नंबर:",
        guardianPhonePlaceholder: "+91 98765 00000",
        btnSaveGuardian: "अभिभावक संपर्क सुरक्षित करें",'''

te_help_trans = '''/* Help Page */
        helpPageTitle: "అత్యవసర సహాయం & సైబర్ మోసాల నివారణ",
        helpPageSub: "ప్రశాంతంగా ఉండండి, వేగంగా స్పందించండి. లావాదేవీలను నిలిపివేయడానికి, ఖాతాలను లాక్ చేయడానికి తక్షణ చర్యలు.",
        helpCalmTitle: "ప్రశాంతంగా ఉండండి — మీరు ఇప్పుడే రక్షణ పొందవచ్చు",
        helpCalmText: "సైబర్ మోసాలు ప్రతిరోజూ వేలాది మంది పౌరులకు ఎదురవుతాయి. మొదటి గంటలోనే తక్షణ చర్యలు తీసుకోవడం ద్వారా మోసపూరిత లావాదేవీలను నిలిపివేసి మీ డబ్బును కాపాడుకునే అవకాశం చాలా ఎక్కువ.",
        helpTapCallTitle: "తక్షణ కాల్ చేయడానికి హెల్ప్‌లైన్లు",
        helpTapCallSub: "అత్యవసర సైబర్ రక్షణ సేవలను సంప్రదించడానికి మీ ఫోన్ స్క్రీన్‌పై నేరుగా నొక్కండి:",
        btnDial1930: "1930 కి కాల్ చేయండి (సైబర్ ఫ్రాడ్ హెల్ప్‌లైన్)",
        descDial1930: "జాతీయ సైబర్ క్రైమ్ రిపోర్టింగ్ హెల్ప్‌లైన్ &bull; టోల్-ఫ్రీ 24x7",
        badgeTollFree: "టోల్ ఫ్రీ",
        btnDial112: "112 కి కాల్ చేయండి (జాతీయ అత్యవసర విభాగం)",
        descDial112: "పోలీస్ &bull; తక్షణ ప్రత్యక్ష సహాయం &bull; బెదిరింపులు / బ్లాక్‌మెయిల్",
        badge24x7: "24x7 అత్యవసరం",
        bankReminderTitle: "ముఖ్యమైన హెచ్చరిక: బ్యాంక్ అధికారిక నంబర్‌ను మాత్రమే వాడండి",
        bankReminderDesc: "<strong>గూగుల్ సెర్చ్ లేదా గూగుల్ మ్యాప్స్‌లో మీ బ్యాంక్ కస్టమర్ కేర్ నంబర్లను ఎప్పుడూ వెతకకండి</strong> — మోసగాళ్లు అక్కడ నకిలీ నంబర్లు ఉంచుతారు. మీ <strong>ATM/డెబిట్ కార్డు వెనుక వైపు</strong> లేదా బ్యాంక్ పాస్‌బుక్‌లో ఉన్న నంబర్‌కు మాత్రమే కాల్ చేయండి.",
        firstHourTitle: "డబ్బు పోగొట్టుకున్న మొదటి 60 నిమిషాలు (గోల్డెన్ అవర్)",
        firstHourSub: "వెంటనే సమాచారం ఇస్తే బ్యాంక్ అధికారులు మరియు 1930 ద్వారా నేరగాడి ఖాతాలోని డబ్బును స్తంభింపజేయవచ్చు. ఈ 5 దశలను పాటించండి:",
        step1Bold: "వెంటనే 1930 కి డయల్ చేయండి:",
        step1Text: "మీ బ్యాంక్ ఖాతా నంబర్, బ్యాంక్ పేరు, లావాదేవీ సమయం మరియు మొత్తం తెలపండి. నేరగాడు డబ్బు విత్‌డ్రా చేయకముందే ఖాతాను ఫ్రీజ్ చేయడానికి 1930 టికెట్ జారీ చేస్తుంది.",
        step2Bold: "బ్యాంక్ యాప్‌లో కార్డ్ మరియు UPI వెంటనే లాక్ చేయండి:",
        step2Text: "ఇప్పుడే మీ అధికారిక మొబైల్ బ్యాంకింగ్ యాప్ తెరవండి. కార్డ్ సెట్టింగ్స్‌కి వెళ్లి డెబిట్ కార్డును తాత్కాలికంగా బ్లాక్ చేయండి మరియు ఆన్‌లైన్ లావాదేవీలను ఆపివేయండి.",
        step3Bold: "12 అంకెల UTR నంబర్ వివరాలు భద్రపరచండి:",
        step3Text: "డబ్బు కట్ అయిన SMS మరియు UPI రసీదు స్క్రీన్‌షాట్ తీయండి. 12 అంకెల UTR/UPI నంబర్, నేరగాడి UPI ID మరియు సమయాన్ని రాసి ఉంచుకోండి.",
        step4Bold: "cybercrime.gov.in లో అధికారిక ఫిర్యాదు చేయండి:",
        step4Text: "జాతీయ సైబర్ క్రైమ్ పోర్టల్‌లో ఫిర్యాదు చేసి, బ్యాంక్ విచారణ కోసం అధికారిక అక్నాలెడ్జ్‌మెంట్ నంబర్ పొందండి.",
        step5Bold: "3 రోజుల్లోగా బ్యాంక్ బ్రాంచ్‌కు లిఖితపూర్వకంగా తెలపండి:",
        step5Text: "1930 ఫిర్యాదు నంబర్‌తో మీ బ్యాంక్ బ్రాంచ్ మేనేజర్‌కు లిఖితపూర్వక ఫిర్యాదు లేఖ ఇవ్వండి. RBI నిబంధనల ప్రకారం వెంటనే సమాచారం ఇస్తే రీఫండ్ పొందే హక్కు ఉంటుంది.",
        freezeNoteTitle: "బ్యాంక్ యాప్‌లో 30 సెకన్లలో కార్డ్ మరియు UPI ని ఎలా ఫ్రీజ్ చేయాలి",
        freezeNoteSub: "నేరగాడి వద్ద మీ కార్డ్ నంబర్ లేదా పిన్ ఉన్నప్పటికీ, బ్యాంక్ యాప్‌లో కార్డ్ వాడకాన్ని ఆపివేస్తే ఒక్క రూపాయి కూడా కట్ కాదు:",
        freezeChip1: "మీ బ్యాంక్ యాప్ తెరవండి (ఉదా. YONO SBI, HDFC MobileBanking, iMobile, Baroda M-Connect).",
        freezeChip2: "<strong>'Cards'</strong> &rarr; <strong>'Manage Debit Card'</strong> లోకి వెళ్లండి &rarr; <strong>'Temporary Lock / Block Card'</strong> ఆన్ చేయండి.",
        freezeChip3: "<strong>'Domestic Online / E-Commerce'</strong> మరియు <strong>'ATM Cash Withdrawal'</strong> స్విచ్‌లను OFF చేయండి.",
        freezeChip4: "<strong>'UPI Settings'</strong> లోకి వెళ్లి <strong>'Deregister UPI Profile'</strong> ఎంచుకోండి లేదా రోజువారీ పరిమితిని ₹1 కి తగ్గించండి.",
        officialPortalTitle: "జాతీయ సైబర్ క్రైమ్ రిపోర్టింగ్ పోర్టల్",
        officialPortalSub: "సైబర్ ఆర్థిక నేరాలను నివేదించడానికి మరియు పోలీసు ఫిర్యాదు చేయడానికి కేంద్ర హోం మంత్రిత్వ శాఖ ఆధ్వర్యంలోని అధికారిక భారత ప్రభుత్వ పోర్టల్:",
        btnOfficialCybercrimeLink: "cybercrime.gov.in లో ఫిర్యాదు చేయండి →",
        guardianTitle: "కుటుంబ సంరక్షక అత్యవసర నంబర్",
        guardianDesc: "మీ కుమారుడు, కుమార్తె లేదా నమ్మకమైన బంధువు ఫోన్ నంబర్‌ను భద్రపరచండి. అనుమానాస్పద కాల్స్ లేదా లింకులు వచ్చినప్పుడు ఒకే ట్యాప్‌తో వారికి హెచ్చరిక పంపవచ్చు.",
        guardianPhoneLabel: "సంరక్షకుడి మొబైల్ నంబర్:",
        guardianPhonePlaceholder: "+91 98765 00000",
        btnSaveGuardian: "గార్డియన్ నంబర్ సేవ్ చేయండి",'''

# Replace Help translations in bottom-up order (TE -> HI -> EN)
pos_te = template.find('te: {')
idx_te_help = template.find('helpPageTitle:', pos_te)
idx_te_admin = template.find('/* Admin Page */', idx_te_help)
if idx_te_admin == -1:
    idx_te_admin = template.find('adminPageTitle:', idx_te_help)
template = template[:idx_te_help] + te_help_trans + "\n\n        " + template[idx_te_admin:]

pos_hi = template.find('hi: {')
idx_hi_help = template.find('helpPageTitle:', pos_hi)
idx_hi_admin = template.find('/* Admin Page */', idx_hi_help)
if idx_hi_admin == -1:
    idx_hi_admin = template.find('adminPageTitle:', idx_hi_help)
template = template[:idx_hi_help] + hi_help_trans + "\n\n        " + template[idx_hi_admin:]

pos_en = template.find('en: {')
idx_en_help = template.find('helpPageTitle:', pos_en)
idx_en_admin = template.find('/* Admin Page */', idx_en_help)
if idx_en_admin == -1:
    idx_en_admin = template.find('adminPageTitle:', idx_en_help)
template = template[:idx_en_help] + en_help_trans + "\n\n        " + template[idx_en_admin:]

# 4. INITIALIZE GUARDIAN PHONE INPUT IF SAVED
if 'const savedGuardian = localStorage.getItem("blaxguard_guardian");' not in template:
    template = template.replace(
        'window.addEventListener("DOMContentLoaded", () => {',
        '''window.addEventListener("DOMContentLoaded", () => {
      const savedGuardian = localStorage.getItem("blaxguard_guardian");
      const guardianInput = document.getElementById("guardianPhoneInput");
      if (savedGuardian && guardianInput) {
        guardianInput.value = savedGuardian;
      }'''
    )

# Save template.html
with open("template.html", "w", encoding="utf-8") as f:
    f.write(template)

# Build index.html
output = template.replace("{{SHIELD_URI}}", shield_uri).replace("{{FULL_URI}}", full_uri)
with open("index.html", "w", encoding="utf-8") as f:
    f.write(output)

print(f"Generated index.html with complete Help page! File size: {os.path.getsize('index.html')} bytes")
