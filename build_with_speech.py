import json
import os
import re

with open("uris.json", "r", encoding="utf-8") as f:
    uris = json.load(f)

shield_uri = uris["shield"]
full_uri = uris["full"]

with open("template.html", "r", encoding="utf-8") as f:
    template = f.read()

# 1. ADD CSS FOR AUDIO DOCK, TOAST & INLINE SPEAKER BUTTONS
audio_css = '''
    /* AUDIO CONTROLLER DOCK & TOAST */
    .audio-control-dock {
      position: fixed;
      bottom: 78px;
      left: 50%;
      transform: translateX(-50%);
      width: calc(100% - 24px);
      max-width: 650px;
      z-index: 250;
      background: var(--topbar-bg);
      border: 2px solid var(--steel-blue);
      border-radius: var(--radius-md);
      box-shadow: 0 8px 30px rgba(0, 0, 0, 0.45);
      padding: 10px 14px;
      animation: slideUpAudio 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    }
    @keyframes slideUpAudio {
      from { transform: translate(-50%, 40px); opacity: 0; }
      to { transform: translate(-50%, 0); opacity: 1; }
    }
    .audio-dock-content {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 10px;
    }
    .audio-dock-left {
      display: flex;
      align-items: center;
      gap: 10px;
      min-width: 0;
      flex: 1;
    }
    .audio-dock-wave {
      font-size: 22px;
      line-height: 1;
      animation: pulseAudio 1.5s infinite ease-in-out;
    }
    @keyframes pulseAudio {
      0%, 100% { transform: scale(1); }
      50% { transform: scale(1.18); }
    }
    .audio-dock-info {
      min-width: 0;
    }
    .audio-dock-status {
      font-size: 14px;
      font-weight: 800;
      color: var(--text-main);
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }
    .audio-dock-sub {
      font-size: 12px;
      color: var(--text-muted);
      font-weight: 600;
    }
    .audio-dock-controls {
      display: flex;
      align-items: center;
      gap: 8px;
      flex-shrink: 0;
    }
    .audio-ctrl-btn {
      background: var(--steel-blue-light);
      border: 1px solid var(--steel-blue-border);
      color: var(--text-main);
      width: 40px;
      height: 40px;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 16px;
      cursor: pointer;
      transition: all 0.2s ease;
    }
    .audio-ctrl-btn:hover {
      background: var(--steel-blue);
      color: #fff;
    }
    .audio-speed-select {
      background: var(--bg-card);
      border: 1.5px solid var(--border-color);
      color: var(--text-main);
      font-size: 13px;
      font-weight: 700;
      border-radius: var(--radius-sm);
      padding: 6px 8px;
      cursor: pointer;
      outline: none;
    }
    .audio-close-btn {
      background: transparent;
      border: none;
      color: var(--text-muted);
      font-size: 16px;
      padding: 4px;
      cursor: pointer;
      margin-left: 2px;
    }
    .audio-close-btn:hover {
      color: var(--text-main);
    }
    .speech-toast {
      position: fixed;
      top: 76px;
      left: 50%;
      transform: translateX(-50%);
      width: calc(100% - 32px);
      max-width: 600px;
      z-index: 350;
      background: #78350f;
      border: 2px solid #f59e0b;
      color: #ffffff;
      border-radius: var(--radius-sm);
      padding: 12px 16px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      box-shadow: 0 10px 25px rgba(0, 0, 0, 0.45);
      animation: fadeIn 0.3s ease;
    }
    .speech-toast-body {
      display: flex;
      align-items: flex-start;
      gap: 10px;
      font-size: 14px;
      line-height: 1.45;
      font-weight: 600;
    }
    .speech-toast-icon {
      font-size: 20px;
      line-height: 1;
      flex-shrink: 0;
    }
    .speech-toast-close {
      background: transparent;
      border: none;
      color: #ffffff;
      font-size: 16px;
      cursor: pointer;
      padding: 4px;
    }
    .speaker-btn-inline {
      background: var(--steel-blue-light);
      border: 1.5px solid var(--steel-blue-border);
      color: var(--steel-blue);
      border-radius: var(--radius-sm);
      padding: 8px 14px;
      font-size: 14px;
      font-weight: 700;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      transition: all 0.2s ease;
      margin-top: 10px;
    }
    .dark .speaker-btn-inline {
      color: #93c5fd;
    }
    .speaker-btn-inline:hover {
      background: var(--steel-blue);
      color: #ffffff;
    }
'''

if "/* AUDIO CONTROLLER DOCK & TOAST */" not in template:
    pos_style_end = template.find("</style>")
    template = template[:pos_style_end] + audio_css + "\n  " + template[pos_style_end:]

