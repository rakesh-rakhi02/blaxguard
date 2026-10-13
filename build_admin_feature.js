const fs = require('fs');

console.log('Reading template.html...');
let template = fs.readFileSync('template.html', 'utf8');

// Normalize line endings to \n
template = template.replace(/\r\n/g, '\n');

// ==============================================================
// 1. ADD CSS FOR ADMIN PAGE & PIN GATE
// ==============================================================
const adminCss = `
    /* ADMIN PAGE STYLES & PIN GATE */
    .admin-pin-card {
      background: var(--bg-card);
      border: 2px solid var(--steel-blue);
      border-radius: var(--radius-md);
      padding: 24px;
      text-align: center;
      max-width: 520px;
      margin: 10px auto;
      box-shadow: var(--shadow-sm);
    }
    .admin-pin-icon {
      font-size: 48px;
      line-height: 1;
      margin-bottom: 12px;
    }
    .demo-pin-callout {
      background: rgba(245, 158, 11, 0.12);
      border: 1.5px dashed var(--verdict-caution);
      border-radius: var(--radius-sm);
      padding: 14px 16px;
      margin: 16px 0;
      text-align: left;
    }
    .demo-pin-badge {
      display: inline-block;
      background: var(--verdict-caution);
      color: #ffffff;
      font-size: 11px;
      font-weight: 800;
      padding: 2px 8px;
      border-radius: 12px;
      letter-spacing: 0.5px;
      margin-bottom: 6px;
    }
    .demo-pin-text {
      font-size: 14.5px;
      line-height: 1.45;
      color: var(--text-main);
    }
    .pin-code-chip {
      background: var(--bg-card);
      color: var(--steel-blue);
      border: 1px solid var(--steel-blue-border);
      padding: 2px 8px;
      border-radius: 4px;
      font-family: monospace;
      font-size: 16px;
      font-weight: 800;
      letter-spacing: 2px;
    }
    .pin-input-wrap {
      margin: 18px 0 10px 0;
    }
    .pin-field {
      width: 100%;
      max-width: 260px;
      text-align: center;
      font-size: 26px;
      letter-spacing: 10px;
      font-weight: 800;
      padding: 12px 14px;
      border: 2px solid var(--steel-blue);
      border-radius: var(--radius-sm);
      background: var(--bg-card-subtle);
      color: var(--text-main);
      outline: none;
      transition: all 0.2s ease;
    }
    .pin-field:focus {
      border-color: var(--teal);
      box-shadow: 0 0 0 3px rgba(13, 148, 136, 0.2);
    }
    .pin-error-box {
      color: var(--verdict-danger);
      background: rgba(220, 38, 38, 0.1);
      border: 1px solid var(--verdict-danger);
      padding: 8px 12px;
      border-radius: var(--radius-sm);
      font-size: 13.5px;
      font-weight: 700;
      margin-top: 10px;
      display: inline-block;
      animation: shake 0.3s ease;
    }
    @keyframes shake {
      0%, 100% { transform: translateX(0); }
      25% { transform: translateX(-6px); }
      75% { transform: translateX(6px); }
    }

    /* ADMIN DASHBOARD HEADER & STATS */
    .admin-toolbar {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 10px;
      flex-wrap: wrap;
      margin-bottom: 16px;
    }
    .admin-session-pill {
      background: rgba(22, 163, 74, 0.15);
      color: var(--verdict-safe);
      border: 1px solid var(--verdict-safe);
      padding: 6px 12px;
      border-radius: 20px;
      font-size: 13px;
      font-weight: 700;
      display: inline-flex;
      align-items: center;
      gap: 6px;
    }
    .admin-stat-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(130px, 1fr));
      gap: 12px;
      margin-bottom: 20px;
    }
    .admin-stat-card {
      background: var(--bg-card-subtle);
      border: 1px solid var(--border-color);
      border-radius: var(--radius-sm);
      padding: 14px 12px;
      text-align: center;
      transition: transform 0.2s ease;
    }
    .admin-stat-card:hover {
      transform: translateY(-2px);
    }
    .admin-stat-num {
      font-size: 26px;
      font-weight: 800;
      color: var(--text-main);
      line-height: 1.2;
    }
    .admin-stat-label {
      font-size: 12.5px;
      color: var(--text-muted);
      font-weight: 600;
      margin-top: 4px;
    }

    /* VERDICT SPLIT CHART */
    .verdict-chart-card {
      background: var(--bg-card);
      border: 1.5px solid var(--border-color);
      border-radius: var(--radius-md);
      padding: 18px 20px;
      margin-bottom: 20px;
    }
    .verdict-chart-layout {
      display: flex;
      align-items: center;
      justify-content: space-around;
      gap: 20px;
      flex-wrap: wrap;
      margin: 16px 0;
    }
    .verdict-donut-wrap {
      position: relative;
      width: 140px;
      height: 140px;
      display: flex;
      align-items: center;
      justify-content: center;
      flex-shrink: 0;
    }
    .donut-svg {
      width: 100%;
      height: 100%;
      transform: rotate(-90deg);
    }
    .donut-center-info {
      position: absolute;
      text-align: center;
    }
    .donut-center-total {
      font-size: 22px;
      font-weight: 800;
      color: var(--text-main);
      line-height: 1;
    }
    .donut-center-sub {
      font-size: 11px;
      font-weight: 700;
      color: var(--text-muted);
      text-transform: uppercase;
    }
    .verdict-legend-grid {
      display: flex;
      flex-direction: column;
      gap: 10px;
      flex: 1;
      min-width: 200px;
    }
    .verdict-legend-item {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 10px;
      padding: 8px 12px;
      border-radius: var(--radius-sm);
      background: var(--bg-card-subtle);
      border: 1px solid var(--border-color);
      font-size: 14px;
      font-weight: 600;
    }
    .verdict-bar-track {
      width: 100%;
      height: 18px;
      border-radius: 9px;
      background: var(--border-color);
      display: flex;
      overflow: hidden;
      margin: 12px 0 6px 0;
    }
    .verdict-bar-seg {
      height: 100%;
      transition: width 0.4s ease;
    }
    .verdict-seg-safe { background: var(--verdict-safe); }
    .verdict-seg-caution { background: var(--verdict-caution); }
    .verdict-seg-danger { background: var(--verdict-danger); }

    /* TOP SCAMS RANKED BARS */
    .top-scam-row {
      margin-bottom: 12px;
    }
    .top-scam-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 14px;
      font-weight: 700;
      color: var(--text-main);
      margin-bottom: 4px;
    }
    .top-scam-track {
      width: 100%;
      height: 10px;
      border-radius: 5px;
      background: var(--border-color);
      overflow: hidden;
    }
    .top-scam-fill {
      height: 100%;
      background: linear-gradient(90deg, var(--steel-blue), var(--teal));
      border-radius: 5px;
      transition: width 0.4s ease;
    }

    /* MODERATION TABLE & ACTIONS */
    .mod-table-wrap {
      overflow-x: auto;
      margin: 12px 0;
      border-radius: var(--radius-sm);
      border: 1px solid var(--border-color);
    }
    .mod-table {
      width: 100%;
      border-collapse: collapse;
      font-size: 13.5px;
      min-width: 600px;
    }
    .mod-table th {
      background: var(--bg-card-subtle);
      color: var(--text-muted);
      font-weight: 800;
      text-align: left;
      padding: 10px 12px;
      border-bottom: 1.5px solid var(--border-color);
    }
    .mod-table td {
      padding: 10px 12px;
      border-bottom: 1px solid var(--border-color);
      color: var(--text-main);
      vertical-align: middle;
    }
    .mod-table tr:hover {
      background: rgba(59, 105, 152, 0.05);
    }
    .mod-hash-preview {
      font-family: monospace;
      font-size: 12.5px;
      color: var(--steel-blue);
      font-weight: 700;
    }
    .mod-action-btns {
      display: flex;
      align-items: center;
      gap: 6px;
    }
    .btn-act {
      padding: 4px 8px;
      font-size: 12px;
      font-weight: 700;
      border-radius: 4px;
      cursor: pointer;
      border: 1px solid transparent;
      transition: all 0.15s ease;
    }
    .btn-act-approve {
      background: rgba(22, 163, 74, 0.15);
      color: var(--verdict-safe);
      border-color: var(--verdict-safe);
    }
    .btn-act-approve:hover {
      background: var(--verdict-safe);
      color: #fff;
    }
    .btn-act-reject {
      background: rgba(217, 119, 6, 0.15);
      color: var(--verdict-caution);
      border-color: var(--verdict-caution);
    }
    .btn-act-reject:hover {
      background: var(--verdict-caution);
      color: #fff;
    }
    .btn-act-remove {
      background: rgba(220, 38, 38, 0.12);
      color: var(--verdict-danger);
      border-color: var(--verdict-danger);
    }
    .btn-act-remove:hover {
      background: var(--verdict-danger);
      color: #fff;
    }

    /* RULE HITS TABLE */
    .rule-hit-row {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      padding: 10px 12px;
      border-bottom: 1px solid var(--border-color);
      font-size: 14px;
    }
    .rule-hit-row:last-child {
      border-bottom: none;
    }
    .rule-hit-info {
      flex: 1;
      min-width: 0;
    }
    .rule-hit-name {
      font-weight: 700;
      color: var(--text-main);
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .rule-hit-desc {
      font-size: 12.5px;
      color: var(--text-muted);
      margin-top: 2px;
    }
    .rule-hit-stats {
      text-align: right;
      flex-shrink: 0;
      min-width: 90px;
    }
    .rule-hit-count {
      font-weight: 800;
      font-size: 15px;
      color: var(--text-main);
    }
    .rule-hit-bar {
      width: 70px;
      height: 6px;
      background: var(--border-color);
      border-radius: 3px;
      overflow: hidden;
      margin-top: 4px;
      margin-left: auto;
    }
    .rule-hit-fill {
      height: 100%;
      background: var(--steel-blue);
      border-radius: 3px;
    }
    .sev-pill {
      font-size: 11px;
      font-weight: 800;
      padding: 2px 6px;
      border-radius: 10px;
    }
    .sev-critical { background: rgba(220, 38, 38, 0.15); color: var(--verdict-danger); }
    .sev-high { background: rgba(217, 119, 6, 0.15); color: var(--verdict-caution); }
    .sev-medium { background: rgba(59, 105, 152, 0.15); color: var(--steel-blue); }

    /* ZERO KNOWLEDGE BANNER */
    .zero-knowledge-banner {
      background: rgba(13, 148, 136, 0.08);
      border: 1.5px solid var(--teal);
      border-radius: var(--radius-sm);
      padding: 14px 16px;
      margin-top: 18px;
      display: flex;
      align-items: flex-start;
      gap: 12px;
    }
    .zero-knowledge-banner p {
      font-size: 13.5px;
      line-height: 1.45;
      color: var(--text-main);
      margin: 0;
    }
`;

