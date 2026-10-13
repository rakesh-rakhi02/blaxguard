const http = require('http');
const fs = require('fs');
const path = require('path');
const engine = require('./engine');
const whatsappBot = require('./whatsapp_bot');

const PORT = 8080;
const ROOT = __dirname;

// In-memory store for Guardian Permission Requests
const guardianRequests = new Map();

const MIME_TYPES = {
  '.html': 'text/html; charset=utf-8',
  '.js': 'application/javascript; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.svg': 'image/svg+xml',
  '.ico': 'image/x-icon'
};

function readBody(req) {
  return new Promise((resolve) => {
    let body = '';
    req.on('data', chunk => body += chunk);
    req.on('end', () => {
      if (!body || !body.trim()) return resolve({});
      try {
        resolve(JSON.parse(body));
      } catch (e) {
        // Fallback for Windows PowerShell quote-stripping: {from:123,text:hello}
        try {
          const fixed = body
            .replace(/([{,]\s*)([a-zA-Z0-9_]+)\s*:/g, '$1"$2":')
            .replace(/:\s*([a-zA-Z0-9_\-\.\:\/]+)\s*([,}])/g, (m, val, end) => {
              if (val === 'true' || val === 'false' || val === 'null' || !isNaN(val)) {
                return `:${val}${end}`;
              }
              return `:"${val}"${end}`;
            });
          return resolve(JSON.parse(fixed));
        } catch (_) {}

        // Fallback: URLSearchParams for x-www-form-urlencoded
        const params = new URLSearchParams(body);
        const obj = {};
        for (const [k, v] of params) obj[k] = v;
        resolve(obj);
      }
    });
  });
}