# 2. INSERT AUDIO CONTROL DOCK & TOAST HTML RIGHT BEFORE BOTTOM NAV
dock_html = '''    <!-- FLOATING AUDIO CONTROLLER DOCK -->
    <div id="audioControlDock" class="audio-control-dock" style="display: none;">
      <div class="audio-dock-content">
        <div class="audio-dock-left">
          <span class="audio-dock-wave" id="audioWaveIcon">🔊</span>
          <div class="audio-dock-info">
            <div class="audio-dock-status" id="audioStatusText">Reading aloud...</div>
            <div class="audio-dock-sub" id="audioLangIndicator">en-IN &bull; 0.9x</div>
          </div>
        </div>
        <div class="audio-dock-controls">
          <button type="button" class="audio-ctrl-btn" id="btnAudioPauseResume" onclick="BlaxGuardSpeech.togglePause()" title="Pause/Resume">
            <span id="audioPauseIcon">⏸️</span>
          </button>
          <button type="button" class="audio-ctrl-btn" onclick="BlaxGuardSpeech.stop()" title="Stop Reading">
            <span>⏹️</span>
          </button>
          <select class="audio-speed-select" id="audioSpeedSelect" onchange="BlaxGuardSpeech.setRate(this.value)">
            <option value="0.8">0.8x (Slow)</option>
            <option value="0.9" selected>0.9x</option>
            <option value="1.0">1.0x</option>
            <option value="1.2">1.2x</option>
          </select>
          <button type="button" class="audio-close-btn" onclick="BlaxGuardSpeech.stop()" title="Close Player">✕</button>
        </div>
      </div>
    </div>

    <!-- TOAST CONTAINER FOR MISSING VOICE NOTIFICATIONS -->
    <div id="speechToast" class="speech-toast" style="display: none;">
      <div class="speech-toast-body">
        <span class="speech-toast-icon">⚠️</span>
        <span id="speechToastMessage">Voice not installed</span>
      </div>
      <button type="button" class="speech-toast-close" onclick="closeSpeechToast()">✕</button>
    </div>

'''

if 'id="audioControlDock"' not in template:
    pos_bottom_nav = template.find('<nav class="bottom-nav"')
    template = template[:pos_bottom_nav] + dock_html + template[pos_bottom_nav:]

# 3. ADD SPEAKER BUTTONS IN SPECIFIC SECTIONS:
# 3A. In Call page hangupBanner: add speaker button
if 'onclick="speakHangupBanner()"' not in template:
    template = template.replace(
        '<!-- ALERT FAMILY ON WHATSAPP BUTTON -->',
        '''<button type="button" class="senior-voice-btn" onclick="speakHangupBanner()" style="margin-bottom: 12px; background: rgba(0,0,0,0.25); border: 1.5px solid #fff; color: #fff;">
            <span>🔊</span> <span data-i18n="btnListenHangup">Listen to Emergency Steps Aloud</span>
          </button>

          <!-- ALERT FAMILY ON WHATSAPP BUTTON -->'''
    )

# 3B. In Report page confirmation card: add speaker button
if 'onclick="speakReportConfirmation()"' not in template:
    template = template.replace(
        '<div class="privacy-stamp">',
        '''<button type="button" class="speaker-btn-inline" onclick="speakReportConfirmation()" style="margin-bottom: 14px; width: 100%; justify-content: center;">
            <span>🔊</span> <span data-i18n="btnListenConfirmation">Listen to Confirmation Receipt Aloud</span>
          </button>

          <div class="privacy-stamp">'''
    )

# 3C. In Help page First Hour card: add speaker button
if 'onclick="speakFirstHourSteps()"' not in template:
    template = template.replace(
        '</ul>\n        </div>\n\n        <!-- Note to Freeze Card / UPI through Bank App -->',
        '''</ul>
          <button type="button" class="speaker-btn-inline" onclick="speakFirstHourSteps()">
            <span>🔊</span> <span data-i18n="btnListenFirstHour">Listen to First 60 Minutes Steps Aloud</span>
          </button>
        </div>

        <!-- Note to Freeze Card / UPI through Bank App -->'''
    )

# 3D. In Help page Freeze card: add speaker button
if 'onclick="speakFreezeGuideSteps()"' not in template:
    template = template.replace(
        '</div>\n        </div>\n\n        <!-- Official Cybercrime Portal Callout -->',
        '''</div>
          <button type="button" class="speaker-btn-inline" onclick="speakFreezeGuideSteps()">
            <span>🔊</span> <span data-i18n="btnListenFreezeGuide">Listen to 30-Second Freeze Steps Aloud</span>
          </button>
        </div>

        <!-- Official Cybercrime Portal Callout -->'''
    )

