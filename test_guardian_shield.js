/**
 * BlaxGuard Family Guardian Shield Test Suite
 * Tests:
 * 1. Creation of Guardian Approval Request for Senior/Child
 * 2. Querying status while Pending
 * 3. Submitting Block Decision via Web Portal API
 * 4. Verifying Real-time Block Enforcement
 * 5. Submitting Allow Decision via WhatsApp Webhook
 * 6. Serving Guardian Mobile Review Portal HTML
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
    req.on('error', reject);
    if (postData) req.write(postData);
    req.end();
  });
}

async function runGuardianTests() {
  console.log("==================================================================");
  console.log("👨‍👩‍👧 BLAXGUARD FAMILY GUARDIAN SHIELD VERIFICATION SUITE");
  console.log("==================================================================");

  const HOST = '127.0.0.1';
  const PORT = 8080;

  // TEST 1: Create a Guardian Permission Request for a predatory loan link
  console.log("\n[TEST 1] Initiate Guardian Approval Request");
  const requestPayload = JSON.stringify({
    url: "http://speedrupee-loan.xyz/app.apk",
    guardianPhone: "+919876543210",
    seniorName: "Grandparent (Senior Citizen)",
    source: "WhatsApp Web Chat"
  });

  const createRes = await httpRequest({
    hostname: HOST,
    port: PORT,
    path: '/api/guardian/request',
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Content-Length': Buffer.byteLength(requestPayload)
    }
  }, requestPayload);

  assert.strictEqual(createRes.statusCode, 200);
  const createData = JSON.parse(createRes.body);
  assert.strictEqual(createData.success, true);
  assert(createData.requestId.startsWith('guard_'), "Must generate guard_ prefix ID");
  assert.strictEqual(createData.status, 'pending');
  assert.strictEqual(createData.verdict, 'danger');
  assert(createData.score >= 70, "Predatory loan must be high risk");
  assert(createData.approvalUrl.includes(createData.requestId));
  console.log(`  ✅ Passed: Request created (${createData.requestId}) with status PENDING, Risk: ${createData.score}/100`);

  const requestId = createData.requestId;

  // TEST 2: Check status polling while pending
  console.log("\n[TEST 2] Senior/Child Browser Status Polling (Pending State)");
  const pollRes1 = await httpRequest({
    hostname: HOST,
    port: PORT,
    path: `/api/guardian/status?id=${requestId}`,
    method: 'GET'
  });

  assert.strictEqual(pollRes1.statusCode, 200);
  const pollData1 = JSON.parse(pollRes1.body);
  assert.strictEqual(pollData1.status, 'pending');
  console.log("  ✅ Passed: Status correctly polled as PENDING — link remains locked");

  // TEST 3: Guardian Decision: BLOCK the link
  console.log("\n[TEST 3] Guardian Decision Submission: BLOCK & PROTECT");
  const blockPayload = JSON.stringify({
    id: requestId,
    decision: 'block'
  });

  const decisionRes = await httpRequest({
    hostname: HOST,
    port: PORT,
    path: '/api/guardian/decision',
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Content-Length': Buffer.byteLength(blockPayload)
    }
  }, blockPayload);

  assert.strictEqual(decisionRes.statusCode, 200);
  const decisionData = JSON.parse(decisionRes.body);
  assert.strictEqual(decisionData.status, 'blocked');
  console.log("  ✅ Passed: Guardian decision recorded as BLOCKED");

  // TEST 4: Senior/Child polling now reflects BLOCKED (Link cannot be opened)
  console.log("\n[TEST 4] Real-Time Enforcement: Verify Link is Permanently Blocked");
  const pollRes2 = await httpRequest({
    hostname: HOST,
    port: PORT,
    path: `/api/guardian/status?id=${requestId}`,
    method: 'GET'
  });

  assert.strictEqual(pollRes2.statusCode, 200);
  const pollData2 = JSON.parse(pollRes2.body);
  assert.strictEqual(pollData2.status, 'blocked');
  assert(pollData2.decisionAt !== null);
  console.log("  ✅ Passed: Senior/child device immediately locks out link permanently");

  // TEST 5: Interactive WhatsApp Decision Command ('ALLOW <id>')
  console.log("\n[TEST 5] Two-Way WhatsApp Decision: Guardian replies ALLOW via chat");
  const whatsappAllowPayload = JSON.stringify({
    from: "919876543210",
    text: `ALLOW ${requestId}`
  });

  const waRes = await httpRequest({
    hostname: HOST,
    port: PORT,
    path: '/api/whatsapp/webhook',
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Content-Length': Buffer.byteLength(whatsappAllowPayload)
    }
  }, whatsappAllowPayload);

  assert.strictEqual(waRes.statusCode, 200);
  const waData = JSON.parse(waRes.body);
  assert.strictEqual(waData.guardianDecision, 'allowed');

  // Verify status is now updated to 'allowed'
  const pollRes3 = await httpRequest({
    hostname: HOST,
    port: PORT,
    path: `/api/guardian/status?id=${requestId}`,
    method: 'GET'
  });
  const pollData3 = JSON.parse(pollRes3.body);
  assert.strictEqual(pollData3.status, 'allowed');
  console.log("  ✅ Passed: WhatsApp ALLOW command updated status to ALLOWED in real time");

  // TEST 6: Verify Guardian Mobile Portal HTML Page
  console.log("\n[TEST 6] Guardian Review Portal Web Interface (GET /guardian)");
  const portalRes = await httpRequest({
    hostname: HOST,
    port: PORT,
    path: `/guardian?id=${requestId}`,
    method: 'GET'
  });

  assert.strictEqual(portalRes.statusCode, 200);
  assert(portalRes.body.includes("BlaxGuard Guardian Shield"));
  assert(portalRes.body.includes("Senior & Child Permission Review"));
  console.log("  ✅ Passed: Guardian review portal loads with responsive UI and action controls");

  console.log("\n==================================================================");
  console.log("🎉 ALL 6 GUARDIAN SHIELD TESTS PASSED (100% GREEN)!");
  console.log("==================================================================");
}

runGuardianTests().catch(err => {
  console.error("❌ Test failed:", err);
  process.exit(1);
});
