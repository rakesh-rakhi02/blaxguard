import json
import os
import re

with open("uris.json", "r", encoding="utf-8") as f:
    uris = json.load(f)

shield_uri = uris["shield"]
full_uri = uris["full"]

with open("template.html", "r", encoding="utf-8") as f:
    template = f.read()

# 1. ADD CSS FOR LEARN PAGE & QUIZ
learn_css = '''
    /* LEARN PAGE & QUIZ STYLES */
    .scam-guide-card {
      background: var(--bg-card);
      border: 1.5px solid var(--border-color);
      border-radius: var(--radius-md);
      padding: 18px 20px;
      margin-bottom: 16px;
      transition: all 0.25s ease;
    }
    .scam-guide-card:hover {
      border-color: var(--steel-blue);
      box-shadow: var(--shadow-sm);
    }
    .scam-card-header {
      display: flex;
      align-items: center;
      gap: 12px;
      margin-bottom: 14px;
      padding-bottom: 12px;
      border-bottom: 1px solid var(--border-color);
    }
    .scam-card-icon {
      font-size: 28px;
      line-height: 1;
      flex-shrink: 0;
    }
    .scam-card-title {
      font-size: 19px;
      font-weight: 800;
      color: var(--text-main);
      line-height: 1.3;
    }
    .scam-card-badge {
      font-size: 12px;
      font-weight: 800;
      padding: 3px 8px;
      border-radius: var(--radius-pill);
      background: var(--steel-blue-light);
      color: var(--steel-blue);
      margin-left: auto;
      white-space: nowrap;
    }
    .dark .scam-card-badge {
      color: #93c5fd;
    }
    .scam-section-block {
      margin-bottom: 12px;
    }
    .scam-section-label {
      font-size: 13.5px;
      font-weight: 800;
      display: flex;
      align-items: center;
      gap: 6px;
      margin-bottom: 4px;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }
    .scam-label-how {
      color: var(--steel-blue);
    }
    .dark .scam-label-how {
      color: #93c5fd;
    }
    .scam-label-signs {
      color: var(--verdict-caution);
    }
    .scam-label-action {
      color: var(--verdict-safe);
    }
    .scam-section-text {
      font-size: 15.5px;
      line-height: 1.5;
      color: var(--text-main);
    }

    /* QUIZ STYLES */
    .quiz-card {
      background: var(--bg-card);
      border: 2px solid var(--steel-blue-border);
      border-radius: var(--radius-md);
      padding: 20px;
      margin-top: 24px;
    }
    .quiz-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 16px;
      padding-bottom: 12px;
      border-bottom: 1px solid var(--border-color);
    }
    .quiz-title {
      font-size: 20px;
      font-weight: 800;
      color: var(--text-main);
    }
    .quiz-score-pill {
      font-size: 14px;
      font-weight: 800;
      background: var(--teal-light);
      color: var(--teal);
      padding: 5px 12px;
      border-radius: var(--radius-pill);
    }
    .dark .quiz-score-pill {
      color: #5eead4;
    }
    .quiz-q-box {
      background: var(--bg-card-subtle);
      border: 1.5px solid var(--border-color);
      border-radius: var(--radius-sm);
      padding: 16px;
      margin-bottom: 16px;
    }
    .quiz-q-num {
      font-size: 13px;
      font-weight: 800;
      color: var(--steel-blue);
      text-transform: uppercase;
      margin-bottom: 6px;
      display: block;
    }
    .dark .quiz-q-num {
      color: #93c5fd;
    }
    .quiz-q-text {
      font-size: 17px;
      font-weight: 700;
      color: var(--text-main);
      line-height: 1.45;
      margin-bottom: 14px;
    }
    .quiz-options-list {
      display: flex;
      flex-direction: column;
      gap: 10px;
    }
    .quiz-opt-btn {
      background: var(--bg-card);
      border: 1.5px solid var(--border-color);
      border-radius: var(--radius-sm);
      padding: 12px 14px;
      text-align: left;
      font-size: 15px;
      font-weight: 600;
      color: var(--text-main);
      cursor: pointer;
      transition: all 0.2s ease;
      display: flex;
      align-items: flex-start;
      gap: 10px;
      line-height: 1.4;
      font-family: inherit;
    }
    .quiz-opt-btn:hover:not(:disabled) {
      border-color: var(--steel-blue);
      background: var(--steel-blue-light);
    }
    .quiz-opt-btn.correct {
      background: var(--verdict-safe-bg) !important;
      border-color: var(--verdict-safe) !important;
      color: #ffffff !important;
    }
    .quiz-opt-btn.incorrect {
      background: var(--verdict-danger-bg) !important;
      border-color: var(--verdict-danger) !important;
      color: #ffffff !important;
    }
    .quiz-opt-btn:disabled {
      cursor: default;
      opacity: 0.95;
    }
    .quiz-feedback-box {
      margin-top: 12px;
      padding: 12px 14px;
      border-radius: var(--radius-sm);
      font-size: 14.5px;
      line-height: 1.45;
      animation: fadeIn 0.3s ease;
    }
    .feedback-correct {
      background: var(--verdict-safe-bg);
      border: 1px solid var(--verdict-safe-border);
      color: var(--text-main);
    }
    .feedback-incorrect {
      background: var(--verdict-danger-bg);
      border: 1px solid var(--verdict-danger-border);
      color: var(--text-main);
    }
    .quiz-summary-card {
      background: var(--steel-blue-light);
      border: 2px solid var(--steel-blue);
      border-radius: var(--radius-md);
      padding: 20px;
      text-align: center;
      margin-top: 16px;
      animation: fadeIn 0.4s ease;
    }
    .quiz-summary-score {
      font-size: 28px;
      font-weight: 800;
      color: var(--text-main);
      margin-bottom: 6px;
    }
    .quiz-summary-msg {
      font-size: 16px;
      color: var(--text-muted);
      margin-bottom: 16px;
    }
'''

if "/* LEARN PAGE & QUIZ STYLES */" not in template:
    pos_style_end = template.find("</style>")
    template = template[:pos_style_end] + learn_css + "\n  " + template[pos_style_end:]