# 3E. In Loan page advice box: add speaker button
if 'onclick="speakLoanAdviceSteps()"' not in template:
    template = template.replace(
        '${adviceListHtml}\n            </ul>\n          </div>\n\n          <button class="senior-voice-btn"',
        '''${adviceListHtml}
            </ul>
            <button type="button" class="speaker-btn-inline" onclick="speakLoanAdviceSteps()">
              <span>🔊</span> <span>${dict.btnListenSteps || "Listen to advice steps aloud"}</span>
            </button>
          </div>

          <button class="senior-voice-btn"'''
    )

# 3F. In Check page Next Steps card: add speaker button
if 'onclick="speakCheckSteps()"' not in template:
    template = template.replace(
        '${dict.stepCyberCrime}</div>\n            </li>\n          </ul>\n        </div>\n\n        <button class="senior-voice-btn"',
        '''${dict.stepCyberCrime}</div>
            </li>
          </ul>
          <button type="button" class="speaker-btn-inline" onclick="speakCheckSteps()">
            <span>🔊</span> <span>${dict.btnListenSteps || "Listen to steps aloud"}</span>
          </button>
        </div>

        <button class="senior-voice-btn"'''
    )

# 4. ADD SPEECH MODULE AND UNIFIED HANDLERS IN JAVASCRIPT
speech_js_module = '''    /* ============================================================== */
    /* BLAXGUARD UNIFIED SPEECH SYNTHESIS ENGINE                      */
    /* Supports: en-IN, hi-IN, te-IN, rate settings, pause/resume/stop*/
    /* Notifies with accessible toast if voice is missing on device.  */
    /* ============================================================== */
    const BlaxGuardSpeech = (function() {
      let _currentUtterance = null;
      let _isPaused = false;
      let _currentRate = 0.9;
      let _availableVoices = [];

      function _loadVoices() {
        if (typeof window !== "undefined" && "speechSynthesis" in window) {
          _availableVoices = window.speechSynthesis.getVoices();
        }
      }

      if (typeof window !== "undefined" && "speechSynthesis" in window) {
        _loadVoices();
        if (window.speechSynthesis.onvoiceschanged !== undefined) {
          window.speechSynthesis.onvoiceschanged = _loadVoices;
        }
      }

      function getLangCode() {
        if (currentLang === "hi") return "hi-IN";
        if (currentLang === "te") return "te-IN";
        return "en-IN";
      }

      function findMatchingVoice(langCode) {
        if (!_availableVoices || _availableVoices.length === 0) {
          _loadVoices();
        }
        const prefix = langCode.split("-")[0].toLowerCase();
        
        let voice = _availableVoices.find(v => 
          v.lang && (v.lang.toLowerCase() === langCode.toLowerCase() || v.lang.toLowerCase().replace('_', '-') === langCode.toLowerCase())
        );
        if (voice) return voice;

        voice = _availableVoices.find(v => v.lang && v.lang.toLowerCase().startsWith(prefix));
        if (voice) return voice;

        return null;
      }

      return {
        getRate() { return _currentRate; },
        setRate(rate) { 
          _currentRate = parseFloat(rate);
          const langName = currentLang === "hi" ? "hi-IN" : (currentLang === "te" ? "te-IN" : "en-IN");
          const langEl = document.getElementById("audioLangIndicator");
          if (langEl) langEl.textContent = `${langName} • ${_currentRate}x`;
          if (_currentUtterance && window.speechSynthesis.speaking && !_isPaused) {
            const text = _currentUtterance.text;
            this.speak(text);
          }
        },

        speak(text) {
          if (!("speechSynthesis" in window)) {
            showVoiceUnavailableToast("unsupported");
            return;
          }

          window.speechSynthesis.cancel();
          _isPaused = false;

          if (!text || !text.trim()) return;

          const langCode = getLangCode();
          const matchedVoice = findMatchingVoice(langCode);

          // If language is Hindi or Telugu and voices are loaded but none match
          if (langCode !== "en-IN" && !matchedVoice && _availableVoices.length > 0) {
            showVoiceUnavailableToast(langCode);
            return;
          }

          const utterance = new SpeechSynthesisUtterance(text);
          utterance.lang = langCode;
          utterance.rate = _currentRate;
          if (matchedVoice) {
            utterance.voice = matchedVoice;
          }

          utterance.onstart = () => {
            _currentUtterance = utterance;
            _isPaused = false;
            updateAudioBarUI("speaking", text);
          };

          utterance.onend = () => {
            _currentUtterance = null;
            _isPaused = false;
            updateAudioBarUI("idle");
          };

          utterance.onerror = (e) => {
            console.warn("SpeechSynthesis error:", e);
            _currentUtterance = null;
            _isPaused = false;
            updateAudioBarUI("idle");
          };

          _currentUtterance = utterance;
          window.speechSynthesis.speak(utterance);
          updateAudioBarUI("speaking", text);
        },

        pause() {
          if ("speechSynthesis" in window && window.speechSynthesis.speaking) {
            window.speechSynthesis.pause();
            _isPaused = true;
            updateAudioBarUI("paused");
          }
        },

        resume() {
          if ("speechSynthesis" in window && _isPaused) {
            window.speechSynthesis.resume();
            _isPaused = false;
            updateAudioBarUI("speaking");
          }
        },

        togglePause() {
          if (_isPaused) {
            this.resume();
          } else {
            this.pause();
          }
        },

        stop() {
          if ("speechSynthesis" in window) {
            window.speechSynthesis.cancel();
          }
          _currentUtterance = null;
          _isPaused = false;
          updateAudioBarUI("idle");
        }
      };
    })();

    function updateAudioBarUI(state, text) {
      const dock = document.getElementById("audioControlDock");
      const statusEl = document.getElementById("audioStatusText");
      const langEl = document.getElementById("audioLangIndicator");
      const pauseIcon = document.getElementById("audioPauseIcon");
      const waveIcon = document.getElementById("audioWaveIcon");

      if (!dock) return;

      const dict = translations[currentLang] || translations.en;
      const langName = currentLang === "hi" ? "हिंदी (hi-IN)" : (currentLang === "te" ? "తెలుగు (te-IN)" : "English (en-IN)");

      if (state === "speaking") {
        dock.style.display = "block";
        if (statusEl) statusEl.textContent = (dict.audioSpeaking || "Reading aloud in {lang}...").replace("{lang}", langName);
        if (langEl) langEl.textContent = `${langName} • ${BlaxGuardSpeech.getRate()}x`;
        if (pauseIcon) pauseIcon.textContent = "⏸️";
        if (waveIcon) waveIcon.style.animationPlayState = "running";
      } else if (state === "paused") {
        dock.style.display = "block";
        if (statusEl) statusEl.textContent = dict.audioPaused || "Audio Paused";
        if (pauseIcon) pauseIcon.textContent = "▶️";
        if (waveIcon) waveIcon.style.animationPlayState = "paused";
      } else {
        dock.style.display = "none";
      }
    }

    function showVoiceUnavailableToast(langCode) {
      const toast = document.getElementById("speechToast");
      const msgEl = document.getElementById("speechToastMessage");
      if (!toast || !msgEl) return;

      const dict = translations[currentLang] || translations.en;
      let msg = "";

      if (langCode === "unsupported") {
        msg = dict.speechUnsupported || "⚠️ Speech synthesis is not supported on your browser.";
      } else if (langCode === "te-IN") {
        msg = dict.voiceMissingTe || "⚠️ Telugu (te-IN) voice is not installed on this device. Please install the language pack in system settings, or read the text above.";
      } else if (langCode === "hi-IN") {
        msg = dict.voiceMissingHi || "⚠️ Hindi (hi-IN) voice is not installed on this device. Please install the language pack in system settings, or read the text above.";
      } else {
        msg = dict.voiceMissingEn || "⚠️ English (en-IN) voice is not installed on this device. Please read the text above.";
      }

      msgEl.textContent = msg;
      toast.style.display = "flex";

      clearTimeout(window._speechToastTimer);
      window._speechToastTimer = setTimeout(() => {
        toast.style.display = "none";
      }, 7000);
    }

    function closeSpeechToast() {
      const toast = document.getElementById("speechToast");
      if (toast) toast.style.display = "none";
    }

    /* SPECIFIC SPEECH ACTION CONTROLLERS */
    function speakRuleEngineAlert() {
      if (!lastAnalysisData) return;
      const data = lastAnalysisData;
      let msg = "";
      if (currentLang === "hi") {
        if (data.verdict === "danger") msg = "सावधान! यह संभावित धोखाधड़ी है। इसका जोखिम स्कोर सौ में से " + data.score + " है। किसी भी लिंक पर क्लिक न करें और नंबर को तुरंत ब्लॉक करें।";
        else if (data.verdict === "caution") msg = "सतर्क रहें! इस संदेश में कुछ संदिग्ध संकेत हैं। कोई भी पासवर्ड या पिन साझा न करें।";
        else msg = "यह संदेश सुरक्षित प्रतीत होता है। कोई भी ज्ञात खतरा नहीं पाया गया।";
      } else if (currentLang === "te") {
        if (data.verdict === "danger") msg = "హెచ్చరిక! ఇది సంభావ్య మోసం. ప్రమాద స్కోర్ " + data.score + ". ఎటువంటి లింక్ తెరవవద్దు మరియు వెంటనే నంబర్ బ్లాక్ చేయండి.";
        else if (data.verdict === "caution") msg = "జాగ్రత్తగా ఉండండి! ఈ సందేశంలో కొన్ని అనుమానాస్పద అంశాలు ఉన్నాయి.";
        else msg = "ఈ సందేశం సురక్షితంగా ఉన్నట్లు కనిపిస్తోంది.";
      } else {
        if (data.verdict === "danger") msg = "Warning! Likely scam detected. Risk score is " + data.score + " out of 100. Do not click links and block the sender immediately.";
        else if (data.verdict === "caution") msg = "Caution! This message contains suspicious elements. Do not share credentials or transfer funds.";
        else msg = "This message appears safe. No known threats were detected.";
      }
      BlaxGuardSpeech.speak(msg);
    }

    function speakCheckSteps() {
      let msg = "";
      if (currentLang === "hi") {
        msg = "सुरक्षा के अगले कदम: कदम एक: नंबर को तुरंत ब्लॉक करें। कदम दो: अपने बैंक के आधिकारिक नंबर पर कॉल करें। कदम तीन: राष्ट्रीय साइबर हेल्पलाइन 1930 पर कॉल करें। कदम चार: cybercrime.gov.in पर रिपोर्ट दर्ज करें।";
      } else if (currentLang === "te") {
        msg = "తదుపరి భద్రతా దశలు: దశ ఒకటి: నంబర్‌ను వెంటనే బ్లాక్ చేయండి. దశ రెండు: మీ బ్యాంక్ అధికారిక నంబర్‌కు కాల్ చేయండి. దశ మూడు: జాతీయ సైబర్ హెల్ప్‌లైన్ 1930 కి డయల్ చేయండి. దశ నాలుగు: cybercrime.gov.in లో ఫిర్యాదు చేయండి.";
      } else {
        msg = "Next Safety Steps: Step 1: Block the sender number immediately. Step 2: Call your bank on its official number. Step 3: Dial National Cyber Crime Helpline 1930. Step 4: Report to cybercrime.gov.in.";
      }
      BlaxGuardSpeech.speak(msg);
    }

    function speakLoanVerdictAlert() {
      if (!lastLoanVerdictData) return;
      const data = lastLoanVerdictData;
      let msg = "";
      if (currentLang === "hi") {
        if (data.verdict === "danger") msg = "सावधान! यह ब्लैकमेल करने वाला अवैध लोन ऐप है। कोई भी अग्रिम फीस न दें और ऐप को तुरंत फोन से हटाएं।";
        else if (data.verdict === "caution") msg = "सतर्क रहें! इस लोन ऑफर में कुछ संदिग्ध शर्तें पाई गई हैं।";
        else msg = "लोन की शर्तें सामान्य हैं। अनुबंध पत्र ध्यानपूर्वक पढ़ें।";
      } else if (currentLang === "te") {
        if (data.verdict === "danger") msg = "హెచ్చరిక! ఇది బ్లాక్‌మెయిల్ చేసే మోసపూరిత లోన్ యాప్. ఎటువంటి అడ్వాన్స్ ఫీజు ఇవ్వకండి మరియు యాప్‌ను వెంటనే తీసివేయండి.";
        else if (data.verdict === "caution") msg = "జాగ్రత్తగా ఉండండి! ఈ లోన్ ఆఫర్‌లో అనుమానాస్పద నిబంధనలు ఉన్నాయి.";
        else msg = "లోన్ నిబంధనలు సురక్షితంగా ఉన్నాయి.";
      } else {
        if (data.verdict === "danger") msg = "Critical Danger! Predatory loan scam detected. Never pay upfront fees and uninstall the application immediately.";
        else if (data.verdict === "caution") msg = "Be careful! Suspicious clauses detected in this loan offer. Verify lender on RBI official portal.";
        else msg = "Loan terms appear standard. Read agreement terms carefully.";
      }
      BlaxGuardSpeech.speak(msg);
    }

    function speakLoanAdviceSteps() {
      let msg = "";
      if (currentLang === "hi") {
        msg = "लोन सुरक्षा सलाह: कोई अग्रिम प्रोसेसिंग फीस न दें। फोन कॉन्टैक्ट्स या फोटो गैलरी की अनुमति कभी न दें। गूगल प्ले स्टोर के बाहर से एपीके डाउनलोड न करें।";
      } else if (currentLang === "te") {
        msg = "లోన్ భద్రతా సలహా: ఎటువంటి ముందస్తు ప్రాసెసింగ్ ఫీజు చెల్లించవద్దు. కాంటాక్ట్‌లు లేదా ఫోటో గ్యాలరీ అనుమతులు ఎప్పుడూ ఇవ్వవద్దు. గూగుల్ ప్లే స్టోర్ వెలుపల APK ఫైళ్లను డౌన్‌లోడ్ చేయవద్దు.";
      } else {
        msg = "Loan Safety Advice: Never pay upfront processing fees before disbursal. Never grant Contacts or Photo permissions to lending apps. Never install APK files outside Google Play.";
      }
      BlaxGuardSpeech.speak(msg);
    }

    function speakHangupBanner() {
      let msg = "";
      if (currentLang === "hi") {
        msg = "कॉल तुरंत काटें! आप एक सक्रिय साइबर अपराधी से बात कर रहे हैं। कदम 1: तुरंत फोन काटें। कदम 2: उसी नंबर पर दोबारा कॉल न करें। कदम 3: 1930 हेल्पलाइन पर कॉल करें। कदम 4: परिवार के किसी सदस्य को बताएं।";
      } else if (currentLang === "te") {
        msg = "వెంటనే కాల్ కట్ చేయండి! మీరు సైబర్ నేరగాడితో మాట్లాడుతున్నారు. దశ 1: వెంటనే ఫోన్ పెట్టేయండి. దశ 2: అదే నంబర్‌కు మళ్లీ కాల్ చేయవద్దు. దశ 3: 1930 హెల్ప్‌లైన్‌కు కాల్ చేయండి. దశ 4: కుటుంబ సభ్యులకు చెప్పండి.";
      } else {
        msg = "HANG UP NOW! You are talking to an active cyber criminal. Step 1: Hang up immediately. Step 2: Don't call back on the same number. Step 3: Dial 1930 Helpline. Step 4: Tell a family member right away.";
      }
      BlaxGuardSpeech.speak(msg);
    }

    function speakRegistryResult() {
      const resBox = document.getElementById("registryLookupResultBox");
      if (!resBox) return;
      const text = resBox.innerText || resBox.textContent;
      BlaxGuardSpeech.speak(text);
    }

    function speakReportConfirmation() {
      let msg = "";
      const cat = document.getElementById("confirmCategoryBadge")?.textContent || "";
      const count = document.getElementById("confirmCounterBadge")?.textContent || "1";
      if (currentLang === "hi") {
        msg = `स्कैम सफलतापूर्वक गुमनाम रूप से दर्ज किया गया। श्रेणी: ${cat}। यह खतरा समुदाय में ${count} बार दर्ज हो चुका है। आपका विवरण सुरक्षित है।`;
      } else if (currentLang === "te") {
        msg = `స్కామ్ విజయవంతంగా అజ్ఞాతంగా నమోదైంది. వర్గం: ${cat}. ఈ ముప్పు కమ్యూనిటీలో ${count} సార్లు నమోదైంది. మీ వివరాలు సురక్షితం.`;
      } else {
        msg = `Scam incident registered anonymously. Category: ${cat}. This threat pattern has now been flagged ${count} time(s) by citizens. Your privacy is protected.`;
      }
      BlaxGuardSpeech.speak(msg);
    }

    function speakScamCard(scamNum) {
      const dict = translations[currentLang] || translations.en;
      const title = dict[`scam${scamNum}Title`] || "";
      const how = dict[`scam${scamNum}How`] || "";
      const signs = dict[`scam${scamNum}Signs`] || "";
      const action = dict[`scam${scamNum}Action`] || "";

      let textToSpeak = `${title}. ${dict.labelHowWorks || "How it works"}: ${how}. ${dict.labelWarningSigns || "Warning signs"}: ${signs}. ${dict.labelWhatToDo || "What to do"}: ${action}.`;
      BlaxGuardSpeech.speak(textToSpeak);
    }

    function speakFirstHourSteps() {
      let msg = "";
      if (currentLang === "hi") {
        msg = "पैसे कटने के बाद पहले 60 मिनट: चरण 1: तुरंत 1930 डायल करें और लेन-देन फ्रीज करवाएं। चरण 2: बैंक ऐप में कार्ड और यूपीआई तुरंत लॉक करें। चरण 3: 12 अंकों का यूटीआर और लेन-देन का स्क्रीनशॉट रखें। चरण 4: cybercrime.gov.in पर औपचारिक शिकायत करें। चरण 5: 3 दिनों के भीतर बैंक शाखा को लिखित शिकायत दें।";
      } else if (currentLang === "te") {
        msg = "డబ్బు పోగొట్టుకున్న మొదటి 60 నిమిషాలు: దశ 1: లావాదేవీలను నిలిపివేయడానికి వెంటనే 1930 కి డయల్ చేయండి. దశ 2: బ్యాంక్ యాప్‌లో డెబిట్ కార్డ్ మరియు UPI ని లాక్ చేయండి. దశ 3: 12 అంకెల UTR నంబర్ వివరాలు భద్రపరచండి. దశ 4: cybercrime.gov.in లో ఫిర్యాదు చేయండి. దశ 5: 3 రోజుల్లోగా బ్యాంక్ బ్రాంచ్‌కు లిఖితపూర్వకంగా తెలపండి.";
      } else {
        msg = "First 60 Minutes After Losing Money: Step 1: Dial 1930 immediately to freeze transactions. Step 2: Freeze Debit card and UPI in your bank app. Step 3: Save 12-digit UTR number and transaction details. Step 4: Lodge complaint on cybercrime.gov.in. Step 5: Notify your bank branch manager in writing within 3 days.";
      }
      BlaxGuardSpeech.speak(msg);
    }

    function speakFreezeGuideSteps() {
      let msg = "";
      if (currentLang === "hi") {
        msg = "बैंक ऐप में 30 सेकंड में कार्ड और यूपीआई कैसे फ्रीज करें: चरण 1: अपना प्रामाणिक बैंक ऐप खोलें। चरण 2: कार्ड्स में जाकर मैनेज डेबिट कार्ड और टेम्परेरी लॉक चालू करें। चरण 3: डोमेस्टिक ऑनलाइन और एटीएम निकासी बंद करें। चरण 4: यूपीआई सेटिंग्स में जाकर प्रोफाइल डी-रजिस्टर करें।";
      } else if (currentLang === "te") {
        msg = "బ్యాంక్ యాప్‌లో 30 సెకన్లలో కార్డ్ మరియు UPI ని ఎలా ఫ్రీజ్ చేయాలి: దశ 1: మీ బ్యాంక్ యాప్ తెరవండి. దశ 2: కార్డ్స్‌లోకి వెళ్లి మేనేజ్ డెబిట్ కార్డ్ మరియు తాత్కాలికంగా బ్లాక్ చేయండి. దశ 3: ఆన్‌లైన్ లావాదేవీలు మరియు ATM విత్‌డ్రా స్విచ్‌లను ఆపివేయండి. దశ 4: UPI సెట్టింగ్స్‌కి వెళ్లి ప్రొఫైల్ డీ-రిజిస్టర్ చేయండి.";
      } else {
        msg = "How to Freeze Your Card and UPI in Bank App: Step 1: Open your genuine mobile bank app. Step 2: Go to Cards, Manage Debit Card, and switch on Temporary Card Lock. Step 3: Turn off Domestic Online and ATM cash withdrawal switches. Step 4: Go to UPI Settings and deregister your UPI profile or reduce limit to 1 rupee.";
      }
      BlaxGuardSpeech.speak(msg);
    }
'''