if (!template.includes('/* ADMIN PAGE STYLES & PIN GATE */')) {
  const styleEndIdx = template.indexOf('</style>');
  template = template.substring(0, styleEndIdx) + adminCss + '\n  ' + template.substring(styleEndIdx);
  console.log('Appended Admin CSS to template.');
}

// ==============================================================
// 2. REPLACE PAGE 8 ADMIN HTML WITH PIN GATE + DASHBOARD
// ==============================================================
const adminPageHtml = `      <!-- ============================================== -->
      <!-- PAGE 8: ADMIN (PIN-Protected Threat & Telemetry Console) -->
      <!-- ============================================== -->
      <section id="page-admin" class="page-section">
        
        <!-- 1. PIN ENTRY GATE (SHOWN WHEN LOCKED) -->
        <div id="adminPinGate" class="admin-pin-card">
          <div class="admin-pin-icon">🔐</div>
          <h2 class="section-title" style="justify-content: center; font-size: 22px;">
            <span>BlaxGuard</span> <span data-i18n="adminPinTitle">Admin Threat Console</span>
          </h2>
          <p class="section-subtitle" style="text-align: center; margin: 6px 0 14px 0;" data-i18n="adminPinSub">
            Authorized threat telemetry, heuristic audits, and community report moderation.
          </p>

          <!-- DEMO ONLY PIN NOTICE -->
          <div class="demo-pin-callout">
            <span class="demo-pin-badge" data-i18n="adminPinDemoBadge">DEMO ONLY</span>
            <div class="demo-pin-text" data-i18n="adminPinDemoNote">
              Default Demo PIN: <strong><span class="pin-code-chip">1234</span></strong> (For evaluation and testing only)
            </div>
          </div>

          <div class="pin-input-wrap">
            <input type="password" id="adminPinInput" class="pin-field" placeholder="••••" maxlength="6" autocomplete="off" onkeydown="if(event.key==='Enter') submitAdminPin()">
            <div id="adminPinError" class="pin-error-box" style="display: none;" data-i18n="errInvalidPin">
              ⚠️ Incorrect PIN. Please use demo PIN 1234.
            </div>
          </div>

          <div style="display: flex; gap: 10px; justify-content: center; flex-wrap: wrap; margin-top: 14px;">
            <button type="button" class="btn btn-primary" onclick="submitAdminPin()" style="flex: 1; min-width: 150px;">
              <span>🔓</span> <span data-i18n="btnUnlockAdmin">Unlock Admin Console</span>
            </button>
            <button type="button" class="btn btn-outline" onclick="quickFillDemoPin()" style="flex: 1; min-width: 150px;">
              <span>⚡</span> <span data-i18n="btnQuickFillPin">Use Demo PIN (1234)</span>
            </button>
          </div>
        </div>

        <!-- 2. ADMIN DASHBOARD VIEW (SHOWN WHEN UNLOCKED) -->
        <div id="adminDashboardView" style="display: none;">
          
          <!-- TOP TOOLBAR -->
          <div class="admin-toolbar">
            <div>
              <h1 class="section-title" style="margin-bottom: 2px;">
                <span>⚙️</span> <span data-i18n="adminDashTitle">Threat Intelligence Telemetry</span>
              </h1>
              <p class="section-subtitle" style="margin-bottom: 0;" data-i18n="adminDashSub">
                Anonymous aggregate threat counts, heuristic rule hits, and community reports.
              </p>
            </div>
            <div style="display: flex; align-items: center; gap: 8px;">
              <span class="admin-session-pill" data-i18n="adminSessionBadge">Auditor Mode: Active 🟢</span>
              <button type="button" class="btn btn-outline" style="padding: 6px 12px; font-size: 13px;" onclick="lockAdmin()">
                <span data-i18n="adminLockBtn">🔒 Lock</span>
              </button>
            </div>
          </div>

          <!-- SUMMARY STAT METRICS -->
          <div class="admin-stat-grid">
            <div class="admin-stat-card">
              <div class="admin-stat-num" id="statTotalChecks" style="color: var(--steel-blue);">1,482</div>
              <div class="admin-stat-label" data-i18n="adminTotalChecksTitle">Total Checks Run</div>
            </div>
            <div class="admin-stat-card">
              <div class="admin-stat-num" id="statScamRate" style="color: var(--verdict-danger);">32.3%</div>
              <div class="admin-stat-label" data-i18n="adminScamRateTitle">Scam Catch Rate</div>
            </div>
            <div class="admin-stat-card">
              <div class="admin-stat-num" id="statRegistryCount" style="color: var(--teal);">8</div>
              <div class="admin-stat-label" data-i18n="adminRegistryCountTitle">Threat Hashes in DB</div>
            </div>
            <div class="admin-stat-card">
              <div class="admin-stat-num" style="color: var(--text-main);">13</div>
              <div class="admin-stat-label" data-i18n="adminActiveRulesTitle">Active Rules Monitored</div>
            </div>
          </div>

          <!-- VERDICT SPLIT CHART (SAFE / CAREFUL / SCAM) -->
          <div class="verdict-chart-card">
            <h3 class="card-title">
              <span>📊</span> <span data-i18n="adminVerdictSplitTitle">Verdict Distribution (Safe vs Careful vs Scam)</span>
            </h3>
            <p class="card-text" style="font-size: 14px; margin-bottom: 12px;" data-i18n="adminVerdictSplitSub">
              Real-time aggregate breakdown of automated decision-support classifications.
            </p>

            <div class="verdict-chart-layout">
              <!-- SVG Donut Chart -->
              <div class="verdict-donut-wrap">
                <svg viewBox="0 0 42 42" class="donut-svg" id="adminDonutSvg">
                  <!-- Injected dynamically in renderAdminDashboard() -->
                </svg>
                <div class="donut-center-info">
                  <div class="donut-center-total" id="adminDonutTotal">1,482</div>
                  <div class="donut-center-sub" data-i18n="adminTotalChecksTitle">Checks</div>
                </div>
              </div>

              <!-- Legend Cards -->
              <div class="verdict-legend-grid">
                <div class="verdict-legend-item">
                  <div style="display: flex; align-items: center; gap: 8px;">
                    <span style="color: var(--verdict-safe); font-size: 16px;">🟢</span>
                    <span data-i18n="adminVerdictSafe">Safe</span>
                  </div>
                  <div id="statVerdictSafeText" style="font-weight: 800; color: var(--verdict-safe);">620 (41.8%)</div>
                </div>
                <div class="verdict-legend-item">
                  <div style="display: flex; align-items: center; gap: 8px;">
                    <span style="color: var(--verdict-caution); font-size: 16px;">🟡</span>
                    <span data-i18n="adminVerdictCaution">Be Careful</span>
                  </div>
                  <div id="statVerdictCautionText" style="font-weight: 800; color: var(--verdict-caution);">384 (25.9%)</div>
                </div>
                <div class="verdict-legend-item">
                  <div style="display: flex; align-items: center; gap: 8px;">
                    <span style="color: var(--verdict-danger); font-size: 16px;">🔴</span>
                    <span data-i18n="adminVerdictScam">Likely Scam</span>
                  </div>
                  <div id="statVerdictScamText" style="font-weight: 800; color: var(--verdict-danger);">478 (32.3%)</div>
                </div>
              </div>
            </div>

            <!-- Segmented horizontal bar -->
            <div class="verdict-bar-track">
              <div id="segBarSafe" class="verdict-bar-seg verdict-seg-safe" style="width: 41.8%;" title="Safe"></div>
              <div id="segBarCaution" class="verdict-bar-seg verdict-seg-caution" style="width: 25.9%;" title="Be Careful"></div>
              <div id="segBarDanger" class="verdict-bar-seg verdict-seg-danger" style="width: 32.3%;" title="Likely Scam"></div>
            </div>
          </div>

          <!-- TOP REPORTED SCAM TYPES -->
          <div class="ui-card">
            <h3 class="card-title">
              <span>🚨</span> <span data-i18n="adminTopScamsTitle">Top Reported Scam Categories</span>
            </h3>
            <p class="card-text" style="font-size: 14px; margin-bottom: 14px;" data-i18n="adminTopScamsSub">
              Anonymous aggregate counts grouped by attack pattern. Zero message logging.
            </p>
            <div id="adminTopScamsContainer">
              <!-- Dynamically populated in renderAdminDashboard() -->
            </div>
          </div>

          <!-- NEWEST REPORTS WITH APPROVE / REJECT / REMOVE ACTIONS -->
          <div class="ui-card">
            <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 8px;">
              <div>
                <h3 class="card-title" style="margin-bottom: 2px;">
                  <span>🛡️</span> <span data-i18n="adminNewestReportsTitle">Community Reports Moderation Queue</span>
                </h3>
                <p class="card-text" style="font-size: 14px;" data-i18n="adminNewestReportsSub">
                  Approve, reject, or remove reported threat identifiers from the live registry.
                </p>
              </div>
              <div class="chips-group" style="margin-bottom: 0;">
                <button type="button" class="chip-btn active" id="chipModAll" onclick="filterModReports('all')">All</button>
                <button type="button" class="chip-btn" id="chipModPending" onclick="filterModReports('pending')">Pending</button>
                <button type="button" class="chip-btn" id="chipModVerified" onclick="filterModReports('verified')">Verified</button>
              </div>
            </div>

            <div class="mod-table-wrap">
              <table class="mod-table">
                <thead>
                  <tr>
                    <th data-i18n="adminColIdentifier">Identifier (Hash Preview)</th>
                    <th data-i18n="adminColCategory">Category</th>
                    <th data-i18n="adminColCount">Reports</th>
                    <th data-i18n="adminColDate">First Seen</th>
                    <th data-i18n="adminColStatus">Registry Status</th>
                    <th data-i18n="adminColActions">Actions</th>
                  </tr>
                </thead>
                <tbody id="adminModTableBody">
                  <!-- Dynamically populated in renderAdminDashboard() -->
                </tbody>
              </table>
            </div>
          </div>

          <!-- RULE-HIT TABLE (WHICH RULES FIRE MOST) -->
          <div class="ui-card">
            <h3 class="card-title">
              <span>📋</span> <span data-i18n="adminRuleHitsTitle">Detection Rule-Hit Frequency Table</span>
            </h3>
            <p class="card-text" style="font-size: 14px; margin-bottom: 12px;" data-i18n="adminRuleHitsSub">
              Which browser detection rules fire most frequently across all message and link scans.
            </p>
            <div id="adminRuleHitsContainer" style="border: 1px solid var(--border-color); border-radius: var(--radius-sm); overflow: hidden;">
              <!-- Dynamically populated in renderAdminDashboard() -->
            </div>
          </div>

          <!-- PRIVACY ARCHITECTURE VERIFICATION BANNER -->
          <div class="zero-knowledge-banner">
            <span style="font-size: 26px; line-height: 1;">🔒</span>
            <p data-i18n="adminPrivacyNotice">
              Zero-Knowledge Privacy Architecture: BlaxGuard stores strictly cryptographic SHA-256 hashes and aggregate integer counters. Message texts, SMS content, and personal identities are never recorded.
            </p>
          </div>

        </div>
      </section>
`;

