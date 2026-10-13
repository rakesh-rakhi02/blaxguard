/**
 * BlaxGuard WhatsApp Scam Helpline Service
 * 
 * Works with Meta WhatsApp Business Cloud API & Twilio WhatsApp Sandbox.
 * 
 * For Meta Cloud API:
 * 1. Register a Meta Developer App at https://developers.facebook.com
 * 2. Add WhatsApp product and configure Webhook to:
 *    https://<YOUR_DOMAIN>/api/whatsapp/webhook
 * 3. Set Verify Token: "blaxguard_secure_token_123"
 * 
 * For Twilio WhatsApp:
 * Configure Incoming Message Webhook in Twilio Console to:
 * https://<YOUR_DOMAIN>/api/whatsapp/twilio
 */

const https = require('https');
const engine = require('./engine');

async function processWhatsAppMessage(senderNumber, incomingText) {
  const result = await engine.evaluateTextSafety(incomingText);

  let emoji = result.verdict === 'danger' ? '🚨' : (result.verdict === 'caution' ? '⚠️' : '✅');
  let title = result.verdict === 'danger' ? 'HIGH RISK SCAM ALERT' : (result.verdict === 'caution' ? 'CAUTION ADVISED' : 'VERIFIED SAFE');

  let reply = `${emoji} *BLAXGUARD WHATSAPP SHIELD* 🇮🇳\n\n`;
  reply += `*Status:* ${title}\n`;
  reply += `*Risk Score:* ${result.score} / 100\n\n`;

  if (result.verifiedLender) {
    reply += `🏛️ *Official RBI Regulated Entity:*\n`;
    reply += `*Name:* ${result.verifiedLender.name}\n`;
    reply += `*Category:* ${result.verifiedLender.category}\n`;
    reply += `*License:* ${result.verifiedLender.license}\n\n`;
  } else if (result.verdict !== 'safe') {
    reply += `🏛️ *RBI Status:* Not verified in the official RBI Regulated Lenders Directory!\n\n`;
  }

  reply += `*Key Findings:*\n`;
  result.reasons.forEach(r => {
    reply += `• ${r}\n`;
  });

  if (result.verdict === 'danger') {
    reply += `\n🛑 *What to do now:*\n`;
    reply += `1. Do NOT click links or install any APK file.\n`;
    reply += `2. Never share your OTP or 4/6-digit UPI PIN.\n`;
    reply += `3. Dial national helpline *1930* immediately if any money was deducted.\n`;
    reply += `4. File report on *cybercrime.gov.in*.\n`;
  } else if (result.verdict === 'safe') {
    reply += `\n✅ *Official Institution:* No malicious or predatory red flags found.\n`;
  }

  return reply;
}

// Dispatches outbound message via Meta WhatsApp Cloud API if credentials exist
async function sendMetaWhatsAppMessage(to, replyText, phoneNumberId = null) {
  const token = (process.env.WHATSAPP_TOKEN || process.env.WHATSAPP_ACCESS_TOKEN || '').trim();
  const phoneId = (phoneNumberId || process.env.WHATSAPP_PHONE_NUMBER_ID || '').trim();

  if (!token || !phoneId) {
    return {
      dispatched: false,
      reason: 'WHATSAPP_ACCESS_TOKEN or WHATSAPP_PHONE_NUMBER_ID not configured (Live Meta API delivery inactive)'
    };
  }

  const payload = JSON.stringify({
    messaging_product: 'whatsapp',
    recipient_type: 'individual',
    to: to,
    type: 'text',
    text: {
      preview_url: false,
      body: replyText
    }
  });

  return new Promise((resolve) => {
    const req = https.request({
      hostname: 'graph.facebook.com',
      port: 443,
      path: `/v19.0/${phoneId}/messages`,
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(payload)
      }
    }, res => {
      let body = '';
      res.on('data', chunk => body += chunk);
      res.on('end', () => {
        try {
          const parsed = JSON.parse(body);
          resolve({ dispatched: res.statusCode === 200, response: parsed });
        } catch (e) {
          resolve({ dispatched: false, error: body });
        }
      });
    });

    req.on('error', err => {
      resolve({ dispatched: false, error: err.message });
    });

    req.write(payload);
    req.end();
  });
}

// If executed directly, run sample test cases
if (require.main === module) {
  console.log("==================================================================");
  console.log("📲 BLAXGUARD WHATSAPP SCAM DETECTION TEST");
  console.log("==================================================================");

  const sampleMessages = [
    { sender: "+919876543210", text: "Urgent: Pre-approved instant loan of Rs 50,000 from Bajaj Finserv: https://www.bajajfinserv.in/personal-loan" },
    { sender: "+919876543210", text: "Electricity power disconnect tonight at 9:30 PM due to unpaid bill. Update now: http://discom-bill.xyz or call 9876543210" },
    { sender: "+919876543210", text: "Instant loan approved! Download app immediately: http://speedrupee-loan.xyz/app.apk" }
  ];

  (async () => {
    for (const sample of sampleMessages) {
      console.log(`\n--- Incoming from ${sample.sender} ---`);
      const reply = await processWhatsAppMessage(sample.sender, sample.text);
      console.log("Automated WhatsApp Reply:\n" + reply);
    }
  })();
}

module.exports = {
  processWhatsAppMessage,
  sendMetaWhatsAppMessage
};