# Replace existing speak functions in template
pos_old_eval_speak = template.find('function speakRuleEngineAlert() {')
pos_init = template.find('/* INITIALIZATION */')
template = template[:pos_old_eval_speak] + speech_js_module + "\n\n    " + template[pos_init:]

# 5. TRANSLATION DICTIONARIES FOR AUDIO AND SPEECH
audio_trans_en = '''btnListenSteps: "Listen to steps aloud",
        btnListenLoanAdvice: "Listen to advice steps aloud",
        btnListenHangup: "Listen to emergency steps aloud",
        btnListenConfirmation: "Listen to confirmation receipt aloud",
        btnListenFirstHour: "Listen to First 60 Minutes steps aloud",
        btnListenFreezeGuide: "Listen to 30-Second freeze steps aloud",
        audioSpeaking: "Reading aloud in {lang}...",
        audioPaused: "Audio Paused",
        voiceMissingHi: "⚠️ Hindi (hi-IN) voice is not installed on this device. Please install the language pack in system settings, or read the text above.",
        voiceMissingTe: "⚠️ Telugu (te-IN) voice is not installed on this device. Please install the language pack in system settings, or read the text above.",
        voiceMissingEn: "⚠️ English (en-IN) voice is not installed on this device. Please read the text above.",
        speechUnsupported: "⚠️ Speech synthesis is not supported on this browser.",'''