const posAdminStart = template.indexOf('<section id="page-admin"');
const posAdminEnd = template.indexOf('</section>', posAdminStart) + 10;
template = template.substring(0, posAdminStart) + adminPageHtml + template.substring(posAdminEnd);
console.log('Replaced page-admin section HTML.');

// ==============================================================
// 3. ENHANCE BlaxGuardDataLayer TO STORE AGGREGATE TELEMETRY
// ==============================================================
// Check where BlaxGuardDataLayer is defined
const posDlStart = template.indexOf('const BlaxGuardDataLayer = (function() {');
const posDlReturn = template.indexOf('return {', posDlStart);

const enhancedTelemetryJs = `      // ============================================================
      // ANONYMOUS AGGREGATE TELEMETRY STORE (Zero message storage)
      // ============================================================
      let _totalChecksRun = 1482;
      const _verdictCounts = {
        safe: 620,
        caution: 384,
        danger: 478
      };

      const _ruleHitCounts = {
        otpPin: 481,
        urgency: 392,
        bankBrand: 356,
        kyc: 347,
        shortUrl: 312,
        instantLoan: 310,
        customerCare: 295,
        riskyTld: 279,
        apkDownload: 268,
        advanceFee: 225,
        httpOnly: 214,
        prize: 198,
        registryMatched: 183
      };
`;

template = template.substring(0, posDlReturn) + enhancedTelemetryJs + '\n      ' + template.substring(posDlReturn);