# 2. REPLACE PAGE 6 LEARN HTML
learn_html = '''      <!-- ============================================== -->
      <!-- PAGE 6: LEARN (8 Scam Cards & Safety Quiz)     -->
      <!-- ============================================== -->
      <section id="page-learn" class="page-section">
        <div class="section-header">
          <h1 class="section-title">
            <span>📚</span> <span data-i18n="learnPageTitle">Scam Awareness Guide</span>
          </h1>
          <p class="section-subtitle" data-i18n="learnPageSub">
            Master the 8 most common scam tactics targeting Indian citizens and test your knowledge with the interactive quiz.
          </p>
        </div>

        <!-- 8 SHORT SCAM CARDS -->

        <!-- Card 1: Fake KYC -->
        <div class="scam-guide-card">
          <div class="scam-card-header">
            <span class="scam-card-icon">🪪</span>
            <div class="scam-card-title" data-i18n="scam1Title">1. Fake KYC Suspension Scam</div>
            <span class="scam-card-badge">KYC Trap</span>
          </div>
          <div class="scam-section-block">
            <div class="scam-section-label scam-label-how"><span>🔧</span> <span data-i18n="labelHowWorks">How it works</span></div>
            <p class="scam-section-text" data-i18n="scam1How">Fraudsters send SMS/WhatsApp saying your bank account, SIM card, or PAN link is suspended. They demand clicking an unofficial link or calling an unknown number to "complete KYC".</p>
          </div>
          <div class="scam-section-block">
            <div class="scam-section-label scam-label-signs"><span>⚠️</span> <span data-i18n="labelWarningSigns">Warning signs</span></div>
            <p class="scam-section-text" data-i18n="scam1Signs">Threatens account block within 24 hours; links ending in .xyz/.top/.live; requests NetBanking password or Aadhaar OTP on web forms.</p>
          </div>
          <div class="scam-section-block">
            <div class="scam-section-label scam-label-action"><span>🛡️</span> <span data-i18n="labelWhatToDo">What to do</span></div>
            <p class="scam-section-text" data-i18n="scam1Action">Never click links in KYC SMS. Visit your home bank branch or use the official mobile app. Legitimate banks never suspend accounts via SMS links.</p>
          </div>
          <button type="button" class="senior-voice-btn" onclick="speakScamCard(1)">
            <span>🔊</span> <span data-i18n="btnListenVoice">Listen in your language</span>
          </button>
        </div>

        <!-- Card 2: OTP Fraud -->
        <div class="scam-guide-card">
          <div class="scam-card-header">
            <span class="scam-card-icon">🔢</span>
            <div class="scam-card-title" data-i18n="scam2Title">2. OTP & Credential Theft</div>
            <span class="scam-card-badge">Credential Theft</span>
          </div>
          <div class="scam-section-block">
            <div class="scam-section-label scam-label-how"><span>🔧</span> <span data-i18n="labelHowWorks">How it works</span></div>
            <p class="scam-section-text" data-i18n="scam2How">Caller claims to be from your bank, courier delivery, or electricity board. They say an OTP was sent to confirm delivery, refund money, or cancel a penalty.</p>
          </div>
          <div class="scam-section-block">
            <div class="scam-section-label scam-label-signs"><span>⚠️</span> <span data-i18n="labelWarningSigns">Warning signs</span></div>
            <p class="scam-section-text" data-i18n="scam2Signs">Caller demands the 4 or 6-digit number on your SMS; extreme rush ("Tell me fast or session expires"); claims OTP is to "receive" money.</p>
          </div>
          <div class="scam-section-block">
            <div class="scam-section-label scam-label-action"><span>🛡️</span> <span data-i18n="labelWhatToDo">What to do</span></div>
            <p class="scam-section-text" data-i18n="scam2Action">Never share OTP with anyone, even if they claim to be police or bank manager. Read the SMS text carefully: banks explicitly write "Do NOT share with anyone".</p>
          </div>
          <button type="button" class="senior-voice-btn" onclick="speakScamCard(2)">
            <span>🔊</span> <span data-i18n="btnListenVoice">Listen in your language</span>
          </button>
        </div>

        <!-- Card 3: Fake Loan Apps -->
        <div class="scam-guide-card">
          <div class="scam-card-header">
            <span class="scam-card-icon">📱</span>
            <div class="scam-card-title" data-i18n="scam3Title">3. Predatory Fake Loan Apps</div>
            <span class="scam-card-badge">Extortion APK</span>
          </div>
          <div class="scam-section-block">
            <div class="scam-section-label scam-label-how"><span>🔧</span> <span data-i18n="labelHowWorks">How it works</span></div>
            <p class="scam-section-text" data-i18n="scam3How">Instant loan apps downloaded via APK links or social ads offer 5-minute loans without CIBIL. Upon installation, they secretly upload your entire contact book and photo gallery.</p>
          </div>
          <div class="scam-section-block">
            <div class="scam-section-label scam-label-signs"><span>⚠️</span> <span data-i18n="labelWarningSigns">Warning signs</span></div>
            <p class="scam-section-text" data-i18n="scam3Signs">Asks for Contacts and Photo permissions; deducts 40% upfront fee; threatens to morph photos and harass family after 7 days.</p>
          </div>
          <div class="scam-section-block">
            <div class="scam-section-label scam-label-action"><span>🛡️</span> <span data-i18n="labelWhatToDo">What to do</span></div>
            <p class="scam-section-text" data-i18n="scam3Action">Borrow only from RBI-registered banks and NBFCs. Never install APK files outside Google Play. Never grant Contacts or Photo permissions to lending apps.</p>
          </div>
          <button type="button" class="senior-voice-btn" onclick="speakScamCard(3)">
            <span>🔊</span> <span data-i18n="btnListenVoice">Listen in your language</span>
          </button>
        </div>

        <!-- Card 4: Digital Arrest -->
        <div class="scam-guide-card">
          <div class="scam-card-header">
            <span class="scam-card-icon">👮</span>
            <div class="scam-card-title" data-i18n="scam4Title">4. Digital Arrest & Police Impersonation</div>
            <span class="scam-card-badge">Coercion Fraud</span>
          </div>
          <div class="scam-section-block">
            <div class="scam-section-label scam-label-how"><span>🔧</span> <span data-i18n="labelHowWorks">How it works</span></div>
            <p class="scam-section-text" data-i18n="scam4How">Scammers call on WhatsApp video wearing fake police/CBI uniforms with official logos. They claim a parcel with illegal drugs or money laundering has your Aadhaar name.</p>
          </div>
          <div class="scam-section-block">
            <div class="scam-section-label scam-label-signs"><span>⚠️</span> <span data-i18n="labelWarningSigns">Warning signs</span></div>
            <p class="scam-section-text" data-i18n="scam4Signs">Threatens immediate arrest; conducts "court hearing" on Skype/video; orders you to stay on video call alone and keep secret from family.</p>
          </div>
          <div class="scam-section-block">
            <div class="scam-section-label scam-label-action"><span>🛡️</span> <span data-i18n="labelWhatToDo">What to do</span></div>
            <p class="scam-section-text" data-i18n="scam4Action">Hang up immediately. Indian Police and CBI NEVER conduct arrests, investigations, or bail proceedings over video calls. Call 1930 immediately.</p>
          </div>
          <button type="button" class="senior-voice-btn" onclick="speakScamCard(4)">
            <span>🔊</span> <span data-i18n="btnListenVoice">Listen in your language</span>
          </button>
        </div>

        <!-- Card 5: Lottery/Prize -->
        <div class="scam-guide-card">
          <div class="scam-card-header">
            <span class="scam-card-icon">🎁</span>
            <div class="scam-card-title" data-i18n="scam5Title">5. Lottery, Prize & Parcel Scam</div>
            <span class="scam-card-badge">Advance Fee</span>
          </div>
          <div class="scam-section-block">
            <div class="scam-section-label scam-label-how"><span>🔧</span> <span data-i18n="labelHowWorks">How it works</span></div>
            <p class="scam-section-text" data-i18n="scam5How">Message claims you won ₹25 Lakh in KBC lottery, a luxury car in a lucky draw, or an iPhone. To claim, you must pay "customs duty", "GST", or "processing charges" in advance.</p>
          </div>
          <div class="scam-section-block">
            <div class="scam-section-label scam-label-signs"><span>⚠️</span> <span data-i18n="labelWarningSigns">Warning signs</span></div>
            <p class="scam-section-text" data-i18n="scam5Signs">You never bought a ticket or entered any contest; demands advance deposit to unlock money; sends fake letters with forged government stamps.</p>
          </div>
          <div class="scam-section-block">
            <div class="scam-section-label scam-label-action"><span>🛡️</span> <span data-i18n="labelWhatToDo">What to do</span></div>
            <p class="scam-section-text" data-i18n="scam5Action">Remember: You can NEVER win a lottery or contest you didn't enter! Genuine prizes never demand advance money. Block the sender and report.</p>
          </div>
          <button type="button" class="senior-voice-btn" onclick="speakScamCard(5)">
            <span>🔊</span> <span data-i18n="btnListenVoice">Listen in your language</span>
          </button>
        </div>

        <!-- Card 6: UPI Collect Request -->
        <div class="scam-guide-card">
          <div class="scam-card-header">
            <span class="scam-card-icon">💸</span>
            <div class="scam-card-title" data-i18n="scam6Title">6. UPI "Collect Request" Trap</div>
            <span class="scam-card-badge">UPI Reversal</span>
          </div>
          <div class="scam-section-block">
            <div class="scam-section-label scam-label-how"><span>🔧</span> <span data-i18n="labelHowWorks">How it works</span></div>
            <p class="scam-section-text" data-i18n="scam6How">A scammer pretending to buy your item on OLX or send a refund says: "I am sending money, please scan this QR code or accept the request and enter your UPI PIN".</p>
          </div>
          <div class="scam-section-block">
            <div class="scam-section-label scam-label-signs"><span>⚠️</span> <span data-i18n="labelWarningSigns">Warning signs</span></div>
            <p class="scam-section-text" data-i18n="scam6Signs">Asking you to enter UPI PIN to "receive" money; QR code sent on WhatsApp with instructions to scan and enter PIN.</p>
          </div>
          <div class="scam-section-block">
            <div class="scam-section-label scam-label-action"><span>🛡️</span> <span data-i18n="labelWhatToDo">What to do</span></div>
            <p class="scam-section-text" data-i18n="scam6Action">Golden Rule: UPI PIN is ONLY needed to SEND money, NEVER to receive money! If anyone tells you to enter your PIN to receive money, decline the request immediately.</p>
          </div>
          <button type="button" class="senior-voice-btn" onclick="speakScamCard(6)">
            <span>🔊</span> <span data-i18n="btnListenVoice">Listen in your language</span>
          </button>
        </div>

        <!-- Card 7: Fake Customer Care -->
        <div class="scam-guide-card">
          <div class="scam-card-header">
            <span class="scam-card-icon">🎧</span>
            <div class="scam-card-title" data-i18n="scam7Title">7. Fake Customer Care & Remote Apps</div>
            <span class="scam-card-badge">Remote Access</span>
          </div>
          <div class="scam-section-block">
            <div class="scam-section-label scam-label-how"><span>🔧</span> <span data-i18n="labelHowWorks">How it works</span></div>
            <p class="scam-section-text" data-i18n="scam7How">Fraudsters post fake mobile numbers on Google Maps for banks, airlines, or delivery services. When called, they ask you to install "AnyDesk", "TeamViewer", or "QuickSupport".</p>
          </div>
          <div class="scam-section-block">
            <div class="scam-section-label scam-label-signs"><span>⚠️</span> <span data-i18n="labelWarningSigns">Warning signs</span></div>
            <p class="scam-section-text" data-i18n="scam7Signs">10-digit mobile number listed instead of 1800 toll-free; asking you to install screen-sharing apps; asking to send ₹10 to "verify" account.</p>
          </div>
          <div class="scam-section-block">
            <div class="scam-section-label scam-label-action"><span>🛡️</span> <span data-i18n="labelWhatToDo">What to do</span></div>
            <p class="scam-section-text" data-i18n="scam7Action">Always get helpline numbers directly from the official bank passbook, official app, or bank portal. Never install remote screen-sharing apps on a caller's request.</p>
          </div>
          <button type="button" class="senior-voice-btn" onclick="speakScamCard(7)">
            <span>🔊</span> <span data-i18n="btnListenVoice">Listen in your language</span>
          </button>
        </div>

        <!-- Card 8: Job/Task Scam -->
        <div class="scam-guide-card">
          <div class="scam-card-header">
            <span class="scam-card-icon">💼</span>
            <div class="scam-card-title" data-i18n="scam8Title">8. Work-From-Home & Task Scams</div>
            <span class="scam-card-badge">Prepaid Task</span>
          </div>
          <div class="scam-section-block">
            <div class="scam-section-label scam-label-how"><span>🔧</span> <span data-i18n="labelHowWorks">How it works</span></div>
            <p class="scam-section-text" data-i18n="scam8How">WhatsApp/Telegram message offering ₹3,000–₹5,000/day for liking YouTube videos or rating hotels. Small initial payout builds trust, followed by demands to invest in "prepaid crypto tasks".</p>
          </div>
          <div class="scam-section-block">
            <div class="scam-section-label scam-label-signs"><span>⚠️</span> <span data-i18n="labelWarningSigns">Warning signs</span></div>
            <p class="scam-section-text" data-i18n="scam8Signs">Work from home with unrealistically high pay; Telegram group with fake member earnings; asking you to deposit money to "unlock" your earnings.</p>
          </div>
          <div class="scam-section-block">
            <div class="scam-section-label scam-label-action"><span>🛡️</span> <span data-i18n="labelWhatToDo">What to do</span></div>
            <p class="scam-section-text" data-i18n="scam8Action">Legitimate employers NEVER ask you to pay money to get a job or task payout. Cease communication immediately as soon as a deposit is requested.</p>
          </div>
          <button type="button" class="senior-voice-btn" onclick="speakScamCard(8)">
            <span>🔊</span> <span data-i18n="btnListenVoice">Listen in your language</span>
          </button>
        </div>

        <!-- 5-QUESTION INTERACTIVE SAFETY QUIZ -->
        <div class="quiz-card" id="quizContainer">
          <div class="quiz-header">
            <div>
              <h3 class="quiz-title">
                <span>🧠</span> <span data-i18n="quizTitle">Scam Defense Safety Quiz</span>
              </h3>
              <p style="font-size: 14px; color: var(--text-muted); margin-top: 4px;" data-i18n="quizSubtitle">
                Test your instincts on 5 real-world scenarios. Immediate explanations provided!
              </p>
            </div>
            <span class="quiz-score-pill" id="quizScorePill">Score: 0 / 5</span>
          </div>

          <!-- Question 1 -->
          <div class="quiz-q-box" id="quizQBox1">
            <span class="quiz-q-num" data-i18n="quizQ1Num">Question 1 of 5</span>
            <div class="quiz-q-text" data-i18n="quizQ1Text">A buyer on OLX sends a QR code on WhatsApp and tells you: "Scan this and enter your UPI PIN to receive ₹5,000 in your bank account." What should you do?</div>
            <div class="quiz-options-list">
              <button type="button" class="quiz-opt-btn" onclick="handleQuizAnswer(1, 0)" id="q1_opt0">
                <span class="opt-letter">A</span> <span data-i18n="q1Opt0">Enter the PIN quickly before the payment link expires.</span>
              </button>
              <button type="button" class="quiz-opt-btn" onclick="handleQuizAnswer(1, 1)" id="q1_opt1">
                <span class="opt-letter">B</span> <span data-i18n="q1Opt1">Do not enter PIN. UPI PIN is only needed to SEND money, never to receive money.</span>
              </button>
              <button type="button" class="quiz-opt-btn" onclick="handleQuizAnswer(1, 2)" id="q1_opt2">
                <span class="opt-letter">C</span> <span data-i18n="q1Opt2">Send the OTP received on SMS instead.</span>
              </button>
            </div>
            <div class="quiz-feedback-box" id="q1_feedback" style="display: none;"></div>
          </div>

          <!-- Question 2 -->
          <div class="quiz-q-box" id="quizQBox2">
            <span class="quiz-q-num" data-i18n="quizQ2Num">Question 2 of 5</span>
            <div class="quiz-q-text" data-i18n="quizQ2Text">Someone on WhatsApp video wearing a police uniform claims a drug parcel has your Aadhaar name and orders you into "Digital Arrest". What is the truth?</div>
            <div class="quiz-options-list">
              <button type="button" class="quiz-opt-btn" onclick="handleQuizAnswer(2, 0)" id="q2_opt0">
                <span class="opt-letter">A</span> <span data-i18n="q2Opt0">There is no legal procedure called "Digital Arrest". Real police never arrest or interrogate over video call.</span>
              </button>
              <button type="button" class="quiz-opt-btn" onclick="handleQuizAnswer(2, 1)" id="q2_opt1">
                <span class="opt-letter">B</span> <span data-i18n="q2Opt1">Follow their instructions and transfer money to their verification account.</span>
              </button>
              <button type="button" class="quiz-opt-btn" onclick="handleQuizAnswer(2, 2)" id="q2_opt2">
                <span class="opt-letter">C</span> <span data-i18n="q2Opt2">Keep it secret from family as instructed by the officer.</span>
              </button>
            </div>
            <div class="quiz-feedback-box" id="q2_feedback" style="display: none;"></div>
          </div>

          <!-- Question 3 -->
          <div class="quiz-q-box" id="quizQBox3">
            <span class="quiz-q-num" data-i18n="quizQ3Num">Question 3 of 5</span>
            <div class="quiz-q-text" data-i18n="quizQ3Text">You receive an SMS: "Dear Customer, your bank account is suspended tonight due to pending KYC. Click http://sbi-update.xyz to verify." How should you respond?</div>
            <div class="quiz-options-list">
              <button type="button" class="quiz-opt-btn" onclick="handleQuizAnswer(3, 0)" id="q3_opt0">
                <span class="opt-letter">A</span> <span data-i18n="q3Opt0">Click the link and enter your NetBanking password.</span>
              </button>
              <button type="button" class="quiz-opt-btn" onclick="handleQuizAnswer(3, 1)" id="q3_opt1">
                <span class="opt-letter">B</span> <span data-i18n="q3Opt1">Call the 10-digit phone number given at the end of the SMS.</span>
              </button>
              <button type="button" class="quiz-opt-btn" onclick="handleQuizAnswer(3, 2)" id="q3_opt2">
                <span class="opt-letter">C</span> <span data-i18n="q3Opt2">Delete the SMS. Banks never send unofficial links or block accounts via SMS without formal branch notice.</span>
              </button>
            </div>
            <div class="quiz-feedback-box" id="q3_feedback" style="display: none;"></div>
          </div>

          <!-- Question 4 -->
          <div class="quiz-q-box" id="quizQBox4">
            <span class="quiz-q-num" data-i18n="quizQ4Num">Question 4 of 5</span>
            <div class="quiz-q-text" data-i18n="quizQ4Text">A "customer care executive" on a call asks you to download "AnyDesk" or "QuickSupport" from Google Play to fix your failed electricity payment. Is this safe?</div>
            <div class="quiz-options-list">
              <button type="button" class="quiz-opt-btn" onclick="handleQuizAnswer(4, 0)" id="q4_opt0">
                <span class="opt-letter">A</span> <span data-i18n="q4Opt0">Yes, as long as it is downloaded from the official Google Play Store.</span>
              </button>
              <button type="button" class="quiz-opt-btn" onclick="handleQuizAnswer(4, 1)" id="q4_opt1">
                <span class="opt-letter">B</span> <span data-i18n="q4Opt1">Absolutely NOT! These apps let scammers see your screen, view your OTPs, and control your phone.</span>
              </button>
              <button type="button" class="quiz-opt-btn" onclick="handleQuizAnswer(4, 2)" id="q4_opt2">
                <span class="opt-letter">C</span> <span data-i18n="q4Opt2">Yes, if they promise to disconnect in 2 minutes.</span>
              </button>
            </div>
            <div class="quiz-feedback-box" id="q4_feedback" style="display: none;"></div>
          </div>

          <!-- Question 5 -->
          <div class="quiz-q-box" id="quizQBox5">
            <span class="quiz-q-num" data-i18n="quizQ5Num">Question 5 of 5</span>
            <div class="quiz-q-text" data-i18n="quizQ5Text">An instant loan app asks for permission to access your Contacts List and Photo Gallery before approving your loan. What should you do?</div>
            <div class="quiz-options-list">
              <button type="button" class="quiz-opt-btn" onclick="handleQuizAnswer(5, 0)" id="q5_opt0">
                <span class="opt-letter">A</span> <span data-i18n="q5Opt0">Grant permission because every loan app needs to verify your identity.</span>
              </button>
              <button type="button" class="quiz-opt-btn" onclick="handleQuizAnswer(5, 1)" id="q5_opt1">
                <span class="opt-letter">B</span> <span data-i18n="q5Opt1">Uninstall the app immediately. Illegal predatory loan apps use contact and gallery access to harass and blackmail you.</span>
              </button>
              <button type="button" class="quiz-opt-btn" onclick="handleQuizAnswer(5, 2)" id="q5_opt2">
                <span class="opt-letter">C</span> <span data-i18n="q5Opt2">Grant permission only for 24 hours.</span>
              </button>
            </div>
            <div class="quiz-feedback-box" id="q5_feedback" style="display: none;"></div>
          </div>

          <!-- Quiz Summary Card (Shown when all 5 answered) -->
          <div id="quizSummaryCard" style="display: none;" class="quiz-summary-card">
            <div class="quiz-summary-score" id="quizFinalScoreDisplay">5 / 5</div>
            <div class="quiz-summary-msg" id="quizFinalMessage">🛡️ Cyber Champion! You scored 100%. You are well equipped to shield yourself and your family.</div>
            <button type="button" class="btn btn-primary" onclick="resetQuiz()" style="max-width: 280px; margin: 0 auto;">
              <span>🔄</span> <span data-i18n="btnRetakeQuiz">Retake Quiz</span>
            </button>
          </div>
        </div>
      </section>'''

