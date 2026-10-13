/**
 * BlaxGuard Central Security & Scam Detection Engine
 * Shared module for REST API, Telegram Bot, WhatsApp Bot, and Browser Extension backend.
 */

// REAL-WORLD RBI REGISTERED LENDERS, BANKS & CERTIFIED DIGITAL LENDING PLATFORMS
const REAL_WORLD_RBI_LENDERS = [
  // Top Scheduled Commercial Banks
  {
    name: "State Bank of India (SBI)",
    aliases: ["sbi", "state bank", "state bank of india", "onlinesbi", "yono"],
    domains: ["sbi.co.in", "onlinesbi.sbi", "onlinesbi.com", "bank.sbi"],
    category: "Scheduled Public Sector Bank",
    license: "RBI / Banking Regulation Act"
  },
  {
    name: "HDFC Bank Ltd",
    aliases: ["hdfc", "hdfc bank", "hdfc personal loan"],
    domains: ["hdfcbank.com", "hdfc.com"],
    category: "Scheduled Commercial Bank",
    license: "RBI / Banking Regulation Act"
  },
  {
    name: "ICICI Bank Ltd",
    aliases: ["icici", "icici bank", "icici direct"],
    domains: ["icicibank.com"],
    category: "Scheduled Commercial Bank",
    license: "RBI / Banking Regulation Act"
  },
  {
    name: "Axis Bank Ltd",
    aliases: ["axis", "axis bank"],
    domains: ["axisbank.com"],
    category: "Scheduled Commercial Bank",
    license: "RBI / Banking Regulation Act"
  },
  {
    name: "Kotak Mahindra Bank",
    aliases: ["kotak", "kotak mahindra", "kotak 811", "kotak bank"],
    domains: ["kotak.com", "kotak811.com"],
    category: "Scheduled Commercial Bank",
    license: "RBI / Banking Regulation Act"
  },
  {
    name: "Punjab National Bank (PNB)",
    aliases: ["pnb", "punjab national bank"],
    domains: ["pnbindia.in", "pnbindia.com"],
    category: "Scheduled Public Sector Bank",
    license: "RBI / Banking Regulation Act"
  },
  {
    name: "Bank of Baroda",
    aliases: ["bob", "bank of baroda", "bob world"],
    domains: ["bankofbaroda.in", "bankofbaroda.com"],
    category: "Scheduled Public Sector Bank",
    license: "RBI / Banking Regulation Act"
  },
  {
    name: "Canara Bank",
    aliases: ["canara", "canara bank"],
    domains: ["canarabank.com"],
    category: "Scheduled Public Sector Bank",
    license: "RBI / Banking Regulation Act"
  },
  {
    name: "Union Bank of India",
    aliases: ["union bank", "union bank of india", "ubi"],
    domains: ["unionbankofindia.co.in"],
    category: "Scheduled Public Sector Bank",
    license: "RBI / Banking Regulation Act"
  },
  {
    name: "IDFC FIRST Bank",
    aliases: ["idfc", "idfc first", "idfc first bank", "idfc bank"],
    domains: ["idfcfirstbank.com"],
    category: "Scheduled Commercial Bank",
    license: "RBI / Banking Regulation Act"
  },
  {
    name: "IndusInd Bank",
    aliases: ["indusind", "indusind bank"],
    domains: ["indusind.com"],
    category: "Scheduled Commercial Bank",
    license: "RBI / Banking Regulation Act"
  },
  {
    name: "Federal Bank",
    aliases: ["federal bank", "federal"],
    domains: ["federalbank.co.in"],
    category: "Scheduled Commercial Bank",
    license: "RBI / Banking Regulation Act"
  },
  {
    name: "Yes Bank Ltd",
    aliases: ["yes bank"],
    domains: ["yesbank.in"],
    category: "Scheduled Commercial Bank",
    license: "RBI / Banking Regulation Act"
  },
  {
    name: "RBL Bank",
    aliases: ["rbl", "rbl bank", "ratnakar bank"],
    domains: ["rblbank.com"],
    category: "Scheduled Commercial Bank",
    license: "RBI / Banking Regulation Act"
  },
  {
    name: "AU Small Finance Bank",
    aliases: ["au bank", "au small finance bank", "au sfb"],
    domains: ["aubank.in"],
    category: "RBI Scheduled Small Finance Bank",
    license: "RBI / SFB License"
  },
  {
    name: "Equitas Small Finance Bank",
    aliases: ["equitas", "equitas bank", "equitas sfb"],
    domains: ["equitasbank.com"],
    category: "RBI Scheduled Small Finance Bank",
    license: "RBI / SFB License"
  },

  // Major Systemically Important NBFCs
  {
    name: "Bajaj Finance Ltd / Bajaj Finserv",
    aliases: ["bajaj finserv", "bajaj finance", "bajaj finserv ltd", "bajaj", "bajaj markets"],
    domains: ["bajajfinserv.in", "bajajfinance.in", "bajajfinservmarkets.in"],
    category: "RBI Registered NBFC-UL (Upper Layer)",
    license: "RBI Reg No. 05.00018 / NBFC"
  },
  {
    name: "Tata Capital Financial Services Ltd",
    aliases: ["tata capital", "tata finance", "tatacapital"],
    domains: ["tatacapital.com"],
    category: "RBI Registered NBFC-UL (Upper Layer)",
    license: "RBI Reg No. 13.00041 / NBFC"
  },
  {
    name: "Mahindra & Mahindra Financial Services Ltd",
    aliases: ["mahindra finance", "m&m financial", "mahindra financial"],
    domains: ["mahindrafinance.com"],
    category: "RBI Registered NBFC-UL",
    license: "RBI Reg No. 13.00072 / NBFC"
  },
  {
    name: "Aditya Birla Finance Ltd",
    aliases: ["aditya birla finance", "aditya birla capital", "abfl", "abc"],
    domains: ["adityabirlacapital.com", "adityabirlafinance.com"],
    category: "RBI Registered NBFC-UL",
    license: "RBI Reg No. 14.01358 / NBFC"
  },
  {
    name: "Muthoot Finance Ltd",
    aliases: ["muthoot", "muthoot finance", "muthoot gold loan"],
    domains: ["muthootfinance.com"],
    category: "RBI Registered NBFC-UL",
    license: "RBI Reg No. 07.00010 / NBFC"
  },
  {
    name: "Shriram Finance Ltd",
    aliases: ["shriram finance", "shriram city", "shriram transport"],
    domains: ["shriramfinance.in", "shriramcity.in"],
    category: "RBI Registered NBFC-UL",
    license: "RBI Reg No. 07.00458 / NBFC"
  },
  {
    name: "L&T Finance Ltd",
    aliases: ["l&t finance", "ltfs", "larsen & toubro finance"],
    domains: ["ltfs.com"],
    category: "RBI Registered NBFC-ML (Middle Layer)",
    license: "RBI Reg No. B-13.01287 / NBFC"
  },
  {
    name: "Poonawalla Fincorp Ltd",
    aliases: ["poonawalla fincorp", "poonawalla finance", "magma fincorp"],
    domains: ["poonawallafincorp.com"],
    category: "RBI Registered NBFC-ML",
    license: "RBI Reg No. 05.01168 / NBFC"
  },
  {
    name: "Cholamandalam Investment and Finance Co Ltd",
    aliases: ["cholamandalam", "chola", "chola finance"],
    domains: ["cholamandalam.com"],
    category: "RBI Registered NBFC-UL",
    license: "RBI Reg No. 07.00029 / NBFC"
  },
  {
    name: "Piramal Capital & Housing Finance Ltd",
    aliases: ["piramal", "piramal finance", "piramal capital"],
    domains: ["piramalfinance.com"],
    category: "RBI Registered NBFC-HFC",
    license: "RBI Reg No. 05.00030 / NBFC"
  },
  {
    name: "Manappuram Finance Ltd",
    aliases: ["manappuram", "manappuram finance"],
    domains: ["manappuram.com"],
    category: "RBI Registered NBFC-ML",
    license: "RBI Reg No. 16.00029 / NBFC"
  },
  {
    name: "IIFL Finance Ltd",
    aliases: ["iifl", "iifl finance", "india infoline"],
    domains: ["iifl.com", "iiflfinance.com"],
    category: "RBI Registered NBFC-ML",
    license: "RBI Reg No. 13.01792 / NBFC"
  },
  {
    name: "Hero FinCorp Ltd",
    aliases: ["hero fincorp", "hero finance"],
    domains: ["herofincorp.com"],
    category: "RBI Registered NBFC-ML",
    license: "RBI Reg No. 14.00445 / NBFC"
  },
  {
    name: "TVS Credit Services Ltd",
    aliases: ["tvs credit", "tvs finance"],
    domains: ["tvscredit.com"],
    category: "RBI Registered NBFC-ML",
    license: "RBI Reg No. 07.00693 / NBFC"
  },
  {
    name: "HDB Financial Services Ltd",
    aliases: ["hdb", "hdb financial", "hdbfs"],
    domains: ["hdbfs.com"],
    category: "RBI Registered NBFC-UL",
    license: "RBI Reg No. 05.06730 / NBFC"
  },
  {
    name: "SMFG India Credit Co Ltd",
    aliases: ["smfg", "smfg india credit", "fullerton", "fullerton india"],
    domains: ["smfgindiacredit.com"],
    category: "RBI Registered NBFC-ML",
    license: "RBI Reg No. 07.00791 / NBFC"
  },
  {
    name: "Home Credit India Finance Pvt Ltd",
    aliases: ["home credit", "home credit india"],
    domains: ["homecredit.co.in"],
    category: "RBI Registered NBFC-ND-SI",
    license: "RBI Reg No. 14.02905 / NBFC"
  },
  {
    name: "DMI Finance Pvt Ltd",
    aliases: ["dmi finance", "dmi"],
    domains: ["dmifinance.in"],
    category: "RBI Registered NBFC-ND-SI",
    license: "RBI Reg No. 14.02052 / NBFC"
  },
  {
    name: "InCred Financial Services Ltd",
    aliases: ["incred", "incred finance"],
    domains: ["incred.com"],
    category: "RBI Registered NBFC-ND-SI",
    license: "RBI Reg No. B-13.01817 / NBFC"
  },

  // Certified Digital Lending Platforms (DLAs) & Fintech Lenders
  {
    name: "KreditBee (KrazyBee Services Pvt Ltd)",
    aliases: ["kreditbee", "krazybee", "kredit bee"],
    domains: ["kreditbee.in", "krazybee.com"],
    category: "RBI Certified Digital Lending Platform / NBFC-ICC",
    license: "RBI Reg No. N-14.03465 / KrazyBee"
  },
  {
    name: "Navi (Navi Finserv Limited)",
    aliases: ["navi", "navi finserv", "navi technologies"],
    domains: ["navi.com"],
    category: "RBI Registered NBFC-ND-SI / DLA",
    license: "RBI Reg No. N-02.00224 / Navi Finserv"
  },
  {
    name: "Money View (Whizdm Innovations Pvt Ltd)",
    aliases: ["money view", "moneyview", "whizdm"],
    domains: ["moneyview.in"],
    category: "RBI Compliant Digital Lending Platform",
    license: "Partner NBFCs: DMI Finance, Aditya Birla, Clix"
  },
  {
    name: "Fibe / EarlySalary (Social Worth Technologies)",
    aliases: ["fibe", "earlysalary", "early salary"],
    domains: ["fibe.in", "earlysalary.com"],
    category: "RBI Certified Digital Lending Platform / Earlysalary NBFC",
    license: "RBI Reg No. N-13.02324 / Earlysalary Services"
  },
  {
    name: "CASHe (Bhanix Finance and Investment Ltd)",
    aliases: ["cashe", "bhanix", "bhanix finance"],
    domains: ["cashe.co.in"],
    category: "RBI Registered NBFC-ICC / DLA",
    license: "RBI Reg No. 13.00221 / Bhanix Finance"
  },
  {
    name: "mPokket (Mayfair Capital Pvt Ltd)",
    aliases: ["mpokket", "m pokket", "mayfair capital"],
    domains: ["mpokket.in"],
    category: "RBI Registered NBFC-ICC / DLA",
    license: "RBI Reg No. B-05.06178 / Mayfair Capital"
  },
  {
    name: "Kissht / RING (Si Creva Capital Services Pvt Ltd)",
    aliases: ["kissht", "ring", "ring app", "si creva"],
    domains: ["kissht.com", "ring.pe"],
    category: "RBI Registered NBFC / DLA",
    license: "RBI Reg No. N-13.02123 / Si Creva"
  },
  {
    name: "LazyPay (PayU Finance India Pvt Ltd)",
    aliases: ["lazypay", "payu finance", "lazy pay"],
    domains: ["lazypay.in", "payufin.com"],
    category: "RBI Registered NBFC-ND-SI / DLA",
    license: "RBI Reg No. N-13.02293 / PayU Finance"
  },
  {
    name: "PaySense (PayU Finance India)",
    aliases: ["paysense", "pay sense"],
    domains: ["gopaysense.com", "paysense.com"],
    category: "RBI Compliant Lending Platform",
    license: "RBI / PayU Finance India"
  },
  {
    name: "CRED Cash (Newtap Finance Pvt Ltd)",
    aliases: ["cred", "cred cash", "newtap finance", "newtap"],
    domains: ["cred.club", "newtap.in"],
    category: "RBI Registered NBFC / DLA",
    license: "RBI Reg No. N-13.02422 / Newtap Finance"
  },
  {
    name: "Slice (Quadrillion Finance Pvt Ltd)",
    aliases: ["slice", "sliceit", "quadrillion"],
    domains: ["sliceit.com"],
    category: "RBI Registered NBFC / DLA",
    license: "RBI Reg No. N-02.00281 / Quadrillion"
  },
  {
    name: "Jupiter Money (Amica Financial Technologies)",
    aliases: ["jupiter", "jupiter money", "amica"],
    domains: ["jupiter.money"],
    category: "RBI Compliant Digital Banking & Lending Partner",
    license: "Partner Bank: Federal Bank & CSB Bank"
  },
  {
    name: "Fi Money (epiFi Technologies Pvt Ltd)",
    aliases: ["fi money", "fi", "epifi"],
    domains: ["fi.money"],
    category: "RBI Compliant Digital Banking & Lending Partner",
    license: "Partner Bank: Federal Bank"
  },
  {
    name: "PayMe India (Mamta Projects Pvt Ltd)",
    aliases: ["payme", "payme india", "mamta projects"],
    domains: ["paymeindia.in"],
    category: "RBI Registered NBFC / DLA",
    license: "RBI Reg No. B-14.02055 / Mamta Projects"
  },
  {
    name: "Rupeek (Rupeek Fintech Pvt Ltd)",
    aliases: ["rupeek", "rupeek gold loan"],
    domains: ["rupeek.com"],
    category: "RBI Compliant Gold Loan Platform",
    license: "Partner Banks: Federal Bank, ICICI, Karur Vysya"
  },
  {
    name: "LoanTap (LoanTap Credit Products Pvt Ltd)",
    aliases: ["loantap", "loan tap"],
    domains: ["loantap.in"],
    category: "RBI Registered NBFC / DLA",
    license: "RBI Reg No. N-13.02241 / LoanTap Credit"
  },
  {
    name: "Faircent (Fairassets Technologies India Pvt Ltd)",
    aliases: ["faircent", "fair assets"],
    domains: ["faircent.com"],
    category: "RBI Registered NBFC-P2P",
    license: "RBI Reg No. N-12.00479 / NBFC-P2P"
  },
  {
    name: "Clix Capital Services Pvt Ltd",
    aliases: ["clix", "clix capital"],
    domains: ["clix.capital"],
    category: "RBI Registered NBFC-ND-SI",
    license: "RBI Reg No. B-14.02057 / NBFC"
  },
  {
    name: "Olyv / SmartCoin (Upmove Capital Pvt Ltd)",
    aliases: ["olyv", "smartcoin", "smart coin", "upmove"],
    domains: ["olyv.in", "smartcoin.co.in"],
    category: "RBI Registered NBFC / DLA",
    license: "RBI Reg No. N-14.03478 / Upmove Capital"
  },
  {
    name: "BankBazaar (A&A Worksuite Pvt Ltd)",
    aliases: ["bankbazaar", "bank bazaar"],
    domains: ["bankbazaar.com"],
    category: "RBI Compliant Financial Supermarket & Aggregator",
    license: "Direct Integration with RBI Scheduled Banks & NBFCs"
  },
  {
    name: "Paisabazaar (Paisabazaar Marketing and Consulting)",
    aliases: ["paisabazaar", "paisa bazaar"],
    domains: ["paisabazaar.com"],
    category: "RBI Compliant Financial Supermarket & Aggregator",
    license: "Direct Integration with RBI Scheduled Banks & NBFCs"
  },
  {
    name: "RBI Sachet Official Portal",
    aliases: ["sachet", "rbi sachet", "sachet rbi"],
    domains: ["sachet.rbi.org.in"],
    category: "Official Reserve Bank of India Portal for Citizen Verification",
    license: "Reserve Bank of India (Official Portal)"
  }
];