// Now add the new methods to the return object of BlaxGuardDataLayer
const dlReturnMethods = `        recordCheck(verdict, matchedRules) {
          _totalChecksRun++;
          if (_verdictCounts[verdict] !== undefined) {
            _verdictCounts[verdict]++;
          }
          if (Array.isArray(matchedRules)) {
            matchedRules.forEach(r => {
              if (_ruleHitCounts[r] !== undefined) {
                _ruleHitCounts[r]++;
              } else {
                _ruleHitCounts[r] = 1;
              }
            });
          }
        },

        getTelemetry() {
          return {
            totalChecks: _totalChecksRun,
            verdicts: { ..._verdictCounts },
            ruleHits: { ..._ruleHitCounts }
          };
        },

        approveReport(hash) {
          const entry = _memoryStore.get(hash);
          if (entry) {
            entry.status = "verified";
            return true;
          }
          return false;
        },

        rejectReport(hash) {
          const entry = _memoryStore.get(hash);
          if (entry) {
            entry.status = "rejected";
            return true;
          }
          return false;
        },

        removeReport(hash) {
          return _memoryStore.delete(hash);
        },
`;

const posReturnOpen = template.indexOf('return {', posDlStart) + 8;
template = template.substring(0, posReturnOpen) + '\n' + dlReturnMethods + template.substring(posReturnOpen);
console.log('Enhanced BlaxGuardDataLayer with telemetry and report moderation methods.');

// Connect evaluateTextSafety to record telemetry
const evalSafetyCall = `      // Record anonymous telemetry in data-layer (only counters, never message text)
      if (typeof BlaxGuardDataLayer !== "undefined") {
        BlaxGuardDataLayer.recordCheck(verdict, matchedRules);
      }`;

if (!template.includes('BlaxGuardDataLayer.recordCheck(verdict, matchedRules);')) {
  template = template.replace(
    'return {\n        score: finalScore,',
    `${evalSafetyCall}\n\n      return {\n        score: finalScore,`
  );
  console.log('Hooked evaluateTextSafety to recordCheck.');
}