pos_learn_start = template.find('<section id="page-learn"')
pos_help_start = template.find('<section id="page-help"')
template = template[:pos_learn_start] + learn_html + "\n\n      " + template[pos_help_start:]

# 3. TRANSLATIONS FOR LEARN & QUIZ
en_learn_trans = '''/* Learn Page */
        learnPageTitle: "Scam Awareness Guide",
        learnPageSub: "Master the 8 most common scam tactics targeting Indian citizens and test your knowledge with the interactive quiz.",
        labelHowWorks: "How it works",
        labelWarningSigns: "Warning signs",
        labelWhatToDo: "What to do",
        btnListenVoice: "Listen in your language",
        scam1Title: "1. Fake KYC Suspension Scam",
        scam1How: "Fraudsters send SMS/WhatsApp saying your bank account, SIM card, or PAN link is suspended. They demand clicking an unofficial link or calling an unknown number to 'complete KYC'.",
        scam1Signs: "Threatens account block within 24 hours; links ending in .xyz/.top/.live; requests NetBanking password or Aadhaar OTP on web forms.",
        scam1Action: "Never click links in KYC SMS. Visit your home bank branch or use the official mobile app. Legitimate banks never suspend accounts via SMS links.",
        scam2Title: "2. OTP & Credential Theft",
        scam2How: "Caller claims to be from your bank, courier delivery, or electricity board. They say an OTP was sent to confirm delivery, refund money, or cancel a penalty.",
        scam2Signs: "Caller demands the 4 or 6-digit number on your SMS; extreme rush ('Tell me fast or session expires'); claims OTP is to 'receive' money.",
        scam2Action: "Never share OTP with anyone, even if they claim to be police or bank manager. Read the SMS text carefully: banks explicitly write 'Do NOT share with anyone'.",
        scam3Title: "3. Predatory Fake Loan Apps",
        scam3How: "Instant loan apps downloaded via APK links or social ads offer 5-minute loans without CIBIL. Upon installation, they secretly upload your entire contact book and photo gallery.",
        scam3Signs: "Asks for Contacts and Photo permissions; deducts 40% upfront fee; threatens to morph photos and harass family after 7 days.",
        scam3Action: "Borrow only from RBI-registered banks and NBFCs. Never install APK files outside Google Play. Never grant Contacts or Photo permissions to lending apps.",
        scam4Title: "4. Digital Arrest & Police Impersonation",
        scam4How: "Scammers call on WhatsApp video wearing fake police/CBI uniforms with official logos. They claim a parcel with illegal drugs or money laundering has your Aadhaar name.",
        scam4Signs: "Threatens immediate arrest; conducts 'court hearing' on Skype/video; orders you to stay on video call alone and keep secret from family.",
        scam4Action: "Hang up immediately. Indian Police and CBI NEVER conduct arrests, investigations, or bail proceedings over video calls. Call 1930 immediately.",
        scam5Title: "5. Lottery, Prize & Parcel Scam",
        scam5How: "Message claims you won ₹25 Lakh in KBC lottery, a luxury car in a lucky draw, or an iPhone. To claim, you must pay 'customs duty', 'GST', or 'processing charges' in advance.",
        scam5Signs: "You never bought a ticket or entered any contest; demands advance deposit to unlock money; sends fake letters with forged government stamps.",
        scam5Action: "Remember: You can NEVER win a lottery or contest you didn't enter! Genuine prizes never demand advance money. Block the sender and report.",
        scam6Title: "6. UPI 'Collect Request' Trap",
        scam6How: "A scammer pretending to buy your item on OLX or send a refund says: 'I am sending money, please scan this QR code or accept the request and enter your UPI PIN'.",
        scam6Signs: "Asking you to enter UPI PIN to 'receive' money; QR code sent on WhatsApp with instructions to scan and enter PIN.",
        scam6Action: "Golden Rule: UPI PIN is ONLY needed to SEND money, NEVER to receive money! If anyone tells you to enter your PIN to receive money, decline the request immediately.",
        scam7Title: "7. Fake Customer Care & Remote Apps",
        scam7How: "Fraudsters post fake mobile numbers on Google Maps for banks, airlines, or delivery services. When called, they ask you to install 'AnyDesk', 'TeamViewer', or 'QuickSupport'.",
        scam7Signs: "10-digit mobile number listed instead of 1800 toll-free; asking you to install screen-sharing apps; asking to send ₹10 to 'verify' account.",
        scam7Action: "Always get helpline numbers directly from the official bank passbook, official app, or bank portal. Never install remote screen-sharing apps on a caller's request.",
        scam8Title: "8. Work-From-Home & Task Scams",
        scam8How: "WhatsApp/Telegram message offering ₹3,000–₹5,000/day for liking YouTube videos or rating hotels. Small initial payout builds trust, followed by demands to invest in 'prepaid crypto tasks'.",
        scam8Signs: "Work from home with unrealistically high pay; Telegram group with fake member earnings; asking you to deposit money to 'unlock' your earnings.",
        scam8Action: "Legitimate employers NEVER ask you to pay money to get a job or task payout. Cease communication immediately as soon as a deposit is requested.",
        quizTitle: "Scam Defense Safety Quiz",
        quizSubtitle: "Test your instincts on 5 real-world scenarios. Immediate explanations provided!",
        quizScoreLabel: "Score: {score} / 5",
        quizQ1Num: "Question 1 of 5",
        quizQ1Text: "A buyer on OLX sends a QR code on WhatsApp and tells you: 'Scan this and enter your UPI PIN to receive ₹5,000 in your bank account.' What should you do?",
        q1Opt0: "Enter the PIN quickly before the payment link expires.",
        q1Opt1: "Do not enter PIN. UPI PIN is only needed to SEND money, never to receive money.",
        q1Opt2: "Send the OTP received on SMS instead.",
        q1Explain: "Correct! Entering your UPI PIN will deduct money from your account, not receive it. UPI PIN is exclusively for authorizing debits.",
        quizQ2Num: "Question 2 of 5",
        quizQ2Text: "Someone on WhatsApp video wearing a police uniform claims a drug parcel has your Aadhaar name and orders you into 'Digital Arrest'. What is the truth?",
        q2Opt0: "There is no legal procedure called 'Digital Arrest'. Real police never arrest or interrogate over video call.",
        q2Opt1: "Follow their instructions and transfer money to their verification account.",
        q2Opt2: "Keep it secret from family as instructed by the officer.",
        q2Explain: "Correct! Indian Police and CBI never interrogate or arrest citizens on Skype or WhatsApp video calls. Hang up and dial 1930 immediately.",
        quizQ3Num: "Question 3 of 5",
        quizQ3Text: "You receive an SMS: 'Dear Customer, your bank account is suspended tonight due to pending KYC. Click http://sbi-update.xyz to verify.' How should you respond?",
        q3Opt0: "Click the link and enter your NetBanking password.",
        q3Opt1: "Call the 10-digit phone number given at the end of the SMS.",
        q3Opt2: "Delete the SMS. Banks never send unofficial links or block accounts via SMS without formal branch notice.",
        q3Explain: "Correct! Legitimate banks never use .xyz domains or block accounts abruptly via SMS. Always verify at your local bank branch.",
        quizQ4Num: "Question 4 of 5",
        quizQ4Text: "A 'customer care executive' on a call asks you to download 'AnyDesk' or 'QuickSupport' from Google Play to fix your failed electricity payment. Is this safe?",
        q4Opt0: "Yes, as long as it is downloaded from the official Google Play Store.",
        q4Opt1: "Absolutely NOT! These apps let scammers see your screen, view your OTPs, and control your phone.",
        q4Opt2: "Yes, if they promise to disconnect in 2 minutes.",
        q4Explain: "Correct! Screen sharing apps allow cybercriminals to watch your screen in real time, intercept OTPs, and wipe out your bank balance.",
        quizQ5Num: "Question 5 of 5",
        quizQ5Text: "An instant loan app asks for permission to access your Contacts List and Photo Gallery before approving your loan. What should you do?",
        q5Opt0: "Grant permission because every loan app needs to verify your identity.",
        q5Opt1: "Uninstall the app immediately. Illegal predatory loan apps use contact and gallery access to harass and blackmail you.",
        q5Opt2: "Grant permission only for 24 hours.",
        q5Explain: "Correct! RBI-approved lenders NEVER demand access to personal contacts or photos. This is the classic signature of extortion loan apps.",
        btnRetakeQuiz: "Retake Quiz",
        feedbackCorrect: "✅ Correct!",
        feedbackIncorrect: "❌ Incorrect!",'''

