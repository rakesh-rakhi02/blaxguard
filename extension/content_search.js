/**
 * BlaxGuard Search Engine Real-Time Inspector
 * Injects safety badges and pop-up warnings on Google and Bing search results
 * using the central BlaxGuard scam detection engine (POST /api/check).
 */

(function () {
  console.log("[BlaxGuard] Search Engine Protection Active (Connected to Backend Engine)");

  const API_ENDPOINT = "http://localhost:8080/api/check";
  const API_TIMEOUT_MS = 2500;

  // In-memory cache to prevent duplicate network calls for the same URL
  const evaluationCache = new Map();

  /**
   * Offline heuristic fallback - explicitly labeled as fallback when backend is unreachable.
   */
  function evaluateOfflineFallback(href) {
    const isRiskyTld = /\.(xyz|top|online|club|buzz|work|live|loan|vip|icu|tk|ml|ga|cf|gq|site|space|guru|cam|rest)(?:[\/\?\s]|$)/i.test(href);
    const isRawIp = /https?:\/\/\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}/i.test(href);
    const isApk = /(\.apk|\.apk\.zip)/i.test(href);

    if (isRiskyTld || isRawIp || isApk) {
      return {
        verdict: "danger",
        score: 75,
        reasons: ["(Offline Fallback) High-risk domain ending (.xyz/.top/IP) or direct APK download detected while BlaxGuard server is unreachable."],
        verifiedLender: null,
        isFallback: true
      };
    }

    return {
      verdict: "unknown",
      score: null,
      reasons: ["(Offline Fallback) BlaxGuard server is unreachable at http://localhost:8080. Unable to verify entity."],
      verifiedLender: null,
      isFallback: true
    };
  }

  /**
   * Evaluates a URL against the central BlaxGuard backend engine with caching, timeouts, and fallback.
   */
  async function evaluateUrlWithEngine(url) {
    if (!url || !url.startsWith("http")) return null;

    // Check cache first to avoid repeated calls
    if (evaluationCache.has(url)) {
      return evaluationCache.get(url);
    }

    const fetchPromise = (async () => {
      try {
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), API_TIMEOUT_MS);

        const response = await fetch(API_ENDPOINT, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ text: url }),
          signal: controller.signal
        });

        clearTimeout(timeoutId);

        if (!response.ok) {
          throw new Error(`HTTP error ${response.status}`);
        }

        const data = await response.json();

        // Validate response schema
        if (data && typeof data === "object" && typeof data.verdict === "string") {
          return {
            verdict: data.verdict, // "safe" | "caution" | "danger"
            score: typeof data.score === "number" ? data.score : 0,
            reasons: Array.isArray(data.reasons) ? data.reasons : [],
            verifiedLender: data.verifiedLender || null,
            hasGenuineWhitelist: !!data.hasGenuineWhitelist,
            isFallback: false
          };
        } else {
          throw new Error("Invalid response schema from BlaxGuard API");
        }
      } catch (err) {
        // Graceful fallback labeled as offline heuristic
        return evaluateOfflineFallback(url);
      }
    })();

    evaluationCache.set(url, fetchPromise);
    return fetchPromise;
  }

  /**
   * Creates an interactive warning modal popup when a suspicious search result or warning badge is clicked.
   */
  function createWarningPopupModal(url, data) {
    const existing = document.getElementById("blaxguard-popup-modal");
    if (existing) existing.remove();

    const overlay = document.createElement("div");
    overlay.id = "blaxguard-popup-modal";
    overlay.style.cssText = `
      position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
      background: rgba(15, 23, 42, 0.8); backdrop-filter: blur(5px);
      display: flex; align-items: center; justify-content: center;
      z-index: 9999999; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    `;

    const scoreDisplay = data.score !== null ? `${data.score} / 100` : "Unrated";
    const statusLabel = data.verdict === "danger" ? "HIGH RISK DANGER" : "CAUTION ADVISED";
    const fallbackBanner = data.isFallback
      ? `<div style="background: #fffbeb; border: 1px solid #fcd34d; color: #92400e; font-size: 11px; padding: 4px 8px; border-radius: 6px; margin-bottom: 10px; font-weight: 600;">⚠️ Notice: Evaluated via offline fallback (BlaxGuard server unreachable)</div>`
      : "";

    const reasonsHtml = (data.reasons && data.reasons.length > 0)
      ? data.reasons.map(r => `<div style="margin-bottom: 4px;">• ${r}</div>`).join("")
      : "• Suspicious, unverified, or high-risk web entity.";

    overlay.innerHTML = `
    const savedPhone = localStorage.getItem("blaxguard_guardian_phone") || "+91 98765 43210";

    overlay.innerHTML = `
      <div style="background: #ffffff; border-radius: 18px; width: 92%; max-width: 500px; padding: 24px; box-shadow: 0 25px 50px -12px rgba(0,0,0,0.5); border: 2.5px solid #ef4444; animation: blaxguardFadeIn 0.2s ease;">
        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 12px;">
          <div style="display: flex; align-items: center; gap: 12px;">
            <span style="font-size: 32px;">🛡️</span>
            <div>
              <h3 style="margin: 0; font-size: 19px; color: #b91c1c; font-weight: 800;">BlaxGuard Guardian Shield</h3>
              <p style="margin: 2px 0 0; font-size: 12.5px; color: #64748b;">Senior & Child Protection Active</p>
            </div>
          </div>
          <span style="background: #fee2e2; color: #b91c1c; font-size: 11.5px; font-weight: 800; padding: 4px 10px; border-radius: 99px; border: 1px solid #fca5a5;">
            LOCKED 🔒
          </span>
        </div>
        
        ${fallbackBanner}

        <div style="background: #fef2f2; border: 1px solid #fecaca; border-radius: 10px; padding: 14px; margin-bottom: 14px;">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
            <span style="font-size: 12.5px; font-weight: 800; color: #991b1b;">Threat Assessment:</span>
            <span style="background: #ef4444; color: #fff; font-size: 11.5px; font-weight: 800; padding: 2px 8px; border-radius: 99px;">${statusLabel} (${scoreDisplay})</span>
          </div>
          <div style="font-size: 12.5px; color: #7f1d1d; line-height: 1.45;">
            ${reasonsHtml}
          </div>
          <div style="margin-top: 10px; font-size: 11.5px; color: #475569; word-break: break-all; background: #fff; padding: 8px; border-radius: 6px; border: 1px dashed #cbd5e1;">
            <strong>Destination:</strong> ${url}
          </div>
        </div>

        <!-- Guardian Approval Section -->
        <div id="blaxguard-search-guardian-section" style="background: #f8fafc; border: 1.5px solid #e2e8f0; border-radius: 12px; padding: 14px; margin-bottom: 16px;">
          <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 6px;">
            <span style="font-size: 18px;">👨‍👩‍👧</span>
            <strong style="font-size: 13px; color: #1e293b;">Family Consent Required</strong>
          </div>
          <p style="font-size: 12px; color: #64748b; line-height: 1.4; margin-bottom: 10px;">
            To prevent financial extortion, this suspicious link is locked and requires approval from your guardian.
          </p>
          <div style="display: flex; gap: 8px;">
            <input id="blaxguard-search-guardian-phone" type="tel" value="${savedPhone}" placeholder="Guardian Phone (+91 ...)" style="flex: 1; padding: 8px 10px; border: 1px solid #cbd5e1; border-radius: 8px; font-size: 13px; outline: none;">
            <button id="blaxguard-search-btn-ask" style="background: #2563eb; color: #fff; border: none; border-radius: 8px; padding: 8px 14px; font-size: 12.5px; font-weight: 700; cursor: pointer; white-space: nowrap;">
              📲 Ask Guardian
            </button>
          </div>
        </div>

        <div style="display: flex; gap: 10px; justify-content: flex-end;">
          <button id="blaxguard-btn-safe" style="padding: 10px 18px; background: #10b981; color: #fff; border: none; border-radius: 8px; font-weight: 700; cursor: pointer; font-size: 13.5px;">
            🛡️ Go Back to Safety
          </button>
        </div>
      </div>
    `;

    document.body.appendChild(overlay);

    let pollInterval = null;

    document.getElementById("blaxguard-btn-safe").onclick = () => {
      if (pollInterval) clearInterval(pollInterval);
      overlay.remove();
    };

    document.getElementById("blaxguard-search-btn-ask").onclick = async () => {
      const phoneInput = document.getElementById("blaxguard-search-guardian-phone").value.trim();
      if (!phoneInput) {
        alert("Please enter a guardian phone number.");
        return;
      }
      localStorage.setItem("blaxguard_guardian_phone", phoneInput);

      const section = document.getElementById("blaxguard-search-guardian-section");
      section.innerHTML = `
        <div style="text-align: center; padding: 12px 6px;">
          <div style="font-size: 28px; margin-bottom: 6px;">⏳</div>
          <strong style="color: #d97706; font-size: 14px;">Approval Request Dispatched!</strong>
          <p style="font-size: 12px; color: #475569; margin: 6px 0;">
            Guardian alert sent to: <strong>${phoneInput}</strong>
          </p>
          <div style="margin: 8px 0; font-size: 11.5px;">
            <a id="blaxguard-search-review-link" href="#" target="_blank" style="color: #2563eb; text-decoration: underline; font-weight: 600;">
              🔗 Click to Open Guardian Review Screen (Demo)
            </a>
          </div>
          <div style="font-size: 11.5px; color: #94a3b8; margin-top: 6px;">
            🔒 Link remains locked until guardian decides.
          </div>
        </div>
      `;

      try {
        const resp = await fetch("http://localhost:8080/api/guardian/request", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            url: url,
            guardianPhone: phoneInput,
            seniorName: "Senior Citizen / Child",
            source: "Search Result"
          })
        });

        const reqData = await resp.json();
        if (reqData.success && reqData.requestId) {
          const pageLink = document.getElementById("blaxguard-search-review-link");
          if (pageLink && reqData.approvalUrl) pageLink.href = reqData.approvalUrl;

          pollInterval = setInterval(async () => {
            try {
              const statusResp = await fetch(`http://localhost:8080/api/guardian/status?id=${reqData.requestId}`);
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
                    <button id="blaxguard-search-open-allowed" style="background: #10b981; color: #fff; border: none; padding: 10px 22px; border-radius: 8px; font-weight: 700; cursor: pointer; font-size: 13.5px;">
                      🚀 Open Link Now
                    </button>
                  </div>
                `;
                document.getElementById("blaxguard-search-open-allowed").onclick = () => {
                  overlay.remove();
                  window.location.href = url;
                };
              }
            } catch (pollErr) {}
          }, 2000);
        }
      } catch (err) {
        section.innerHTML = `<div style="color: #dc2626; font-size: 12px; text-align: center; padding: 8px;">⚠️ Server unreachable. Link kept locked.</div>`;
      }
    };
  }

  /**
   * Scans visible search result anchors on Google & Bing and applies safety badges asynchronously.
   */
  async function scanSearchResults() {
    // Select result anchors on Google or Bing that haven't been scanned
    const links = document.querySelectorAll("a[href^='http']:not([data-blaxguard-scanned])");

    for (const a of links) {
      a.setAttribute("data-blaxguard-scanned", "true");
      const href = a.href;

      // Skip internal search engine domains
      if (href.includes("google.com") || href.includes("google.co.in") || href.includes("bing.com") || href.includes("gstatic.com")) {
        continue;
      }

      // Query the central BlaxGuard scam engine
      evaluateUrlWithEngine(href).then(evalResult => {
        if (!evalResult) return;

        if (evalResult.verdict === "danger" || evalResult.verdict === "caution") {
          // Avoid duplicate badge injection
          if (a.nextSibling && a.nextSibling.classList && a.nextSibling.classList.contains("blaxguard-badge")) return;

          const badge = document.createElement("span");
          badge.className = "blaxguard-badge";
          badge.style.cssText = `
            display: inline-flex; align-items: center; gap: 4px;
            background: #fee2e2; color: #b91c1c; border: 1px solid #ef4444;
            font-size: 11px; font-weight: 700; padding: 2px 7px; border-radius: 6px;
            margin-left: 6px; vertical-align: middle; cursor: pointer; text-decoration: none;
          `;
          badge.innerHTML = `⚠️ Suspicious Link`;
          const tooltipReason = evalResult.reasons?.[0] || "Unverified domain";
          badge.title = `BlaxGuard: [${evalResult.verdict.toUpperCase()}] Risk Score: ${evalResult.score}/100. ${tooltipReason}`;

          a.parentNode.insertBefore(badge, a.nextSibling);

          // Intercept clicks on the link to pop warning
          a.addEventListener("click", (e) => {
            e.preventDefault();
            e.stopPropagation();
            createWarningPopupModal(href, evalResult);
          });

          badge.addEventListener("click", (e) => {
            e.preventDefault();
            e.stopPropagation();
            createWarningPopupModal(href, evalResult);
          });
        } else if (evalResult.verdict === "safe") {
          // Avoid duplicate badge injection
          if (a.nextSibling && a.nextSibling.classList && a.nextSibling.classList.contains("blaxguard-badge")) return;

          const badge = document.createElement("span");
          badge.className = "blaxguard-badge";
          badge.style.cssText = `
            display: inline-flex; align-items: center; gap: 4px;
            background: #d1fae5; color: #065f46; border: 1px solid #10b981;
            font-size: 11px; font-weight: 700; padding: 2px 7px; border-radius: 6px;
            margin-left: 6px; vertical-align: middle;
          `;
          badge.innerHTML = `🏛️ Verified Entity`;
          const entityDesc = evalResult.verifiedLender
            ? `${evalResult.verifiedLender.name} (${evalResult.verifiedLender.category})`
            : "Verified Clean";
          badge.title = `BlaxGuard: ${entityDesc}`;

          a.parentNode.insertBefore(badge, a.nextSibling);
        }
      });
    }
  }

  // Initial scan and MutationObserver for dynamically loaded / paged search results
  scanSearchResults();
  const observer = new MutationObserver(() => scanSearchResults());
  observer.observe(document.body, { childList: true, subtree: true });
})();