// ==============================================================
// 4. ADD ADMIN JS CONTROLLERS & PIN AUTH LOGIC
// ==============================================================
const adminControllersJs = `    /* ============================================================== */
    /* ADMIN PORTAL LOGIC & DEMO PIN SCREEN CONTROLLERS               */
    /* ============================================================== */
    const DEMO_ADMIN_PIN = "1234";
    let isAdminAuthenticated = false;
    let currentModFilter = "all";

    function submitAdminPin() {
      const pinInput = document.getElementById("adminPinInput");
      const errBox = document.getElementById("adminPinError");
      const entered = pinInput ? pinInput.value.trim() : "";

      if (entered === DEMO_ADMIN_PIN) {
        isAdminAuthenticated = true;
        sessionStorage.setItem("blaxguard_admin_auth", "true");
        if (errBox) errBox.style.display = "none";
        if (pinInput) pinInput.value = "";
        showAdminDashboard();
      } else {
        if (errBox) {
          errBox.style.display = "inline-block";
          errBox.classList.remove("pin-error-box");
          void errBox.offsetWidth; // trigger reflow
          errBox.classList.add("pin-error-box");
        }
        if (pinInput) {
          pinInput.focus();
          pinInput.select();
        }
      }
    }

    function quickFillDemoPin() {
      const pinInput = document.getElementById("adminPinInput");
      if (pinInput) {
        pinInput.value = DEMO_ADMIN_PIN;
        submitAdminPin();
      }
    }

    function lockAdmin() {
      isAdminAuthenticated = false;
      sessionStorage.removeItem("blaxguard_admin_auth");
      const pinGate = document.getElementById("adminPinGate");
      const dashView = document.getElementById("adminDashboardView");
      const pinInput = document.getElementById("adminPinInput");
      const errBox = document.getElementById("adminPinError");

      if (pinGate) pinGate.style.display = "block";
      if (dashView) dashView.style.display = "none";
      if (pinInput) pinInput.value = "";
      if (errBox) errBox.style.display = "none";
    }

    function showAdminDashboard() {
      const pinGate = document.getElementById("adminPinGate");
      const dashView = document.getElementById("adminDashboardView");
      if (pinGate) pinGate.style.display = "none";
      if (dashView) dashView.style.display = "block";
      renderAdminDashboard();
    }

    function filterModReports(status) {
      currentModFilter = status;
      ['all', 'pending', 'verified'].forEach(st => {
        const btn = document.getElementById("chipMod" + st.charAt(0).toUpperCase() + st.slice(1));
        if (btn) {
          if (st === status) btn.classList.add("active");
          else btn.classList.remove("active");
        }
      });
      renderModTable();
    }

    function approveReportUI(hash) {
      BlaxGuardDataLayer.approveReport(hash);
      const dict = translations[currentLang] || translations.en;
      alert(dict.adminToastApproved || "✅ Threat approved and published as Verified Threat in Registry.");
      renderAdminDashboard();
      renderRegistryList();
    }

    function rejectReportUI(hash) {
      BlaxGuardDataLayer.rejectReport(hash);
      const dict = translations[currentLang] || translations.en;
      alert(dict.adminToastRejected || "⚠️ Threat marked as Rejected / Inactive in Registry.");
      renderAdminDashboard();
      renderRegistryList();
    }

    function removeReportUI(hash) {
      BlaxGuardDataLayer.removeReport(hash);
      const dict = translations[currentLang] || translations.en;
      alert(dict.adminToastRemoved || "🗑️ Report identifier removed from Registry.");
      renderAdminDashboard();
      renderRegistryList();
    }

    function renderModTable() {
      const tbody = document.getElementById("adminModTableBody");
      if (!tbody) return;

      const dict = translations[currentLang] || translations.en;
      let reports = BlaxGuardDataLayer.getAllReports();

      if (currentModFilter !== "all") {
        reports = reports.filter(r => (r.status || "pending") === currentModFilter);
      }

      if (reports.length === 0) {
        tbody.innerHTML = '<tr><td colspan="6" style="text-align: center; color: var(--text-muted); padding: 18px;">No reports in this category.</td></tr>';
        return;
      }

      let html = "";
      reports.forEach(r => {
        const typeName = getScamTypeName(r.scamType);
        const hashShort = r.hash.slice(0, 10) + "..." + r.hash.slice(-6);
        const statusClass = r.status === "verified" ? "threat-status-verified" : (r.status === "rejected" ? "threat-status-flagged" : "threat-status-active");
        const statusText = r.status === "verified" 
          ? (dict.adminStatusVerified || "Verified Threat") 
          : (r.status === "rejected" ? (dict.adminStatusRejected || "Rejected") : (dict.adminStatusPending || "Pending Review"));

        html += \`
          <tr>
            <td>
              <span class="mod-hash-preview" title="\${r.hash}">sha256:\${hashShort}</span>
              \${r.display ? '<div style="font-size: 11.5px; color: var(--text-muted);">' + r.display + '</div>' : ''}
            </td>
            <td><span class="scam-type-badge">\${typeName}</span></td>
            <td><strong style="color: var(--steel-blue);">\${r.count}</strong></td>
            <td style="color: var(--text-muted); font-size: 12.5px;">\${r.date || r.firstReported || "2026-10-06"}</td>
            <td><span class="threat-status-badge \${statusClass}">\${statusText}</span></td>
            <td>
              <div class="mod-action-btns">
                <button type="button" class="btn-act btn-act-approve" onclick="approveReportUI('\${r.hash}')" title="Approve as Verified Threat">
                  \${dict.adminActionApprove || "Approve"}
                </button>
                <button type="button" class="btn-act btn-act-reject" onclick="rejectReportUI('\${r.hash}')" title="Reject Report">
                  \${dict.adminActionReject || "Reject"}
                </button>
                <button type="button" class="btn-act btn-act-remove" onclick="removeReportUI('\${r.hash}')" title="Remove from Registry">
                  \${dict.adminActionRemove || "Remove"}
                </button>
              </div>
            </td>
          </tr>
        \`;
      });
      tbody.innerHTML = html;
    }

    function renderAdminDashboard() {
      const telemetry = BlaxGuardDataLayer.getTelemetry();
      const dict = translations[currentLang] || translations.en;
      const total = telemetry.totalChecks || 1;
      const safe = telemetry.verdicts.safe || 0;
      const caution = telemetry.verdicts.caution || 0;
      const danger = telemetry.verdicts.danger || 0;

      const safePct = ((safe / total) * 100).toFixed(1);
      const cautionPct = ((caution / total) * 100).toFixed(1);
      const dangerPct = ((danger / total) * 100).toFixed(1);

      // 1. Metric numbers
      const elTotal = document.getElementById("statTotalChecks");
      if (elTotal) elTotal.textContent = total.toLocaleString();

      const elScamRate = document.getElementById("statScamRate");
      if (elScamRate) elScamRate.textContent = (((caution + danger) / total) * 100).toFixed(1) + "%";

      const elRegCount = document.getElementById("statRegistryCount");
      if (elRegCount) elRegCount.textContent = BlaxGuardDataLayer.getAllReports().length;

      // 2. Verdict Split (Donut Chart & Segmented Bar)
      const elDonutTotal = document.getElementById("adminDonutTotal");
      if (elDonutTotal) elDonutTotal.textContent = total.toLocaleString();

      const elSafeText = document.getElementById("statVerdictSafeText");
      if (elSafeText) elSafeText.textContent = \`\${safe} (\${safePct}%)\`;

      const elCautionText = document.getElementById("statVerdictCautionText");
      if (elCautionText) elCautionText.textContent = \`\${caution} (\${cautionPct}%)\`;

      const elScamText = document.getElementById("statVerdictScamText");
      if (elScamText) elScamText.textContent = \`\${danger} (\${dangerPct}%)\`;

      const barSafe = document.getElementById("segBarSafe");
      if (barSafe) barSafe.style.width = safePct + "%";
      const barCaution = document.getElementById("segBarCaution");
      if (barCaution) barCaution.style.width = cautionPct + "%";
      const barDanger = document.getElementById("segBarDanger");
      if (barDanger) barDanger.style.width = dangerPct + "%";

      // SVG Donut calculation (circumference of r=15.9155 is 100)
      const svg = document.getElementById("adminDonutSvg");
      if (svg) {
        const offsetSafe = 100 - parseFloat(safePct);
        const offsetCaution = offsetSafe - parseFloat(cautionPct);
        svg.innerHTML = \`
          <circle cx="21" cy="21" r="15.9155" fill="transparent" stroke="var(--border-color)" stroke-width="6"></circle>
          <circle cx="21" cy="21" r="15.9155" fill="transparent" stroke="var(--verdict-safe)" stroke-width="6"
                  stroke-dasharray="\${safePct} \${100 - parseFloat(safePct)}" stroke-dashoffset="0"></circle>
          <circle cx="21" cy="21" r="15.9155" fill="transparent" stroke="var(--verdict-caution)" stroke-width="6"
                  stroke-dasharray="\${cautionPct} \${100 - parseFloat(cautionPct)}" stroke-dashoffset="-\${safePct}"></circle>
          <circle cx="21" cy="21" r="15.9155" fill="transparent" stroke="var(--verdict-danger)" stroke-width="6"
                  stroke-dasharray="\${dangerPct} \${100 - parseFloat(dangerPct)}" stroke-dashoffset="-\${parseFloat(safePct) + parseFloat(cautionPct)}"></circle>
        \`;
      }

      // 3. Top Reported Scam Types
      const reports = BlaxGuardDataLayer.getAllReports();
      const catCounts = {};
      let totalReportCount = 0;
      reports.forEach(r => {
        catCounts[r.scamType] = (catCounts[r.scamType] || 0) + (r.count || 1);
        totalReportCount += (r.count || 1);
      });
      totalReportCount = Math.max(1, totalReportCount);

      const topCats = Object.entries(catCounts).sort((a, b) => b[1] - a[1]);
      const topScamsContainer = document.getElementById("adminTopScamsContainer");
      if (topScamsContainer) {
        let html = "";
        topCats.forEach(([cat, cnt]) => {
          const typeName = getScamTypeName(cat);
          const pct = ((cnt / totalReportCount) * 100).toFixed(1);
          html += \`
            <div class="top-scam-row">
              <div class="top-scam-header">
                <span>\${typeName}</span>
                <span>\${cnt} reports (\${pct}%)</span>
              </div>
              <div class="top-scam-track">
                <div class="top-scam-fill" style="width: \${pct}%;"></div>
              </div>
            </div>
          \`;
        });
        topScamsContainer.innerHTML = html;
      }

      // 4. Moderation Table
      renderModTable();

      // 5. Rule Hits Frequency Table
      const ruleHitsContainer = document.getElementById("adminRuleHitsContainer");
      if (ruleHitsContainer) {
        const rulesMeta = [
          { key: "otpPin", sev: "critical", nameKey: "ruleNameOtp", descKey: "ruleDescOtp" },
          { key: "urgency", sev: "high", nameKey: "ruleNameUrgency", descKey: "ruleDescUrgency" },
          { key: "bankBrand", sev: "high", nameKey: "ruleNameBankBrand", descKey: "ruleDescBankBrand" },
          { key: "kyc", sev: "high", nameKey: "ruleNameKyc", descKey: "ruleDescKyc" },
          { key: "apkDownload", sev: "critical", nameKey: "ruleNameApk", descKey: "ruleDescApk" },
          { key: "shortUrl", sev: "medium", nameKey: "ruleNameShortUrl", descKey: "ruleDescShortUrl" },
          { key: "instantLoan", sev: "high", nameKey: "ruleNameInstantLoan", descKey: "ruleDescInstantLoan" },
          { key: "customerCare", sev: "high", nameKey: "ruleNameCustomerCare", descKey: "ruleDescCustomerCare" },
          { key: "riskyTld", sev: "medium", nameKey: "ruleNameRiskyTld", descKey: "ruleDescRiskyTld" },
          { key: "advanceFee", sev: "critical", nameKey: "ruleNameAdvanceFee", descKey: "ruleDescAdvanceFee" },
          { key: "httpOnly", sev: "medium", nameKey: "ruleNameHttpOnly", descKey: "ruleDescHttpOnly" },
          { key: "prize", sev: "medium", nameKey: "ruleNamePrize", descKey: "ruleDescPrize" },
          { key: "registryMatched", sev: "critical", nameKey: "ruleNameRegistryMatched", descKey: "ruleDescRegistryMatched" }
        ];

        // Sort rules by hit count descending
        rulesMeta.sort((a, b) => (telemetry.ruleHits[b.key] || 0) - (telemetry.ruleHits[a.key] || 0));

        let html = "";
        rulesMeta.forEach(r => {
          const hits = telemetry.ruleHits[r.key] || 0;
          const pct = ((hits / total) * 100).toFixed(1);
          const name = dict[r.nameKey] || r.key;
          const desc = dict[r.descKey] || "";
          const sevClass = "sev-" + r.sev;
          const sevText = r.sev === "critical" 
            ? (dict.adminSeverityCritical || "Critical") 
            : (r.sev === "high" ? (dict.adminSeverityHigh || "High") : (dict.adminSeverityMedium || "Medium"));

          html += \`
            <div class="rule-hit-row">
              <div class="rule-hit-info">
                <div class="rule-hit-name">
                  <span>\${name}</span>
                  <span class="sev-pill \${sevClass}">\${sevText}</span>
                </div>
                <div class="rule-hit-desc">\${desc}</div>
              </div>
              <div class="rule-hit-stats">
                <div class="rule-hit-count">\${hits}</div>
                <div style="font-size: 11.5px; color: var(--text-muted);">\${pct}% of scans</div>
                <div class="rule-hit-bar">
                  <div class="rule-hit-fill" style="width: \${pct}%;"></div>
                </div>
              </div>
            </div>
          \`;
        });
        ruleHitsContainer.innerHTML = html;
      }
    }
`;

const posRefreshAdmin = template.indexOf('function refreshAdminData()');
template = template.substring(0, posRefreshAdmin) + adminControllersJs + '\n\n    ' + template.substring(posRefreshAdmin);
console.log('Injected Admin JS controllers.');