hi_learn_trans = '''/* Learn Page */
        learnPageTitle: "साइबर सुरक्षा जागरूकता गाइड",
        learnPageSub: "भारतीय नागरिकों को निशाना बनाने वाले 8 सबसे आम स्कैम को समझें और सुरक्षा क्विज़ से अपनी तैयारी परखें।",
        labelHowWorks: "यह कैसे काम करता है",
        labelWarningSigns: "चेतावनी के संकेत",
        labelWhatToDo: "बचाव के उपाय",
        btnListenVoice: "अपनी भाषा में सुनें",
        scam1Title: "1. फर्जी बैंक / सिम केवाईसी जाल",
        scam1How: "धोखेबाज एसएमएस या व्हाट्सएप भेजते हैं कि आपका बैंक खाता, सिम कार्ड या पैन कार्ड निलंबित हो गया है। वे 'केवाईसी पूरा करने' के लिए लिंक पर क्लिक करने या अनजान नंबर पर कॉल करने का दबाव बनाते हैं।",
        scam1Signs: "24 घंटे में खाता बंद होने की धमकी; .xyz/.top/.live जैसे फर्जी लिंक; वेब फॉर्म पर नेटबैंकिंग पासवर्ड या आधार ओटीपी मांगना।",
        scam1Action: "केवाईसी एसएमएस के लिंक पर कभी क्लिक न करें। हमेशा अपनी बैंक शाखा जाएं या आधिकारिक बैंक ऐप का उपयोग करें। बैंक कभी भी एसएमएस लिंक से खाते बंद नहीं करते।",
        scam2Title: "2. ओटीपी व गोपनीय पासवर्ड चोरी",
        scam2How: "कॉलर बैंक, पार्सल डिलीवरी या बिजली विभाग का अधिकारी बनकर कॉल करता है। वे दावा करते हैं कि डिलीवरी की पुष्टि करने, रिफंड पाने या जुर्माना रोकने के लिए ओटीपी बताना जरूरी है।",
        scam2Signs: "एसएमएस पर आए 4 या 6 अंकों के गुप्त कोड की मांग; जल्दी करने का दबाव ('जल्दी बताएं वरना समय समाप्त हो जाएगा'); पैसे 'पाने' के लिए ओटीपी मांगना।",
        scam2Action: "ओटीपी किसी के साथ साझा न करें, भले ही कॉलर पुलिस या बैंक मैनेजर होने का दावा करे। एसएमएस संदेश को ध्यान से पढ़ें: बैंक स्पष्ट लिखते हैं 'किसी के साथ साझा न करें'।",
        scam3Title: "3. अवैध लोन ऐप व ब्लैकमेलिंग",
        scam3How: "सोशल मीडिया या एपीके लिंक से डाउनलोड किए गए अवैध लोन ऐप बिना सिबिल के 5 मिनट में लोन देने का वादा करते हैं। इंस्टॉल होते ही वे आपकी पूरी फोन बुक और निजी फोटो चोरी कर लेते हैं।",
        scam3Signs: "फोन कॉन्टैक्ट्स और गैलरी की अनुमति मांगना; खाते में भेजने से पहले 40% फीस काट लेना; 7 दिन बाद फोटो एडिट करके परिवार को बदनाम करने की धमकी देना।",
        scam3Action: "केवल आरबीआई-पंजीकृत बैंकों व एनबीएफसी से ही लोन लें। गूगल प्ले स्टोर के बाहर से एपीके कभी इंस्टॉल न करें। लोन ऐप्स को कभी कॉन्टैक्ट्स या गैलरी की अनुमति न दें।",
        scam4Title: "4. डिजिटल अरेस्ट व पुलिस का फर्जी डर",
        scam4How: "धोखेबाज पुलिस या सीबीआई की वर्दी पहनकर व्हाट्सएप वीडियो कॉल करते हैं। वे दावा करते हैं कि आपके आधार कार्ड पर नशीली दवाओं या मनी लॉन्ड्रिंग का पार्सल पकड़ा गया है।",
        scam4Signs: "तुरंत गिरफ्तारी की धमकी; स्काइप या वीडियो पर 'अदालत की सुनवाई' का नाटक; कमरे में अकेले रहने और परिवार से छिपाने का आदेश।",
        scam4Action: "तुरंत फोन काट दें। भारतीय पुलिस और सीबीआई कभी भी वीडियो कॉल पर गिरफ्तारी, पूछताछ या जमानत की प्रक्रिया नहीं करते। तुरंत 1930 पर कॉल करें।",
        scam5Title: "5. लॉटरी, इनाम व पार्सल धोखाधड़ी",
        scam5How: "संदेश आता है कि आपने केबीसी में ₹25 लाख, लकी ड्रा में कार या उपहार जीता है। इनाम पाने के लिए पहले 'सीमा शुल्क (कस्टम्स)', 'जीएसटी' या 'फाइल चार्ज' जमा करने को कहा जाता है।",
        scam5Signs: "आपने कभी किसी लॉटरी या प्रतियोगिता में भाग नहीं लिया; पैसे पाने के लिए अग्रिम पैसे की मांग; सरकारी मुहर वाले फर्जी प्रमाणपत्र भेजना।",
        scam5Action: "याद रखें: जिसमें आपने भाग ही नहीं लिया, वह इनाम कभी नहीं जीत सकते! असली इनाम कभी पहले पैसे नहीं मांगते। नंबर को तुरंत ब्लॉक करें।",
        scam6Title: "6. यूपीआई 'कलेक्ट रिक्वेस्ट' जाल",
        scam6How: "ओएलएक्स का खरीदार या रिफंड एजेंट बनकर धोखेबाज कहता है: 'मैं आपको पैसे भेज रहा हूं, कृपया क्यूआर कोड स्कैन करें या रिक्वेस्ट स्वीकार करके अपना यूपीआई पिन डालें'।",
        scam6Signs: "पैसे 'पाने' के लिए यूपीआई पिन डालने को कहना; व्हाट्सएप पर भेजा गया क्यूआर कोड जिसे स्कैन करने को कहा जाए।",
        scam6Action: "सुनहरा नियम: यूपीआई पिन केवल पैसे भेजने के लिए होता है, पैसे पाने के लिए कभी नहीं! यदि कोई पैसे देने के लिए पिन मांगे, तो तुरंत मना कर दें।",
        scam7Title: "7. फर्जी कस्टमर केयर व स्क्रीन शेयरिंग",
        scam7How: "गूगल सर्च या मैप्स पर धोखेबाज बैंकों, कोरियर या गैस कंपनियों के नाम पर फर्जी मोबाइल नंबर डाल देते हैं। कॉल करने पर वे 'AnyDesk' या 'QuickSupport' डाउनलोड करवाते हैं।",
        scam7Signs: "टोल-फ्री 1800 के बजाय 10 अंकों का मोबाइल नंबर; स्क्रीन शेयरिंग ऐप डाउनलोड करने का दबाव; जांच के नाम पर ₹10 भेजने को कहना।",
        scam7Action: "हेल्पलाइन नंबर हमेशा अपनी पासबुक, आधिकारिक ऐप या सत्यापित वेबसाइट से लें। फोन पर किसी के कहने पर कभी भी रिमोट ऐप इंस्टॉल न करें।",
        scam8Title: "8. वर्क फ्रॉम होम व यूट्यूब लाइक स्कैम",
        scam8How: "व्हाट्सएप/टेलीग्राम पर यूट्यूब वीडियो लाइक करने या होटल रेटिंग देने के लिए रोजाना ₹3,000–₹5,000 देने का लालच। शुरुआत में छोटे भुगतान करके भरोसा जीतते हैं, फिर बड़ा निवेश मांगते हैं।",
        scam8Signs: "बिना मेहनत अत्यधिक कमाई का वादा; टेलीग्राम ग्रुप में फर्जी मुनाफे के स्क्रीनशॉट; पैसे निकालने के लिए पहले पैसे जमा करने की शर्त।",
        scam8Action: "सच्ची कंपनियां कभी नौकरी देने या पैसे कमाने के लिए अग्रिम पैसे नहीं मांगतीं। पैसे जमा करने की मांग आते ही बातचीत तुरंत बंद कर दें।",
        quizTitle: "साइबर सुरक्षा जांच क्विज़",
        quizSubtitle: "5 वास्तविक परिदृश्यों में अपनी समझ परखें। प्रत्येक उत्तर के साथ तत्काल सही व्याख्या प्राप्त करें!",
        quizScoreLabel: "अंक: {score} / 5",
        quizQ1Num: "प्रश्न 1 / 5",
        quizQ1Text: "ओएलएक्स का खरीदार व्हाट्सएप पर क्यूआर कोड भेजकर कहता है: 'इसे स्कैन करके यूपीआई पिन डालें ताकि आपके खाते में ₹5,000 जमा हो सकें।' आपको क्या करना चाहिए?",
        q1Opt0: "भुगतान लिंक समाप्त होने से पहले तुरंत पिन दर्ज करें।",
        q1Opt1: "पिन दर्ज न करें। यूपीआई पिन केवल पैसे भेजने के लिए होता है, पाने के लिए कभी नहीं।",
        q1Opt2: "पिन के स्थान पर एसएमएस पर आया ओटीपी भेजें।",
        q1Explain: "सही! यूपीआई पिन डालते ही आपके खाते से पैसे कट जाएंगे। पैसे प्राप्त करने के लिए किसी पिन की आवश्यकता नहीं होती।",
        quizQ2Num: "प्रश्न 2 / 5",
        quizQ2Text: "पुलिस की वर्दी पहने एक व्यक्ति व्हाट्सएप वीडियो कॉल पर दावा करता है कि आपके नाम से ड्रग्स का पार्सल मिला है और आपको 'डिजिटल अरेस्ट' किया गया है। सच्चाई क्या है?",
        q2Opt0: "'डिजिटल अरेस्ट' नाम की कोई कानूनी प्रक्रिया नहीं है। असली पुलिस कभी वीडियो कॉल पर पूछताछ या गिरफ्तारी नहीं करती।",
        q2Opt1: "उनके निर्देश मानें और सत्यापन खाते में पैसे ट्रांसफर करें।",
        q2Opt2: "अधिकारी के कहे अनुसार इसे परिवार से गुप्त रखें।",
        q2Explain: "सही! कानून प्रवर्तन एजेंसियां वीडियो कॉल पर कभी भी जांच या गिरफ्तारी नहीं करतीं। तुरंत फोन काटें और 1930 डायल करें।",
        quizQ3Num: "प्रश्न 3 / 5",
        quizQ3Text: "आपको एक एसएमएस मिलता है: 'केवाईसी लंबित होने के कारण आपका बैंक खाता आज रात बंद हो जाएगा। सत्यापित करने के लिए http://sbi-update.xyz पर क्लिक करें।' आपको क्या करना चाहिए?",
        q3Opt0: "लिंक पर क्लिक करें और नेटबैंकिंग पासवर्ड दर्ज करें।",
        q3Opt1: "एसएमएस में दिए गए 10 अंकों के मोबाइल नंबर पर कॉल करें।",
        q3Opt2: "एसएमएस डिलीट करें। बैंक कभी भी अनधिकृत लिंक नहीं भेजते और न ही बिना सूचना खाता ब्लॉक करते हैं।",
        q3Explain: "सही! बैंक कभी भी .xyz डोमेन का उपयोग नहीं करते। किसी भी संदेह की स्थिति में हमेशा अपनी बैंक शाखा से संपर्क करें।",
        quizQ4Num: "प्रश्न 4 / 5",
        quizQ4Text: "बिजली बिल भुगतान की समस्या ठीक करने के लिए एक 'कस्टमर केयर' अधिकारी आपसे प्ले स्टोर से 'AnyDesk' डाउनलोड करने को कहता है। क्या यह सुरक्षित है?",
        q4Opt0: "हां, क्योंकि यह आधिकारिक गूगल प्ले स्टोर से डाउनलोड हो रहा है।",
        q4Opt1: "बिल्कुल नहीं! ये ऐप धोखेबाजों को आपकी स्क्रीन देखने, ओटीपी पढ़ने और फोन नियंत्रित करने की अनुमति देते हैं।",
        q4Opt2: "हां, यदि वे 2 मिनट में डिस्कनेक्ट करने का वादा करते हैं।",
        q4Explain: "सही! स्क्रीन शेयरिंग ऐप से धोखेबाज आपके ओटीपी सीधे देख सकते हैं और आपके खाते से सारे पैसे निकाल सकते हैं।",
        quizQ5Num: "प्रश्न 5 / 5",
        quizQ5Text: "एक लोन ऐप लोन स्वीकृत करने से पहले आपके फोन कॉन्टैक्ट्स और फोटो गैलरी की अनुमति मांगता है। आपको क्या करना चाहिए?",
        q5Opt0: "अनुमति दें क्योंकि हर लोन ऐप को पहचान सत्यापन की आवश्यकता होती है।",
        q5Opt1: "ऐप को तुरंत अनइंस्टॉल करें। अवैध लोन ऐप कॉन्टैक्ट्स और फोटो का उपयोग ब्लैकमेल करने के लिए करते हैं।",
        q5Opt2: "केवल 24 घंटों के लिए अनुमति दें।",
        q5Explain: "सही! आरबीआई-अनुमोदित वित्तीय संस्थान कभी भी व्यक्तिगत कॉन्टैक्ट्स या फोटो गैलरी की मांग नहीं करते।",
        btnRetakeQuiz: "पुनः क्विज़ दें",
        feedbackCorrect: "✅ सही उत्तर!",
        feedbackIncorrect: "❌ गलत उत्तर!",'''

