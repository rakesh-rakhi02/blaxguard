/**
 * BlaxGuard Official Telegram Scam Detection Bot (Resilient Service Edition)
 * Long-polling daemon bot that detects scams, predatory loans, and phishing links in forwarded messages.
 * 
 * Secure Token Configuration (Checked in order):
 * 1. Environment variable: TELEGRAM_BOT_TOKEN
 * 2. CLI argument: node telegram_bot.js <token>
 * 3. Local .env file: TELEGRAM_BOT_TOKEN=<token>
 */

const https = require('https');
const fs = require('fs');
const path = require('path');
const engine = require('./engine');

// 1. Secure Environment / Token Loader (Zero dependencies)
function loadLocalEnv(envFilePath = path.join(__dirname, '.env')) {
  if (fs.existsSync(envFilePath)) {
    try {
      const content = fs.readFileSync(envFilePath, 'utf8');
      const lines = content.split(/\r?\n/);
      for (const line of lines) {
        const trimmed = line.trim();
        if (!trimmed || trimmed.startsWith('#')) continue;
        const match = trimmed.match(/^([A-Za-z0-9_]+)\s*=\s*(.*)$/);
        if (match) {
          const key = match[1];
          let val = match[2].trim();
          if ((val.startsWith('"') && val.endsWith('"')) || (val.startsWith("'") && val.endsWith("'"))) {
            val = val.slice(1, -1);
          }
          if (!process.env[key]) {
            process.env[key] = val;
          }
        }
      }
    } catch (e) {
      // Ignore reading error if file is inaccessible
    }
  }
}

function resolveToken(argvToken) {
  loadLocalEnv();
  return (process.env.TELEGRAM_BOT_TOKEN || argvToken || process.argv[2] || '').trim();
}

function maskToken(str, token = TOKEN) {
  if (!str || !token) return str || '';
  return String(str).split(token).join('***REDACTED***');
}

let TOKEN = resolveToken();
let TELEGRAM_API = `https://api.telegram.org/bot${TOKEN}`;
let isShuttingDown = false;
let offset = 0;
let consecutiveErrors = 0;

function setToken(newToken) {
  TOKEN = (newToken || '').trim();
  TELEGRAM_API = `https://api.telegram.org/bot${TOKEN}`;
}

// 2. Resilient Telegram API Client with Timeout & Error Redaction
function callTelegramApi(method, data = {}, timeoutMs = 45000, customBaseUrl = null) {
  return new Promise((resolve, reject) => {
    const payload = JSON.stringify(data);
    const baseUrl = customBaseUrl || TELEGRAM_API;
    const url = new URL(`${baseUrl}/${method}`);

    const transport = url.protocol === 'http:' ? require('http') : https;

    const req = transport.request(url, {
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
        try {
          resolve(JSON.parse(body));
        } catch (e) {
          reject(new Error(`Invalid JSON response from Telegram API (${res.statusCode})`));
        }
      });
    });

    req.on('timeout', () => {
      req.destroy(new Error("Telegram API request timed out"));
    });

    req.on('error', err => {
      const safeMsg = maskToken(err.message, TOKEN);
      reject(new Error(safeMsg));
    });

    req.write(payload);
    req.end();
  });
}