// Check handleRouting and update to handle admin
template = template.replace(
  'if (route === hash) {\n            pageEl.classList.add("active");\n          } else {',
  `if (route === hash) {
            pageEl.classList.add("active");
            if (route === "admin") {
              if (sessionStorage.getItem("blaxguard_admin_auth") === "true") {
                isAdminAuthenticated = true;
                showAdminDashboard();
              } else {
                lockAdmin();
              }
            }
          } else {`
);
console.log('Connected handleRouting to Admin lock/unlock state.');

// Update setLanguage to call renderAdminDashboard if authenticated
template = template.replace(
  'renderRegistryList();',
  'renderRegistryList();\n      if (isAdminAuthenticated) renderAdminDashboard();'
);
console.log('Connected setLanguage to renderAdminDashboard.');

// ==============================================================
// 5. TRANSLATIONS (EN, HI, TE) FOR ADMIN CONSOLE
// ==============================================================
const adminTransEn = `adminPinTitle: "Admin Threat Console",
        adminPinSub: "Authorized threat intelligence, heuristic audits, and community report moderation.",
        adminPinDemoBadge: "DEMO ONLY",
        adminPinDemoNote: "Default Demo PIN: <strong><span class='pin-code-chip'>1234</span></strong> (For evaluation and testing only)",
        adminPinPlaceholder: "Enter 4-Digit PIN",
        btnUnlockAdmin: "Unlock Admin Console",
        btnQuickFillPin: "Use Demo PIN (1234)",
        errInvalidPin: "⚠️ Incorrect PIN. Please use demo PIN 1234.",
        adminLockBtn: "🔒 Lock",
        adminSessionBadge: "Auditor Mode: Active 🟢",
        adminDashTitle: "Threat Intelligence Telemetry",
        adminDashSub: "Anonymous aggregate threat counts, heuristic rule hits, and community reports.",
        adminTotalChecksTitle: "Total Checks Run",
        adminTotalChecksSub: "Aggregate scans via rule engine",
        adminScamRateTitle: "Scam Catch Rate",
        adminScamRateSub: "Flagged Caution or Scam",
        adminRegistryCountTitle: "Threat Hashes in DB",
        adminRegistryCountSub: "Cryptographic SHA-256 records",
        adminActiveRulesTitle: "Active Rules Monitored",
        adminActiveRulesSub: "Zero-knowledge heuristic checks",
        adminVerdictSplitTitle: "Verdict Distribution (Safe vs Careful vs Scam)",
        adminVerdictSplitSub: "Real-time breakdown of automated decision-support classifications.",
        adminVerdictSafe: "Safe (Green)",
        adminVerdictCaution: "Be Careful (Amber)",
        adminVerdictScam: "Likely Scam (Red)",
        adminTopScamsTitle: "Top Reported Scam Categories",
        adminTopScamsSub: "Anonymous aggregate counts grouped by attack pattern. Zero message logging.",
        adminNewestReportsTitle: "Community Reports Moderation Queue",
        adminNewestReportsSub: "Approve, reject, or remove reported threat identifiers from the live registry.",
        adminPrivacyNotice: "Zero-Knowledge Privacy Architecture: BlaxGuard stores strictly cryptographic SHA-256 hashes and aggregate integer counters. Message texts, SMS content, and personal identities are never recorded.",
        adminColIdentifier: "Identifier (Hash Preview)",
        adminColCategory: "Category",
        adminColCount: "Reports",
        adminColDate: "First Seen",
        adminColStatus: "Registry Status",
        adminColActions: "Actions",
        adminActionApprove: "Approve",
        adminActionReject: "Reject",
        adminActionRemove: "Remove",
        adminStatusVerified: "Verified Threat",
        adminStatusPending: "Pending Review",
        adminStatusRejected: "Rejected Flag",
        adminToastApproved: "✅ Threat approved and published as Verified Threat in Registry.",
        adminToastRejected: "⚠️ Threat marked as Rejected / Inactive in Registry.",
        adminToastRemoved: "🗑️ Report identifier removed from Registry.",
        adminRuleHitsTitle: "Detection Rule-Hit Frequency Table",
        adminRuleHitsSub: "Which browser detection rules fire most frequently across all message and link scans.",
        adminSeverityCritical: "Critical",
        adminSeverityHigh: "High",
        adminSeverityMedium: "Medium",
        ruleNameUrgency: "False Urgency / Panic Claims",
        ruleDescUrgency: "Immediate disconnection, 2-hour deadlines, panic threats",
        ruleNameOtp: "OTP / PIN / CVV Requests",
        ruleDescOtp: "Demands secret one-time passwords or security credentials",
        ruleNameKyc: "Fake KYC Expiry & Bill Bait",
        ruleDescKyc: "Electricity disconnection, SIM block, Aadhaar/PAN re-KYC",
        ruleNameBankBrand: "Bank & Govt Brand Spoofing",
        ruleDescBankBrand: "Impersonates SBI, HDFC, ICICI, Police, CBI, Postal, RBI",
        ruleNameApk: "Malicious APK / Remote Access",
        ruleDescApk: "Prompts downloading APKs or screen-sharing tools (AnyDesk)",
        ruleNameCustomerCare: "10-Digit Fake Customer Care",
        ruleDescCustomerCare: "Personal mobile numbers impersonating official helplines",
        ruleNameInstantLoan: "Predatory Instant Loan Bait",
        ruleDescInstantLoan: "Instant approval without CIBIL, demanding contacts permission",
        ruleNameShortUrl: "Shortened / Masked URLs",
        ruleDescShortUrl: "bit.ly, tinyurl, or suspicious redirect link masking",
        ruleNameRiskyTld: "Risky / Free Domain Extensions",
        ruleDescRiskyTld: "Non-standard TLDs (.xyz, .top, .site, .live, .cam)",
        ruleNameAdvanceFee: "Advance Fee Before Disbursal",
        ruleDescAdvanceFee: "Upfront processing charges or GST advance requests",
        ruleNameHttpOnly: "Insecure Plain HTTP Links",
        ruleDescHttpOnly: "Unencrypted links lacking HTTPS transport security",
        ruleNamePrize: "Lottery & Reward Points Bait",
        ruleDescPrize: "Lucky draw wins, cash rewards, parcel clearance fees",
        ruleNameRegistryMatched: "Community Registry Match",
        ruleDescRegistryMatched: "Identified against known citizen-reported scam hashes",`;