te_learn_trans = '''/* Learn Page */
        learnPageTitle: "సైబర్ భద్రతా మార్గదర్శిని",
        learnPageSub: "భారతీయ పౌరులను లక్ష్యంగా చేసుకునే 8 ప్రధాన సైబర్ మోసాలను తెలుసుకోండి మరియు భద్రతా క్విజ్ ద్వారా మీ పరిజ్ఞానాన్ని పరీక్షించుకోండి.",
        labelHowWorks: "ఇది ఎలా జరుగుతుంది",
        labelWarningSigns: "హెచ్చరిక సంకేతాలు",
        labelWhatToDo: "ఏమి చేయాలి",
        btnListenVoice: "మీ భాషలో వినండి",
        scam1Title: "1. నకిలీ బ్యాంక్ / సిమ్ KYC మోసం",
        scam1How: "మీ బ్యాంక్ ఖాతా లేదా సిమ్ కార్డ్ నిలిపివేయబడిందని నేరగాళ్లు సందేశం పంపుతారు. 'KYC పూర్తి చేయడానికి' అనధికారిక లింక్‌పై క్లిక్ చేయాలని లేదా నంబర్‌కు కాల్ చేయాలని ఒత్తిడి చేస్తారు.",
        scam1Signs: "24 గంటల్లో ఖాతా బ్లాక్ అవుతుందనే బెదిరింపు; .xyz/.top/.live వంటి నకిలీ లింకులు; వెబ్‌సైట్‌లో పాస్‌వర్డ్ లేదా ఆధార్ OTP అడగడం.",
        scam1Action: "KYC SMS లోని లింక్‌లపై ఎప్పుడూ క్లిక్ చేయవద్దు. మీ బ్యాంక్ బ్రాంచ్‌ను సంప్రదించండి లేదా అధికారిక యాప్‌ను మాత్రమే ఉపయోగించండి.",
        scam2Title: "2. OTP మరియు రహస్య పిన్ చోరీ",
        scam2How: "బ్యాంక్ మేనేజర్ లేదా కొరియర్ డెలివరీ బాయ్ అని చెప్పి కాల్ చేస్తారు. డెలివరీ నిర్ధారణకు లేదా రిఫండ్ డబ్బు జమ చేయడానికి OTP చెప్పాలని కోరతారు.",
        scam2Signs: "SMS లో వచ్చిన 4 లేదా 6 అంకెల OTP ని అడగడం; తీవ్రమైన తొందరపెట్టడం ('వెంటనే చెప్పండి లేకపోతే రద్దవుతుంది'); డబ్బు 'రావడానికి' OTP అడగడం.",
        scam2Action: "పోలీసులైనా లేదా బ్యాంక్ అధికారులైనా ఎవరితోనూ OTP ని పంచుకోవద్దు. బ్యాంకులు 'ఎవరికీ చెప్పవద్దు' అని స్పష్టంగా రాస్తాయి.",
        scam3Title: "3. వేధింపుల నకిలీ లోన్ యాప్‌లు",
        scam3How: "సిబిల్ స్కోర్ లేకుండా 5 నిమిషాల్లో లోన్ ఇస్తామని సోషల్ మీడియా లింకుల ద్వారా యాప్‌లను డౌన్‌లోడ్ చేయిస్తారు. ఇన్‌స్టాల్ చేయగానే మీ కాంటాక్ట్‌లు మరియు ప్రైవేట్ ఫోటోలను దొంగిలిస్తారు.",
        scam3Signs: "కాంటాక్ట్‌లు, ఫోటో గ్యాలరీ అనుమతులు అడగడం; ముందుగానే 40% ఫీజు మినహాయించడం; 7 రోజుల తర్వాత ఫోటోలు మార్ఫింగ్ చేసి బంధువులను వేధిస్తామని బెదిరించడం.",
        scam3Action: "RBI ఆమోదిత బ్యాంకులు లేదా NBFC ల నుండి మాత్రమే రుణాలు తీసుకోండి. గూగుల్ ప్లే స్టోర్ వెలుపల APK ఫైళ్లను ఇన్‌స్టాల్ చేయవద్దు.",
        scam4Title: "4. డిజిటల్ అరెస్ట్ మరియు నకిలీ పోలీస్ కాల్",
        scam4How: "పోలీస్ లేదా సీబీఐ యూనిఫాం ధరించి వాట్సాప్ వీడియో కాల్ చేస్తారు. మీ ఆధార్ కార్డు పేరుతో డ్రగ్స్ పార్సిల్ పట్టుబడిందని, మిమ్మల్ని అరెస్ట్ చేస్తామని భయపెడతారు.",
        scam4Signs: "వెంటనే అరెస్ట్ చేస్తామని బెదిరించడం; స్కైప్ లేదా వీడియోలో నకిలీ కోర్టు విచారణ; గదిలో ఒంటరిగా ఉండాలని, కుటుంబానికి చెప్పవద్దని ఆజ్ఞాపించడం.",
        scam4Action: "వెంటనే కాల్ కట్ చేయండి. భారత పోలీసులు లేదా సీబీఐ వీడియో కాల్స్‌లో ఎప్పుడూ అరెస్టులు లేదా విచారణలు చేయరు. వెంటనే 1930 కి కాల్ చేయండి.",
        scam5Title: "5. లాటరీ, బహుమతులు మరియు కొరియర్ మోసం",
        scam5How: "మీరు KBC లాటరీలో ₹25 లక్షలు లేదా లక్కీ డ్రాలో కారు గెలుచుకున్నారని సందేశం వస్తుంది. బహుమతిని క్లెయిమ్ చేసుకోవడానికి ముందుగా 'కస్టమ్స్ డ్యూటీ' లేదా 'రిజిస్ట్రేషన్ ఫీజు' కట్టాలని అడుగుతారు.",
        scam5Signs: "మీరు అసలు ఎలాంటి లాటరీ టికెట్ కొనలేదు; డబ్బు రావడానికి ముందుగానే డబ్బు కట్టాలనడం; నకిలీ ప్రభుత్వ ముద్రలతో కూడిన పత్రాలు పంపడం.",
        scam5Action: "గుర్తుంచుకోండి: మీరు పాల్గొనని పోటీలో ఎప్పుడూ బహుమతి గెలవలేరు! నిజమైన బహుమతులు ఎప్పుడూ ముందస్తు రుసుము అడగవు.",
        scam6Title: "6. UPI 'కలెక్ట్ రిక్వెస్ట్' ఉచ్చు",
        scam6How: "OLX కొనుగోలుదారుగా నటిస్తూ: 'నేను మీకు డబ్బులు పంపుతున్నాను, దయచేసి ఈ QR కోడ్ స్కాన్ చేసి మీ UPI పిన్ నమోదు చేయండి' అని నమ్మిస్తారు.",
        scam6Signs: "డబ్బు 'పొందడానికి' UPI పిన్ ఎంటర్ చేయాలని చెప్పడం; వాట్సాప్‌లో QR కోడ్ పంపి స్కాన్ చేయమనడం.",
        scam6Action: "బంగారు నియమం: UPI పిన్ అనేది కేవలం డబ్బులు పంపడానికి మాత్రమే, డబ్బులు తీసుకోవడానికి ఎప్పుడూ కాదు! ఎవరైనా పిన్ అడిగితే వెంటనే తిరస్కరించండి.",
        scam7Title: "7. నకిలీ కస్టమర్ కేర్ మరియు రిమోట్ యాప్‌లు",
        scam7How: "గూగుల్ సెర్చ్‌లో బ్యాంకులు, ఎయిర్‌లైన్స్ లేదా కొరియర్ సేవల పేరుతో నేరగాళ్లు నకిలీ నంబర్లు ఉంచుతారు. కాల్ చేసినప్పుడు 'AnyDesk' లేదా 'QuickSupport' డౌన్‌లోడ్ చేయమంటారు.",
        scam7Signs: "1800 టోల్-ఫ్రీ బదులుగా 10 అంకెల మొబైల్ నంబర్ ఉండటం; స్క్రీన్-షేరింగ్ యాప్‌లను డౌన్‌లోడ్ చేయమనడం; ఖాతా తనిఖీకి ₹10 పంపమనడం.",
        scam7Action: "హెల్ప్‌లైన్ నంబర్లను ఎల్లప్పుడూ మీ అధికారిక బ్యాంక్ పాస్‌బుక్ లేదా యాప్ నుండి మాత్రమే పొందండి. ఫోన్ కాల్‌లో ఎప్పుడూ స్క్రీన్ షేరింగ్ యాప్‌లను ఇన్‌స్టాల్ చేయవద్దు.",
        scam8Title: "8. వర్క్ ఫ్రమ్ హోమ్ మరియు యూట్యూబ్ టాస్క్ స్కామ్",
        scam8How: "యూట్యూబ్ వీడియోలను లైక్ చేయడానికి రోజుకు ₹3,000–₹5,000 ఇస్తామని వాట్సాప్/టెలిగ్రామ్ మెసేజ్ పంపుతారు. మొదట్లో చిన్న చెల్లింపులు చేసి నమ్మకం కుదిర్చి, ఆపై క్రిప్టో టాస్క్‌లలో పెట్టుబడి పెట్టమంటారు.",
        scam8Signs: "సులభంగా ఎక్కువ డబ్బు వస్తుందని చెప్పడం; టెలిగ్రామ్ గ్రూపుల్లో నకిలీ లాభాల స్క్రీన్‌షాట్లు; సంపాదించిన డబ్బు తీసుకోవడానికి ముందే డబ్బు కట్టమనడం.",
        scam8Action: "నిజమైన కంపెనీలు ఉద్యోగం లేదా చెల్లింపు ఇవ్వడానికి ఎప్పుడూ డబ్బులు అడగవు. డిపాజిట్ అడిగిన వెంటనే మెసేజ్‌లను నిలిపివేయండి.",
        quizTitle: "సైబర్ రక్షణ భద్రతా క్విజ్",
        quizSubtitle: "5 నిజ జీవిత సమస్యలలో మీ సామర్థ్యాన్ని పరీక్షించుకోండి. ప్రతి సమాధానానికి తక్షణ వివరణ లభిస్తుంది!",
        quizScoreLabel: "స్కోరు: {score} / 5",
        quizQ1Num: "ప్రశ్న 1 / 5",
        quizQ1Text: "OLX కొనుగోలుదారు వాట్సాప్‌లో QR కోడ్ పంపి: 'దీన్ని స్కాన్ చేసి UPI పిన్ నమోదు చేస్తే మీ ఖాతాలో ₹5,000 జమవుతాయి' అని చెప్పాడు. మీరు ఏమి చేయాలి?",
        q1Opt0: "సమయం ముగిసేలోపు త్వరగా పిన్ నమోదు చేయాలి.",
        q1Opt1: "పిన్ నమోదు చేయకూడదు. UPI పిన్ అనేది డబ్బులు పంపడానికి మాత్రమే, తీసుకోవడానికి కాదు.",
        q1Opt2: "పిన్ బదులుగా SMS లో వచ్చిన OTP ని పంపాలి.",
        q1Explain: "సరైన సమాధానం! UPI పిన్ నమోదు చేస్తే మీ ఖాతా నుండి డబ్బులు కట్ అవుతాయి. డబ్బులు రావడానికి ఎలాంటి పిన్ అవసరం లేదు.",
        quizQ2Num: "ప్రశ్న 2 / 5",
        quizQ2Text: "పోలీస్ యూనిఫాం ధరించిన వ్యక్తి వాట్సాప్ వీడియో కాల్‌లో మీ ఆధార్‌తో డ్రగ్స్ పట్టుబడ్డాయని, మీరు 'డిజిటల్ అరెస్ట్' లో ఉన్నారని బెదిరించాడు. నిజం ఏమిటి?",
        q2Opt0: "'డిజిటల్ అరెస్ట్' అనే చట్టపరమైన విధానం లేదు. నిజమైన పోలీసులు వీడియో కాల్‌లో అరెస్టులు చేయరు.",
        q2Opt1: "వారి మాటలు విని పరిశీలన ఖాతాకు డబ్బులు బదిలీ చేయాలి.",
        q2Opt2: "అధికారి చెప్పినట్లు కుటుంబానికి చెప్పకుండా రహస్యంగా ఉంచాలి.",
        q2Explain: "సరైన సమాధానం! పోలీసులు వీడియో కాల్ ద్వారా విచారణ లేదా అరెస్టులు చేయరు. వెంటనే ఫోన్ కట్ చేసి 1930 కి కాల్ చేయండి.",
        quizQ3Num: "ప్రశ్న 3 / 5",
        quizQ3Text: "మీకు ఒక SMS వచ్చింది: 'KYC పెండింగ్‌లో ఉన్నందున మీ బ్యాంక్ ఖాతా నిలిపివేయబడుతుంది. ధృవీకరించడానికి http://sbi-update.xyz పై క్లిక్ చేయండి.' మీరు ఎలా స్పందించాలి?",
        q3Opt0: "లింక్‌పై క్లిక్ చేసి నెట్‌బ్యాంకింగ్ పాస్‌వర్డ్ నమోదు చేయాలి.",
        q3Opt1: "SMS లో ఇచ్చిన 10 అంకెల మొబైల్ నంబర్‌కు కాల్ చేయాలి.",
        q3Opt2: "SMS ను తొలగించాలి. బ్యాంకులు ఎప్పుడూ అనధికారిక లింకులు పంపవు లేదా నోటీసు లేకుండా ఖాతా బ్లాక్ చేయవు.",
        q3Explain: "సరైన సమాధానం! బ్యాంకులు ఎప్పుడూ .xyz డొమైన్‌లను ఉపయోగించవు. అనుమానం ఉంటే నేరుగా బ్యాంక్ బ్రాంచ్‌ను సంప్రదించండి.",
        quizQ4Num: "ప్రశ్న 4 / 5",
        quizQ4Text: "విద్యుత్ బిల్లు సమస్యను పరిష్కరించడానికి ఒక 'కస్టమర్ కేర్' వ్యక్తి ప్లే స్టోర్ నుండి 'AnyDesk' డౌన్‌లోడ్ చేయమని అడిగాడు. ఇది సురక్షితమేనా?",
        q4Opt0: "అవును, గూగుల్ ప్లే స్టోర్ నుండి డౌన్‌లోడ్ చేస్తున్నందున సురక్షితమే.",
        q4Opt1: "ఖచ్చితంగా కాదు! ఈ యాప్‌ల ద్వారా నేరగాళ్లు మీ స్క్రీన్‌ను చూసి, OTP లను దొంగిలించి ఫోన్‌ను నియంత్రించగలరు.",
        q4Opt2: "అవును, 2 నిమిషాల్లో తీసివేస్తే పర్వాలేదు.",
        q4Explain: "సరైన సమాధానం! స్క్రీన్ షేరింగ్ యాప్‌ల ద్వారా సైబర్ నేరగాళ్లు మీ OTP లను ప్రత్యక్షంగా చూసి బ్యాంక్ ఖాతా ఖాళీ చేస్తారు.",
        quizQ5Num: "ప్రశ్న 5 / 5",
        quizQ5Text: "ఒక లోన్ యాప్ రుణం ఇచ్చే ముందు మీ కాంటాక్ట్‌లు మరియు ఫోటో గ్యాలరీ అనుమతులను అడిగింది. మీరు ఏమి చేయాలి?",
        q5Opt0: "ప్రతి లోన్ యాప్ గుర్తింపు ధృవీకరణ అడుగుతుంది కాబట్టి అనుమతి ఇవ్వాలి.",
        q5Opt1: "యాప్‌ను వెంటనే అన్‌ఇన్‌స్టాల్ చేయాలి. నకిలీ లోన్ యాప్‌లు బ్లాక్‌మెయిల్ చేయడానికి వీటిని వాడతాయి.",
        q5Opt2: "కేవలం 24 గంటలకు మాత్రమే అనుమతి ఇవ్వాలి.",
        q5Explain: "సరైన సమాధానం! RBI ఆమోదిత సంస్థలు వ్యక్తిగత కాంటాక్ట్‌లు లేదా ప్రైవేట్ ఫోటోలను ఎప్పుడూ అడగవు.",
        btnRetakeQuiz: "మళ్లీ క్విజ్ రాయండి",
        feedbackCorrect: "✅ సరైన సమాధానం!",
        feedbackIncorrect: "❌ తప్పు సమాధానం!",'''