const server = http.createServer(async (req, res) => {
  // CORS Headers for Extension, WhatsApp, and Telegram Webhooks
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');

  if (req.method === 'OPTIONS') {
    res.writeHead(204);
    res.end();
    return;
  }

  const urlObj = new URL(req.url, `http://${req.headers.host || 'localhost'}`);
  const pathname = urlObj.pathname;

  // ==========================================
  // REST API ENDPOINTS
  // ==========================================

  // 1. POST /api/check (Evaluate link, SMS, or phone number)
  if (req.method === 'POST' && pathname === '/api/check') {
    const data = await readBody(req);
    const text = data.text || data.message || data.url || '';
    if (!text) {
      res.writeHead(400, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ error: 'Missing text or url parameter' }));
      return;
    }
    const result = await engine.evaluateTextSafety(text);
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({
      success: true,
      text: text,
      ...result,
      timestamp: new Date().toISOString()
    }));
    return;
  }

  // 2. POST /api/loan (Evaluate loan app / offer)
  if (req.method === 'POST' && pathname === '/api/loan') {
    const data = await readBody(req);
    const lender = data.lender || data.url || data.name || '';
    const flags = data.flags || {};
    const result = engine.evaluateLoanApp(lender, flags);
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({
      success: true,
      lender: lender,
      ...result,
      timestamp: new Date().toISOString()
    }));
    return;
  }

  // 3. GET /api/rbi/lookup (Lookup lender name or domain in RBI registry)
  if (req.method === 'GET' && pathname === '/api/rbi/lookup') {
    const query = urlObj.searchParams.get('q') || '';
    const match = engine.lookupRbiLender(query);
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({
      success: true,
      query: query,
      isVerified: !!match,
      lender: match || null
    }));
    return;
  }

  // 4. GET & POST /api/whatsapp/webhook (WhatsApp Cloud API Webhook)
  if (pathname === '/api/whatsapp/webhook') {
    if (req.method === 'GET') {
      // Hub challenge verification for Meta Webhook setup
      const mode = urlObj.searchParams.get('hub.mode');
      const token = urlObj.searchParams.get('hub.verify_token');
      const challenge = urlObj.searchParams.get('hub.challenge');
      const VERIFY_TOKEN = process.env.WHATSAPP_VERIFY_TOKEN || 'blaxguard_secure_token_123';

      if (mode === 'subscribe' && token === VERIFY_TOKEN) {
        res.writeHead(200, { 'Content-Type': 'text/plain' });
        res.end(challenge);
        return;
      }
      res.writeHead(403, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ error: 'Forbidden: Invalid verify token' }));
      return;
    }

    if (req.method === 'POST') {
      const data = await readBody(req);
      const auditResult = await handleWhatsAppIncoming(data);
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({
        status: 'received',
        ...auditResult
      }));
      return;
    }
  }

  // 5. POST /api/whatsapp/twilio (Twilio WhatsApp Webhook)
  if (pathname === '/api/whatsapp/twilio' && req.method === 'POST') {
    const data = await readBody(req);
    const from = data.From || data.from || 'unknown';
    const text = data.Body || data.body || data.text || '';
    if (!text) {
      res.writeHead(200, { 'Content-Type': 'text/xml' });
      res.end('<Response></Response>');
      return;
    }
    const replyText = await whatsappBot.processWhatsAppMessage(from, text);
    const escapedXml = replyText.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
    res.writeHead(200, { 'Content-Type': 'text/xml' });
    res.end(`<Response><Message>${escapedXml}</Message></Response>`);
    return;
  }

  // 6. GET /guardian & /guardian.html (Interactive Guardian Review Page)
  if (pathname === '/guardian' || pathname === '/guardian.html') {
    const guardianFile = path.join(ROOT, 'guardian.html');
    if (fs.existsSync(guardianFile)) {
      res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
      fs.createReadStream(guardianFile).pipe(res);
      return;
    }
  }

  // 7. POST /api/guardian/request (Initiate Guardian Approval Request)
  if (req.method === 'POST' && pathname === '/api/guardian/request') {
    const data = await readBody(req);
    const targetUrl = data.url || data.text || '';
    const guardianPhone = data.guardianPhone || data.phone || '+91 98765 43210';
    const seniorName = data.seniorName || 'Family Member (Senior / Child)';
    const source = data.source || 'Browser Extension';

    if (!targetUrl) {
      res.writeHead(400, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ error: 'Missing target url parameter' }));
      return;
    }

    const evalResult = await engine.evaluateTextSafety(targetUrl);
    const reqId = 'guard_' + Date.now().toString(36) + '_' + Math.random().toString(36).substr(2, 4);

    const requestRecord = {
      id: reqId,
      url: targetUrl,
      guardianPhone: guardianPhone,
      seniorName: seniorName,
      source: source,
      status: 'pending', // 'pending' | 'allowed' | 'blocked'
      score: evalResult.score,
      verdict: evalResult.verdict,
      reasons: evalResult.reasons,
      verifiedLender: evalResult.verifiedLender,
      createdAt: new Date().toISOString(),
      decisionAt: null
    };

    guardianRequests.set(reqId, requestRecord);

    const host = req.headers.host || `localhost:${PORT}`;
    const approvalUrl = `http://${host}/guardian?id=${reqId}`;
    const alertMessage = `🚨 *BLAXGUARD GUARDIAN ALERT* 🇮🇳\n\n` +
      `Your family member (*${seniorName}*) attempted to open a high-risk link!\n\n` +
      `🔗 *Target Link:* ${targetUrl}\n` +
      `⚠️ *Threat Score:* ${evalResult.score} / 100 (${evalResult.verdict.toUpperCase()})\n` +
      `*Findings:* ${(evalResult.reasons || []).slice(0, 2).join(' ')}\n\n` +
      `Do you allow them to open this link?\n` +
      `👉 *Tap to Review & Decide:* ${approvalUrl}\n` +
      `Or reply *BLOCK* or *ALLOW* to this chat.`;

    console.log(`[Guardian Shield] New Approval Request created: ${reqId} for ${targetUrl}`);
    console.log(`[Guardian Shield] Alert sent to ${guardianPhone}:\n${alertMessage}`);

    // If Meta Cloud API credentials exist, send live WhatsApp alert
    whatsappBot.sendMetaWhatsAppMessage(guardianPhone.replace(/\D/g, ''), alertMessage)
      .catch(err => console.error('[Guardian WhatsApp Notification Error]', err));

    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({
      success: true,
      requestId: reqId,
      approvalUrl: approvalUrl,
      status: 'pending',
      score: evalResult.score,
      verdict: evalResult.verdict,
      reasons: evalResult.reasons,
      guardianPhone: guardianPhone,
      message: 'Guardian approval request dispatched'
    }));
    return;
  }

  // 8. GET /api/guardian/status (Check Decision Status)
  if (req.method === 'GET' && pathname === '/api/guardian/status') {
    const reqId = urlObj.searchParams.get('id');
    if (!reqId || !guardianRequests.has(reqId)) {
      res.writeHead(404, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ error: 'Guardian request not found or expired' }));
      return;
    }

    const reqObj = guardianRequests.get(reqId);
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({
      success: true,
      ...reqObj
    }));
    return;
  }

  // 9. POST /api/guardian/decision (Submit Allow or Block Decision)
  if (req.method === 'POST' && pathname === '/api/guardian/decision') {
    const data = await readBody(req);
    const reqId = data.id || data.requestId;
    const decision = (data.decision || '').toLowerCase(); // 'allow' or 'block'

    if (!reqId || !guardianRequests.has(reqId)) {
      res.writeHead(404, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ error: 'Guardian request not found' }));
      return;
    }

    if (decision !== 'allow' && decision !== 'block') {
      res.writeHead(400, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ error: 'Invalid decision: must be "allow" or "block"' }));
      return;
    }

    const reqObj = guardianRequests.get(reqId);
    reqObj.status = decision === 'allow' ? 'allowed' : 'blocked';
    reqObj.decisionAt = new Date().toISOString();
    console.log(`[Guardian Shield] Decision updated: ${reqId} => ${reqObj.status}`);

    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({
      success: true,
      id: reqId,
      status: reqObj.status,
      decisionAt: reqObj.decisionAt
    }));
    return;
  }

  // 10. GET /api/guardian/list (List all requests for web dashboard)
  if (req.method === 'GET' && pathname === '/api/guardian/list') {
    const list = Array.from(guardianRequests.values()).reverse().slice(0, 20);
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({
      success: true,
      count: list.length,
      requests: list
    }));
    return;
  }

  // ==========================================
  // STATIC FILE SERVING
  // ==========================================
  let reqPath = decodeURI(pathname);
  if (reqPath === '/' || reqPath === '') {
    reqPath = '/index.html';
  }

  const filePath = path.join(ROOT, reqPath);

  // Security: prevent path traversal outside root
  if (!filePath.startsWith(ROOT)) {
    res.writeHead(403, { 'Content-Type': 'text/plain' });
    res.end('403 Forbidden');
    return;
  }

  fs.stat(filePath, (err, stats) => {
    if (err || !stats.isFile()) {
      res.writeHead(404, { 'Content-Type': 'text/plain' });
      res.end('404 Not Found');
      return;
    }

    const ext = path.extname(filePath).toLowerCase();
    const contentType = MIME_TYPES[ext] || 'application/octet-stream';

    res.writeHead(200, {
      'Content-Type': contentType,
      'Cache-Control': 'no-cache'
    });

    const stream = fs.createReadStream(filePath);
    stream.pipe(res);
  });
});

