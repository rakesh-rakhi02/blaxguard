# 🛡️ BlaxGuard: WhatsApp, Telegram & Search Engine Setup Guide

This guide explains how to connect BlaxGuard to **Search Engines (Google, Bing)**, **WhatsApp**, and **Telegram** for real-time scam detection and pop-up warnings.

---

## 1. 🌐 Browser Extension (Google/Bing Search & WhatsApp/Telegram Web Pop-up Warnings)

The extension monitors Google/Bing search results and chat links on WhatsApp Web and Telegram Web, displaying instant pop-up alerts before you open dangerous links.

### How to Install in Chrome or Edge:
1. Open your browser and go to:
   - In Chrome: `chrome://extensions`
   - In Edge: `edge://extensions`
2. Enable **"Developer mode"** (toggle in the top-right corner).
3. Click the **"Load unpacked"** button.
4. Select the `extension` folder located inside this project:
   `c:\Users\odela\OneDrive\Desktop\tkr\extension`
5. That's it! 
   - When you search on **Google** or **Bing**, suspicious links will automatically display a **`⚠️ Suspicious Link`** badge, and clicking one will trigger a protective safety pop-up.
   - When you click a link inside **WhatsApp Web** or **Telegram Web**, BlaxGuard will intercept it and show an instant warning if it is a scam or unverified loan app.

---

## 2. 🤖 Telegram Scam Detection Bot

Citizens can forward any suspicious WhatsApp message, SMS, loan offer, or link directly to your Telegram Bot.

### Quick Setup (Takes 60 Seconds):
1. Open Telegram and search for the official bot: **`@BotFather`**.
2. Send `/newbot` and follow the prompts to choose a bot name (e.g., `MyBlaxGuardBot`).
3. Copy the HTTP API token provided by BotFather (looks like `123456789:ABCdefGhIJKlmNo...`).
4. Start the bot on your computer:
   ```powershell
   node telegram_bot.js YOUR_BOT_TOKEN_HERE
   ```
5. Open Telegram, start a chat with your bot, and forward any message to it. It will instantly reply with the safety verdict, risk score, and RBI verification status!

---

## 3. 📲 WhatsApp Scam Helpline Bot

BlaxGuard includes built-in support for the **Meta WhatsApp Business Cloud API** and **Twilio WhatsApp Sandbox**.

### Testing WhatsApp Replies Locally:
Run the built-in test suites:
```powershell
node whatsapp_bot.js
node test_whatsapp_webhook.js
```

### Local Webhook Testing with cURL:

1. **Verify Webhook Handshake (GET):**
```powershell
curl.exe "http://localhost:8080/api/whatsapp/webhook?hub.mode=subscribe&hub.verify_token=blaxguard_secure_token_123&hub.challenge=test1234"
```

2. **Simulate Inbound WhatsApp Scam Message (POST):**
```powershell
curl.exe -X POST http://localhost:8080/api/whatsapp/webhook -d "from=919876543210&text=Urgent: instant loan approved http://speedrupee-loan.xyz/app.apk"
```

3. **Simulate Inbound Safe RBI Bank Message (POST):**
```powershell
curl.exe -X POST http://localhost:8080/api/whatsapp/webhook -d "from=919876543210&text=Personal loan at https://kreditbee.in"
```

### Live Public Webhook with ngrok:
To connect your local BlaxGuard server to live WhatsApp Cloud API or Twilio:
```powershell
# In a separate terminal, expose port 8080:
ngrok http 8080
```
Copy your secure forwarding URL (e.g. `https://abc123.ngrok-free.app`) and configure it in your WhatsApp settings.

### Production Setup (WhatsApp Cloud API):
1. Go to [Meta Developers Portal](https://developers.facebook.com) and create a Business App with the **WhatsApp** product.
2. In the WhatsApp Webhook configuration:
   - **Callback URL:** `https://<YOUR_NGROK_DOMAIN>/api/whatsapp/webhook`
   - **Verify Token:** `blaxguard_secure_token_123`
   - **Webhook Fields:** Subscribe to `messages`.
3. Whenever a citizen sends or forwards a message to your WhatsApp number, BlaxGuard automatically analyzes the message and returns the structured scam audit.

---

## 4. ⚡ Central REST API Endpoints

BlaxGuard server is running at `http://localhost:8080` and exposes these live endpoints:

- `POST /api/check`: Scans links, SMS, phone numbers, or messages.
  ```json
  // Request
  { "text": "Urgent: Electricity disconnect tonight. Pay at http://discom-bill.xyz" }
  
  // Response
  { "success": true, "score": 70, "verdict": "danger", "reasons": [...] }
  ```

- `POST /api/loan`: Audits loan apps, links, or NBFC names against the RBI registry.
  ```json
  // Request
  { "lender": "https://kreditbee.in", "flags": {} }
  
  // Response
  { "success": true, "score": 0, "verdict": "safe", "isLenderVerified": true }
  ```

- `GET /api/rbi/lookup?q=kreditbee.in`: Checks if a domain or entity is registered with the RBI.
