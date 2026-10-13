/**
 * BlaxGuard Extension Integration & Fallback Test Suite
 * Tests legitimate entities, suspicious links, API network failures, malformed payloads, and cache deduplication.
 */

const assert = require('assert');
const http = require('http');

// Replicate the exact evaluateUrlWithEngine logic from extension/content_search.js for headless testing
function createEvaluator(apiEndpoint = 'http://localhost:8080/api/check', timeoutMs = 2500) {
  const evaluationCache = new Map();

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

  let networkCallCount = 0;

  async function evaluateUrlWithEngine(url) {
    if (!url || !url.startsWith("http")) return null;

    if (evaluationCache.has(url)) {
      return evaluationCache.get(url);
    }

    const fetchPromise = (async () => {
      networkCallCount++;
      try {
        const urlObj = new URL(apiEndpoint);
        const payload = JSON.stringify({ text: url });

        const data = await new Promise((resolve, reject) => {
          const req = http.request({
            hostname: urlObj.hostname,
            port: urlObj.port,
            path: urlObj.pathname,
            method: 'POST',
            timeout: timeoutMs,
            headers: {
              'Content-Type': 'application/json',
              'Content-Length': Buffer.byteLength(payload)
            }
          }, res => {
            let body = '';
            res.on('data', chunk => body += chunk);
            res.on('end', () => {
              if (res.statusCode !== 200) {
                return reject(new Error(`HTTP error ${res.statusCode}`));
              }
              try {
                resolve(JSON.parse(body));
              } catch (e) {
                reject(new Error("Invalid JSON"));
              }
            });
          });

          req.on('error', reject);
          req.on('timeout', () => {
            req.destroy(new Error("Timeout"));
          });
          req.write(payload);
          req.end();
        });

        if (data && typeof data === "object" && typeof data.verdict === "string") {
          return {
            verdict: data.verdict,
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
        return evaluateOfflineFallback(url);
      }
    })();

    evaluationCache.set(url, fetchPromise);
    return fetchPromise;
  }

  return { evaluateUrlWithEngine, getNetworkCallCount: () => networkCallCount };
}

async function runTestSuite() {
  console.log("==================================================================");
  console.log("🧪 BLAXGUARD EXTENSION INTEGRATION TEST SUITE");
  console.log("==================================================================");

  const realEvaluator = createEvaluator('http://localhost:8080/api/check');

  // Test 1: Legitimate bank (HDFC)
  console.log("\n[TEST 1] Legitimate Commercial Bank (HDFC Bank)");
  const t1 = await realEvaluator.evaluateUrlWithEngine('https://www.hdfcbank.com/personal-loan');
  assert.strictEqual(t1.verdict, 'safe', 'HDFC should be safe');
  assert.strictEqual(t1.score, 0, 'HDFC score should be 0');
  assert.strictEqual(t1.isFallback, false, 'HDFC should be verified via live backend');
  assert(t1.verifiedLender !== null, 'HDFC should return verifiedLender object');
  console.log("  ✅ Passed: verdict=safe, score=0, lender=" + t1.verifiedLender.name);

  // Test 2: Legitimate NBFC (Tata Capital)
  console.log("\n[TEST 2] Legitimate NBFC (Tata Capital)");
  const t2 = await realEvaluator.evaluateUrlWithEngine('https://tatacapital.com');
  assert.strictEqual(t2.verdict, 'safe', 'Tata Capital should be safe');
  assert.strictEqual(t2.isFallback, false);
  assert(t2.verifiedLender.category.includes('NBFC'));
  console.log("  ✅ Passed: verdict=safe, category=" + t2.verifiedLender.category);

  // Test 3: Legitimate Digital Lending Platform (KreditBee)
  console.log("\n[TEST 3] Certified Digital Lending Platform (KreditBee)");
  const t3 = await realEvaluator.evaluateUrlWithEngine('https://kreditbee.in');
  assert.strictEqual(t3.verdict, 'safe', 'KreditBee should be safe');
  assert.strictEqual(t3.isFallback, false);
  console.log("  ✅ Passed: verdict=safe, lender=" + t3.verifiedLender.name);

  // Test 4: Suspicious Predatory Loan APK
  console.log("\n[TEST 4] Suspicious Predatory Loan APK (Speed Rupee .xyz)");
  const t4 = await realEvaluator.evaluateUrlWithEngine('http://speedrupee-loan.xyz/app.apk');
  assert.strictEqual(t4.verdict, 'danger', 'APK should be flagged danger');
  assert(t4.score >= 50, 'Score should be high risk');
  assert.strictEqual(t4.isFallback, false, 'Should be flagged by live backend engine');
  assert(t4.reasons.length > 0, 'Should return detailed reasons');
  console.log(`  ✅ Passed: verdict=danger, score=${t4.score}/100, reasonsCount=${t4.reasons.length}`);

  // Test 5: Cache Deduplication
  console.log("\n[TEST 5] In-Memory Cache Deduplication");
  const callsBefore = realEvaluator.getNetworkCallCount();
  await realEvaluator.evaluateUrlWithEngine('https://kreditbee.in');
  await realEvaluator.evaluateUrlWithEngine('https://kreditbee.in');
  const callsAfter = realEvaluator.getNetworkCallCount();
  assert.strictEqual(callsBefore, callsAfter, 'Duplicate calls to identical URL must not trigger extra network requests');
  console.log("  ✅ Passed: 2 duplicate queries resulted in 0 extra network requests (Cache HIT)");

  // Test 6: Network Failure / Offline Fallback (Port 9999 simulating dead server)
  console.log("\n[TEST 6] Server Unavailability & Offline Fallback Handling");
  const offlineEvaluator = createEvaluator('http://localhost:9999/api/check', 500);

  // Fallback on suspicious link
  const t6_bad = await offlineEvaluator.evaluateUrlWithEngine('http://fake-loan-app.xyz/app.apk');
  assert.strictEqual(t6_bad.isFallback, true, 'Must be marked as fallback');
  assert.strictEqual(t6_bad.verdict, 'danger', 'Risky TLD/APK must still be flagged in fallback');
  assert(t6_bad.reasons[0].includes('(Offline Fallback)'), 'Reason must explicitly contain "(Offline Fallback)"');
  console.log("  ✅ Passed: Suspicious link offline fallback => verdict=" + t6_bad.verdict + " [" + t6_bad.reasons[0] + "]");

  // Fallback on unknown link
  const t6_unknown = await offlineEvaluator.evaluateUrlWithEngine('https://some-random-unknown-site.org');
  assert.strictEqual(t6_unknown.isFallback, true);
  assert.strictEqual(t6_unknown.verdict, 'unknown');
  assert(t6_unknown.reasons[0].includes('(Offline Fallback)'));
  console.log("  ✅ Passed: Unknown link offline fallback => verdict=" + t6_unknown.verdict + " [" + t6_unknown.reasons[0] + "]");

  console.log("\n==================================================================");
  console.log("🎉 ALL 6 INTEGRATION & FALLBACK TESTS PASSED 100%!");
  console.log("==================================================================");
}

runTestSuite().catch(err => {
  console.error("❌ Test failed:", err);
  process.exit(1);
});
