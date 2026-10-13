# 🛡️ BlaxGuard – AI-Powered Scam Detection and Protection

BlaxGuard is a scam detection and digital safety project designed to help users identify potentially fraudulent links, scam messages, fake loan applications, and suspicious online content before they interact with them.

The project aims to improve online safety by providing suspicious-link warnings through browser extensions and supporting scam detection through messaging integrations.

## 📌 Table of Contents

- About the Project
- Problem Statement
- Key Features
- Technology Stack
- Project Architecture
- Prerequisites
- Installation and Setup
- How to Run the Browser Extension
- How to Set Up the Telegram Bot
- How to Configure WhatsApp Integration
- How to Test the Project
- Security Considerations
- Limitations
- Future Enhancements
- Contributors

---

## 🎯 About the Project

Online scams are increasing through fraudulent websites, phishing links, fake loan applications, and scam messages distributed through messaging platforms.

Many users cannot easily distinguish legitimate links from malicious ones.

BlaxGuard aims to provide an additional layer of protection by identifying potentially suspicious content and displaying warnings to users.

The project includes a browser extension and messaging integrations, depending on the components configured in the deployment.

## 🚨 Problem Statement

**Protecting People from Scam Messages and Fake Loan Apps**

Fake links, fraudulent loan apps, phishing websites, and fake customer-care numbers can expose users to financial losses and personal-data theft.

BlaxGuard aims to help users recognize potential threats before they click suspicious links or interact with fraudulent content.

## ✨ Key Features

### 1. Suspicious Link Detection
Analyzes supported links using the detection methods implemented in the project.

### 2. Browser Extension
Provides browser-based scam warnings on supported websites.

### 3. Suspicious Link Warning Badge
Displays a warning badge when a link is identified as potentially suspicious by the configured detection logic.

### 4. Telegram Bot Integration
Supports scam-checking functionality through Telegram when the bot and its detection service are configured.

### 5. WhatsApp Integration
Supports WhatsApp-based scam detection when the WhatsApp Business Platform integration is configured.

### 6. User Awareness
Helps users recognize potentially dangerous links and understand the importance of online safety.

> Note: Available features depend on the components configured in your project. Detection results are not guaranteed to be accurate.

---

## 🛠️ Technology Stack

The technologies used depend on the components included in the repository.

- **Frontend:** HTML, CSS, JavaScript
- **Browser Extension:** Chrome Extension APIs
- **Messaging Integration:** Telegram Bot API
- **WhatsApp Integration:** WhatsApp Business Platform / Meta Cloud API, if configured
- **Version Control:** Git and GitHub

Additional libraries, backend frameworks, and detection services may be required depending on the implementation.

---

## 🏗️ Project Architecture

The project follows this general workflow:

1. A user encounters a suspicious link or message.
2. The browser extension or messaging interface receives the supported input.
3. The configured detection logic analyzes the input.
4. The system determines whether the content should be flagged as potentially suspicious.
5. A warning or detection result is presented to the user.

```text
              User
               |
       Suspicious Link
               |
      +--------+--------+
      |        |        |
   Browser  Telegram  WhatsApp
  Extension    Bot       Bot
      |        |        |
      +--------+--------+
               |
       Detection Logic
               |
       Risk Assessment
               |
       +-------+-------+
       |               |
    Suspicious       No Risk
       |               |
   Show Warning    Show Result
```

This diagram represents the intended workflow. Actual execution depends on the integrations and detection methods implemented in the repository.

---

# 🚀 Installation and Setup

## Step 1: Download the Repository

Open the BlaxGuard GitHub repository:

https://github.com/rakesh-rakhi02/blaxguard

You can download the project using either method below.

### Method A: Download ZIP

1. Open the repository on GitHub.
2. Click the **Code** button.
3. Select **Download ZIP**.
4. Extract the downloaded ZIP file.
5. Open the extracted project folder in VS Code.

### Method B: Clone Using Git

Install Git if it is not already installed.

Open PowerShell or the VS Code terminal and execute:

```bash
git clone https://github.com/rakesh-rakhi02/blaxguard.git
```

Move into the downloaded repository:

```bash
cd blaxguard
```

Open the project in VS Code:

```bash
code .
```

---

## Step 2: Inspect the Project Files

Before executing the project, identify the available files and folders.

In the VS Code terminal, run:

```powershell
dir
```

Check for the following types of files:

- `manifest.json` — browser extension configuration
- `index.html` — web interface, if included
- JavaScript files — application logic
- `package.json` — Node.js dependencies and scripts, if included
- Bot source files — Telegram integration, if included
- Backend source files — server and detection logic, if included
- `.env.example` — environment variable template, if provided

The actual filenames may differ.

**Important:** Follow the commands for the components that actually exist in your repository.

---

# 🌐 How to Run the Browser Extension

## Step 1: Open Chrome

Open Google Chrome.

Navigate to:

`chrome://extensions/`

For Microsoft Edge, navigate to:

`edge://extensions/`

## Step 2: Enable Developer Mode

1. Find the Developer mode toggle.
2. Turn it ON.
3. Wait for the additional options to appear.

## Step 3: Load the Extension

1. Click **Load unpacked**.
2. Browse to the downloaded BlaxGuard project.
3. Select the folder containing the extension's `manifest.json`.
4. Click **Select Folder**.

If the extension is inside a subfolder, select that subfolder rather than the repository's root folder.

## Step 4: Verify Installation

1. Check whether BlaxGuard appears on the extensions page.
2. Confirm that the extension is enabled.
3. Open the extension's details if you need to inspect its permissions.
4. Open a supported website and test the implemented detection features.

If Chrome displays an error, inspect the extension's error details and check the browser console.

## Step 5: Test Suspicious-Link Warnings

1. Open a supported website.
2. Find a link that your detection system can analyze.
3. Trigger the implemented scanning functionality.
4. Observe whether BlaxGuard displays a warning for a link flagged by its detection logic.
5. Review the result and confirm that the extension behaves as expected.

Use controlled test cases rather than clicking real malicious links.

> A warning may not appear on every website if the extension only supports specific pages or link types.

---

# 🤖 How to Set Up the Telegram Bot

Follow this section if the Telegram bot source code is included in the repository.

## Step 1: Create a Telegram Bot

1. Open Telegram.
2. Search for the official `@BotFather` account.
3. Start a conversation.
4. Send:

   `/newbot`

5. Enter a display name for your bot.
6. Enter a unique username ending in `bot`.
7. Copy the API token provided by BotFather.

**Security:** Never upload your Telegram bot token to GitHub or share it publicly.

## Step 2: Configure the Bot Token

Check the Telegram bot source code to determine how it reads the token.

If the application supports environment variables, create a local `.env` file using the variable name expected by the code.

For example:

```env
TELEGRAM_BOT_TOKEN=YOUR_TELEGRAM_BOT_TOKEN
```

Replace the placeholder with your actual token.

Do not commit `.env` to GitHub.

If the project expects a different environment variable name, use the name specified in its source code.

## Step 3: Install Dependencies

If the bot uses Node.js and contains a `package.json`, open the terminal in the relevant directory and run:

```bash
npm install
```

If the bot is implemented in Python, use the dependency instructions provided by the project.

Do not run both commands unless the project actually uses both environments.

## Step 4: Start the Telegram Bot

For a Node.js project, inspect the scripts in `package.json` and run the appropriate command.

For example, if the project defines a `start` script:

```bash
npm start
```

For a Python bot, use the entry-point filename specified by the project.

For example:

```bash
python bot.py
```

Replace `bot.py` with the actual filename if it differs.

## Step 5: Test the Bot

1. Open Telegram.
2. Search for your bot using its exact username.
3. Open the bot and press Start.
4. Send a message or link supported by the implementation.
5. Check the bot's response.
6. Inspect the terminal logs if the bot does not respond.

The bot must be running and correctly configured to process messages.

---

# 💬 How to Configure WhatsApp Integration

Follow this section only if the repository includes WhatsApp integration code.

## Step 1: Set Up Meta Developer Access

1. Open the Meta for Developers website:

   https://developers.facebook.com/

2. Sign in to your Meta account.
3. Create or select an application.
4. Add the WhatsApp product if required.
5. Open the WhatsApp API configuration.

## Step 2: Configure WhatsApp Credentials

Depending on your implementation, you may need:

- WhatsApp Business Account ID
- Phone Number ID
- Access token
- Webhook verification token
- Backend callback URL

Store credentials in environment variables rather than directly in source code.

Example:

```env
WHATSAPP_ACCESS_TOKEN=YOUR_ACCESS_TOKEN
WHATSAPP_PHONE_NUMBER_ID=YOUR_PHONE_NUMBER_ID
WHATSAPP_VERIFY_TOKEN=YOUR_WEBHOOK_VERIFY_TOKEN
```

These are example variable names. Match them to the names used by your backend.

Never commit actual credentials to GitHub.

## Step 3: Configure the Webhook

If your implementation receives WhatsApp messages through webhooks:

1. Start the backend service.
2. Deploy it to an HTTPS-accessible server or use an appropriate development tunnel.
3. Configure the callback URL in Meta Developer settings.
4. Configure the verification token.
5. Subscribe to the required WhatsApp webhook events.
6. Verify that incoming messages reach your backend.

## Step 4: Test WhatsApp Integration

1. Complete the required Meta setup.
2. Use an authorized test number or configured WhatsApp Business number.
3. Send a supported test message.
4. Confirm that the webhook receives it.
5. Check that the configured detection logic processes the input.
6. Verify that the expected response is returned.

WhatsApp integration will not work merely by installing the browser extension. It requires the appropriate backend, credentials, and Meta configuration.

---

# ▶️ Running the Web Application or Backend

If the repository contains a Node.js application with a `package.json`:

## Step 1: Install Node.js

Install a compatible Node.js version from:

https://nodejs.org/

Restart the terminal after installation if necessary.

Check the installation:

```bash
node --version
npm --version
```

## Step 2: Install Project Dependencies

Navigate to the directory containing `package.json`.

Run:

```bash
npm install
```

## Step 3: Configure Environment Variables

Inspect the project documentation and source code.

Create a local `.env` file if the application requires environment variables.

Add the variable names expected by the implementation.

Do not upload API keys or tokens.

## Step 4: Start the Application

Inspect the available scripts:

```bash
npm run
```

Run the appropriate script defined by the project.

For example, if a `dev` script exists:

```bash
npm run dev
```

If a `start` script exists:

```bash
npm start
```

Open the local URL displayed in the terminal.

**Note:** These commands are conditional. The actual startup command depends on the repository's framework and `package.json`.

---

# 🧪 How to Test BlaxGuard

Use the following checklist to verify the components you have implemented.

| Test Case | Expected Result |
|---|---|
| Install the browser extension | Extension loads successfully |
| Open a supported website | Extension operates on supported pages |
| Submit a suspicious test URL | Detection logic returns the expected result |
| Submit a known benign test URL | Detection logic returns the expected result |
| Start the Telegram bot | Bot becomes available |
| Send a supported Telegram message | Bot processes the message |
| Configure WhatsApp integration | Backend receives supported test messages |
| Trigger a suspicious-link warning | Warning appears when the implemented rules flag the link |

Use known benign URLs and safe, controlled test data. Never use a successful test result as proof that every real-world scam can be detected.

---

# 🔐 Security Considerations

- Never commit API keys, passwords, or bot tokens.
- Keep `.env` files out of version control.
- Request only the browser permissions the extension needs.
- Avoid storing sensitive messages or personal data unnecessarily.
- Validate and sanitize user input.
- Use HTTPS for production services and webhooks.
- Protect backend endpoints against unauthorized requests.
- Rotate credentials immediately if they are accidentally exposed.

---

# ⚠️ Limitations

- Scam detection may produce false positives and false negatives.
- New phishing websites and scam techniques appear frequently.
- Detection accuracy depends on the implemented rules, models, and data sources.
- Some features require an internet connection and external service configuration.
- Browser extensions may not operate on restricted browser pages.
- Telegram and WhatsApp features require their respective integrations to be configured.

BlaxGuard should be treated as an additional safety tool, not a guarantee that a website or message is safe.

---

# 🚀 Future Enhancements

Potential future improvements include:

- Machine-learning-based phishing URL classification
- Detection of fake loan applications
- Identification of suspicious customer-care numbers
- Improved scam-message analysis
- Integration with reputable threat-intelligence sources
- More detailed explanations for detection results
- Multilingual scam warnings
- A reporting system for suspicious links
- Improved false-positive handling

These are potential enhancements and should not be considered implemented unless the corresponding functionality exists in the codebase.

---

# 👨‍💻 Contributors

**BlaxGuard Project Team**

GitHub Repository:

https://github.com/rakesh-rakhi02/blaxguard

---

## 📄 License

A license has not been specified in this README. Add a suitable license file if you intend to distribute the project under an open-source license.