const adminTransHi = `adminPinTitle: "BlaxGuard एडमिन कंसोल",
        adminPinSub: "अधिकृत खतरा विश्लेषण, हीयूरिस्टिक ऑडिट एवं सामुदायिक रिपोर्ट मॉडरेशन।",
        adminPinDemoBadge: "केवल डेमो",
        adminPinDemoNote: "डिफ़ॉल्ट डेमो पिन: <strong><span class='pin-code-chip'>1234</span></strong> (परीक्षण और मूल्यांकन के लिए)",
        adminPinPlaceholder: "4-अंकों का पिन दर्ज करें",
        btnUnlockAdmin: "एडमिन कंसोल अनलॉक करें",
        btnQuickFillPin: "डेमो पिन भरें (1234)",
        errInvalidPin: "⚠️ अमान्य पिन। कृपया डेमो पिन 1234 का उपयोग करें।",
        adminLockBtn: "🔒 लॉक",
        adminSessionBadge: "ऑडिटर मोड: सक्रिय 🟢",
        adminDashTitle: "थ्रेट इंटेलिजेंस टेलीमेट्री",
        adminDashSub: "अनाम कुल खतरे के आंकड़े, सुरक्षा नियमों की सक्रियता और सामुदायिक रिपोर्टें।",
        adminTotalChecksTitle: "कुल जांचे गए संदेश",
        adminTotalChecksSub: "रूल इंजन द्वारा कुल स्कैन",
        adminScamRateTitle: "पहचाने गए खतरे की दर",
        adminScamRateSub: "सावधान या संभावित फ्रॉड",
        adminRegistryCountTitle: "सामुदायिक थ्रेट हैश",
        adminRegistryCountSub: "क्रिप्टोग्राफिक SHA-256 रिकॉर्ड",
        adminActiveRulesTitle: "सक्रिय सुरक्षा नियम",
        adminActiveRulesSub: "गोपनीय हीयूरिस्टिक जांचें",
        adminVerdictSplitTitle: "निर्णय वितरण एवं जोखिम अनुपात",
        adminVerdictSplitSub: "स्वचालित निर्णय प्रणाली के परिणामों का लाइव विवरण।",
        adminVerdictSafe: "सुरक्षित (हरा)",
        adminVerdictCaution: "सतर्क रहें (पीला)",
        adminVerdictScam: "संभावित फ्रॉड (लाल)",
        adminTopScamsTitle: "शीर्ष रिपोर्ट की गई धोखाधड़ी श्रेणियां",
        adminTopScamsSub: "हमलों के पैटर्न अनुसार अनाम कुल आंकड़े। कोई मूल संदेश संग्रहीत नहीं होता।",
        adminNewestReportsTitle: "सामुदायिक रिपोर्ट मॉडरेशन कतार",
        adminNewestReportsSub: "सक्रिय रजिस्ट्री में रिपोर्ट किए गए खतरों को स्वीकृत, अस्वीकृत या हटाएं।",
        adminPrivacyNotice: "जीरो-नॉलेज प्राइवेसी आर्किटेक्चर: BlaxGuard केवल अनाम SHA-256 हैश और कुल संख्या सुरक्षित रखता है। संदेशों का मूल टेक्स्ट या व्यक्तिगत विवरण कभी भी स्टोर नहीं किया जाता।",
        adminColIdentifier: "पहचानकर्ता (हैश पूर्वावलोकन)",
        adminColCategory: "श्रेणी",
        adminColCount: "रिपोर्ट",
        adminColDate: "दर्ज तिथि",
        adminColStatus: "रजिस्ट्री स्थिति",
        adminColActions: "कार्रवाई",
        adminActionApprove: "स्वीकृत करें",
        adminActionReject: "अस्वीकृत करें",
        adminActionRemove: "हटाएं",
        adminStatusVerified: "सत्यापित खतरा",
        adminStatusPending: "समीक्षा लंबित",
        adminStatusRejected: "अस्वीकृत रिपोर्ट",
        adminToastApproved: "✅ खतरा स्वीकृत और रजिस्ट्री में 'सत्यापित खतरा' के रूप में अपडेट किया गया।",
        adminToastRejected: "⚠️ रिपोर्ट को रजिस्ट्री में 'अस्वीकृत' चिह्नित किया गया।",
        adminToastRemoved: "🗑️ पहचानकर्ता को रजिस्ट्री से हटा दिया गया।",
        adminRuleHitsTitle: "सुरक्षा नियम सक्रियता आवृत्ति तालिका",
        adminRuleHitsSub: "संदेश और लिंक स्कैनिंग में सबसे अधिक बार ट्रिगर होने वाले नियम।",
        adminSeverityCritical: "अति गंभीर",
        adminSeverityHigh: "उच्च",
        adminSeverityMedium: "मध्यम",
        ruleNameUrgency: "झूठा डर और तात्कालिकता",
        ruleDescUrgency: "बिजली कटने या 2 घंटे में खाते ब्लॉक की धमकी",
        ruleNameOtp: "ओटीपी या पिन की मांग",
        ruleDescOtp: "गोपनीय वन-टाइम पासवर्ड या बैंकिंग पिन मांगना",
        ruleNameKyc: "फर्जी केवाईसी और बिल की मांग",
        ruleDescKyc: "केवाईसी समाप्त होने या सिम ब्लॉक का दावा",
        ruleNameBankBrand: "बैंक और सरकारी ब्रांड नकल",
        ruleDescBankBrand: "SBI, HDFC, पुलिस, CBI या RBI के नाम पर धोखा",
        ruleNameApk: "दुर्भावनापूर्ण APK / स्क्रीन शेयर",
        ruleDescApk: "संदिग्ध APK या AnyDesk ऐप डाउनलोड करवाना",
        ruleNameCustomerCare: "10-अंकों का फर्जी कस्टमर केयर",
        ruleDescCustomerCare: "व्यक्तिगत मोबाइल नंबर को आधिकारिक हेल्पलाइन बताना",
        ruleNameInstantLoan: "अवैध तत्काल लोन का लालच",
        ruleDescInstantLoan: "बिना कागजात लोन और कॉन्टैक्ट्स की मांग",
        ruleNameShortUrl: "छोटे किए गए या छिपे हुए लिंक",
        ruleDescShortUrl: "bit.ly, tinyurl या रीडायरेक्ट लिंक",
        ruleNameRiskyTld: "खतरनाक डोमेन एक्सटेंशन",
        ruleDescRiskyTld: "असामान्य एक्सटेंशन (.xyz, .top, .live, .site)",
        ruleNameAdvanceFee: "लोन से पहले अग्रिम फीस",
        ruleDescAdvanceFee: "प्रोसेसिंग या जीएसटी के नाम पर पहले पैसे मांगना",
        ruleNameHttpOnly: "असुरक्षित प्लेन HTTP लिंक",
        ruleDescHttpOnly: "बिना HTTPS सुरक्षा वाले असुरक्षित लिंक",
        ruleNamePrize: "लॉटरी और फर्जी रिवॉर्ड का लालच",
        ruleDescPrize: "इनाम जीतने, लॉटरी या पार्सल शुल्क की मांग",
        ruleNameRegistryMatched: "सामुदायिक रजिस्ट्री में दर्ज",
        ruleDescRegistryMatched: "नागरिकों द्वारा पहले से रिपोर्ट किए गए फ्रॉड हैश से मिलान",`;

