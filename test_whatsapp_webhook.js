/**
 * BlaxGuard WhatsApp Webhook Integration Test Suite
 * Tests:
 * 1. Meta Webhook GET Verification (hub.challenge handshake)
 * 2. Meta Webhook GET Rejection on invalid verify token
 * 3. Meta Cloud API POST Webhook (nested payload with predatory loan APK)
 * 4. Direct / Flat POST Webhook (safe RBI entity verification)
 * 5. Twilio POST Webhook (TwiML response with danger audit)
 */

const assert = require('assert');
const http = require('http');

function httpRequest(options, postData = null) {
  return new Promise((resolve, reject) => {
    const req = http.request(options, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        resolve({
          statusCode: res.statusCode,
          headers: res.headers,
          body: data
        });
      });
    });

    req.on('error', (err) => reject(err));

    if (postData) {
      req.write(postData);
    }
    req.end();
  });
}

async function runWhatsAppTests() {
  console.log("==================================================================");
  console.log("📲 BLAXGUARD WHATSAPP WEBHOOK TEST SUITE");
  console.log("==================================================================");

  const HOST = '127.0.0.1';
  const PORT = 8080;

  // TEST 1: Meta Webhook GET handshake verification
  console.log("\n[TEST 1] Meta Cloud API Webhook Handshake (GET Verification)");
  const challengeCode = "challenge_123456789";
  const getHandshake = await httpRequest({
    hostname: HOST,
    port: PORT,
    path: `/api/whatsapp/webhook?hub.mode=subscribe&hub.verify_token=blaxguard_secure_token_123&hub.challenge=${challengeCode}`,
    method: 'GET'
  });

  assert.strictEqual(getHandshake.statusCode, 200, "Must return HTTP 200 OK");
  assert.strictEqual(getHandshake.body, challengeCode, "Must echo hub.challenge verbatim");
  console.log("  ✅ Passed: Meta challenge handshake returned HTTP 200 with matching challenge code");

  // TEST 2: Rejection of invalid verify token
  console.log("\n[TEST 2] Security: Rejection of Invalid Webhook Verify Token");
  const getReject = await httpRequest({
    hostname: HOST,
    port: PORT,
    path: `/api/whatsapp/webhook?hub.mode=subscribe&hub.verify_token=wrong_token_xyz&hub.challenge=${challengeCode}`,
    method: 'GET'
  });

  assert.strictEqual(getReject.statusCode, 403, "Must return HTTP 403 Forbidden for bad token");
  console.log("  ✅ Passed: Invalid verify token was rejected with HTTP 403");

  // TEST 3: Meta Cloud API Nested Payload (Predatory Loan APK Threat)
  console.log("\n[TEST 3] Meta Cloud API Inbound Webhook (Predatory Loan Threat)");
  const metaPayload = JSON.stringify({
    object: "whatsapp_business_account",
    entry: [
      {
        id: "WABA_ID_001",
        changes: [
          {
            value: {
              messaging_product: "whatsapp",
              metadata: {
                display_phone_number: "+15551234567",
                phone_number_id: "109876543210"
              },
              contacts: [
                {
                  profile: { name: "Citizen User" },
                  wa_id: "919876543210"
                }
              ],
              messages: [
                {
                  from: "919876543210",
                  id: "wamid.HBgLM...",
                  timestamp: "1710000000",
                  type: "text",
                  text: {
                    body: "URGENT: Pre-approved 50,000 cash loan! Download instant APK at http://speedrupee-fastloan.xyz/app.apk"
                  }
                }
              ]
            },
            field: "messages"
          }
        ]
      }
    ]
  });

  const postMeta = await httpRequest({
    hostname: HOST,
    port: PORT,
    path: '/api/whatsapp/webhook',
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Content-Length': Buffer.byteLength(metaPayload)
    }
  }, metaPayload);

  assert.strictEqual(postMeta.statusCode, 200, "Webhook must acknowledge with HTTP 200");
  const metaRes = JSON.parse(postMeta.body);
  assert.strictEqual(metaRes.status, 'received');
  assert.strictEqual(metaRes.verdict, 'danger', "Verdict must be danger");
  assert.strictEqual(metaRes.score, 100, "Predatory loan APK score must be 100");
  assert(metaRes.reply.includes("BLAXGUARD WHATSAPP SHIELD"), "Reply must include header");
  assert(metaRes.reply.includes("HIGH RISK SCAM ALERT"), "Reply status must be high risk");
  assert(metaRes.reply.includes("1930"), "Must include 1930 emergency helpline");
  assert(metaRes.reply.includes("cybercrime.gov.in"), "Must include cybercrime.gov.in portal");
  console.log(`  ✅ Passed: Meta payload audited => Verdict: ${metaRes.verdict.toUpperCase()}, Score: ${metaRes.score}/100, 1930 Guidance included`);

  // TEST 4: Direct Testing Payload (Safe RBI Registered Entity)
  console.log("\n[TEST 4] Direct Payload Webhook (Safe RBI Registered Lender)");
  const directPayload = JSON.stringify({
    from: "919876543210",
    text: "Check your personal loan offer at https://kreditbee.in"
  });

  const postDirect = await httpRequest({
    hostname: HOST,
    port: PORT,
    path: '/api/whatsapp/webhook',
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Content-Length': Buffer.byteLength(directPayload)
    }
  }, directPayload);

  assert.strictEqual(postDirect.statusCode, 200);
  const directRes = JSON.parse(postDirect.body);
  assert.strictEqual(directRes.verdict, 'safe', "KreditBee must evaluate as safe");
  assert.strictEqual(directRes.score, 0, "Score must be 0");
  assert(directRes.reply.includes("KrazyBee Services Pvt Ltd"), "Must mention verified NBFC name");
  console.log(`  ✅ Passed: Direct payload audited => Verdict: ${directRes.verdict.toUpperCase()}, Score: ${directRes.score}/100, RBI Lender verified`);

  // TEST 5: Twilio WhatsApp Webhook (TwiML XML response)
  console.log("\n[TEST 5] Twilio WhatsApp Webhook (TwiML Protocol)");
  const twilioFormData = "From=whatsapp%3A%2B919876543210&Body=Electricity+bill+unpaid+disconnect+tonight+http%3A%2F%2Fdiscom-bill.xyz";
  const postTwilio = await httpRequest({
    hostname: HOST,
    port: PORT,
    path: '/api/whatsapp/twilio',
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
      'Content-Length': Buffer.byteLength(twilioFormData)
    }
  }, twilioFormData);

  assert.strictEqual(postTwilio.statusCode, 200);
  assert(postTwilio.headers['content-type'].includes('text/xml'), "Must return XML content type");
  assert(postTwilio.body.includes("<Response><Message>"), "Must be valid TwiML");
  assert(postTwilio.body.includes("BLAXGUARD WHATSAPP SHIELD"));
  assert(postTwilio.body.includes("1930"));
  console.log("  ✅ Passed: Twilio webhook processed successfully and responded with TwiML XML");

  console.log("\n==================================================================");
  console.log("🎉 ALL 5 WHATSAPP WEBHOOK TESTS PASSED 100%!");
  console.log("==================================================================");
}

runWhatsAppTests().catch(err => {
  console.error("❌ Test failed:", err);
  process.exit(1);
});