audio_trans_hi = '''btnListenSteps: "चरणों को बोलकर सुनें",
        btnListenLoanAdvice: "सलाह के चरणों को सुनें",
        btnListenHangup: "आपातकालीन चरणों को सुनें",
        btnListenConfirmation: "पुष्टि रसीद को बोलकर सुनें",
        btnListenFirstHour: "पहले 60 मिनट के चरणों को सुनें",
        btnListenFreezeGuide: "30-सेकंड फ्रीज चरणों को सुनें",
        audioSpeaking: "{lang} में पढ़कर सुनाया जा रहा है...",
        audioPaused: "आवाज रोकी गई",
        voiceMissingHi: "⚠️ आपके डिवाइस पर हिंदी (hi-IN) आवाज स्थापित नहीं है। कृपया सेटिंग्स में भाषा पैक जोड़ें या ऊपर लिखा टेक्स्ट पढ़ें।",
        voiceMissingTe: "⚠️ आपके डिवाइस पर तेलुगु (te-IN) आवाज स्थापित नहीं है। कृपया सेटिंग्स में भाषा पैक जोड़ें या ऊपर लिखा टेक्स्ट पढ़ें।",
        voiceMissingEn: "⚠️ आपके डिवाइस पर अंग्रेजी आवाज स्थापित नहीं है। कृपया ऊपर लिखा टेक्स्ट पढ़ें।",
        speechUnsupported: "⚠️ इस ब्राउज़र में स्पीच सिंथेसिस समर्थित नहीं है।",'''