function extractDomain(inputStr) {
  let s = (inputStr || "").trim();
  if (!s) return null;
  if (/^[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(\/.*)?$/i.test(s) && !s.startsWith("http")) {
    s = "https://" + s;
  }
  try {
    const url = new URL(s);
    let host = url.hostname.toLowerCase();
    if (host.startsWith("www.")) host = host.substring(4);
    return host;
  } catch(e) {
    const m = s.match(/(?:https?:\/\/)?(?:www\.)?([a-zA-Z0-9-]+\.[a-zA-Z0-9.-]+)/i);
    if (m && m[1]) return m[1].toLowerCase().replace(/^www\./, "");
    return null;
  }
}

function lookupRbiLender(query) {
  if (!query) return null;
  const q = query.trim().toLowerCase();
  const domain = extractDomain(q);

  for (const lender of REAL_WORLD_RBI_LENDERS) {
    if (domain) {
      const dMatch = lender.domains.some(d => domain === d || domain.endsWith("." + d));
      if (dMatch) return lender;
    }
    const lname = lender.name.toLowerCase();
    if (lname === q || lname.includes(q) || (q.length >= 3 && q.includes(lname))) {
      return lender;
    }
    const aliasMatch = lender.aliases.some(a => {
      const la = a.toLowerCase();
      return la === q || (q.length >= 3 && (la.includes(q) || q.includes(la)));
    });
    if (aliasMatch) return lender;

    const domainTextMatch = lender.domains.some(d => q.includes(d));
    if (domainTextMatch) return lender;
  }
  return null;
}

const genuineDomains = [
  "onlinesbi.sbi", "sbi.co.in", "hdfcbank.com", "icicibank.com", "axisbank.com",
  "pnbindia.in", "rbi.org.in", "sachet.rbi.org.in", "cybercrime.gov.in", "gov.in", "nic.in",
  "pmkisan.gov.in", "epfindia.gov.in", "incometax.gov.in", "jio.com", "airtel.in", "bsnl.co.in",
  "irctc.co.in", "indiapost.gov.in", "swiggy.com", "zomato.com", "amazon.in", "flipkart.com", "karnataka.gov.in"
];
REAL_WORLD_RBI_LENDERS.forEach(l => {
  if (Array.isArray(l.domains)) {
    l.domains.forEach(d => {
      if (!genuineDomains.includes(d)) genuineDomains.push(d);
    });
  }
});

const RULE_DESCRIPTIONS = {
  urgency: "Creates extreme urgency, panic, or false deadline pressure.",
  otpPin: "Demands OTP, UPI PIN, or secret credential disclosure.",
  digitalArrest: "Threatens digital arrest, CBI/Police notice, or false legal warrant.",
  taskScam: "Promises easy daily income from YouTube likes, Telegram tasks, or part-time ratings.",
  telecomThreat: "Threatens immediate SIM card disconnection or Aadhaar block.",
  kycExpiry: "Falsely claims KYC, PAN, or account has expired or suspended.",
  prizes: "Lures with fake lottery prizes, cashback, or KBC lucky draw winnings.",
  advanceFee: "Demands upfront processing fees, registration charge, or refundable security deposit.",
  loanBait: "Offers unrealistic instant loans without credit checks or valid verification.",
  remoteApk: "Instructs downloading unverified APK files or remote control apps (AnyDesk/RustDesk/TeamViewer).",
  fakeCareNum: "Quotes a personal 10-digit mobile number as official customer care.",
  shortLink: "Uses a shortened URL (bit.ly, tinyurl, etc.) to hide the actual scam website destination.",
  riskyTld: "Uses a high-risk domain ending (.xyz, .top, .live, etc.) frequently used in phishing attacks.",
  missingHttps: "Link is insecure (missing HTTPS encryption). Official financial services mandate HTTPS.",
  brandSpoof: "Imitates a reputed bank, utility, or government brand on an unauthorized website.",
  registryMatched: "Community threat: Already flagged in citizen fraud database!"
};

async function evaluateTextSafety(rawText) {
  const text = (rawText || "").trim();
  const lower = text.toLowerCase();

  let score = 0;
  let matchedRules = [];
  let matchedRegistryEntry = null;

  const hasProtectiveWarning = /(do not share|never share|never asks for|never asks|not you\?|do not disclose|valid for \d+ min)/i.test(lower);

  const urgencyRegex = /\b(urgent|immediately|right now|within \d+ hours?|within \d+ mins?|last chance|account will be blocked|service suspended|electricity power disconnect|power cutoff|tonight at \d+|sim blocked today)\b/i;
  if (urgencyRegex.test(lower)) {
    score += 25;
    matchedRules.push("urgency");
  }

  const otpRegex = /\b(otp|upi pin|4-digit pin|6-digit pin|share pin|enter pin|provide otp|send otp|verify otp|share code|enter upi|password)\b/i;
  if (otpRegex.test(lower)) {
    if (!hasProtectiveWarning) {
      const isDemandingCredentials = /(share|send|enter|provide|verify).*(otp|pin|password)|(otp|pin|password).*(share|send|enter|provide)/i.test(lower);
      score += isDemandingCredentials ? 45 : 30;
      matchedRules.push("otpPin");
    }
  }

  const digitalArrestRegex = /\b(cbi|cyber crime cell|cyber cell|arrest warrant|fir lodged|section 420|money laundering|customs officer|narcotics department|video call immediately|digital arrest|police notice|police officer|investigation officer|speak to police)\b/i;
  if (digitalArrestRegex.test(lower)) {
    score += 45;
    matchedRules.push("digitalArrest");
  }

  const taskScamRegex = /\b(part-time|work from home|earn daily|earn ₹|earn rs|like youtube|daily income|telegram @|telegram channel|review task|task job)\b/i;
  if (taskScamRegex.test(lower)) {
    score += 40;
    matchedRules.push("taskScam");
  }

  const telecomThreatRegex = /\b(sim card will be deactivated|sim deactivat|disconnected today|trai notice|registered on your aadhaar|verification desk)\b/i;
  if (telecomThreatRegex.test(lower)) {
    score += 35;
    matchedRules.push("telecomThreat");
  }

  const kycRegex = /\b(kyc expired|update kyc|kyc pending|pan aadhaar link|pan blocked|pan card block|account blocked|kyc verification|sim kyc|aadhaar update|kyc suspension|put on hold)\b/i;
  if (kycRegex.test(lower)) {
    score += 30;
    matchedRules.push("kycExpiry");
  }

  const prizeRegex = /\b(congratulations|you won|won lottery|lucky draw|kbc|cashback of rs|prize money|reward points|claim ₹|claim rs|gift voucher|winner draw)\b/i;
  if (prizeRegex.test(lower)) {
    score += 30;
    matchedRules.push("prizes");
  }

  const feeRegex = /\b(processing fee|registration fee|refundable fee|pay deposit|advance payment|pay ₹\d+|pay rs \d+ to claim|security deposit|transfer fee|courier charge|clearance fee)\b/i;
  if (feeRegex.test(lower)) {
    score += 30;
    matchedRules.push("advanceFee");
  }

  const loanRegex = /\b(pre-approved loan|instant loan|instant cash|no cibil|without cibil|loan in 5 mins|0% interest loan|instant ₹|instant rs|quick cash loan)\b/i;
  if (loanRegex.test(lower)) {
    score += 30;
    matchedRules.push("loanBait");
  }

  const remoteApkRegex = /(\.apk|\.apk\.zip|download apk|download app|install app to update|anydesk|teamviewer|rustdesk|quicksupport|screen share|alpemix|airmirror|whatsapp gold)\b/i;
  if (remoteApkRegex.test(lower)) {
    score += 40;
    matchedRules.push("remoteApk");
  }

  const careKeyword = /\b(customer care|helpline|support|helpdesk|call us at|call officer|toll free|verification desk|kyc desk)\b/i.test(lower);
  const mobileNumberMatch = /(?:\+?91[\-\s]?)?([6-9]\d{9})\b/.exec(lower);
  const isOfficialHelpline = /\b(1800\d{4,8}|1912|1930|112)\b/.test(lower);

  if (careKeyword && mobileNumberMatch && !isOfficialHelpline) {
    score += 35;
    matchedRules.push("fakeCareNum");
  }

  const shortLinkRegex = /(bit\.ly|tinyurl\.com|t\.co|is\.gd|cutt\.ly|rb\.gy|shorturl\.at|ow\.ly|buff\.ly|goo\.gl)/i;
  if (shortLinkRegex.test(lower)) {
    score += 25;
    matchedRules.push("shortLink");
  }

  const riskyTldRegex = /\.(xyz|top|online|club|buzz|work|live|loan|vip|icu|tk|ml|ga|cf|gq|site|space|guru|cam|rest)(?:[\/\?\s]|$)/i;
  const rawIpRegex = /https?:\/\/\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}/i;
  if (riskyTldRegex.test(lower) || rawIpRegex.test(lower)) {
    score += 30;
    matchedRules.push("riskyTld");
  }

  const httpRegex = /http:\/\/[a-z0-9\-\._~:\/\?#\[\]@!\$&'\(\)\*\+,;=]+/i;
  if (httpRegex.test(text) && !text.includes("https://")) {
    score += 15;
    matchedRules.push("missingHttps");
  }

  const brandKeywords = /(sbi|hdfc|icici|axis|pnb|rbi|gov|pmkisan|epfo|discom|electricity|bescom|bsnl|jio|airtel|incometax|irctc|indiapost|whatsapp|telegram)/i;
  const urlMatches = text.match(/https?:\/\/[^\s]+/gi) || [];
  let isSpoofed = false;
  let hasGenuineWhitelist = false;

  const verifiedEntity = lookupRbiLender(text);
  if (verifiedEntity) {
    hasGenuineWhitelist = true;
  }

  for (let rawU of urlMatches) {
    const u = rawU.replace(/[.,;!?)]+$/, "");
    try {
      const urlObj = new URL(u);
      const hostname = urlObj.hostname.toLowerCase();
      const cleanHost = hostname.replace(/^www\./, "");
      const isOfficial = genuineDomains.some(d => cleanHost === d || cleanHost.endsWith("." + d));

      if (isOfficial) {
        hasGenuineWhitelist = true;
      } else if (brandKeywords.test(hostname)) {
        isSpoofed = true;
      }
    } catch (e) {
      if (brandKeywords.test(u) && !genuineDomains.some(d => u.toLowerCase().includes(d))) {
        isSpoofed = true;
      }
    }
  }

  if (isSpoofed) {
    score += 35;
    matchedRules.push("brandSpoof");
  }

  const hasSevereScamIndicators = matchedRules.some(r => ["urgency", "riskyTld", "shortLink", "brandSpoof", "remoteApk", "fakeCareNum", "prizes", "advanceFee", "loanBait", "digitalArrest", "taskScam", "telecomThreat", "registryMatched"].includes(r));
  const hasCriticalThreat = matchedRules.some(r => ["riskyTld", "brandSpoof", "remoteApk", "digitalArrest", "taskScam", "telecomThreat", "registryMatched"].includes(r));
  const hasCredentialTheft = matchedRules.includes("otpPin") && !hasProtectiveWarning;

  if (hasGenuineWhitelist && !hasCriticalThreat && !hasCredentialTheft) {
    score = 0;
    matchedRules = matchedRules.filter(r => r !== "loanBait" && r !== "urgency" && r !== "shortLink" && r !== "missingHttps");
  } else if (hasProtectiveWarning && !hasSevereScamIndicators && score <= 35) {
    score = 0;
    matchedRules = matchedRules.filter(r => r !== "otpPin");
  } else if (hasGenuineWhitelist && score <= 35) {
    score = 0;
  }

  let finalScore = Math.min(100, Math.max(0, score));
  let verdict = "safe";
  if (finalScore >= 50) {
    verdict = "danger";
  } else if (finalScore >= 20) {
    verdict = "caution";
  } else {
    verdict = "safe";
  }

  const reasons = matchedRules.map(k => RULE_DESCRIPTIONS[k] || k);
  if (reasons.length === 0) {
    if (verifiedEntity) {
      reasons.push(`Verified RBI-Regulated Institution: ${verifiedEntity.name} (${verifiedEntity.category})`);
    } else {
      reasons.push("No known scam triggers or deceptive vectors detected.");
    }
  }

  return {
    score: finalScore,
    verdict: verdict,
    matchedRules: matchedRules,
    reasons: reasons,
    verifiedLender: verifiedEntity || null,
    hasGenuineWhitelist: hasGenuineWhitelist
  };
}

