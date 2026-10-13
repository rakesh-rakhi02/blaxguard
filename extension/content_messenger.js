/**
 * BlaxGuard Messenger Protection (WhatsApp Web & Telegram Web)
 * Intercepts links clicked in chat messages and applies Family Guardian Shield
 * to prevent seniors and children from opening high-risk scam/predatory loan links.
 */

(function () {
  console.log("[BlaxGuard] WhatsApp & Telegram Protection Active (Guardian Shield Enabled)");

  const API_ENDPOINT = "http://localhost:8080/api/check";
  const GUARDIAN_REQUEST_API = "http://localhost:8080/api/guardian/request";
  const GUARDIAN_STATUS_API = "http://localhost:8080/api/guardian/status";

  const RISKY_TLDS = /\.(xyz|top|online|club|buzz|work|live|loan|vip|icu|tk|ml|ga|cf|gq|site|space|guru|cam|rest)(?:[\/\?\s]|$)/i;

  function showMessengerWarningPopup(url, score, reasons) {
    const existing = document.getElementById("blaxguard-messenger-modal");
    if (existing) existing.remove();

    const savedPhone = localStorage.getItem("blaxguard_guardian_phone") || "+91 98765 43210";

    const overlay = document.createElement("div");
    overlay.id = "blaxguard-messenger-modal";
    overlay.style.cssText = `
      position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
      background: rgba(15, 23, 42, 0.85); backdrop-filter: blur(6px);
      display: flex; align-items: center; justify-content: center;
      z-index: 99999999; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    `;

    overlay.innerHTML = `
      <div style="background: #ffffff; border-radius: 20px; width: 92%; max-width: 500px; padding: 26px; box-shadow: 0 25px 50px -12px rgba(0,0,0,0.5); border: 2.5px solid #ef4444;">
        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 14px;">
          <div style="display: flex; align-items: center; gap: 12px;">
            <span style="font-size: 34px;">🛡️</span>
            <div>
              <h3 style="margin: 0; font-size: 19px; color: #dc2626; font-weight: 800;">BlaxGuard Guardian Shield</h3>
              <p style="margin: 2px 0 0; font-size: 12.5px; color: #64748b;">Senior & Child Protection Active</p>
            </div>
          </div>
          <span style="background: #fee2e2; color: #b91c1c; font-size: 11.5px; font-weight: 800; padding: 4px 10px; border-radius: 99px; border: 1px solid #fca5a5;">
            LOCKED 🔒
          </span>
        </div>

        <div style="background: #fef2f2; border: 1.5px solid #fca5a5; border-radius: 12px; padding: 14px; margin-bottom: 14px;">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
            <span style="font-size: 12.5px; font-weight: 800; color: #991b1b;">Threat Risk Score:</span>
            <span style="background: #ef4444; color: #fff; font-size: 12px; font-weight: 800; padding: 2px 8px; border-radius: 99px;">${score} / 100 DANGER</span>
          </div>
          <div style="font-size: 12.5px; color: #7f1d1d; line-height: 1.45;">
            ${reasons.map(r => `<div>• ${r}</div>`).join("")}
          </div>
          <div style="margin-top: 10px; font-size: 11.5px; color: #334155; word-break: break-all; background: #fff; padding: 8px; border-radius: 6px; border: 1px dashed #cbd5e1;">
            <strong>Target Link:</strong> ${url}
          </div>
        </div>

        <!-- Guardian Approval Section -->
        <div id="blaxguard-guardian-section" style="background: #f8fafc; border: 1.5px solid #e2e8f0; border-radius: 12px; padding: 14px; margin-bottom: 16px;">
          <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 6px;">
            <span style="font-size: 18px;">👨‍👩‍👧</span>
            <strong style="font-size: 13px; color: #1e293b;">Family Consent Required</strong>
          </div>
          <p style="font-size: 12px; color: #64748b; line-height: 1.4; margin-bottom: 10px;">
            To protect seniors and children from financial fraud, this suspicious link cannot be opened without Guardian permission.
          </p>
          <div style="display: flex; gap: 8px;">
            <input id="blaxguard-input-phone" type="tel" value="${savedPhone}" placeholder="Guardian Phone (+91 ...)" style="flex: 1; padding: 8px 10px; border: 1px solid #cbd5e1; border-radius: 8px; font-size: 13px; outline: none;">
            <button id="blaxguard-btn-send-guardian" style="background: #2563eb; color: #fff; border: none; border-radius: 8px; padding: 8px 14px; font-size: 12.5px; font-weight: 700; cursor: pointer; white-space: nowrap;">
              📲 Ask Guardian
            </button>
          </div>
        </div>

        <div style="display: flex; gap: 10px; justify-content: flex-end;">
          <button id="blaxguard-chat-btn-safe" style="padding: 10px 18px; background: #10b981; color: #fff; border: none; border-radius: 8px; font-weight: 700; cursor: pointer; font-size: 13.5px;">
            🛡️ Stay Safe (Cancel)
          </button>
        </div>
      </div>
    `;

    document.body.appendChild(overlay);

    let pollInterval = null;

    document.getElementById("blaxguard-chat-btn-safe").onclick = () => {
      if (pollInterval) clearInterval(pollInterval);
      overlay.remove();
    };

    // Guardian request button handler
    document.getElementById("blaxguard-btn-send-guardian").onclick = async () => {
      const phoneInput = document.getElementById("blaxguard-input-phone").value.trim();
      if (!phoneInput) {
        alert("Please enter a guardian phone number.");
        return;
      }
      localStorage.setItem("blaxguard_guardian_phone", phoneInput);

      const section = document.getElementById("blaxguard-guardian-section");
      section.innerHTML = `
        <div style="text-align: center; padding: 12px 6px;">
          <div style="font-size: 28px; margin-bottom: 6px; animation: spin 1s infinite linear;">⏳</div>
          <strong style="color: #d97706; font-size: 14px;">Approval Request Dispatched!</strong>
          <p style="font-size: 12px; color: #475569; margin: 6px 0;">
            Guardian alert sent to: <strong>${phoneInput}</strong>
          </p>
          <div id="blaxguard-live-link-box" style="margin: 8px 0; font-size: 11.5px;">
            <a id="blaxguard-guardian-page-link" href="#" target="_blank" style="color: #2563eb; text-decoration: underline; font-weight: 600;">
              🔗 Click to Open Guardian Review Screen (Demo)
            </a>
          </div>
          <div style="font-size: 11.5px; color: #94a3b8; margin-top: 6px;">
            🔒 Link remains locked until guardian decides.
          </div>
        </div>
      `;

      try {
        const resp = await fetch(GUARDIAN_REQUEST_API, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            url: url,
            guardianPhone: phoneInput,
            seniorName: "Senior Citizen / Child",
            source: "Chat Link"
          })
        });

        const reqData = await resp.json();
        if (reqData.success && reqData.requestId) {
          const pageLink = document.getElementById("blaxguard-guardian-page-link");
          if (pageLink && reqData.approvalUrl) {
            pageLink.href = reqData.approvalUrl;
          }

          // Start live polling for Guardian decision
          pollInterval = setInterval(async () => {
            try {
              const statusResp = await fetch(`${GUARDIAN_STATUS_API}?id=${reqData.requestId}`);
              if (!statusResp.ok) return;
              const statusData = await statusResp.json();

              if (statusData.status === "blocked") {
                clearInterval(pollInterval);
                section.innerHTML = `
                  <div style="text-align: center; padding: 14px 8px; background: #fef2f2; border: 1.5px solid #ef4444; border-radius: 10px;">
                    <div style="font-size: 32px; margin-bottom: 4px;">🛑</div>
                    <strong style="color: #dc2626; font-size: 14.5px;">ACCESS DENIED BY GUARDIAN</strong>
                    <p style="font-size: 12px; color: #7f1d1d; margin-top: 4px; line-height: 1.4;">
                      Your guardian reviewed this link and determined it is UNSAFE.<br>
                      <strong>For your protection, this link will NOT be opened.</strong>
                    </p>
                  </div>
                `;
              } else if (statusData.status === "allowed") {
                clearInterval(pollInterval);
                section.innerHTML = `
                  <div style="text-align: center; padding: 14px 8px; background: #ecfdf5; border: 1.5px solid #10b981; border-radius: 10px;">
                    <div style="font-size: 32px; margin-bottom: 4px;">✅</div>
                    <strong style="color: #059669; font-size: 14.5px;">APPROVED BY GUARDIAN</strong>
                    <p style="font-size: 12px; color: #065f46; margin: 4px 0 10px;">
                      Your guardian has granted permission to open this destination.
                    </p>
                    <button id="blaxguard-btn-open-allowed" style="background: #10b981; color: #fff; border: none; padding: 10px 22px; border-radius: 8px; font-weight: 700; cursor: pointer; font-size: 13.5px;">
                      🚀 Open Link Now
                    </button>
                  </div>
                `;
                document.getElementById("blaxguard-btn-open-allowed").onclick = () => {
                  overlay.remove();
                  window.open(url, "_blank");
                };
              }
            } catch (pollErr) {
              // Ignore transient poll failures
            }
          }, 2000);
        }
      } catch (err) {
        section.innerHTML = `
          <div style="color: #dc2626; font-size: 12px; text-align: center; padding: 8px;">
            ⚠️ Unable to connect to BlaxGuard server to dispatch request.
          </div>
        `;
      }
    };
  }

  // Intercept all link clicks in WhatsApp Web and Telegram Web
  document.addEventListener("click", async (e) => {
    const link = e.target.closest("a");
    if (!link || !link.href) return;

    const href = link.href;
    if (!href.startsWith("http")) return;
    if (href.includes("whatsapp.com") || href.includes("telegram.org")) return;

    // Fast heuristic check
    const isRiskyTld = RISKY_TLDS.test(href);
    const isApk = href.toLowerCase().includes(".apk");

    // Intercept click
    e.preventDefault();
    e.stopPropagation();

    try {
      // Query central BlaxGuard API
      const resp = await fetch(API_ENDPOINT, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: href })
      });
      const data = await resp.json();

      if (data.verdict === "danger" || data.verdict === "caution") {
        showMessengerWarningPopup(href, data.score, data.reasons || ["Unverified domain"]);
      } else {
        // Safe link, open normally
        window.open(href, "_blank");
      }
    } catch (err) {
      // Offline fallback: check basic threat markers
      if (isRiskyTld || isApk) {
        showMessengerWarningPopup(href, 75, ["Suspicious high-risk web domain or APK file download"]);
      } else {
        window.open(href, "_blank");
      }
    }
  }, true);
})();