audio_trans_te = '''btnListenSteps: "దశలను వినిపించండి",
        btnListenLoanAdvice: "సలహా దశలను వినిపించండి",
        btnListenHangup: "అత్యవసర దశలను వినిపించండి",
        btnListenConfirmation: "రసీదు వివరాలను వినిపించండి",
        btnListenFirstHour: "మొదటి 60 నిమిషాల దశలను వినిపించండి",
        btnListenFreezeGuide: "30-సెకన్ల ఫ్రీజ్ దశలను వినిపించండి",
        audioSpeaking: "{lang}లో చదివి వినిపిస్తోంది...",
        audioPaused: "ఆడియో పాజ్ చేయబడింది",
        voiceMissingHi: "⚠️ మీ పరికరంలో హిందీ (hi-IN) వాయిస్ ఇన్‌స్టాల్ చేయబడలేదు. దయచేసి సెట్టింగ్స్‌లో వాయిస్ ఇన్‌స్టాల్ చేసుకోండి లేదా పై సమాచారాన్ని చదవండి.",
        voiceMissingTe: "⚠️ మీ పరికరంలో తెలుగు (te-IN) వాయిస్ ఇన్‌స్టాల్ చేయబడలేదు. దయచేసి సెట్టింగ్స్‌లో వాయిస్ ఇన్‌స్టాల్ చేసుకోండి లేదా పై సమాచారాన్ని చదవండి.",
        voiceMissingEn: "⚠️ మీ పరికరంలో ఇంగ్లీష్ వాయిస్ ఇన్‌స్టాల్ చేయబడలేదు. దయచేసి పై సమాచారాన్ని చదవండి.",
        speechUnsupported: "⚠️ ఈ బ్రౌజర్‌లో స్పీచ్ సింథసిస్ సపోర్ట్ చేయదు.",'''

# Insert in EN, HI, TE
pos_te = template.find('te: {')
pos_te_end = template.find('let currentLang =')
template = template[:pos_te_end-10] + "        " + audio_trans_te + "\n      },\n" + template[pos_te_end-8:]

pos_hi = template.find('hi: {')
pos_te = template.find('te: {')
template = template[:pos_te-10] + "        " + audio_trans_hi + "\n      },\n      " + template[pos_te:]

pos_en = template.find('en: {')
pos_hi = template.find('hi: {')
template = template[:pos_hi-10] + "        " + audio_trans_en + "\n      },\n      " + template[pos_hi:]

# Save template.html
with open("template.html", "w", encoding="utf-8") as f:
    f.write(template)

# Build index.html
output = template.replace("{{SHIELD_URI}}", shield_uri).replace("{{FULL_URI}}", full_uri)
with open("index.html", "w", encoding="utf-8") as f:
    f.write(output)

print(f"Generated index.html with complete SpeechSynthesis Engine! File size: {os.path.getsize('index.html')} bytes")