async function handleWhatsAppIncoming(body) {
  try {
    let from = '';
    let text = '';
    let phoneNumberId = null;

    // Check Meta WhatsApp Cloud API nested structure
    const entry = body.entry?.[0];
    const changes = entry?.changes?.[0];
    const value = changes?.value;
    const message = value?.messages?.[0];

    if (message && message.type === 'text') {
      from = message.from;
      text = message.text?.body;
      phoneNumberId = value?.metadata?.phone_number_id;
    } else {
      // Direct testing payload format (curl / postman / simulated)
      text = body.text || body.Body || body.message || '';
      from = body.from || body.From || body.sender || 'unknown';
      phoneNumberId = body.phone_number_id || null;
    }

    if (!text) {
      return { warning: 'No valid text message found in webhook payload' };
    }

    console.log(`[WhatsApp Webhook] Incoming message from ${from}: "${text}"`);

    // Check if message is a Guardian decision command: ALLOW or BLOCK
    const decisionMatch = text.trim().match(/^(allow|block|approve|deny)(?:\s+([a-zA-Z0-9_\-]+))?/i);
    if (decisionMatch) {
      const decisionType = (decisionMatch[1].toLowerCase() === 'allow' || decisionMatch[1].toLowerCase() === 'approve') ? 'allowed' : 'blocked';
      let reqId = decisionMatch[2];
      let targetReq = null;

      if (reqId && guardianRequests.has(reqId)) {
        targetReq = guardianRequests.get(reqId);
      } else {
        // Find latest pending request
        for (const [id, item] of guardianRequests.entries()) {
          if (item.status === 'pending') {
            targetReq = item;
            reqId = id;
            break;
          }
        }
      }

      if (targetReq) {
        targetReq.status = decisionType;
        targetReq.decisionAt = new Date().toISOString();
        console.log(`[Guardian Shield] WhatsApp Decision recorded: ${reqId} => ${decisionType}`);

        const replyMsg = decisionType === 'blocked'
          ? `🛑 *BLAXGUARD GUARDIAN SHIELD* 🇮🇳\n\n✅ *Link BLOCKED Successfully!*\nYour family member's screen has been LOCKED. The dangerous link will NOT open.`
          : `✅ *BLAXGUARD GUARDIAN SHIELD* 🇮🇳\n\n⚠️ *Link ALLOWED*\nYour family member has been granted one-time access to proceed.`;

        await whatsappBot.sendMetaWhatsAppMessage(from, replyMsg, phoneNumberId);
        return {
          sender: from,
          text: text,
          guardianDecision: decisionType,
          requestId: reqId,
          reply: replyMsg
        };
      }
    }

    // Route directly to engine.evaluateTextSafety without altering existing scoring criteria
    const evalResult = await engine.evaluateTextSafety(text);
    console.log(`[WhatsApp Webhook] Verdict: ${evalResult.verdict} (Score: ${evalResult.score}/100)`);

    // Generate structured WhatsApp audit response
    const replyText = await whatsappBot.processWhatsAppMessage(from, text);

    // If Meta Cloud API credentials are configured, dispatch outbound message
    const dispatchResult = await whatsappBot.sendMetaWhatsAppMessage(from, replyText, phoneNumberId);

    return {
      sender: from,
      text: text,
      verdict: evalResult.verdict,
      score: evalResult.score,
      reasons: evalResult.reasons,
      verifiedLender: evalResult.verifiedLender,
      reply: replyText,
      dispatch: dispatchResult
    };
  } catch (err) {
    console.error('Error handling WhatsApp message:', err);
    return { error: err.message };
  }
}

server.on('error', (err) => {
  if (err.code === 'EADDRINUSE') {
    const ALT_PORT = PORT + 1;
    console.log(`Port ${PORT} in use, trying ${ALT_PORT}...`);
    server.listen(ALT_PORT, () => {
      console.log(`BlaxGuard server running at http://localhost:${ALT_PORT}`);
    });
  } else {
    console.error('Server error:', err);
  }
});

server.listen(PORT, () => {
  console.log(`BlaxGuard server & Scam Detection API running at http://localhost:${PORT}`);
});