# Replace Learn translations in template bottom-up (TE -> HI -> EN)
pos_te = template.find('te: {')
idx_te_learn = template.find('learnPageTitle:', pos_te)
idx_te_help = template.find('helpPageTitle:', pos_te)
template = template[:idx_te_learn] + te_learn_trans + "\n\n        " + template[idx_te_help:]

pos_hi = template.find('hi: {')
idx_hi_learn = template.find('learnPageTitle:', pos_hi)
idx_hi_help = template.find('helpPageTitle:', pos_hi)
template = template[:idx_hi_learn] + hi_learn_trans + "\n\n        " + template[idx_hi_help:]

pos_en = template.find('en: {')
idx_en_learn = template.find('learnPageTitle:', pos_en)
idx_en_help = template.find('helpPageTitle:', pos_en)
template = template[:idx_en_learn] + en_learn_trans + "\n\n        " + template[idx_en_help:]

# 4. ADD QUIZ CONTROLLER AND SPEAK SCAM CARD IN JAVASCRIPT
quiz_controller_js = '''    /* ============================================================== */
    /* LEARN PAGE: 5-QUESTION SAFETY QUIZ CONTROLLER & AUDIO ASSISTANT */
    /* ============================================================== */
    const quizAnswers = {
      1: 1, // Q1 correct option index (B)
      2: 0, // Q2 correct option index (A)
      3: 2, // Q3 correct option index (C)
      4: 1, // Q4 correct option index (B)
      5: 1  // Q5 correct option index (B)
    };

    let userQuizResponses = {};
    let currentQuizScore = 0;

    function handleQuizAnswer(qNum, selectedIndex) {
      if (userQuizResponses[qNum] !== undefined) return; // already answered

      userQuizResponses[qNum] = selectedIndex;
      const isCorrect = (selectedIndex === quizAnswers[qNum]);
      if (isCorrect) currentQuizScore++;

      // Update button visual states
      for (let i = 0; i <= 2; i++) {
        const btn = document.getElementById(`q${qNum}_opt${i}`);
        if (!btn) continue;
        btn.disabled = true;
        if (i === quizAnswers[qNum]) {
          btn.classList.add("correct");
        } else if (i === selectedIndex && !isCorrect) {
          btn.classList.add("incorrect");
        }
      }

      // Show feedback box
      const fbBox = document.getElementById(`q${qNum}_feedback`);
      const dict = translations[currentLang] || translations.en;
      if (fbBox) {
        fbBox.style.display = "block";
        fbBox.className = `quiz-feedback-box ${isCorrect ? 'feedback-correct' : 'feedback-incorrect'}`;
        const headerText = isCorrect ? (dict.feedbackCorrect || "✅ Correct!") : (dict.feedbackIncorrect || "❌ Incorrect!");
        const explainText = dict[`q${qNum}Explain`] || "";
        fbBox.innerHTML = `
          <div style="font-weight: 800; font-size: 15px; margin-bottom: 4px;">${headerText}</div>
          <div style="font-size: 14px;">${explainText}</div>
        `;
      }

      // Update Score Pill
      const scorePill = document.getElementById("quizScorePill");
      if (scorePill) {
        scorePill.textContent = (dict.quizScoreLabel || "Score: {score} / 5").replace("{score}", currentQuizScore);
      }

      // Check if all 5 answered
      if (Object.keys(userQuizResponses).length === 5) {
        showQuizSummary();
      }
    }

    function showQuizSummary() {
      const summaryCard = document.getElementById("quizSummaryCard");
      const scoreDisplay = document.getElementById("quizFinalScoreDisplay");
      const msgDisplay = document.getElementById("quizFinalMessage");
      const dict = translations[currentLang] || translations.en;

      if (!summaryCard) return;
      summaryCard.style.display = "block";

      if (scoreDisplay) {
        scoreDisplay.textContent = `${currentQuizScore} / 5`;
      }

      if (msgDisplay) {
        if (currentQuizScore === 5) {
          msgDisplay.textContent = currentLang === 'hi'
            ? "🛡️ शानदार! आपने 5/5 अंक प्राप्त किए। आप और आपका परिवार पूरी तरह सुरक्षित हैं!"
            : (currentLang === 'te'
              ? "🛡️ అద్భుతం! మీరు 5/5 స్కోర్ సాధించారు. సైబర్ మోసాల నుండి మీ కుటుంబం సురక్షితంగా ఉంటుంది!"
              : "🛡️ Cyber Champion! You scored 5/5. You are well equipped to shield yourself and your family.");
        } else if (currentQuizScore >= 3) {
          msgDisplay.textContent = currentLang === 'hi'
            ? "👍 अच्छा प्रयास! आपने बुनियादी नियम समझ लिए हैं। ऊपर दिए गए 8 कार्ड्स एक बार और पढ़ें।"
            : (currentLang === 'te'
              ? "👍 మంచి ప్రయత్నం! ప్రాథమిక నియమాలు అర్థమయ్యాయి. పూర్తి భద్రత కోసం పై 8 కార్డులను చదవండి."
              : "👍 Well Done! You understand the key rules. Review the cards above to stay 100% scam-proof.");
        } else {
          msgDisplay.textContent = currentLang === 'hi'
            ? "⚠️ अभ्यास जारी रखें! ऊपर दिए गए 8 कार्ड्स को ध्यानपूर्वक पढ़ें और दोबारा क्विज़ दें।"
            : (currentLang === 'te'
              ? "⚠️ సాధన అవసరం! పైన ఉన్న 8 కార్డులను జాగ్రత్తగా చదివి మళ్లీ ప్రయత్నించండి."
              : "⚠️ Practice Needed! Read through the 8 scam cards above carefully and retake the quiz.");
        }
      }

      summaryCard.scrollIntoView({ behavior: "smooth", block: "nearest" });
    }

    function resetQuiz() {
      userQuizResponses = {};
      currentQuizScore = 0;

      const dict = translations[currentLang] || translations.en;
      const scorePill = document.getElementById("quizScorePill");
      if (scorePill) {
        scorePill.textContent = (dict.quizScoreLabel || "Score: {score} / 5").replace("{score}", 0);
      }

      for (let q = 1; q <= 5; q++) {
        for (let i = 0; i <= 2; i++) {
          const btn = document.getElementById(`q${q}_opt${i}`);
          if (btn) {
            btn.disabled = false;
            btn.classList.remove("correct", "incorrect");
          }
        }
        const fbBox = document.getElementById(`q${q}_feedback`);
        if (fbBox) fbBox.style.display = "none";
      }

      const summaryCard = document.getElementById("quizSummaryCard");
      if (summaryCard) summaryCard.style.display = "none";

      const quizContainer = document.getElementById("quizContainer");
      if (quizContainer) quizContainer.scrollIntoView({ behavior: "smooth", block: "start" });
    }

    /* AUDIO READOUT FOR 8 SCAM CARDS */
    function speakScamCard(scamNum) {
      if (!("speechSynthesis" in window)) return;
      window.speechSynthesis.cancel();

      const dict = translations[currentLang] || translations.en;
      const title = dict[`scam${scamNum}Title`] || "";
      const action = dict[`scam${scamNum}Action`] || "";
      const textToSpeak = `${title}. ${dict.labelWhatToDo || "What to do"}: ${action}`;

      let langCode = "en-IN";
      if (currentLang === "hi") langCode = "hi-IN";
      else if (currentLang === "te") langCode = "te-IN";

      const utterance = new SpeechSynthesisUtterance(textToSpeak);
      utterance.lang = langCode;
      utterance.rate = 0.9;
      window.speechSynthesis.speak(utterance);
    }
'''

# Replace old speakRule function with new quiz controller and speakScamCard
pos_old_sr = template.find('function speakRule(')
pos_sr_end = template.find('/* INITIALIZATION */', pos_old_sr)
template = template[:pos_old_sr] + quiz_controller_js + "\n\n    " + template[pos_sr_end:]

# Save updated template.html
with open("template.html", "w", encoding="utf-8") as f:
    f.write(template)

# Build index.html
output = template.replace("{{SHIELD_URI}}", shield_uri).replace("{{FULL_URI}}", full_uri)
with open("index.html", "w", encoding="utf-8") as f:
    f.write(output)

print(f"Generated index.html with complete Learn page & 5-question quiz! File size: {os.path.getsize('index.html')} bytes")