const adminTransTe = `adminPinTitle: "BlaxGuard అడ్మిన్ కన్సోల్",
        adminPinSub: "అధీకృత ముప్పు సమాచారం, పరిశీలనలు మరియు కమ్యూనిటీ రిపోర్ట్ పర్యవేక్షణ.",
        adminPinDemoBadge: "డెమో మాత్రమే",
        adminPinDemoNote: "డిఫాల్ట్ డెమో పిన్: <strong><span class='pin-code-chip'>1234</span></strong> (పరీక్షించడానికి మాత్రమే)",
        adminPinPlaceholder: "4-అంకెల పిన్ నమోదు చేయండి",
        btnUnlockAdmin: "అడ్మిన్ కన్సోల్ అన్‌లాక్ చేయండి",
        btnQuickFillPin: "డెమో పిన్ వాడండి (1234)",
        errInvalidPin: "⚠️ తప్పుడు పిన్. దయచేసి డెమో పిన్ 1234 ఉపయోగించండి.",
        adminLockBtn: "🔒 లాక్",
        adminSessionBadge: "ఆడిటర్ మోడ్: యాక్టివ్ 🟢",
        adminDashTitle: "ముప్పు సమాచార టెలిమెట్రీ",
        adminDashSub: "అజ్ఞాత మొత్తం ముప్పు గణాంకాలు, సెక్యూరిటీ రూల్స్ ట్రిగ్గర్లు మరియు రిపోర్టులు.",
        adminTotalChecksTitle: "మొత్తం నిర్వహించిన తనిఖీలు",
        adminTotalChecksSub: "రూల్ ఇంజిన్ ద్వారా జరిగిన మొత్తం స్కాన్లు",
        adminScamRateTitle: "గుర్తించిన ముప్పు శాతం",
        adminScamRateSub: "హెచ్చరిక లేదా మోసపూరిత గుర్తింపులు",
        adminRegistryCountTitle: "కమ్యూనిటీ ముప్పు హ్యాష్‌లు",
        adminRegistryCountSub: "క్రిప్టోగ్రాఫిక్ SHA-256 రికార్డులు",
        adminActiveRulesTitle: "యాక్టివ్ రూల్స్ పర్యవేక్షణ",
        adminActiveRulesSub: "జీరో-నాలెడ్జ్ పరిశీలనలు",
        adminVerdictSplitTitle: "నిర్ణయాల విభజన & ప్రమాద నిష్పత్తి",
        adminVerdictSplitSub: "ఆటోమేటెడ్ నిర్ణయ మద్దతు వ్యవస్థ ఫలితాల ప్రత్యక్ష విశ్లేషణ.",
        adminVerdictSafe: "సురక్షితం (ఆకుపచ్చ)",
        adminVerdictCaution: "జాగ్రత్త (పసుపు)",
        adminVerdictScam: "మోసం (ఎరుపు)",
        adminTopScamsTitle: "అత్యధికంగా నివేదించబడిన మోసాల వర్గాలు",
        adminTopScamsSub: "దాడుల విధానం ప్రకారం అజ్ఞాత గణాంకాలు. సందేశాలు ఎప్పుడూ సేవ్ చేయబడవు.",
        adminNewestReportsTitle: "కమ్యూనిటీ రిపోర్టుల మోడరేషన్ క్యూ",
        adminNewestReportsSub: "లైవ్ రిజిస్ట్రీలో నమోదైన ముప్పులను ఆమోదించండి, తిరస్కరించండి లేదా తొలగించండి.",
        adminPrivacyNotice: "జీరో-నాలెడ్జ్ గోప్యతా విధానం: BlaxGuard కేవలం అజ్ఞాత SHA-256 హ్యాష్‌లను మరియు మొత్తం సంఖ్యలను మాత్రమే భద్రపరుస్తుంది. అసలు సందేశాలు లేదా వ్యక్తిగత వివరాలు ఎప్పుడూ భద్రపరచబడవు.",
        adminColIdentifier: "గుర్తింపు హ్యాష్ (ప్రివ్యూ)",
        adminColCategory: "వర్గం",
        adminColCount: "రిపోర్టులు",
        adminColDate: "నమోదైన తేదీ",
        adminColStatus: "రిజిస్ట్రీ స్థితి",
        adminColActions: "చర్యలు",
        adminActionApprove: "ఆమోదించు",
        adminActionReject: "తిరస్కరించు",
        adminActionRemove: "తొలగించు",
        adminStatusVerified: "ధృవీకరించబడిన ముప్పు",
        adminStatusPending: "సమీక్ష పెండింగ్",
        adminStatusRejected: "తిరస్కరించబడింది",
        adminToastApproved: "✅ ముప్పు ఆమోదించబడింది మరియు రిజిస్ట్రీలో 'ధృవీకరించబడిన ముప్పు'గా నవీకరించబడింది.",
        adminToastRejected: "⚠️ రిపోర్ట్ రిజిస్ట్రీలో 'తిరస్కరించబడింది'గా మార్చబడింది.",
        adminToastRemoved: "🗑️ రిపోర్ట్ రిజిస్ట్రీ నుండి తొలగించబడింది.",
        adminRuleHitsTitle: "సెక్యూరిటీ రూల్స్ యాక్టివేషన్ పట్టిక",
        adminRuleHitsSub: "సందేశాలు మరియు లింకుల స్కాన్లలో అత్యధికంగా ప్రేరేపించబడే నిబంధనలు.",
        adminSeverityCritical: "తీవ్రమైనది",
        adminSeverityHigh: "అధికం",
        adminSeverityMedium: "మధ్యస్థం",
        ruleNameUrgency: "తప్పుడు ఆవశ్యకత & భయం",
        ruleDescUrgency: "విద్యుత్ సరఫరా నిలిపివేత లేదా ఖాతా బ్లాక్ బెదిరింపులు",
        ruleNameOtp: "OTP లేదా పిన్ అభ్యర్థనలు",
        ruleDescOtp: "రహస్య వన్-టైమ్ పాస్‌వర్డ్‌లు లేదా బ్యాంకింగ్ పిన్ డిమాండ్",
        ruleNameKyc: "నకిలీ KYC & బిల్లు గడువు",
        ruleDescKyc: "KYC గడువు ముగిసిందని లేదా సిమ్ బ్లాక్ అవుతుందని బెదిరింపులు",
        ruleNameBankBrand: "బ్యాంక్ & ప్రభుత్వ గుర్తింపుల దుర్వినియోగం",
        ruleDescBankBrand: "SBI, HDFC, పోలీస్, CBI లేదా RBI పేరుతో మోసాలు",
        ruleNameApk: "హానికర APK / స్క్రీన్ షేరింగ్ యాప్‌లు",
        ruleDescApk: "మోసపూరిత APKలు లేదా AnyDesk యాప్‌లను డౌన్‌లోడ్ చేయించడం",
        ruleNameCustomerCare: "10-అంకెల నకిలీ కస్టమర్ కేర్",
        ruleDescCustomerCare: "వ్యక్తిగత మొబైల్ నంబర్లను అధికారిక హెల్ప్‌లైన్‌గా చూపించడం",
        ruleNameInstantLoan: "అక్రమ లోన్ యాప్‌ల ఎర",
        ruleDescInstantLoan: "డాక్యుమెంట్లు లేకుండా తక్షణ లోన్ మరియు కాంటాక్ట్‌ల డిమాండ్",
        ruleNameShortUrl: "కుదించబడిన / దాచిన లింకులు",
        ruleDescShortUrl: "bit.ly, tinyurl లేదా రీడైరెక్ట్ లింకులు",
        ruleNameRiskyTld: "ప్రమాదకర డొమైన్ పొడిగింపులు",
        ruleDescRiskyTld: "అనుమానాస్పద డొమైన్లు (.xyz, .top, .live, .site)",
        ruleNameAdvanceFee: "లోన్ ఇవ్వకముందే అడ్వాన్స్ ఫీజు",
        ruleDescAdvanceFee: "ప్రాసెసింగ్ లేదా జీఎస్టీ పేరుతో ముందుగానే డబ్బులు అడగడం",
        ruleNameHttpOnly: "రక్షణ లేని ప్లెయిన్ HTTP లింకులు",
        ruleDescHttpOnly: "HTTPS భద్రత లేని ప్రమాదకర లింకులు",
        ruleNamePrize: "లాటరీ & నకిలీ బహుమతుల ఎర",
        ruleDescPrize: "లక్కీ డ్రా గెలుచుకున్నారని లేదా కొరియర్ ఫీజుల పేరిట మోసం",
        ruleNameRegistryMatched: "కమ్యూనిటీ రిజిస్ట్రీలో మ్యాచ్ అయ్యింది",
        ruleDescRegistryMatched: "ఇప్పటికే పౌరులచే రిపోర్ట్ చేయబడిన ముప్పు హ్యాష్‌లతో సరిపోలింది",`;

// Insert into EN, HI, TE dictionaries right before closing brace
template = template.replace(
  'speechUnsupported: "⚠️ Speech synthesis is not supported on this browser.",\n      },',
  `speechUnsupported: "⚠️ Speech synthesis is not supported on this browser.",\n        ${adminTransEn}\n      },`
);

template = template.replace(
  'speechUnsupported: "⚠️ इस ब्राउज़र में स्पीच सिंथेसिस समर्थित नहीं है।",\n      },',
  `speechUnsupported: "⚠️ इस ब्राउज़र में स्पीच सिंथेसिस समर्थित नहीं है।",\n        ${adminTransHi}\n      },`
);

template = template.replace(
  'speechUnsupported: "⚠️ ఈ బ్రౌజర్‌లో స్పీచ్ సింథసిస్ సపోర్ట్ చేయదు.",\n      }\n    };',
  `speechUnsupported: "⚠️ ఈ బ్రౌజర్‌లో స్పీచ్ సింథసిస్ సపోర్ట్ చేయదు.",\n        ${adminTransTe}\n      }\n    };`
);
console.log('Appended Admin translations in EN, HI, TE.');

// Save template.html
fs.writeFileSync('template.html', template, 'utf8');

// Build index.html
const uris = JSON.parse(fs.readFileSync('uris.json', 'utf8'));
const indexHtml = template.replace('{{SHIELD_URI}}', uris.shield).replace('{{FULL_URI}}', uris.full);
fs.writeFileSync('index.html', indexHtml, 'utf8');

console.log('Successfully written template.html and index.html with Admin features!');