function evaluateLoanApp(lenderInput, flags = {}) {
  const input = (lenderInput || "").trim();
  const match = lookupRbiLender(input);
  const isVerified = !!match;

  let score = 0;
  const reasons = [];

  const getFlag = (k) => {
    const cap = k.charAt(0).toUpperCase() + k.slice(1);
    return !!(flags[k] || flags[cap]);
  };

  if (getFlag("contacts")) {
    score += 30;
    reasons.push("Illegal demand for Contacts or Gallery access (Severe extortion risk)");
  }
  if (getFlag("upfront")) {
    score += 25;
    reasons.push("Demands advance fee or deposit before loan disbursal (Advance fee fraud)");
  }
  if (getFlag("hidden")) {
    score += 15;
    reasons.push("Hidden charges, 7-day arbitrary tenure, or missing Key Fact Statement (KFS)");
  }
  if (getFlag("harassment")) {
    score += 30;
    reasons.push("Abusive harassment, morphed photo threats, or family intimidation");
  }
  if (getFlag("noRbi")) {
    score += 20;
    reasons.push("No disclosed RBI-licensed NBFC or Banking partner");
  }
  if (getFlag("unrealistic")) {
    score += 15;
    reasons.push("Unrealistic instant loan approval without credit checks or verification");
  }
  if (getFlag("pressure")) {
    score += 15;
    reasons.push("High-pressure rush tactics to prevent critical verification");
  }
  if (getFlag("apkSource")) {
    score += 25;
    reasons.push("Unverified side-loaded APK outside Google Play Store");
  }

  if (!isVerified && input.length > 0) {
    score += 15;
    reasons.push("Lender / link is not verified in the official RBI Regulated Lenders registry");
  } else if (isVerified && score === 0) {
    score = 0;
  }

  const finalScore = Math.min(100, Math.max(0, score));
  let verdict = "safe";
  if (finalScore >= 50 || getFlag("contacts") || getFlag("harassment") || getFlag("upfront")) {
    verdict = "danger";
  } else if (finalScore >= 20) {
    verdict = "caution";
  } else {
    verdict = "safe";
  }

  if (reasons.length === 0 && isVerified) {
    reasons.push(`Verified RBI-Regulated Institution: ${match.name} (${match.category})`);
  }

  return {
    score: finalScore,
    verdict: verdict,
    reasons: reasons,
    isLenderVerified: isVerified,
    lenderMatch: match
  };
}

module.exports = {
  REAL_WORLD_RBI_LENDERS,
  extractDomain,
  lookupRbiLender,
  evaluateTextSafety,
  evaluateLoanApp
};