// 3. Message Processing & Response Dispatch
async function sendTelegramMessage(chatId, text, parseMode = 'Markdown', customBaseUrl = null) {
  try {
    const res = await callTelegramApi('sendMessage', {
      chat_id: chatId,
      text: text,
      parse_mode: parseMode,
      disable_web_page_preview: true
    }, 15000, customBaseUrl);

    if (res && !res.ok && res.description && res.description.toLowerCase().includes("can't parse entities")) {
      // Fallback: send as plain text without parse_mode if markdown entities fail
      return await callTelegramApi('sendMessage', {
        chat_id: chatId,
        text: text.replace(/[*_`\[\]]/g, ''),
        disable_web_page_preview: true
      }, 15000, customBaseUrl);
    }
    return res;
  } catch (err) {
    console.error('[Telegram Bot] Send message error:', maskToken(err.message, TOKEN));
    return null;
  }
}

async function handleMessage(msg, customBaseUrl = null) {
  const chatId = msg.chat?.id;
  const text = (msg.text || msg.caption || '').trim();

  if (!chatId || !text) return null;

  if (text === '/start' || text.startsWith('/start ') || text.startsWith('/start@')) {
    const welcome = `🛡️ *Welcome to BlaxGuard Scam Shield* 🇮🇳\n\nForward any SMS, WhatsApp message, unknown link, or loan offer to this bot.\n\nBlaxGuard will instantly check it against the *Real-World RBI Registry*, known scam patterns, and predatory extortion markers.\n\n*Try forwarding any message now!*`;
    return await sendTelegramMessage(chatId, welcome, 'Markdown', customBaseUrl);
  }

  if (text === '/help' || text.startsWith('/help ') || text.startsWith('/help@')) {
    const helpText = `🛡️ *BlaxGuard Help & Safety Guide* 🇮🇳\n\n` +
      `• *How to use:* Forward any suspicious message, link, or loan app to this chat.\n` +
      `• *Checks performed:* RBI NBFC Registry, high-risk domains, fake APKs, extortion tactics.\n` +
      `• *Emergency Helpline:* Dial *1930* (National Cyber Crime Reporting Helpline).\n` +
      `• *Official Portal:* [cybercrime.gov.in](https://cybercrime.gov.in)`;
    return await sendTelegramMessage(chatId, helpText, 'Markdown', customBaseUrl);
  }

  if (text === '/status' || text.startsWith('/status ') || text.startsWith('/status@')) {
    const statusText = `🛡️ *BlaxGuard Service Status* 🇮🇳\n\n` +
      `• Bot Engine: *Online & Active*\n` +
      `• Central Safety Engine: *Operational*\n` +
      `• RBI Registry Verification: *Enabled*`;
    return await sendTelegramMessage(chatId, statusText, 'Markdown', customBaseUrl);
  }

  // Evaluate text safety using central engine
  const result = await engine.evaluateTextSafety(text);

  let verdictEmoji = '✅';
  let verdictText = 'VERIFIED SAFE';
  if (result.verdict === 'danger') {
    verdictEmoji = '🚨';
    verdictText = 'HIGH RISK SCAM / FRAUD';
  } else if (result.verdict === 'caution') {
    verdictEmoji = '⚠️';
    verdictText = 'CAUTION / UNVERIFIED';
  }

  let reasonsList = result.reasons.map(r => `• ${r}`).join('\n');

  let rbiText = '';
  if (result.verifiedLender) {
    rbiText = `\n🏛️ *RBI Status:* Verified Registered Entity\n*Name:* ${result.verifiedLender.name}\n*Category:* ${result.verifiedLender.category}\n*License:* ${result.verifiedLender.license}\n`;
  } else if (result.verdict !== 'safe') {
    rbiText = `\n🏛️ *RBI Status:* Not verified in the official RBI Regulated Lenders Directory!\n`;
  }

  let reply = `${verdictEmoji} *BLAXGUARD SAFETY AUDIT* 🇮🇳\n`;
  reply += `━━━━━━━━━━━━━━━━━━━━━\n`;
  reply += `*Verdict:* ${verdictText}\n`;
  reply += `*Risk Score:* ${result.score} / 100\n`;
  reply += `${rbiText}\n`;
  reply += `*Analysis Findings:*\n${reasonsList}\n\n`;

  if (result.verdict === 'danger') {
    reply += `🚨 *Immediate Action Steps:*\n`;
    reply += `1. Do NOT click links or install any .apk file.\n`;
    reply += `2. Never share OTP or 4/6-digit UPI PIN.\n`;
    reply += `3. Dial national cyber helpline *1930* immediately if money was deducted.\n`;
    reply += `4. Report at [cybercrime.gov.in](https://cybercrime.gov.in)\n`;
  } else if (result.verdict === 'safe') {
    reply += `✅ *Safe:* No predatory extortion or phishing triggers detected.\n`;
  }

  return await sendTelegramMessage(chatId, reply, 'Markdown', customBaseUrl);
}

// 4. Polling Lifecycle with Webhook Conflict Resolution & Exponential Backoff
async function pollUpdates() {
  if (isShuttingDown) return;

  try {
    const res = await callTelegramApi('getUpdates', { offset, timeout: 30 });

    if (res && res.ok && Array.isArray(res.result)) {
      consecutiveErrors = 0; // Reset backoff counter on success
      for (const update of res.result) {
        offset = update.update_id + 1;
        if (update.message) {
          try {
            await handleMessage(update.message);
          } catch (handlerErr) {
            console.error('[Telegram Bot] Error processing message:', handlerErr.message);
          }
        }
      }
      setImmediate(pollUpdates);
      return;
    }

    // Handle Telegram API Error Responses (res.ok === false)
    if (res && !res.ok) {
      const code = res.error_code;
      const desc = res.description || '';

      if (code === 401) {
        console.error(`[Telegram Bot] ❌ Authentication failed: ${desc} (401 Unauthorized).`);
        console.error('[Telegram Bot] Please check your TELEGRAM_BOT_TOKEN.');
        process.exit(1);
      }

      if (code === 409) {
        if (desc.includes('webhook')) {
          console.log('[Telegram Bot] 🔄 Webhook conflict detected. Removing webhook and activating polling...');
          await callTelegramApi('deleteWebhook', { drop_pending_updates: false });
          await new Promise(r => setTimeout(r, 2000));
        } else {
          console.warn('[Telegram Bot] ⚠️ Conflict (409): Another polling instance is running with this token. Pausing 10s...');
          await new Promise(r => setTimeout(r, 10000));
        }
        setImmediate(pollUpdates);
        return;
      }

      if (code === 429) {
        const waitSec = res.parameters?.retry_after || 5;
        console.warn(`[Telegram Bot] ⏳ Rate limited (429). Retrying after ${waitSec}s...`);
        await new Promise(r => setTimeout(r, waitSec * 1000));
        setImmediate(pollUpdates);
        return;
      }

      console.warn(`[Telegram Bot] API error (${code}): ${desc}`);
    }
  } catch (err) {
    consecutiveErrors++;
    const backoffSec = Math.min(15, Math.pow(2, Math.min(consecutiveErrors, 4)));
    console.error(`[Telegram Bot] Network/polling error: ${maskToken(err.message, TOKEN)}. Reconnecting in ${backoffSec}s...`);
    await new Promise(r => setTimeout(r, backoffSec * 1000));
  }

  if (!isShuttingDown) {
    setImmediate(pollUpdates);
  }
}

// 5. Startup Sequence & Health Verification
async function startBot() {
  TOKEN = resolveToken();
  if (!TOKEN) {
    console.log("==================================================================");
    console.log("⚠️ BLAXGUARD TELEGRAM BOT SETUP INSTRUCTIONS");
    console.log("==================================================================");
    console.log("1. Open Telegram and search for @BotFather");
    console.log("2. Type /newbot and follow instructions to create your free bot");
    console.log("3. Copy the API Token provided by BotFather");
    console.log("4. Start this bot using one of these secure methods:");
    console.log("   - Environment Variable: $env:TELEGRAM_BOT_TOKEN=\"<TOKEN>\"");
    console.log("                           node telegram_bot.js");
    console.log("   - Local .env file:      TELEGRAM_BOT_TOKEN=<TOKEN>");
    console.log("   - Direct CLI parameter: node telegram_bot.js <TOKEN>");
    console.log("==================================================================");
    console.log("Note: Bot paused cleanly. Provide token to activate live polling.");
    process.exit(0);
  }

  setToken(TOKEN);

  console.log("==================================================================");
  console.log("🤖 BLAXGUARD TELEGRAM SCAM SHIELD SERVICE");
  console.log("==================================================================");

  try {
    // Verify bot identity
    const me = await callTelegramApi('getMe', {}, 10000);
    if (!me || !me.ok || !me.result) {
      const desc = me?.description || 'Token rejected by Telegram API';
      const code = me?.error_code || '401';
      console.error(`[Telegram Bot] ❌ Unable to verify bot identity: ${desc} (Code: ${code})`);
      console.error('[Telegram Bot] Please verify your TELEGRAM_BOT_TOKEN with @BotFather.');
      process.exit(1);
    }

    const botUser = me.result;
    console.log(`✅ Connected successfully as: @${botUser.username} (${botUser.first_name || 'BlaxGuard Bot'})`);
    console.log(`🆔 Bot ID: ${botUser.id}`);

    // Automatically resolve any leftover webhook configuration
    const delWebhook = await callTelegramApi('deleteWebhook', { drop_pending_updates: false }, 10000);
    if (delWebhook && delWebhook.ok) {
      console.log('🔄 Webhook status checked & cleared for long-polling.');
    }

    console.log('⚡ Service status: LIVE & LISTENING for citizen reports');
    console.log('==================================================================');

    pollUpdates();
  } catch (startupErr) {
    const safeError = maskToken(startupErr.message, TOKEN);
    console.error('[Telegram Bot] Startup failure:', safeError);
    if (safeError.includes('unable to verify the first certificate')) {
      console.log('💡 Windows Tip: If running on Windows, execute with: node --use-system-ca telegram_bot.js');
    }
    process.exit(1);
  }
}

// Graceful process termination
process.on('SIGINT', () => {
  console.log('\n[Telegram Bot] Received SIGINT. Shutting down gracefully...');
  isShuttingDown = true;
  process.exit(0);
});

process.on('SIGTERM', () => {
  console.log('\n[Telegram Bot] Received SIGTERM. Shutting down gracefully...');
  isShuttingDown = true;
  process.exit(0);
});

// Run automatically when called directly
if (require.main === module) {
  startBot();
}

module.exports = {
  loadLocalEnv,
  resolveToken,
  setToken,
  maskToken,
  callTelegramApi,
  sendTelegramMessage,
  handleMessage,
  startBot
};
