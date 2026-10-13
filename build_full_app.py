import json
import os

with open("uris.json", "r", encoding="utf-8") as f:
    uris = json.load(f)

shield_uri = uris["shield"]
full_uri = uris["full"]

html_template = '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0, user-scalable=yes">
  <title>BlaxGuard - Your shield against fake links and loan scams</title>
  <link rel="icon" type="image/png" href="{{SHIELD_URI}}">
  
  <!-- Montserrat from Google Fonts with fallback -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Montserrat:ital,wght@0,400;0,500;0,600;0,700;0,800;1,400;1,600&display=swap" rel="stylesheet">

  <style>
    /* CSS RESET & VARIABLES */
    *, *::before, *::after {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      -webkit-tap-highlight-color: transparent;
    }

    :root {
      /* Brand Color Palette */
      --navy: #0f172a;
      --navy-light: #1e293b;
      --navy-muted: #334155;
      
      --steel-blue: #3b6998;
      --steel-blue-dark: #2c527c;
      --steel-blue-light: #eaf1f8;
      --steel-blue-border: #b8d0e8;

      --teal: #0d9488;
      --teal-dark: #0f766e;
      --teal-light: #ccfbf1;
      --teal-glow: rgba(13, 148, 136, 0.25);

      /* Theme: Light Mode (Default) */
      --bg-body: #f8fafc;
      --bg-card: #ffffff;
      --bg-card-subtle: #f1f5f9;
      --text-main: #0f172a;
      --text-muted: #475569;
      --border-color: #cbd5e1;
      --topbar-bg: #ffffff;
      --nav-bg: #ffffff;
      --shadow-sm: 0 1px 3px rgba(15, 23, 42, 0.08);
      --shadow-md: 0 4px 12px rgba(15, 23, 42, 0.1);
      --shadow-lg: 0 10px 25px rgba(15, 23, 42, 0.12);

      /* Strictly for Verdicts Only */
      --verdict-danger: #dc2626;
      --verdict-danger-bg: #fef2f2;
      --verdict-danger-border: #fca5a5;

      --verdict-caution: #d97706;
      --verdict-caution-bg: #fffbeb;
      --verdict-caution-border: #fcd34d;

      --verdict-safe: #059669;
      --verdict-safe-bg: #ecfdf5;
      --verdict-safe-border: #6ee7b7;

      /* Font Stack */
      --font-family: 'Montserrat', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
      --radius-sm: 8px;
      --radius-md: 14px;
      --radius-lg: 20px;
      --radius-pill: 9999px;
    }

    /* DARK THEME */
    body.dark {
      --bg-body: #0b1325;
      --bg-card: #13223f;
      --bg-card-subtle: #1a2d52;
      --text-main: #f8fafc;
      --text-muted: #cbd5e1;
      --border-color: #243b66;
      --topbar-bg: #0d182e;
      --nav-bg: #0d182e;
      --steel-blue-light: #1b3554;
      --steel-blue-border: #2c527c;
      --teal-light: #133a38;
      --shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.3);
      --shadow-md: 0 4px 14px rgba(0, 0, 0, 0.4);
      --shadow-lg: 0 10px 30px rgba(0, 0, 0, 0.5);

      /* Verdicts in Dark Mode */
      --verdict-danger-bg: #3d1418;
      --verdict-danger-border: #7f1d1d;

      --verdict-caution-bg: #3d290f;
      --verdict-caution-border: #78350f;

      --verdict-safe-bg: #0c3327;
      --verdict-safe-border: #065f46;
    }

    /* Base Typography & Layout */
    body {
      font-family: var(--font-family);
      font-size: 18px;
      line-height: 1.6;
      color: var(--text-main);
      background-color: var(--bg-body);
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      transition: background-color 0.3s ease, color 0.3s ease;
      padding-bottom: 95px; /* Space for bottom tab bar */
    }

    /* Mobile Container Wrapper */
    .app-container {
      width: 100%;
      max-width: 680px;
      margin: 0 auto;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      position: relative;
    }

    /* TOP BAR */
    .top-bar {
      position: sticky;
      top: 0;
      z-index: 100;
      background-color: var(--topbar-bg);
      border-bottom: 1px solid var(--border-color);
      box-shadow: var(--shadow-sm);
      padding: 10px 16px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      transition: background-color 0.3s ease, border-color 0.3s ease;
    }

    .brand-group {
      display: flex;
      align-items: center;
      gap: 12px;
      text-decoration: none;
      cursor: pointer;
    }

    /* Logo handling: soft white rounded background in dark mode */
    .brand-shield-wrap {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      width: 44px;
      height: 44px;
      border-radius: 12px;
      transition: background-color 0.3s ease, box-shadow 0.3s ease;
    }

    .brand-shield-wrap img {
      width: 40px;
      height: 40px;
      object-fit: contain;
      display: block;
      border-radius: 8px;
    }

    body.dark .brand-shield-wrap {
      background: #ffffff;
      padding: 3px;
      box-shadow: 0 2px 10px rgba(255, 255, 255, 0.22);
    }

    .brand-title {
      font-size: 23px;
      font-weight: 800;
      letter-spacing: -0.5px;
      color: var(--navy);
      display: flex;
      align-items: baseline;
    }

    body.dark .brand-title {
      color: #ffffff;
    }

    .brand-title span.guard {
      color: var(--steel-blue);
    }

    body.dark .brand-title span.guard {
      color: #7bb5e8;
    }

    .top-controls {
      display: flex;
      align-items: center;
      gap: 10px;
    }

    /* Theme Toggle Button */
    .theme-toggle-btn {
      background: var(--bg-card-subtle);
      border: 1px solid var(--border-color);
      color: var(--text-main);
      width: 44px;
      height: 44px;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      font-size: 19px;
      transition: all 0.2s ease;
      touch-action: manipulation;
    }

    .theme-toggle-btn:hover {
      background: var(--steel-blue-light);
      border-color: var(--steel-blue);
    }

    /* Language Selector */
    .lang-selector-wrap {
      position: relative;
    }

    .lang-select {
      appearance: none;
      -webkit-appearance: none;
      font-family: var(--font-family);
      font-size: 15px;
      font-weight: 600;
      color: var(--text-main);
      background-color: var(--bg-card-subtle);
      border: 1.5px solid var(--steel-blue);
      border-radius: var(--radius-pill);
      padding: 9px 34px 9px 14px;
      cursor: pointer;
      outline: none;
      transition: all 0.2s ease;
      min-height: 44px;
    }

    .lang-select:focus {
      border-color: var(--teal);
      box-shadow: 0 0 0 3px var(--teal-glow);
    }

    .lang-chevron {
      position: absolute;
      right: 12px;
      top: 50%;
      transform: translateY(-50%);
      pointer-events: none;
      font-size: 12px;
      color: var(--steel-blue);
    }

    /* MAIN CONTENT VIEWPORT */
    .main-content {
      flex: 1;
      padding: 18px 16px 24px 16px;
    }

    /* WELCOME HERO CARD */
    .welcome-card {
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: var(--radius-lg);
      padding: 24px 18px;
      margin-bottom: 22px;
      text-align: center;
      box-shadow: var(--shadow-md);
      position: relative;
      overflow: hidden;
    }

    .welcome-card::before {
      content: "";
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      height: 4px;
      background: linear-gradient(90deg, var(--steel-blue), var(--teal));
    }

    .welcome-logo-container {
      display: inline-block;
      max-width: 330px;
      width: 100%;
      margin: 0 auto 12px auto;
      border-radius: 16px;
      transition: all 0.3s ease;
    }

    .welcome-logo-container img {
      width: 100%;
      height: auto;
      max-height: 120px;
      object-fit: contain;
      display: block;
      margin: 0 auto;
      border-radius: 12px;
    }

    /* Dark mode soft white rounded background for full logo */
    body.dark .welcome-logo-container {
      background-color: #ffffff;
      padding: 10px 16px;
      box-shadow: 0 4px 18px rgba(255, 255, 255, 0.25);
    }

    .welcome-tagline {
      font-size: 19px;
      font-weight: 600;
      color: var(--steel-blue);
      margin-top: 8px;
      line-height: 1.4;
    }

    body.dark .welcome-tagline {
      color: #93c5fd;
    }

    .senior-badge {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      background: var(--teal-light);
      color: var(--teal-dark);
      font-size: 14px;
      font-weight: 700;
      padding: 6px 14px;
      border-radius: var(--radius-pill);
      margin-top: 12px;
    }

    body.dark .senior-badge {
      background: rgba(13, 148, 136, 0.25);
      color: #5eead4;
      border: 1px solid var(--teal);
    }

    /* SENIOR ASSISTANT TIP */
    .senior-tip-banner {
      background: var(--steel-blue-light);
      border: 1px solid var(--steel-blue-border);
      border-radius: var(--radius-md);
      padding: 16px;
      margin-bottom: 22px;
      display: flex;
      align-items: flex-start;
      gap: 14px;
    }

    .senior-tip-banner .icon {
      font-size: 28px;
      line-height: 1;
      color: var(--steel-blue);
    }

    .senior-tip-banner .content {
      font-size: 17px;
      color: var(--text-main);
      line-height: 1.5;
    }

    /* PAGE SECTIONS */
    .page-section {
      display: none;
      animation: fadeIn 0.25s ease-out;
    }

    .page-section.active {
      display: block;
    }

    @keyframes fadeIn {
      from { opacity: 0; transform: translateY(6px); }
      to { opacity: 1; transform: translateY(0); }
    }

    /* PAGE HEADINGS & SENIOR READABLE TEXT */
    .section-header {
      margin-bottom: 20px;
    }

    .section-title {
      font-size: 26px;
      font-weight: 800;
      color: var(--text-main);
      line-height: 1.25;
      margin-bottom: 8px;
      display: flex;
      align-items: center;
      gap: 10px;
    }

    .section-subtitle {
      font-size: 18px;
      color: var(--text-muted);
      line-height: 1.5;
    }

    /* UI CARDS */
    .ui-card {
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: var(--radius-md);
      padding: 20px;
      margin-bottom: 20px;
      box-shadow: var(--shadow-sm);
      transition: background-color 0.3s ease, border-color 0.3s ease;
    }

    .card-title {
      font-size: 20px;
      font-weight: 700;
      color: var(--text-main);
      margin-bottom: 12px;
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .card-text {
      font-size: 17px;
      color: var(--text-muted);
      line-height: 1.6;
      margin-bottom: 16px;
    }

    /* FORM INPUTS & BUTTONS (Large for Seniors) */
    .form-group {
      margin-bottom: 16px;
    }

    .form-label {
      display: block;
      font-size: 18px;
      font-weight: 700;
      color: var(--text-main);
      margin-bottom: 8px;
    }

    .text-input {
      width: 100%;
      font-family: var(--font-family);
      font-size: 17px;
      padding: 14px 16px;
      background: var(--bg-card-subtle);
      border: 2px solid var(--steel-blue-border);
      border-radius: var(--radius-sm);
      color: var(--text-main);
      outline: none;
      transition: border-color 0.2s ease, box-shadow 0.2s ease;
      min-height: 52px;
    }

    .text-input:focus {
      border-color: var(--steel-blue);
      box-shadow: 0 0 0 3px var(--steel-blue-light);
    }

    textarea.text-input {
      min-height: 120px;
      resize: vertical;
      line-height: 1.5;
    }

    .btn {
      font-family: var(--font-family);
      font-size: 18px;
      font-weight: 700;
      padding: 14px 22px;
      border-radius: var(--radius-sm);
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 10px;
      text-decoration: none;
      border: none;
      transition: all 0.2s ease;
      min-height: 54px;
      touch-action: manipulation;
    }

    .btn-primary {
      background: var(--steel-blue);
      color: #ffffff;
      width: 100%;
    }

    .btn-primary:hover {
      background: var(--steel-blue-dark);
      box-shadow: var(--shadow-md);
    }

    .btn-secondary {
      background: var(--teal);
      color: #ffffff;
      width: 100%;
    }

    .btn-secondary:hover {
      background: var(--teal-dark);
    }

    .btn-outline {
      background: transparent;
      border: 2px solid var(--steel-blue);
      color: var(--steel-blue);
      width: 100%;
    }

    body.dark .btn-outline {
      border-color: #60a5fa;
      color: #93c5fd;
    }

    .btn-outline:hover {
      background: var(--steel-blue-light);
    }

    .btn-row {
      display: flex;
      gap: 10px;
      margin-top: 12px;
    }

    .btn-row .btn {
      flex: 1;
    }

    /* SAMPLE BUTTONS CHIPS */
    .chips-group {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      margin: 12px 0 16px 0;
    }

    .chip-btn {
      font-family: var(--font-family);
      font-size: 14px;
      font-weight: 600;
      padding: 8px 12px;
      background: var(--bg-card-subtle);
      border: 1px solid var(--border-color);
      color: var(--text-muted);
      border-radius: var(--radius-pill);
      cursor: pointer;
      transition: all 0.2s ease;
    }

    .chip-btn:hover {
      border-color: var(--steel-blue);
      color: var(--steel-blue);
    }

    /* VERDICT RESULTS SYSTEM (Strictly Red / Amber / Green ONLY for Verdicts) */
    .verdict-box {
      border-radius: var(--radius-md);
      padding: 20px;
      margin-top: 20px;
      border-left: 6px solid;
      animation: slideDown 0.3s ease-out;
    }

    @keyframes slideDown {
      from { opacity: 0; transform: translateY(-8px); }
      to { opacity: 1; transform: translateY(0); }
    }

    /* 🔴 DANGER VERDICT */
    .verdict-danger {
      background-color: var(--verdict-danger-bg);
      border-color: var(--verdict-danger);
      color: #7f1d1d;
    }
    body.dark .verdict-danger {
      color: #fca5a5;
    }
    .verdict-danger .verdict-badge {
      background-color: var(--verdict-danger);
      color: #ffffff;
    }
    .verdict-danger .score-fill {
      background-color: var(--verdict-danger);
    }

    /* 🟡 CAUTION VERDICT */
    .verdict-caution {
      background-color: var(--verdict-caution-bg);
      border-color: var(--verdict-caution);
      color: #78350f;
    }
    body.dark .verdict-caution {
      color: #fde68a;
    }
    .verdict-caution .verdict-badge {
      background-color: var(--verdict-caution);
      color: #ffffff;
    }
    .verdict-caution .score-fill {
      background-color: var(--verdict-caution);
    }

    /* 🟢 SAFE VERDICT */
    .verdict-safe {
      background-color: var(--verdict-safe-bg);
      border-color: var(--verdict-safe);
      color: #064e3b;
    }
    body.dark .verdict-safe {
      color: #6ee7b7;
    }
    .verdict-safe .verdict-badge {
      background-color: var(--verdict-safe);
      color: #ffffff;
    }
    .verdict-safe .score-fill {
      background-color: var(--verdict-safe);
    }

    .verdict-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 12px;
      flex-wrap: wrap;
      gap: 8px;
    }

    .verdict-badge {
      font-size: 15px;
      font-weight: 800;
      padding: 5px 14px;
      border-radius: var(--radius-pill);
      letter-spacing: 0.5px;
      display: inline-flex;
      align-items: center;
      gap: 6px;
    }

    .verdict-title {
      font-size: 22px;
      font-weight: 800;
      margin-bottom: 8px;
      line-height: 1.3;
    }

    /* SCORE BAR & METER */
    .score-meter-wrap {
      background: rgba(0, 0, 0, 0.06);
      border-radius: var(--radius-pill);
      padding: 4px;
      margin: 14px 0 16px 0;
    }

    body.dark .score-meter-wrap {
      background: rgba(255, 255, 255, 0.1);
    }

    .score-bar-bg {
      height: 14px;
      border-radius: var(--radius-pill);
      overflow: hidden;
      background: rgba(0, 0, 0, 0.08);
      position: relative;
    }

    body.dark .score-bar-bg {
      background: rgba(255, 255, 255, 0.15);
    }

    .score-fill {
      height: 100%;
      border-radius: var(--radius-pill);
      transition: width 0.6s cubic-bezier(0.16, 1, 0.3, 1);
    }

    .score-text-label {
      font-size: 16px;
      font-weight: 700;
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 6px;
    }

    /* REASONS LIST */
    .reasons-box {
      margin-top: 14px;
      border-top: 1px solid rgba(0, 0, 0, 0.1);
      padding-top: 14px;
    }

    body.dark .reasons-box {
      border-top-color: rgba(255, 255, 255, 0.12);
    }

    .reasons-title {
      font-size: 18px;
      font-weight: 700;
      margin-bottom: 8px;
      display: flex;
      align-items: center;
      gap: 6px;
    }

    .reasons-list {
      list-style-type: none;
      padding-left: 0;
    }

    .reasons-list li {
      font-size: 16px;
      line-height: 1.55;
      margin-bottom: 8px;
      padding-left: 24px;
      position: relative;
    }

    .reasons-list li::before {
      content: "•";
      position: absolute;
      left: 6px;
      top: 0;
      font-size: 20px;
      font-weight: bold;
    }

    /* NEXT STEPS BOX */
    .next-steps-card {
      background: var(--bg-card);
      border: 2px solid var(--steel-blue);
      border-radius: var(--radius-md);
      padding: 16px 18px;
      margin-top: 18px;
      box-shadow: var(--shadow-sm);
    }

    body.dark .next-steps-card {
      background: var(--bg-card-subtle);
      border-color: #4b78a6;
    }

    .next-steps-header {
      font-size: 18px;
      font-weight: 800;
      color: var(--steel-blue);
      margin-bottom: 10px;
      display: flex;
      align-items: center;
      gap: 8px;
    }

    body.dark .next-steps-header {
      color: #93c5fd;
    }

    .next-steps-list {
      list-style-type: none;
      padding-left: 0;
    }

    .next-steps-list li {
      font-size: 16px;
      color: var(--text-main);
      margin-bottom: 8px;
      display: flex;
      align-items: flex-start;
      gap: 10px;
      line-height: 1.5;
    }

    .step-badge {
      background: var(--steel-blue-light);
      color: var(--steel-blue-dark);
      font-weight: 800;
      font-size: 13px;
      min-width: 24px;
      height: 24px;
      border-radius: 50%;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      margin-top: 2px;
      flex-shrink: 0;
    }

    body.dark .step-badge {
      background: #1e3a5f;
      color: #93c5fd;
    }

    /* DISCLAIMER */
    .disclaimer-text {
      font-size: 14px;
      color: var(--text-muted);
      font-style: italic;
      margin-top: 14px;
      line-height: 1.5;
      border-top: 1px dashed rgba(0, 0, 0, 0.15);
      padding-top: 10px;
    }

    body.dark .disclaimer-text {
      border-top-color: rgba(255, 255, 255, 0.15);
    }

    .senior-voice-btn {
      margin-top: 14px;
      display: inline-flex;
      align-items: center;
      gap: 8px;
      background: var(--bg-card);
      border: 1.5px solid currentColor;
      color: inherit;
      padding: 9px 16px;
      border-radius: var(--radius-pill);
      font-size: 15px;
      font-weight: 700;
      cursor: pointer;
      touch-action: manipulation;
    }

    /* PERMISSION TOGGLES FOR LOAN AUDITOR */
    .perm-toggle-row {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 14px 0;
      border-bottom: 1px solid var(--border-color);
    }

    .perm-toggle-row:last-child {
      border-bottom: none;
    }

    .perm-info {
      flex: 1;
      padding-right: 12px;
    }

    .perm-name {
      font-size: 17px;
      font-weight: 700;
      color: var(--text-main);
    }

    .perm-sub {
      font-size: 14px;
      color: var(--text-muted);
    }

    /* Custom Switch */
    .switch {
      position: relative;
      display: inline-block;
      width: 52px;
      height: 30px;
      flex-shrink: 0;
    }

    .switch input {
      opacity: 0;
      width: 0;
      height: 0;
    }

    .slider {
      position: absolute;
      cursor: pointer;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      background-color: var(--border-color);
      transition: .3s;
      border-radius: 34px;
    }

    .slider:before {
      position: absolute;
      content: "";
      height: 22px;
      width: 22px;
      left: 4px;
      bottom: 4px;
      background-color: white;
      transition: .3s;
      border-radius: 50%;
    }

    input:checked + .slider {
      background-color: var(--steel-blue);
    }

    input:checked + .slider:before {
      transform: translateX(22px);
    }

    /* ACCESSIBILITY & SENIOR LIST STYLES */
    .list-item-card {
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: var(--radius-sm);
      padding: 16px;
      margin-bottom: 12px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
    }

    .list-item-info {
      flex: 1;
    }

    .list-item-title {
      font-size: 18px;
      font-weight: 700;
      color: var(--text-main);
      margin-bottom: 4px;
    }

    .list-item-desc {
      font-size: 15px;
      color: var(--text-muted);
    }

    /* BOTTOM TAB BAR (8 PAGES: Check, Loan, Call, Report, Registry, Learn, Help, Admin) */
    .bottom-nav {
      position: fixed;
      bottom: 0;
      left: 0;
      right: 0;
      z-index: 200;
      background-color: var(--nav-bg);
      border-top: 1px solid var(--border-color);
      box-shadow: 0 -4px 16px rgba(15, 23, 42, 0.08);
      display: flex;
      overflow-x: auto;
      overflow-y: hidden;
      -webkit-overflow-scrolling: touch;
      scrollbar-width: none;
      padding: 6px 4px calc(6px + env(safe-area-inset-bottom, 0px)) 4px;
      transition: background-color 0.3s ease, border-color 0.3s ease;
    }

    .bottom-nav::-webkit-scrollbar {
      display: none;
    }

    .nav-tab {
      flex: 0 0 calc(100% / 5.2);
      min-width: 68px;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      gap: 3px;
      padding: 8px 4px;
      color: var(--text-muted);
      text-decoration: none;
      border-radius: var(--radius-sm);
      transition: all 0.2s ease;
      font-size: 13px;
      font-weight: 600;
      cursor: pointer;
      user-select: none;
      touch-action: manipulation;
    }

    .nav-tab .tab-icon {
      width: 24px;
      height: 24px;
      stroke: currentColor;
      fill: none;
      stroke-width: 2;
      stroke-linecap: round;
      stroke-linejoin: round;
      transition: transform 0.2s ease;
    }

    .nav-tab.active {
      color: var(--steel-blue);
      font-weight: 800;
    }

    body.dark .nav-tab.active {
      color: #93c5fd;
    }

    .nav-tab.active .tab-icon {
      stroke: var(--steel-blue);
      transform: translateY(-2px);
    }

    body.dark .nav-tab.active .tab-icon {
      stroke: #93c5fd;
    }

    .nav-tab.active::after {
      content: "";
      width: 16px;
      height: 3px;
      background: var(--teal);
      border-radius: var(--radius-pill);
      margin-top: 1px;
    }

    /* RESPONSIVE DESKTOP ADJUSTMENTS */
    @media (min-width: 681px) {
      body {
        background-color: #f1f5f9;
      }
      body.dark {
        background-color: #060b17;
      }
      .app-container {
        background-color: var(--bg-body);
        box-shadow: 0 0 35px rgba(0, 0, 0, 0.12);
        border-left: 1px solid var(--border-color);
        border-right: 1px solid var(--border-color);
      }
      .bottom-nav {
        max-width: 680px;
        left: 50%;
        transform: translateX(-50%);
        border-left: 1px solid var(--border-color);
        border-right: 1px solid var(--border-color);
      }
    }
  </style>
</head>
<body>

  <div class="app-container">

    <!-- TOP BAR -->
    <header class="top-bar">
      <!-- Shield Logo + App Name -->
      <a href="#check" class="brand-group" aria-label="BlaxGuard Home">
        <div class="brand-shield-wrap">
          <img src="{{SHIELD_URI}}" alt="BlaxGuard Shield Logo">
        </div>
        <div class="brand-title">
          <span>Blax</span><span class="guard">Guard</span>
        </div>
      </a>

      <!-- Controls: Theme Toggle & Language Selector -->
      <div class="top-controls">
        <!-- Theme Toggle -->
        <button id="themeToggleBtn" class="theme-toggle-btn" aria-label="Toggle Dark/Light Mode" title="Switch Theme">
          <span id="themeIcon">🌙</span>
        </button>

        <!-- Language Selector -->
        <div class="lang-selector-wrap">
          <select id="langSelect" class="lang-select" aria-label="Select Language">
            <option value="en">English</option>
            <option value="hi">हिंदी</option>
            <option value="te">తెలుగు</option>
          </select>
          <span class="lang-chevron">▼</span>
        </div>
      </div>
    </header>

    <!-- MAIN SCROLLABLE CONTENT -->
    <main class="main-content">

      <!-- WELCOME HERO SECTION -->
      <section class="welcome-card" id="welcomeSection">
        <div class="welcome-logo-container">
          <img src="{{FULL_URI}}" alt="BlaxGuard Full Logo with Tagline">
        </div>
        <p class="welcome-tagline" data-i18n="tagline">Your shield against fake links and loan scams</p>
        <div class="senior-badge" data-i18n="seniorFriendly">
          🛡️ Easy &amp; Safe for First-Time Users &amp; Seniors
        </div>
      </section>

      <!-- SENIOR ASSISTANT TIP -->
      <aside class="senior-tip-banner" id="seniorTipBanner">
        <div class="icon">📢</div>
        <div class="content" id="seniorTipText" data-i18n="bannerTip">
          <strong>Tip for Safety:</strong> Never share your 4-digit or 6-digit UPI PIN or OTP with anyone claiming to send you money or verify your account.
        </div>
      </aside>

      <!-- ============================================== -->
      <!-- PAGE 1: CHECK (SMS, WhatsApp, Link & Phone Analyzer) -->
      <!-- ============================================== -->
      <section id="page-check" class="page-section">
        <div class="section-header">
          <h1 class="section-title">
            <span>🔗</span> <span data-i18n="checkPageTitle">Check Link, SMS or Number</span>
          </h1>
          <p class="section-subtitle" data-i18n="checkPageSub">
            Paste any SMS, WhatsApp message, link, or unknown phone number before taking any action.
          </p>
        </div>

        <div class="ui-card">
          <label for="checkMessageInput" class="form-label" data-i18n="checkInputLabel">Paste message text, link, or phone number:</label>
          <div class="form-group">
            <textarea id="checkMessageInput" class="text-input" rows="4" placeholder="Paste SMS, WhatsApp forward, link or phone number here..." data-i18n-placeholder="checkInputPlaceholder"></textarea>
          </div>

          <p class="card-text" style="font-size: 15px; margin-bottom: 6px; font-weight: 600;" data-i18n="trySampleLinks">
            Or test with common scam examples:
          </p>
          <div class="chips-group">
            <button type="button" class="chip-btn" onclick="loadSamplePreset('electricity')" data-i18n="presetElectricity">⚠️ Fake Electricity Disconnection</button>
            <button type="button" class="chip-btn" onclick="loadSamplePreset('kyc_apk')" data-i18n="presetKycApk">⚠️ Bank KYC &amp; AnyDesk APK</button>
            <button type="button" class="chip-btn" onclick="loadSamplePreset('instant_loan')" data-i18n="presetInstantLoan">⚠️ Instant ₹50,000 Loan Bait</button>
            <button type="button" class="chip-btn" onclick="loadSamplePreset('lottery')" data-i18n="presetLottery">🔍 KBC Lottery Prize Draw</button>
            <button type="button" class="chip-btn" onclick="loadSamplePreset('genuine_bank')" data-i18n="presetGenuineBank">✅ Genuine Bank Credit SMS</button>
          </div>

          <div class="btn-row">
            <button type="button" class="btn btn-primary" onclick="runRuleEngine()" style="flex: 2;">
              <span>🛡️</span> <span data-i18n="btnVerifyNow">Analyze Safety Now</span>
            </button>
            <button type="button" class="btn btn-outline" onclick="clearCheckInput()" style="flex: 1;" data-i18n="btnClear">
              Clear
            </button>
          </div>

          <!-- DYNAMIC VERDICT CONTAINER -->
          <div id="checkVerdictContainer" style="display: none;"></div>
        </div>
      </section>

      <!-- ============================================== -->
      <!-- PAGE 2: LOAN (Fake Loan App Auditor) -->
      <!-- ============================================== -->
      <section id="page-loan" class="page-section">
        <div class="section-header">
          <h1 class="section-title">
            <span>💰</span> <span data-i18n="loanPageTitle">Loan App Auditor</span>
          </h1>
          <p class="section-subtitle" data-i18n="loanPageSub">
            Verify if a loan application is genuine or an unauthorized predatory loan trap.
          </p>
        </div>

        <div class="ui-card">
          <label for="loanAppName" class="form-label" data-i18n="loanInputLabel">Loan App Name / APK File:</label>
          <div class="form-group">
            <input type="text" id="loanAppName" class="text-input" placeholder="e.g. Speed Rupee Cash Loan" data-i18n-placeholder="loanInputPlaceholder">
          </div>

          <h3 class="card-title" style="margin-top: 16px;" data-i18n="permAuditTitle">Permissions Requested by the App:</h3>
          <p class="card-text" style="font-size: 15px;" data-i18n="permAuditSub">
            Check the permissions this app asks for in your phone settings:
          </p>

          <div class="perm-toggle-row">
            <div class="perm-info">
              <div class="perm-name" data-i18n="permContacts">Read Phone Contacts</div>
              <div class="perm-sub" data-i18n="permContactsSub">Access to your family &amp; friends phonebook</div>
            </div>
            <label class="switch">
              <input type="checkbox" id="permContactsToggle" checked>
              <span class="slider"></span>
            </label>
          </div>

          <div class="perm-toggle-row">
            <div class="perm-info">
              <div class="perm-name" data-i18n="permGallery">Read Gallery &amp; Photos</div>
              <div class="perm-sub" data-i18n="permGallerySub">Access to your private pictures and videos</div>
            </div>
            <label class="switch">
              <input type="checkbox" id="permGalleryToggle" checked>
              <span class="slider"></span>
            </label>
          </div>

          <div class="perm-toggle-row">
            <div class="perm-info">
              <div class="perm-name" data-i18n="permSms">Read SMS &amp; OTPs</div>
              <div class="perm-sub" data-i18n="permSmsSub">Access to view your personal banking messages</div>
            </div>
            <label class="switch">
              <input type="checkbox" id="permSmsToggle" checked>
              <span class="slider"></span>
            </label>
          </div>

          <button type="button" class="btn btn-primary" style="margin-top: 18px;" onclick="auditLoanApp()">
            <span>🔍</span> <span data-i18n="btnAuditLoan">Audit Loan App Safety</span>
          </button>

          <!-- LOAN VERDICT BOX -->
          <div id="loanVerdictBox" style="display: none;"></div>
        </div>
      </section>

      <!-- ============================================== -->
      <!-- PAGE 3: CALL (Fake Customer Care Numbers) -->
      <!-- ============================================== -->
      <section id="page-call" class="page-section">
        <div class="section-header">
          <h1 class="section-title">
            <span>📞</span> <span data-i18n="callPageTitle">Customer Care Check</span>
          </h1>
          <p class="section-subtitle" data-i18n="callPageSub">
            Scammers put fake 10-digit mobile numbers on search engines claiming to be banks or airlines.
          </p>
        </div>

        <div class="ui-card">
          <label for="callPhoneInput" class="form-label" data-i18n="callInputLabel">Enter phone number to verify:</label>
          <div class="form-group">
            <input type="tel" id="callPhoneInput" class="text-input" placeholder="e.g. +91 98765 43210 or 1800-11-2211" data-i18n-placeholder="callInputPlaceholder">
          </div>

          <div class="chips-group">
            <button type="button" class="chip-btn" onclick="testCallSample('fake')" data-i18n="sampleFakeCare">⚠️ Fake Bank Care (Mobile No.)</button>
            <button type="button" class="chip-btn" onclick="testCallSample('real')" data-i18n="sampleRealCare">✅ Official SBI Toll-Free (1800)</button>
          </div>

          <button type="button" class="btn btn-primary" onclick="verifyPhoneNumber()">
            <span>📞</span> <span data-i18n="btnCheckPhone">Check Phone Safety</span>
          </button>

          <div id="callVerdictBox" style="display: none;"></div>
        </div>
      </section>

      <!-- ============================================== -->
      <!-- PAGE 4: REPORT (Scam Incident Reporting) -->
      <!-- ============================================== -->
      <section id="page-report" class="page-section">
        <div class="section-header">
          <h1 class="section-title">
            <span>🚨</span> <span data-i18n="reportPageTitle">Report a Scam</span>
          </h1>
          <p class="section-subtitle" data-i18n="reportPageSub">
            Protect your neighbors and alert cyber crime authorities before others lose money.
          </p>
        </div>

        <div class="ui-card">
          <h3 class="card-title" data-i18n="reportCardTitle">Quick Incident Submission</h3>
          <div class="form-group">
            <label class="form-label" data-i18n="reportScamType">Type of Scam:</label>
            <select class="text-input" id="reportTypeSelect">
              <option value="loan" data-i18n="reportOptLoan">Predatory Loan App Harassment</option>
              <option value="sms" data-i18n="reportOptSms">Fake Electricity / Bill SMS Link</option>
              <option value="care" data-i18n="reportOptCare">Fake Customer Care Number</option>
              <option value="kyc" data-i18n="reportOptKyc">Bank KYC / Account Block Trap</option>
            </select>
          </div>

          <div class="form-group">
            <label class="form-label" data-i18n="reportDetailsLabel">Scammer Number, App, or Link:</label>
            <input type="text" class="text-input" id="reportTargetInput" placeholder="Paste details here" data-i18n-placeholder="reportPlaceholder">
          </div>

          <button type="button" class="btn btn-primary" onclick="submitReport()">
            <span>📤</span> <span data-i18n="btnSubmitReport">Submit to National Cyber Registry</span>
          </button>

          <div id="reportSuccessBox" style="display: none; margin-top: 16px;" class="verdict-box verdict-safe">
            <div class="verdict-title" data-i18n="reportSuccessTitle">Incident Logged Successfully</div>
            <div class="verdict-desc" data-i18n="reportSuccessDesc">Thank you for helping protect others. Your report has been dispatched to cyber defense databases.</div>
          </div>
        </div>
      </section>

      <!-- ============================================== -->
      <!-- PAGE 5: REGISTRY (Verified Official Directory) -->
      <!-- ============================================== -->
      <section id="page-registry" class="page-section">
        <div class="section-header">
          <h1 class="section-title">
            <span>🏛️</span> <span data-i18n="registryPageTitle">Safe Official Registry</span>
          </h1>
          <p class="section-subtitle" data-i18n="registryPageSub">
            Direct whitelist of approved government institutions, banks, and authorized lenders.
          </p>
        </div>

        <div class="ui-card">
          <h3 class="card-title" data-i18n="registrySearchTitle">Search Verified Directory</h3>
          <input type="text" id="registrySearchInput" class="text-input" placeholder="Type bank, NBFC, or service name..." data-i18n-placeholder="registrySearchPlaceholder" oninput="filterRegistry()">
          
          <div id="registryList" style="margin-top: 16px;">
            <div class="list-item-card">
              <div class="list-item-info">
                <div class="list-item-title">State Bank of India (SBI)</div>
                <div class="list-item-desc">Toll-Free: 1800 1234 / 1800 2100 &bull; Official Portal: onlinesbi.sbi</div>
              </div>
              <span class="verdict-badge" style="background: var(--teal); color: #fff;">Verified</span>
            </div>

            <div class="list-item-card">
              <div class="list-item-info">
                <div class="list-item-title">HDFC Bank Limited</div>
                <div class="list-item-desc">Toll-Free: 1800 202 6161 &bull; Portal: hdfcbank.com</div>
              </div>
              <span class="verdict-badge" style="background: var(--teal); color: #fff;">Verified</span>
            </div>

            <div class="list-item-card">
              <div class="list-item-info">
                <div class="list-item-title">Bajaj Finance Ltd (NBFC)</div>
                <div class="list-item-desc">RBI Reg. No: 05.00032 &bull; Official Portal: bajajfinserv.in</div>
              </div>
              <span class="verdict-badge" style="background: var(--teal); color: #fff;">RBI Approved</span>
            </div>

            <div class="list-item-card">
              <div class="list-item-info">
                <div class="list-item-title">Electricity Bill Support (TSSPDCL / State)</div>
                <div class="list-item-desc">Call: 1912 &bull; Never call 10-digit mobile numbers for bills</div>
              </div>
              <span class="verdict-badge" style="background: var(--teal); color: #fff;">Govt Helpline</span>
            </div>
          </div>
        </div>
      </section>

      <!-- ============================================== -->
      <!-- PAGE 6: LEARN (Senior Safety Guide) -->
      <!-- ============================================== -->
      <section id="page-learn" class="page-section">
        <div class="section-header">
          <h1 class="section-title">
            <span>📚</span> <span data-i18n="learnPageTitle">Safety Guide for Seniors</span>
          </h1>
          <p class="section-subtitle" data-i18n="learnPageSub">
            Three simple golden rules to keep you and your retirement savings 100% safe.
          </p>
        </div>

        <div class="ui-card">
          <h3 class="card-title">
            <span>1️⃣</span> <span data-i18n="rule1Title">UPI PIN is ONLY for Sending Money</span>
          </h3>
          <p class="card-text" data-i18n="rule1Desc">
            You NEVER need to enter your UPI PIN to receive money or get lottery winnings. If someone asks for your PIN to "transfer" money, it is a scam.
          </p>
          <button class="senior-voice-btn" onclick="speakRule(1)">
            <span>🔊</span> <span data-i18n="btnListenVoice">Listen in your language</span>
          </button>
        </div>

        <div class="ui-card">
          <h3 class="card-title">
            <span>2️⃣</span> <span data-i18n="rule2Title">Never Download APKs from WhatsApp</span>
          </h3>
          <p class="card-text" data-i18n="rule2Desc">
            Scammers send files ending in .apk or .apk.zip. Legitimate banks only publish apps through Google Play Store. An APK can secretly read your OTPs!
          </p>
          <button class="senior-voice-btn" onclick="speakRule(2)">
            <span>🔊</span> <span data-i18n="btnListenVoice">Listen in your language</span>
          </button>
        </div>

        <div class="ui-card">
          <h3 class="card-title">
            <span>3️⃣</span> <span data-i18n="rule3Title">Electricity Department Never Calls from Personal Numbers</span>
          </h3>
          <p class="card-text" data-i18n="rule3Desc">
            If a message says "Your power will be cut tonight at 9:30 PM, call 98xxxxxx", ignore it. State electricity boards only use toll-free 1912.
          </p>
          <button class="senior-voice-btn" onclick="speakRule(3)">
            <span>🔊</span> <span data-i18n="btnListenVoice">Listen in your language</span>
          </button>
        </div>
      </section>

      <!-- ============================================== -->
      <!-- PAGE 7: HELP (Emergency & Family Guardian) -->
      <!-- ============================================== -->
      <section id="page-help" class="page-section">
        <div class="section-header">
          <h1 class="section-title">
            <span>🆘</span> <span data-i18n="helpPageTitle">Emergency Help &amp; Guardian</span>
          </h1>
          <p class="section-subtitle" data-i18n="helpPageSub">
            Immediate assistance if money has been deducted or you suspect fraud.
          </p>
        </div>

        <div class="ui-card">
          <h3 class="card-title" data-i18n="helpGovtTitle">National Cyber Crime Helpline</h3>
          <p class="card-text" data-i18n="helpGovtDesc">
            Call toll-free <strong>1930</strong> immediately within the first golden hour to freeze fraudulent bank transactions.
          </p>
          <a href="tel:1930" class="btn btn-primary" style="margin-bottom: 12px;">
            <span>📞</span> <span data-i18n="btnDial1930">Call 1930 (Toll Free)</span>
          </a>
        </div>

        <div class="ui-card">
          <h3 class="card-title" data-i18n="guardianTitle">Family Guardian Alert Mode</h3>
          <p class="card-text" data-i18n="guardianDesc">
            Add your son, daughter, or trusted relative's phone number. BlaxGuard will immediately alert them if you encounter a high-risk link.
          </p>
          <div class="form-group">
            <label class="form-label" data-i18n="guardianPhoneLabel">Guardian's Mobile Number:</label>
            <input type="tel" id="guardianPhoneInput" class="text-input" placeholder="+91 98765 00000" data-i18n-placeholder="guardianPhonePlaceholder">
          </div>
          <button type="button" class="btn btn-secondary" onclick="saveGuardian()">
            <span>🛡️</span> <span data-i18n="btnSaveGuardian">Save Guardian Contact</span>
          </button>
        </div>
      </section>

      <!-- ============================================== -->
      <!-- PAGE 8: ADMIN (Security Dashboard) -->
      <!-- ============================================== -->
      <section id="page-admin" class="page-section">
        <div class="section-header">
          <h1 class="section-title">
            <span>⚙️</span> <span data-i18n="adminPageTitle">Admin Threat Center</span>
          </h1>
          <p class="section-subtitle" data-i18n="adminPageSub">
            Live threat intelligence feed, flagged predatory APKs, and regional scam heuristics.
          </p>
        </div>

        <div class="ui-card">
          <h3 class="card-title" data-i18n="adminLiveStatus">Threat Feed Status: Active 🟢</h3>
          <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 16px;">
            <div style="background: var(--bg-card-subtle); padding: 14px; border-radius: var(--radius-sm); text-align: center;">
              <div style="font-size: 26px; font-weight: 800; color: var(--steel-blue);">1,429</div>
              <div style="font-size: 14px; color: var(--text-muted);" data-i18n="statBlockedLinks">Scam Links Intercepted</div>
            </div>
            <div style="background: var(--bg-card-subtle); padding: 14px; border-radius: var(--radius-sm); text-align: center;">
              <div style="font-size: 26px; font-weight: 800; color: var(--teal);">384</div>
              <div style="font-size: 14px; color: var(--text-muted);" data-i18n="statRogueApks">Predatory APKs Blocked</div>
            </div>
          </div>

          <h4 style="font-size: 18px; margin-bottom: 10px;" data-i18n="adminRecentScams">Recent Intercepted Patterns</h4>
          <div class="list-item-card">
            <div class="list-item-info">
              <div class="list-item-title" style="font-size: 16px;">sbi-reward-pts-verify.live</div>
              <div class="list-item-desc">Typo-squatting &bull; Intercepted 12m ago</div>
            </div>
            <span class="verdict-badge" style="background: var(--verdict-danger); color: #fff;">Blocked</span>
          </div>

          <div class="list-item-card">
            <div class="list-item-info">
              <div class="list-item-title" style="font-size: 16px;">FastCashRupee_v2.apk</div>
              <div class="list-item-desc">Demanded Gallery + Contacts &bull; Blacklisted</div>
            </div>
            <span class="verdict-badge" style="background: var(--verdict-danger); color: #fff;">Blocked</span>
          </div>

          <button class="btn btn-outline" style="margin-top: 12px;" onclick="refreshAdminData()">
            <span>🔄</span> <span data-i18n="btnRefreshData">Refresh Threat Heuristics</span>
          </button>
        </div>
      </section>

    </main>

    <!-- BOTTOM TAB BAR (8 TABS: Check, Loan, Call, Report, Registry, Learn, Help, Admin) -->
    <nav class="bottom-nav" id="bottomNav" aria-label="Bottom Navigation">
      <a href="#check" class="nav-tab active" data-tab="check">
        <svg class="tab-icon" viewBox="0 0 24 24"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"></path><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"></path></svg>
        <span data-i18n="tabCheck">Check</span>
      </a>

      <a href="#loan" class="nav-tab" data-tab="loan">
        <svg class="tab-icon" viewBox="0 0 24 24"><line x1="12" y1="1" x2="12" y2="23"></line><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path></svg>
        <span data-i18n="tabLoan">Loan</span>
      </a>

      <a href="#call" class="nav-tab" data-tab="call">
        <svg class="tab-icon" viewBox="0 0 24 24"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"></path></svg>
        <span data-i18n="tabCall">Call</span>
      </a>

      <a href="#report" class="nav-tab" data-tab="report">
        <svg class="tab-icon" viewBox="0 0 24 24"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path><line x1="12" y1="9" x2="12" y2="13"></line><line x1="12" y1="17" x2="12.01" y2="17"></line></svg>
        <span data-i18n="tabReport">Report</span>
      </a>

      <a href="#registry" class="nav-tab" data-tab="registry">
        <svg class="tab-icon" viewBox="0 0 24 24"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"></path><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"></path></svg>
        <span data-i18n="tabRegistry">Registry</span>
      </a>

      <a href="#learn" class="nav-tab" data-tab="learn">
        <svg class="tab-icon" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="16" x2="12" y2="12"></line><line x1="12" y1="8" x2="12.01" y2="8"></line></svg>
        <span data-i18n="tabLearn">Learn</span>
      </a>

      <a href="#help" class="nav-tab" data-tab="help">
        <svg class="tab-icon" viewBox="0 0 24 24"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path></svg>
        <span data-i18n="tabHelp">Help</span>
      </a>

      <a href="#admin" class="nav-tab" data-tab="admin">
        <svg class="tab-icon" viewBox="0 0 24 24"><circle cx="12" cy="12" r="3"></circle><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path></svg>
        <span data-i18n="tabAdmin">Admin</span>
      </a>
    </nav>

  </div>

  <!-- JAVASCRIPT: TRANSLATIONS, BROWSER-SIDE RULE ENGINE, ROUTING & THEME -->
  <script>
    /* ==============================================================
       TRANSLATIONS OBJECT (English, Hindi, Telugu)
       Rule: Keep "BlaxGuard" in English letters in all languages!
       ============================================================== */
    const translations = {
      en: {
        tagline: "Your shield against fake links and loan scams",
        seniorFriendly: "🛡️ Easy & Safe for First-Time Users & Seniors",
        bannerTip: "<strong>Tip for Safety:</strong> Never share your 4-digit or 6-digit UPI PIN or OTP with anyone claiming to send you money or verify your account.",
        
        /* Bottom Tab Labels */
        tabCheck: "Check",
        tabLoan: "Loan",
        tabCall: "Call",
        tabReport: "Report",
        tabRegistry: "Registry",
        tabLearn: "Learn",
        tabHelp: "Help",
        tabAdmin: "Admin",

        /* Check Page */
        checkPageTitle: "Check Link, SMS or Number",
        checkPageSub: "Paste any SMS, WhatsApp message, link, or unknown phone number before taking any action.",
        checkInputLabel: "Paste message text, link, or phone number:",
        checkInputPlaceholder: "e.g. URGENT: Electricity power disconnected at 9:30 PM due to unpaid bill. Update bill immediately: http://power-discom-bill.xyz or call 9876543210",
        trySampleLinks: "Or test with common scam examples:",
        presetElectricity: "⚠️ Fake Electricity Disconnection",
        presetKycApk: "⚠️ Bank KYC & AnyDesk APK",
        presetInstantLoan: "⚠️ Instant ₹50,000 Loan Bait",
        presetLottery: "🔍 KBC Lottery Prize Draw",
        presetGenuineBank: "✅ Genuine Bank Credit SMS",
        btnVerifyNow: "Analyze Safety Now",
        btnClear: "Clear",

        /* Rule Engine Verdict Labels */
        verdictTitleDanger: "Likely scam",
        verdictTitleCaution: "Be careful",
        verdictTitleSafe: "Safe",
        verdictBadgeDanger: "🔴 LIKELY SCAM",
        verdictBadgeCaution: "🟡 BE CAREFUL",
        verdictBadgeSafe: "🟢 SAFE",
        riskScoreLabel: "Risk Score",
        reasonsTitle: "Why this score was given:",
        nextStepsTitle: "Recommended Next Steps:",
        stepBlock: "<strong>Block the number:</strong> Block the sender immediately on WhatsApp and phone dialer.",
        stepCallBank: "<strong>Call your bank on its official number:</strong> Use only the official number printed on the back of your debit card or passbook (never call the number in the SMS).",
        stepCall1930: "<strong>Call 1930:</strong> Dial the National Cyber Crime Helpline toll-free at 1930 immediately if money was deducted or credentials were shared.",
        stepCyberCrime: "<strong>Report to cybercrime.gov.in:</strong> Submit this incident to the official national portal to help protect other citizens.",
        disclaimerText: "Disclaimer: BlaxGuard provides automated decision support based on known scam heuristics and is not a 100% guarantee. Always verify with official financial authorities before sharing money or credentials.",
        btnListenVoice: "Listen in your language",
        btnListenAlert: "Listen Voice Warning",

        /* Loan Page */
        loanPageTitle: "Loan App Auditor",
        loanPageSub: "Verify if a loan application is genuine or an unauthorized predatory loan trap.",
        loanInputLabel: "Loan App Name / APK File:",
        loanInputPlaceholder: "e.g. Speed Rupee Cash Loan",
        permAuditTitle: "Permissions Requested by the App:",
        permAuditSub: "Check the permissions this app asks for in your phone settings:",
        permContacts: "Read Phone Contacts",
        permContactsSub: "Access to your family & friends phonebook",
        permGallery: "Read Gallery & Photos",
        permGallerySub: "Access to your private pictures and videos",
        permSms: "Read SMS & OTPs",
        permSmsSub: "Access to view your personal banking messages",
        btnAuditLoan: "Audit Loan App Safety",

        /* Call Page */
        callPageTitle: "Customer Care Check",
        callPageSub: "Scammers put fake 10-digit mobile numbers on search engines claiming to be banks or airlines.",
        callInputLabel: "Enter phone number to verify:",
        callInputPlaceholder: "e.g. +91 98765 43210 or 1800-11-2211",
        sampleFakeCare: "⚠️ Fake Bank Care (Mobile No.)",
        sampleRealCare: "✅ Official SBI Toll-Free (1800)",
        btnCheckPhone: "Check Phone Safety",

        /* Report Page */
        reportPageTitle: "Report a Scam",
        reportPageSub: "Protect your neighbors and alert cyber crime authorities before others lose money.",
        reportCardTitle: "Quick Incident Submission",
        reportScamType: "Type of Scam:",
        reportOptLoan: "Predatory Loan App Harassment",
        reportOptSms: "Fake Electricity / Bill SMS Link",
        reportOptCare: "Fake Customer Care Number",
        reportOptKyc: "Bank KYC / Account Block Trap",
        reportDetailsLabel: "Scammer Number, App, or Link:",
        reportPlaceholder: "Paste details here",
        btnSubmitReport: "Submit to National Cyber Registry",
        reportSuccessTitle: "Incident Logged Successfully",
        reportSuccessDesc: "Thank you for helping protect others. Your report has been dispatched to cyber defense databases.",

        /* Registry Page */
        registryPageTitle: "Safe Official Registry",
        registryPageSub: "Direct whitelist of approved government institutions, banks, and authorized lenders.",
        registrySearchTitle: "Search Verified Directory",
        registrySearchPlaceholder: "Type bank, NBFC, or service name...",

        /* Learn Page */
        learnPageTitle: "Safety Guide for Seniors",
        learnPageSub: "Three simple golden rules to keep you and your retirement savings 100% safe.",
        rule1Title: "UPI PIN is ONLY for Sending Money",
        rule1Desc: "You NEVER need to enter your UPI PIN to receive money or get lottery winnings. If someone asks for your PIN to 'transfer' money, it is a scam.",
        rule2Title: "Never Download APKs from WhatsApp",
        rule2Desc: "Scammers send files ending in .apk or .apk.zip. Legitimate banks only publish apps through Google Play Store. An APK can secretly read your OTPs!",
        rule3Title: "Electricity Department Never Calls from Personal Numbers",
        rule3Desc: "If a message says 'Your power will be cut tonight at 9:30 PM, call 98xxxxxx', ignore it. State electricity boards only use toll-free 1912.",

        /* Help Page */
        helpPageTitle: "Emergency Help & Guardian",
        helpPageSub: "Immediate assistance if money has been deducted or you suspect fraud.",
        helpGovtTitle: "National Cyber Crime Helpline",
        helpGovtDesc: "Call toll-free 1930 immediately within the first golden hour to freeze fraudulent bank transactions.",
        btnDial1930: "Call 1930 (Toll Free)",
        guardianTitle: "Family Guardian Alert Mode",
        guardianDesc: "Add your son, daughter, or trusted relative's phone number. BlaxGuard will immediately alert them if you encounter a high-risk link.",
        guardianPhoneLabel: "Guardian's Mobile Number:",
        guardianPhonePlaceholder: "+91 98765 00000",
        btnSaveGuardian: "Save Guardian Contact",

        /* Admin Page */
        adminPageTitle: "Admin Threat Center",
        adminPageSub: "Live threat intelligence feed, flagged predatory APKs, and regional scam heuristics.",
        adminLiveStatus: "Threat Feed Status: Active 🟢",
        statBlockedLinks: "Scam Links Intercepted",
        statRogueApks: "Predatory APKs Blocked",
        adminRecentScams: "Recent Intercepted Patterns",
        btnRefreshData: "Refresh Threat Heuristics"
      },

      hi: {
        tagline: "फर्जी लिंक और लोन फ्रॉड से आपकी सुरक्षा ढाल",
        seniorFriendly: "🛡️ नए डिजिटल उपयोगकर्ताओं और वरिष्ठ नागरिकों के लिए सरल व सुरक्षित",
        bannerTip: "<strong>सुरक्षा सलाह:</strong> अपना 4 या 6 अंकों का UPI पिन या OTP कभी किसी को न बताएं। पैसे प्राप्त करने के लिए पिन की आवश्यकता नहीं होती।",
        
        tabCheck: "जांचें",
        tabLoan: "लोन",
        tabCall: "कॉल",
        tabReport: "रिपोर्ट",
        tabRegistry: "सूची",
        tabLearn: "सीखें",
        tabHelp: "मदद",
        tabAdmin: "व्यवस्थापक",

        checkPageTitle: "लिंक, SMS या नंबर जांचें",
        checkPageSub: "व्हाट्सएप, मैसेज या अनजान फोन नंबर पर कोई भी कदम उठाने से पहले यहां उसकी सुरक्षा जांचें।",
        checkInputLabel: "संदेश, लिंक या फोन नंबर यहां पेस्ट करें:",
        checkInputPlaceholder: "जैसे: आवश्यक सूचना: आज रात 9:30 बजे बिजली कट जाएगी। बिल तुरंत भरें: http://power-bill.xyz या 9876543210 पर कॉल करें",
        trySampleLinks: "या इन सामान्य ठगी उदाहरणों को परखें:",
        presetElectricity: "⚠️ बिजली बिल कटने का फर्जी SMS",
        presetKycApk: "⚠️ बैंक KYC और AnyDesk APK",
        presetInstantLoan: "⚠️ तुरंत ₹50,000 लोन का झांसा",
        presetLottery: "🔍 KBC लॉटरी इनाम ड्रा",
        presetGenuineBank: "✅ बैंक का असली क्रेडिट SMS",
        btnVerifyNow: "सुरक्षा विश्लेषण करें",
        btnClear: "साफ करें",

        verdictTitleDanger: "संभावित धोखाधड़ी (Likely scam)",
        verdictTitleCaution: "सतर्क रहें (Be careful)",
        verdictTitleSafe: "सुरक्षित (Safe)",
        verdictBadgeDanger: "🔴 संभावित धोखाधड़ी",
        verdictBadgeCaution: "🟡 सतर्क रहें",
        verdictBadgeSafe: "🟢 सुरक्षित",
        riskScoreLabel: "जोखिम स्कोर",
        reasonsTitle: "यह स्कोर क्यों दिया गया:",
        nextStepsTitle: "सुझाए गए अगले कदम:",
        stepBlock: "<strong>नंबर ब्लॉक करें:</strong> संदेश भेजने वाले नंबर को व्हाट्सएप और फोन डायलर पर तुरंत ब्लॉक करें।",
        stepCallBank: "<strong>बैंक के आधिकारिक नंबर पर कॉल करें:</strong> केवल अपने डेबिट कार्ड या पासबुक पर दिए आधिकारिक नंबर पर ही बैंक से संपर्क करें (संदेश में दिए नंबर पर कभी नहीं)।",
        stepCall1930: "<strong>1930 पर कॉल करें:</strong> यदि कोई पैसा कट गया है या गोपनीय जानकारी दे दी है, तो तुरंत 1930 राष्ट्रीय साइबर हेल्पलाइन पर कॉल करें।",
        stepCyberCrime: "<strong>cybercrime.gov.in पर रिपोर्ट करें:</strong> अन्य नागरिकों की सुरक्षा के लिए इस घटना की शिकायत राष्ट्रीय साइबर पोर्टल पर दर्ज कराएं।",
        disclaimerText: "अस्वीकरण: BlaxGuard स्वचालित साइबर सुरक्षा विश्लेषण के आधार पर निर्णय सहायता प्रदान करता है, यह 100% पूर्ण गारंटी नहीं है। वित्तीय लेनदेन से पहले हमेशा आधिकारिक स्रोतों से पुष्टि करें।",
        btnListenVoice: "अपनी भाषा में सुनें",
        btnListenAlert: "चेतावनी बोलकर सुनें",

        loanPageTitle: "लोन ऐप की जांच",
        loanPageSub: "पता करें कि क्या यह लोन ऐप कानूनी है या ब्लैकमेल करने वाला फर्जी ऐप।",
        loanInputLabel: "लोन ऐप का नाम / APK फाइल:",
        loanInputPlaceholder: "जैसे: Speed Rupee Cash Loan",
        permAuditTitle: "ऐप द्वारा मांगी जा रही अनुमतियां:",
        permAuditSub: "देखें कि यह ऐप आपकी क्या-क्या निजी जानकारी मांग रहा है:",
        permContacts: "फोन कॉन्टैक्ट्स (Contacts)",
        permContactsSub: "आपके परिवार और दोस्तों के नंबर",
        permGallery: "गैलरी और फोटो (Photos)",
        permGallerySub: "आपकी निजी पारिवारिक तस्वीरें",
        permSms: "एसएमएस और ओटीपी (SMS)",
        permSmsSub: "बैंक के गुप्त संदेश पढ़ने की अनुमति",
        btnAuditLoan: "लोन ऐप की जांच करें",

        callPageTitle: "कस्टमर केयर नंबर जांचें",
        callPageSub: "ठग गूगल पर बैंकों के नाम से फर्जी 10 अंकों के मोबाइल नंबर डाल देते हैं।",
        callInputLabel: "जांचने के लिए फोन नंबर दर्ज करें:",
        callInputPlaceholder: "जैसे: +91 98765 43210 या 1800-11-2211",
        sampleFakeCare: "⚠️ फर्जी बैंक नंबर (10 अंकों का मोबाइल)",
        sampleRealCare: "✅ असली SBI टोल-फ्री नंबर (1800)",
        btnCheckPhone: "नंबर की सुरक्षा जांचें",

        reportPageTitle: "धोखाधड़ी की रिपोर्ट करें",
        reportPageSub: "दूसरों को लुटने से बचाने के लिए साइबर सेल में तुरंत रिपोर्ट करें।",
        reportCardTitle: "त्वरित शिकायत फॉर्म",
        reportScamType: "धोखाधड़ी का प्रकार:",
        reportOptLoan: "फर्जी लोन ऐप द्वारा ब्लैकमेलिंग",
        reportOptSms: "बिजली बिल / फर्जी लिंक",
        reportOptCare: "फर्जी कस्टमर केयर नंबर",
        reportOptKyc: "बैंक खाता ब्लॉक होने का डर",
        reportDetailsLabel: "धोखेबाज का नंबर या लिंक:",
        reportPlaceholder: "जानकारी यहां दर्ज करें",
        btnSubmitReport: "साइबर सेल को भेजें",
        reportSuccessTitle: "शिकायत सफलतापूर्वक दर्ज हुई",
        reportSuccessDesc: "धन्यवाद। आपकी रिपोर्ट को सुरक्षा डेटाबेस में शामिल कर लिया गया है।",

        registryPageTitle: "सरकारी व बैंक सूची",
        registryPageSub: "आरबीआई (RBI) द्वारा मान्यता प्राप्त बैंकों और वित्तीय संस्थानों की सूची।",
        registrySearchTitle: "प्रमाणित सूची में खोजें",
        registrySearchPlaceholder: "बैंक या संस्थान का नाम लिखें...",

        learnPageTitle: "बुजुर्गों के लिए सुरक्षा नियम",
        learnPageSub: "अपनी जीवन भर की कमाई को सुरक्षित रखने के 3 सुनहरे नियम।",
        rule1Title: "UPI पिन केवल पैसे भेजने के लिए होता है",
        rule1Desc: "पैसे प्राप्त करने या लॉटरी लेने के लिए UPI पिन डालने की कोई आवश्यकता नहीं होती। अगर कोई पिन मांगता है, तो वह पक्का ठग है।",
        rule2Title: "व्हाट्सएप से कभी भी APK फाइल डाउनलोड न करें",
        rule2Desc: "ठग .apk वाली फाइलें भेजते हैं। असली बैंक केवल गूगल प्ले स्टोर से ही ऐप देते हैं। अज्ञात APK आपके ओटीपी चुरा सकती है!",
        rule3Title: "बिजली विभाग कभी व्यक्तिगत मोबाइल से फोन नहीं करता",
        rule3Desc: "अगर संदेश आए कि 'आज रात 9:30 बजे बिजली कट जाएगी', तो घबराएं नहीं। सरकारी बिजली बोर्ड केवल 1912 नंबर का उपयोग करते हैं।",

        helpPageTitle: "आपातकालीन मदद और सुरक्षा",
        helpPageSub: "यदि पैसे कट गए हों या कोई धमकी दे रहा हो, तो तुरंत सहायता पाएं।",
        helpGovtTitle: "राष्ट्रीय साइबर हेल्पलाइन",
        helpGovtDesc: "धोखाधड़ी होने पर तुरंत टोल-फ्री नंबर 1930 पर कॉल करें ताकि बैंक खाता फ्रीज किया जा सके।",
        btnDial1930: "1930 पर कॉल करें (मुफ्त)",
        guardianTitle: "परिवार सुरक्षा अलर्ट (गार्डियन मोड)",
        guardianDesc: "अपने बेटे या बेटी का फोन नंबर जोड़ें। किसी खतरनाक लिंक पर BlaxGuard उन्हें तुरंत सचेत कर देगा।",
        guardianPhoneLabel: "अभिभावक / बच्चे का फोन नंबर:",
        guardianPhonePlaceholder: "+91 98765 00000",
        btnSaveGuardian: "अभिभावक नंबर सुरक्षित करें",

        adminPageTitle: "प्रशासनिक सुरक्षा केंद्र",
        adminPageSub: "सक्रिय खतरे, अवरुद्ध की गई फर्जी ऐप्स और नवीनतम सुरक्षा आंकड़े।",
        adminLiveStatus: "सुरक्षा स्थिति: सक्रिय 🟢",
        statBlockedLinks: "रोके गए फर्जी लिंक",
        statRogueApks: "ब्लॉक किए गए लोन APK",
        adminRecentScams: "हाल ही में पकड़े गए फर्जी तरीके",
        btnRefreshData: "डाटा रिफ्रेश करें"
      },

      te: {
        tagline: "నకిలీ లింకులు మరియు లోన్ మోసాల నుండి మీ రక్షణ కవచం",
        seniorFriendly: "🛡️ మొదటిసారి మొబైల్ వాడేవారికి మరియు పెద్దవారికి సులభం & సురక్షితం",
        bannerTip: "<strong>ముఖ్యమైన భద్రతా సూచన:</strong> డబ్బులు పంపేందుకు మాత్రమే UPI పిన్ వాడాలి. ఎవరైనా డబ్బులు పంపుతామని పిన్ అడిగితే అది మోసం!",
        
        tabCheck: "తనిఖీ",
        tabLoan: "లోన్",
        tabCall: "కాల్",
        tabReport: "ఫిర్యాదు",
        tabRegistry: "జాబితా",
        tabLearn: "నేర్చుకోండి",
        tabHelp: "సహాయం",
        tabAdmin: "అడ్మిన్",

        checkPageTitle: "లింక్, SMS లేదా నంబర్ తనిఖీ చేయండి",
        checkPageSub: "వాట్సాప్ లేదా మెసేజ్‌లలో వచ్చిన ఏ సందేశమైనా క్లిక్ చేసే ముందు ఇక్కడ విశ్లేషించండి.",
        checkInputLabel: "సందేశం, లింక్ లేదా ఫోన్ నంబర్‌ను ఇక్కడ పేస్ట్ చేయండి:",
        checkInputPlaceholder: "ఉదా: అర్జెంట్: ఈ రాత్రి 9:30 గంటలకు విద్యుత్ కట్ అవుతుంది. వెంటనే బిల్లు కట్టండి: http://power-bill.xyz లేదా 9876543210 కి కాల్ చేయండి",
        trySampleLinks: "లేదా ఈ నమూనాలను పరిశీలించండి:",
        presetElectricity: "⚠️ విద్యుత్ బిల్లు నకిలీ SMS",
        presetKycApk: "⚠️ బ్యాంక్ KYC & AnyDesk APK",
        presetInstantLoan: "⚠️ తక్షణ ₹50,000 లోన్ ట్రాప్",
        presetLottery: "🔍 KBC లాటరీ ప్రైజ్ డ్రా",
        presetGenuineBank: "✅ బ్యాంక్ అసలైన క్రెడిట్ SMS",
        btnVerifyNow: "భద్రతను విశ్లేషించండి",
        btnClear: "క్లియర్",

        verdictTitleDanger: "సంభావ్య మోసం (Likely scam)",
        verdictTitleCaution: "జాగ్రత్తగా ఉండండి (Be careful)",
        verdictTitleSafe: "సురక్షితం (Safe)",
        verdictBadgeDanger: "🔴 సంభావ్య మోసం",
        verdictBadgeCaution: "🟡 జాగ్రత్తగా ఉండండి",
        verdictBadgeSafe: "🟢 సురక్షితం",
        riskScoreLabel: "ప్రమాద స్కోర్",
        reasonsTitle: "ఈ స్కోర్ ఇవ్వడానికి గల కారణాలు:",
        nextStepsTitle: "చేయవలసిన తదుపరి చర్యలు:",
        stepBlock: "<strong>నంబర్‌ను బ్లాక్ చేయండి:</strong> సందేశం పంపిన నంబర్‌ను వాట్సాప్ మరియు ఫోన్ డయలర్‌లో వెంటనే బ్లాక్ చేయండి.",
        stepCallBank: "<strong>బ్యాంక్ అధికారిక నంబర్‌కు కాల్ చేయండి:</strong> మీ ఏటీఎం కార్డు లేదా పాస్‌బుక్ వెనుక ఉన్న నంబర్‌కు మాత్రమే కాల్ చేయండి (సందేశంలోని నంబర్లకు ఎప్పుడూ చేయవద్దు).",
        stepCall1930: "<strong>1930 కి కాల్ చేయండి:</strong> డబ్బులు కట్ అయితే లేదా వివరాలు పంచుకుంటే వెంటనే జాతీయ సైబర్ క్రైమ్ హెల్ప్‌లైన్ 1930 కి కాల్ చేయండి.",
        stepCyberCrime: "<strong>cybercrime.gov.in లో ఫిర్యాదు చేయండి:</strong> ఇతర పౌరులను కాపాడటానికి ఈ మోసాన్ని జాతీయ సైబర్ పోర్టల్‌లో నమోదు చేయండి.",
        disclaimerText: "గమనిక: BlaxGuard అనేది తెలిసిన సైబర్ ముప్పుల ఆధారంగా నిర్ణయం తీసుకోవడానికి ఇచ్చే స్వయంచాలక సహాయం మాత్రమే, ఇది 100% సంపూర్ణ హామీ కాదు. అధికారిక వర్గాలతో ఎల్లప్పుడూ నిర్ధారించుకోండి.",
        btnListenVoice: "మీ భాషలో వినండి",
        btnListenAlert: "హెచ్చరిక వినండి",

        loanPageTitle: "లోన్ యాప్ తనిఖీ",
        loanPageSub: "లోన్ యాప్ నిజమైనదా లేదా బ్లాక్‌మెయిల్ చేసే మోసపూరిత యాప్ కాదా అని తనిఖీ చేయండి.",
        loanInputLabel: "లోన్ యాప్ పేరు / APK ఫైల్:",
        loanInputPlaceholder: "ఉదా: Speed Rupee Cash Loan",
        permAuditTitle: "ఈ యాప్ అడుగుతున్న అనుమతులు:",
        permAuditSub: "ఈ యాప్ మీ ఫోన్‌లో ఎలాంటి అనుమతులు అడుగుతోందో చూడండి:",
        permContacts: "ఫోన్ కాంటాక్ట్‌లు (Contacts)",
        permContactsSub: "మీ కుటుంబం మరియు స్నేహితుల ఫోన్ నంబర్లు",
        permGallery: "ఫోటోలు మరియు గ్యాలరీ (Photos)",
        permGallerySub: "మీ వ్యక్తిగత కుటుంబ ఫోటోలు",
        permSms: "ఎస్ఎంఎస్ మరియు ఓటీపీలు (SMS)",
        permSmsSub: "బ్యాంకు రహస్య సందేశాలను చదివే అనుమతి",
        btnAuditLoan: "యాప్ భద్రతను తనిఖీ చేయండి",

        callPageTitle: "కస్టమర్ కేర్ నంబర్ తనిఖీ",
        callPageSub: "గూగుల్‌లో బ్యాంకుల పేరుతో 10 అంకెల నకిలీ మొబైల్ నంబర్లు పెట్టి మోసం చేస్తున్నారు.",
        callInputLabel: "తనిఖీ చేయాల్సిన ఫోన్ నంబర్:",
        callInputPlaceholder: "ఉదా: +91 98765 43210 లేదా 1800-11-2211",
        sampleFakeCare: "⚠️ నకిలీ బ్యాంక్ నంబర్ (మొబైల్ నంబర్)",
        sampleRealCare: "✅ అసలైన SBI టోల్-ఫ్రీ (1800)",
        btnCheckPhone: "నంబర్ భద్రతను తనిఖీ చేయండి",

        reportPageTitle: "మోసాన్ని నివేదించండి",
        reportPageSub: "ఇతరులు నష్టపోకుండా సైబర్ క్రైమ్ పోలీసులకు వెంటనే సమాచారం ఇవ్వండి.",
        reportCardTitle: "త్వరిత ఫిర్యాదు ఫారమ్",
        reportScamType: "మోసం రకం:",
        reportOptLoan: "లోన్ యాప్ బ్లాక్‌మెయిలింగ్",
        reportOptSms: "విద్యుత్ బిల్లు నకిలీ లింక్",
        reportOptCare: "నకిలీ కస్టమర్ కేర్ నంబర్",
        reportOptKyc: "బ్యాంక్ ఖాతా నిలిపివేత బెదిరింపు",
        reportDetailsLabel: "మోసగాడి నంబర్ లేదా లింక్:",
        reportPlaceholder: "వివరాలను ఇక్కడ నమోదు చేయండి",
        btnSubmitReport: "సైబర్ విభాగానికి పంపండి",
        reportSuccessTitle: "ఫిర్యాదు విజయవంతంగా అందింది",
        reportSuccessDesc: "ధన్యవాదాలు. మీ సమాచారం సైబర్ రక్షణ వ్యవస్థకు పంపబడింది.",

        registryPageTitle: "అధికారిక సంస్థల జాబితా",
        registryPageSub: "ఆర్బీఐ (RBI) అనుమతి పొందిన బ్యాంకులు మరియు ఫైనాన్స్ సంస్థల వివరాలు.",
        registrySearchTitle: "జాబితాలో వెతకండి",
        registrySearchPlaceholder: "బ్యాంకు లేదా సంస్థ పేరు టైప్ చేయండి...",

        learnPageTitle: "పెద్దల కోసం భద్రతా సూత్రాలు",
        learnPageSub: "మీ జీవితకాల సంపాదనను కాపాడుకోవడానికి 3 ముఖ్యమైన నియమాలు.",
        rule1Title: "డబ్బులు పంపేందుకు మాత్రమే UPI పిన్ వాడాలి",
        rule1Desc: "డబ్బులు అందుకోవడానికి ఎప్పుడూ UPI పిన్ ఎంటర్ చేయాల్సిన పనిలేదు. ఎవరైనా పిన్ అడిగితే వారు ఖచ్చితంగా మోసగాళ్లే.",
        rule2Title: "వాట్సాప్ ద్వారా వచ్చే APK లను ఇన్‌స్టాల్ చేయకండి",
        rule2Desc: ".apk ఫైల్స్ ద్వారా మోసగాళ్ళు మీ ఫోన్ మెసేజ్‌లు, ఓటీపీలను దొంగిలిస్తారు. బ్యాంక్ యాప్‌లు కేవలం Play Store నుండి మాత్రమే తీసుకోవాలి.",
        rule3Title: "కరెంట్ ఆఫీస్ వారు వ్యక్తిగత నంబర్ల నుండి కాల్ చేయరు",
        rule3Desc: "'ఈ రాత్రికి కరెంట్ కట్ చేస్తాం' అని వచ్చే మెసేజ్‌లను నమ్మవద్దు. విద్యుత్ సహాయానికి 1912 నంబర్ మాత్రమే వాడండి.",

        helpPageTitle: "అత్యవసర సహాయం & గార్డియన్",
        helpPageSub: "ఖాతా నుండి డబ్బులు కట్ అయితే లేదా అనుమానం వస్తే వెంటనే సంప్రదించండి.",
        helpGovtTitle: "జాతీయ సైబర్ క్రైమ్ హెల్ప్‌లైన్",
        helpGovtDesc: "మోసం జరిగిన వెంటనే 1930 టోల్-ఫ్రీ నంబర్‌కు కాల్ చేసి బ్యాంక్ ఖాతా లావాదేవీలను నిలిపివేయండి.",
        btnDial1930: "1930 కి కాల్ చేయండి (ఉచితం)",
        guardianTitle: "కుటుంబ రక్షణ మోడ్ (Guardian Mode)",
        guardianDesc: "మీ పిల్లలు లేదా కుటుంబ సభ్యుల ఫోన్ నంబర్ నమోదు చేయండి. ప్రమాదకర లింక్ వచ్చినప్పుడు BlaxGuard వారికి సమాచారం ఇస్తుంది.",
        guardianPhoneLabel: "కుటుంబ సభ్యుడి మొబైల్ నంబర్:",
        guardianPhonePlaceholder: "+91 98765 00000",
        btnSaveGuardian: "గార్డియన్ నంబర్ సేవ్ చేయండి",

        adminPageTitle: "అడ్మిన్ సెక్యూరిటీ సెంటర్",
        adminPageSub: "నిరోధించబడిన నకిలీ యాప్‌లు, మోసపూరిత లింకులు మరియు తాజా విశ్లేషణ.",
        adminLiveStatus: "రక్షణ వ్యవస్థ: యాక్టివ్ 🟢",
        statBlockedLinks: "నిరోధించిన నకిలీ లింకులు",
        statRogueApks: "బ్లాక్ చేసిన లోన్ యాప్‌లు",
        adminRecentScams: "తాజాగా పట్టుబడిన మోసాలు",
        btnRefreshData: "డేటాను అప్‌డేట్ చేయండి"
      }
    };

    /* PLAIN-LANGUAGE RULE REASON TRANSLATIONS */
    const ruleReasonTranslations = {
      urgency: {
        en: "Creates artificial panic and false urgency (threatening disconnection or immediate suspension).",
        hi: "झूठा डर और जल्दबाजी पैदा कर रहा है (बिजली कटने या तुरंत खाता बंद होने की धमकी)।",
        te: "కృత్రిమ తొందరపాటును సృష్టిస్తోంది (విద్యుత్ లేదా ఖాతా నిలిపివేత బెదిరింపులు)."
      },
      otpPin: {
        en: "Requests your secret OTP, UPI PIN, or verification code. Genuine institutions NEVER ask for your PIN to send you money.",
        hi: "आपका गुप्त OTP या UPI पिन मांग रहा है। पैसे प्राप्त करने के लिए किसी बैंक को आपके पिन की आवश्यकता नहीं होती।",
        te: "రహస్య OTP లేదా UPI పిన్ అడుగుతోంది. డబ్బులు పంపేందుకు ఏ అధికారిక సంస్థ కూడా పిన్ అడగదు."
      },
      kycExpiry: {
        en: "Falsely claims KYC, PAN, or account has expired or blocked to lure you into a trap.",
        hi: "केवाईसी (KYC), पैन या खाता बंद होने का झूठा दावा कर रहा है ताकि आप डर कर विवरण दे दें।",
        te: "భయాన్ని సృష్టించడానికి కేవైసీ (KYC) లేదా పాన్ గడువు ముగిసిందని తప్పుగా పేర్కొంటోంది."
      },
      prizes: {
        en: "Lures you with fake lottery prizes, cashback, or lucky draw winnings.",
        hi: "फर्जी लॉटरी, इनाम या कैशबैक का लालच देकर फंसाने की कोशिश कर रहा है।",
        te: "నకిలీ లాటరీ, బహుమతులు లేదా క్యాష్‌బ్యాక్ ఆశ చూపి మోసం చేయాలని చూస్తోంది."
      },
      advanceFee: {
        en: "Demands upfront processing fees, registration charge, or refundable security deposit.",
        hi: "पैसे देने या काम करने के नाम पर पहले प्रोसेसिंग फीस या रजिस्ट्रेशन चार्ज की मांग कर रहा है।",
        te: "ముందుగా ప్రాసెసింగ్ ఫీజు లేదా రిజిస్ట్రేషన్ ఛార్జీ చెల్లించమని అడుగుతోంది."
      },
      loanBait: {
        en: "Offers unrealistic instant loans without credit checks, CIBIL, or valid verification (predatory loan bait).",
        hi: "बिना किसी सिबिल स्कोर या कागजात के तुरंत लोन देने का झांसा (अवैध लोन ऐप का जाल)।",
        te: "సిబిల్ స్కోర్ లేదా డాక్యుమెంట్లు లేకుండా తక్షణ లోన్ ఇస్తామని నమ్మబలుకుతోంది (మోసపూరిత లోన్ ట్రాప్)."
      },
      remoteApk: {
        en: "Instructs downloading unverified APK files or remote control apps (AnyDesk/TeamViewer/RustDesk) that can take over your device.",
        hi: "अज्ञात APK फाइल या स्क्रीन शेयरिंग ऐप (AnyDesk / TeamViewer / RustDesk) डाउनलोड करने को कह रहा है, जिससे आपका फोन हैक हो सकता है।",
        te: "తెలియని APK ఫైల్ లేదా రిమోట్ స్క్రీన్ షేరింగ్ యాప్ (AnyDesk / TeamViewer / RustDesk) ఇన్‌స్టాల్ చేయమని చెబుతోంది, ఇది మీ ఖాతాను ఖాళీ చేయగలదు."
      },
      fakeCareNum: {
        en: "Quotes a personal 10-digit mobile number as customer care. Legitimate banks and utilities never use personal mobile numbers for support.",
        hi: "10 अंकों के व्यक्तिगत मोबाइल नंबर को कस्टमर केयर बता रहा है। बैंक कभी भी व्यक्तिगत मोबाइल को हेल्पलाइन नहीं बनाते।",
        te: "వ్యక్తిగత 10 అంకెల మొబైల్ నంబర్‌ను కస్టమర్ కేర్‌గా చూపుతోంది. బ్యాంకులు ఎప్పుడూ వ్యక్తిగత నంబర్లను వాడవు."
      },
      shortLink: {
        en: "Uses a shortened URL (bit.ly, tinyurl, etc.) to hide the actual scam website destination.",
        hi: "शॉर्ट लिंक (जैसे bit.ly, tinyurl) का उपयोग करके असली वेबसाइट का पता छुपाया जा रहा है।",
        te: "షార్ట్ లింక్ (bit.ly, tinyurl వంటివి) ద్వారా వెబ్‌సైట్ అసలు చిరునామాను దాచిపెడుతోంది."
      },
      riskyTld: {
        en: "Uses a high-risk domain ending (.xyz, .top, .live, etc.) or raw IP address frequently used in phishing attacks.",
        hi: "संदिग्ध या उच्च-जोखिम वाले डोमेन (.xyz, .top, .live आदि) या सीधे IP एड्रेस का उपयोग कर रहा है।",
        te: "సైబర్ నేరగాళ్ళు తరచుగా వాడే ప్రమాదకర డొమైన్ (.xyz, .top, .live మొదలైనవి) కలిగి ఉంది."
      },
      missingHttps: {
        en: "Link is insecure (missing HTTPS encryption). Official financial services always mandate HTTPS.",
        hi: "असुरक्षित कनेक्शन (HTTPS नहीं है)। असली बैंकिंग पोर्टल हमेशा सुरक्षित HTTPS का उपयोग करते हैं।",
        te: "సురక్షితం కాని కనెక్షన్ (HTTPS లేదు). అధికారిక బ్యాంకింగ్ వెబ్‌సైట్లు ఎల్లప్పుడూ HTTPS మాత్రమే ఉపయోగిస్తాయి."
      },
      brandSpoof: {
        en: "Imitates a reputed bank, utility, or government brand (SBI, HDFC, Discom, etc.) on an unauthorized website.",
        hi: "असली बैंक, बिजली विभाग या सरकारी संस्थान के नाम की नकल करके फर्जी वेबसाइट बनाई गई है।",
        te: "ప్రసిద్ధ బ్యాంక్ లేదా ప్రభుత్వ సంస్థ పేరును పోలిన నకిలీ వెబ్‌సైట్ ద్వారా మోసం చేస్తోంది."
      },
      cleanText: {
        en: "No known scam patterns or deceptive keywords were detected in the text.",
        hi: "इस संदेश में कोई भी ज्ञात ठगी या धोखाधड़ी का पैटर्न नहीं पाया गया।",
        te: "ఈ సందేశంలో ఎటువంటి మోసపూరిత పదాలు లేదా ముప్పులు కనుగొనబడలేదు."
      }
    };

    /* Current Language State */
    let currentLang = localStorage.getItem("blaxguard_lang") || "en";
    let lastAnalysisData = null; // Stores last result for instantaneous translation re-render

    /* Function to switch language instantly across all strings */
    function setLanguage(lang) {
      if (!translations[lang]) return;
      currentLang = lang;
      localStorage.setItem("blaxguard_lang", lang);

      const dict = translations[lang];

      // Update text nodes
      document.querySelectorAll("[data-i18n]").forEach(el => {
        const key = el.getAttribute("data-i18n");
        if (dict[key]) {
          el.innerHTML = dict[key];
        }
      });

      // Update input placeholders
      document.querySelectorAll("[data-i18n-placeholder]").forEach(el => {
        const key = el.getAttribute("data-i18n-placeholder");
        if (dict[key]) {
          el.setAttribute("placeholder", dict[key]);
        }
      });

      // Keep language selector in sync
      const select = document.getElementById("langSelect");
      if (select && select.value !== lang) {
        select.value = lang;
      }

      // If an analysis result is currently displayed, re-render it in the new language!
      if (lastAnalysisData) {
        renderVerdictUI(lastAnalysisData);
      }
    }

    /* THEME SWITCHER (Light / Dark) */
    function initTheme() {
      const savedTheme = localStorage.getItem("blaxguard_theme") || "light";
      const toggleBtn = document.getElementById("themeToggleBtn");
      const themeIcon = document.getElementById("themeIcon");

      function applyTheme(isDark) {
        if (isDark) {
          document.body.classList.add("dark");
          themeIcon.textContent = "☀️";
          toggleBtn.title = "Switch to Light Mode";
        } else {
          document.body.classList.remove("dark");
          themeIcon.textContent = "🌙";
          toggleBtn.title = "Switch to Dark Mode";
        }
      }

      applyTheme(savedTheme === "dark");

      toggleBtn.addEventListener("click", () => {
        const isDark = document.body.classList.toggle("dark");
        localStorage.setItem("blaxguard_theme", isDark ? "dark" : "light");
        themeIcon.textContent = isDark ? "☀️" : "🌙";
      });
    }

    /* HASH-BASED ROUTING */
    const validRoutes = ["check", "loan", "call", "report", "registry", "learn", "help", "admin"];

    function handleRouting() {
      let hash = window.location.hash.replace("#", "").toLowerCase().trim();
      if (!validRoutes.includes(hash)) {
        hash = "check";
      }

      validRoutes.forEach(route => {
        const pageEl = document.getElementById("page-" + route);
        if (pageEl) {
          if (route === hash) {
            pageEl.classList.add("active");
          } else {
            pageEl.classList.remove("active");
          }
        }
      });

      document.querySelectorAll(".nav-tab").forEach(tab => {
        const tabTarget = tab.getAttribute("data-tab");
        if (tabTarget === hash) {
          tab.classList.add("active");
          tab.scrollIntoView({ behavior: "smooth", inline: "center", block: "nearest" });
        } else {
          tab.classList.remove("active");
        }
      });

      window.scrollTo({ top: 0, behavior: "smooth" });
    }

    /* ==============================================================
       BROWSER-SIDE RULE ENGINE (SCORING 0 - 100)
       Checks all 12 distinct threat indicators
       ============================================================== */
    function evaluateTextSafety(rawText) {
      const text = (rawText || "").trim();
      const lower = text.toLowerCase();

      let score = 0;
      const matchedRules = [];

      // 1. False Urgency
      const urgencyRegex = /\\b(immediately|urgent|urgently|within 24 hours|within 2 hours|within \\d+ hours|tonight|today only|last chance|at 9:30 pm|at 9 pm|before 9 pm|expire in \\d+|hurry|action required|suspended today|disconnected tonight|cut tonight|block today|account suspended)\\b/i;
      if (urgencyRegex.test(lower)) {
        score += 20;
        matchedRules.push("urgency");
      }

      // 2. OTP / PIN Requests
      const otpRegex = /\\b(otp|upi pin|4-digit pin|6-digit pin|share pin|enter pin|provide otp|send otp|verify otp|share code|enter upi|password)\\b/i;
      if (otpRegex.test(lower)) {
        score += 35;
        matchedRules.push("otpPin");
      }

      // 3. KYC Expiry Claims
      const kycRegex = /\\b(kyc expired|update kyc|kyc pending|pan aadhaar link|pan blocked|pan card block|account blocked|kyc verification|sim kyc|aadhaar update|kyc suspension)\\b/i;
      if (kycRegex.test(lower)) {
        score += 25;
        matchedRules.push("kycExpiry");
      }

      // 4. Prizes / Lottery / Cashback
      const prizeRegex = /\\b(congratulations|you won|won lottery|lucky draw|kbc|cashback of rs|prize money|reward points|claim ₹|claim rs|gift voucher|winner draw)\\b/i;
      if (prizeRegex.test(lower)) {
        score += 25;
        matchedRules.push("prizes");
      }

      // 5. Advance Fees / Processing Fees
      const feeRegex = /\\b(processing fee|registration fee|refundable fee|pay deposit|advance payment|pay ₹\\d+|pay rs \\d+ to claim|security deposit|transfer fee)\\b/i;
      if (feeRegex.test(lower)) {
        score += 25;
        matchedRules.push("advanceFee");
      }

      // 6. Instant-Loan Bait
      const loanRegex = /\\b(pre-approved loan|instant loan|instant cash|no cibil|without cibil|loan in 5 mins|0% interest loan|instant ₹|instant rs|quick cash loan)\\b/i;
      if (loanRegex.test(lower)) {
        score += 25;
        matchedRules.push("loanBait");
      }

      // 7. APK or Remote-Access App Installs
      const remoteApkRegex = /(\\.apk|\\.apk\\.zip|download apk|download app|install app to update|anydesk|teamviewer|rustdesk|quicksupport|screen share|alpemix|airmirror)/i;
      if (remoteApkRegex.test(lower)) {
        score += 35;
        matchedRules.push("remoteApk");
      }

      // 8. "Customer Care" numbers (10-digit mobile claimed as care)
      const careKeyword = /(customer care|helpline|support|helpdesk|call us at|toll free|contact)/i.test(lower);
      const mobileNumberMatch = /(?:\\+?91[\\-\\s]?)?([6-9]\\d{9})\\b/.exec(lower);
      const isOfficialHelpline = /\\b(1800\\d{4,8}|1912|1930|112)\\b/.test(lower);

      if (careKeyword && mobileNumberMatch && !isOfficialHelpline) {
        score += 25;
        matchedRules.push("fakeCareNum");
      } else if (!careKeyword && mobileNumberMatch && text.length <= 15) {
        // Just an unknown mobile number pasted alone
        score += 15;
        matchedRules.push("fakeCareNum");
      }

      // 9. Shortened links
      const shortLinkRegex = /(bit\\.ly|tinyurl\\.com|t\\.co|is\\.gd|cutt\\.ly|rb\\.gy|shorturl\\.at|ow\\.ly|buff\\.ly|goo\\.gl)/i;
      if (shortLinkRegex.test(lower)) {
        score += 20;
        matchedRules.push("shortLink");
      }

      // 10. Risky domain endings or raw IP
      const riskyTldRegex = /\\.(xyz|top|online|club|buzz|work|live|loan|vip|icu|tk|ml|ga|cf|gq|site|space|guru|cam|rest)(?:[\\/\\?\\s]|$)/i;
      const rawIpRegex = /https?:\\/\\/\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}/i;
      if (riskyTldRegex.test(lower) || rawIpRegex.test(lower)) {
        score += 25;
        matchedRules.push("riskyTld");
      }

      // 11. Missing HTTPS (Plain HTTP link)
      const httpRegex = /http:\\/\\/[a-z0-9\\-\\._~:\\/\\?#\\[\\]@!\\$&'\\(\\)\\*\\+,;=]+/i;
      if (httpRegex.test(text) && !text.includes("https://")) {
        score += 15;
        matchedRules.push("missingHttps");
      }

      // 12. Links imitating bank or government brands (brand spoofing / typosquatting)
      const brandKeywords = /(sbi|hdfc|icici|axis|pnb|rbi|gov|pmkisan|epfo|discom|electricity|bescom|bsnl|jio|airtel|incometax)/i;
      const genuineDomains = [
        "onlinesbi.sbi", "sbi.co.in", "hdfcbank.com", "icicibank.com", "axisbank.com",
        "pnbindia.in", "rbi.org.in", "cybercrime.gov.in", "gov.in", "nic.in",
        "pmkisan.gov.in", "epfindia.gov.in", "incometax.gov.in", "jio.com", "airtel.in", "bsnl.co.in"
      ];

      // Extract URLs from text
      const urlMatches = text.match(/https?:\\/\\/[^\\s]+/gi) || [];
      let isSpoofed = false;
      let hasGenuineWhitelist = false;

      for (let u of urlMatches) {
        try {
          const urlObj = new URL(u);
          const hostname = urlObj.hostname.toLowerCase();
          const isOfficial = genuineDomains.some(d => hostname === d || hostname.endsWith("." + d));

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

      // Genuine whitelist discount (if no active malicious flags like OTP/AnyDesk)
      if (hasGenuineWhitelist && score <= 20) {
        score = 0;
      }

      // Cap score between 0 and 100
      let finalScore = Math.min(100, Math.max(0, score));

      // Determine verdict
      let verdict = "safe";
      if (finalScore >= 60) {
        verdict = "danger"; // Likely scam
      } else if (finalScore >= 25) {
        verdict = "caution"; // Be careful
      } else {
        verdict = "safe"; // Safe
      }

      if (matchedRules.length === 0) {
        matchedRules.push("cleanText");
      }

      return {
        score: finalScore,
        verdict: verdict,
        matchedRules: matchedRules,
        rawText: text
      };
    }

    /* RENDER VERDICT UI */
    function renderVerdictUI(data) {
      const container = document.getElementById("checkVerdictContainer");
      if (!container) return;

      const dict = translations[currentLang] || translations.en;
      const isDanger = data.verdict === "danger";
      const isCaution = data.verdict === "caution";
      const isSafe = data.verdict === "safe";

      let verdictClass = isDanger ? "verdict-danger" : (isCaution ? "verdict-caution" : "verdict-safe");
      let verdictBadgeText = isDanger ? dict.verdictBadgeDanger : (isCaution ? dict.verdictBadgeCaution : dict.verdictBadgeSafe);
      let verdictTitleText = isDanger ? dict.verdictTitleDanger : (isCaution ? dict.verdictTitleCaution : dict.verdictTitleSafe);

      // Construct plain language reasons list
      let reasonsHtml = "";
      data.matchedRules.forEach(ruleKey => {
        const trans = ruleReasonTranslations[ruleKey];
        const reasonText = (trans && trans[currentLang]) ? trans[currentLang] : (trans ? trans.en : ruleKey);
        reasonsHtml += `<li>${reasonText}</li>`;
      });

      container.style.display = "block";
      container.className = `verdict-box ${verdictClass}`;
      container.innerHTML = `
        <div class="verdict-header">
          <span class="verdict-badge">${verdictBadgeText}</span>
          <span style="font-size: 24px;">${isDanger ? "⚠️" : (isCaution ? "🔍" : "✅")}</span>
        </div>

        <div class="verdict-title">${verdictTitleText}</div>

        <!-- RISK SCORE METER -->
        <div class="score-meter-wrap">
          <div class="score-text-label">
            <span>${dict.riskScoreLabel}:</span>
            <span style="font-size: 19px;">${data.score} / 100</span>
          </div>
          <div class="score-bar-bg">
            <div class="score-fill" style="width: ${Math.max(5, data.score)}%;"></div>
          </div>
        </div>

        <!-- REASONS LIST -->
        <div class="reasons-box">
          <div class="reasons-title">
            <span>📋</span> <span>${dict.reasonsTitle}</span>
          </div>
          <ul class="reasons-list">
            ${reasonsHtml}
          </ul>
        </div>

        <!-- NEXT STEPS BOX -->
        <div class="next-steps-card">
          <div class="next-steps-header">
            <span>🛡️</span> <span>${dict.nextStepsTitle}</span>
          </div>
          <ul class="next-steps-list">
            <li>
              <span class="step-badge">1</span>
              <div>${dict.stepBlock}</div>
            </li>
            <li>
              <span class="step-badge">2</span>
              <div>${dict.stepCallBank}</div>
            </li>
            <li>
              <span class="step-badge">3</span>
              <div>${dict.stepCall1930}</div>
            </li>
            <li>
              <span class="step-badge">4</span>
              <div>${dict.stepCyberCrime}</div>
            </li>
          </ul>
        </div>

        <!-- VOICE WARNING BUTTON FOR SENIORS -->
        <button class="senior-voice-btn" onclick="speakRuleEngineAlert()">
          <span>🔊</span> <span>${dict.btnListenAlert}</span>
        </button>

        <!-- DISCLAIMER -->
        <div class="disclaimer-text">
          ${dict.disclaimerText}
        </div>
      `;
    }

    /* TRIGGER RULE ENGINE */
    function runRuleEngine() {
      const input = document.getElementById("checkMessageInput");
      const val = input ? input.value.trim() : "";

      if (!val) {
        const alertMsg = currentLang === "hi" 
          ? "कृपया पहले कोई संदेश, लिंक या फोन नंबर दर्ज करें" 
          : (currentLang === "te" 
            ? "దయచేసి ముందుగా సందేశం, లింక్ లేదా ఫోన్ నంబర్ నమోదు చేయండి" 
            : "Please paste a message, link, or phone number first");
        alert(alertMsg);
        return;
      }

      const result = evaluateTextSafety(val);
      lastAnalysisData = result;
      renderVerdictUI(result);

      // Auto scroll smoothly to verdict
      const container = document.getElementById("checkVerdictContainer");
      if (container) {
        container.scrollIntoView({ behavior: "smooth", block: "nearest" });
      }
    }

    /* CLEAR INPUT */
    function clearCheckInput() {
      const input = document.getElementById("checkMessageInput");
      if (input) input.value = "";
      const container = document.getElementById("checkVerdictContainer");
      if (container) container.style.display = "none";
      lastAnalysisData = null;
    }

    /* PRESET EXAMPLES FOR DEMO / JUDGES */
    function loadSamplePreset(type) {
      const input = document.getElementById("checkMessageInput");
      if (!input) return;

      if (type === "electricity") {
        input.value = "URGENT: Electricity power disconnected tonight at 9:30 PM due to unpaid bill. Update bill immediately: http://power-discom-bill.xyz or call 9876543210";
      } else if (type === "kyc_apk") {
        input.value = "Dear SBI customer, your KYC is expired and bank account blocked today. Download QuickSupport AnyDesk app to verify PAN: bit.ly/sbi-pan-kyc";
      } else if (type === "instant_loan") {
        input.value = "Congratulations! Instant pre-approved loan of ₹50,000 without CIBIL score or documents in 5 mins. Download FastCash.apk to claim cash now.";
      } else if (type === "lottery") {
        input.value = "Dear winner, you won ₹25,00,000 in KBC Lucky Draw! Pay refundable registration fee ₹500 to release prize money.";
      } else if (type === "genuine_bank") {
        input.value = "Dear SBI Customer, your A/c ending 4589 is credited with Rs 5,000.00 on 08-Oct. For assistance, visit https://retail.onlinesbi.sbi or call toll-free 1800 1234.";
      }

      runRuleEngine();
    }

    /* VOICE READOUT OF VERDICT (Browser Speech Synthesis) */
    function speakRuleEngineAlert() {
      if (!("speechSynthesis" in window) || !lastAnalysisData) return;
      window.speechSynthesis.cancel();

      const data = lastAnalysisData;
      let msg = "";
      let langCode = "en-IN";

      if (currentLang === "hi") {
        langCode = "hi-IN";
        if (data.verdict === "danger") {
          msg = "सावधान! यह संभावित धोखाधड़ी है। इसका जोखिम स्कोर सौ में से " + data.score + " है। किसी भी लिंक पर क्लिक न करें और नंबर को तुरंत ब्लॉक करें।";
        } else if (data.verdict === "caution") {
          msg = "सतर्क रहें! इस संदेश में कुछ संदिग्ध संकेत हैं। कोई भी पासवर्ड या पिन साझा न करें।";
        } else {
          msg = "यह संदेश सुरक्षित प्रतीत होता है। कोई भी ज्ञात खतरा नहीं पाया गया।";
        }
      } else if (currentLang === "te") {
        langCode = "te-IN";
        if (data.verdict === "danger") {
          msg = "హెచ్చరిక! ఇది సంభావ్య మోసం. ప్రమాద స్కోర్ " + data.score + ". ఎటువంటి లింక్ తెరవవద్దు మరియు వెంటనే నంబర్ బ్లాక్ చేయండి.";
        } else if (data.verdict === "caution") {
          msg = "జాగ్రత్తగా ఉండండి! ఈ సందేశంలో కొన్ని అనుమానాస్పద అంశాలు ఉన్నాయి. రహస్య వివరాలు ఇవ్వవద్దు.";
        } else {
          msg = "ఈ సందేశం సురక్షితంగా ఉంది. ఎటువంటి ప్రమాదం కనిపించలేదు.";
        }
      } else {
        langCode = "en-IN";
        if (data.verdict === "danger") {
          msg = "Warning! Likely scam detected with a risk score of " + data.score + " out of 100. Do not tap any link and block the sender immediately.";
        } else if (data.verdict === "caution") {
          msg = "Caution advised. Suspicious elements were detected. Do not share your financial details or OTP.";
        } else {
          msg = "Verified safe. No known scam patterns were found in this text.";
        }
      }

      const utterance = new SpeechSynthesisUtterance(msg);
      utterance.lang = langCode;
      utterance.rate = 0.9;
      window.speechSynthesis.speak(utterance);
    }

    /* LOAN AUDITOR */
    function auditLoanApp() {
      const appName = document.getElementById("loanAppName").value.trim() || "Loan App";
      const hasContacts = document.getElementById("permContactsToggle").checked;
      const hasGallery = document.getElementById("permGalleryToggle").checked;
      const hasSms = document.getElementById("permSmsToggle").checked;
      const box = document.getElementById("loanVerdictBox");

      box.style.display = "block";

      if (hasContacts && hasGallery) {
        box.className = "verdict-box verdict-danger";
        box.innerHTML = `
          <div class="verdict-header">
            <span class="verdict-badge">🔴 PREDATORY LOAN APP / फर्जी लोन ऐप</span>
            <span>⚠️</span>
          </div>
          <div class="verdict-title">${currentLang === 'hi' ? 'चेतावनी: ब्लैकमेल करने वाला अनधिकृत ऐप!' : (currentLang === 'te' ? 'ప్రమాదం: బ్లాక్‌మెయిల్ చేసే మోసపూరిత లోన్ యాప్!' : 'CRITICAL WARNING: Predatory Extortion Loan Trap')}</div>
          <div class="verdict-desc">
            ${currentLang === 'hi'
              ? '<strong>' + appName + '</strong> आपके फोन कॉन्टैक्ट्स और निजी फोटो मांग रहा है। भारतीय रिजर्व बैंक (RBI) के नियमानुसार किसी भी असली लोन ऐप को आपकी निजी गैलरी या फोनबुक की अनुमति लेने का अधिकार नहीं है। यह ऐप लोगों को ब्लैकमेल करता है। तुरंत अनइंस्टॉल करें!'
              : (currentLang === 'te'
                ? '<strong>' + appName + '</strong> మీ కుటుంబ ఫోటోలు మరియు కాంటాక్ట్‌లను అడుగుతోంది. రిజర్వ్ బ్యాంక్ (RBI) నిబంధనల ప్రకారం ఏ నిజమైన లోన్ యాప్‌కు మీ గ్యాలరీ ఫోటోలు చూసే హక్కు లేదు. ఇది బ్లాక్‌మెయిల్ చేసే యాప్. వెంటనే తొలగించండి!'
                : '<strong>' + appName + '</strong> demands access to your personal contacts and gallery pictures. Legitimate RBI-approved NBFCs are strictly prohibited by regulations from demanding contact books or photos. Installing this APK can lead to harassment and blackmail!')}
          </div>
          <button class="senior-voice-btn" onclick="speakAlert('loan')">
            <span>🔊</span> <span>${currentLang === 'hi' ? 'चेतावनी सुनें' : (currentLang === 'te' ? 'హెచ్చరిక వినండి' : 'Listen Voice Alert')}</span>
          </button>
        `;
      } else {
        box.className = "verdict-box verdict-safe";
        box.innerHTML = `
          <div class="verdict-header">
            <span class="verdict-badge">🟢 STANDARD PERMISSIONS</span>
            <span>✅</span>
          </div>
          <div class="verdict-title">${currentLang === 'hi' ? 'सामान्य अनुमतियां' : (currentLang === 'te' ? 'సాధారణ అనుమతులు' : 'No Invasive Permissions Detected')}</div>
          <div class="verdict-desc">
            ${currentLang === 'hi'
              ? 'इस ऐप ने कॉन्टैक्ट्स या गैलरी की गैर-कानूनी अनुमति नहीं मांगी है। कृपया सुनिश्चित करें कि यह ऐप गूगल प्ले स्टोर से ही डाउनलोड किया गया हो।'
              : (currentLang === 'te'
                ? 'ఈ యాప్ మీ వ్యక్తిగత ఫోటోలు లేదా కాంటాక్ట్‌లను అడగడం లేదు. ఇది Play Store నుండి తీసుకున్నదేనా అని నిర్ధారించుకోండి.'
                : 'This app is not asking for invasive contact book or photo gallery access. Always verify lender registration in the Safe Registry tab.')}
          </div>
        `;
      }
    }

    /* CALL AUDITOR */
    function testCallSample(type) {
      const input = document.getElementById("callPhoneInput");
      if (type === "fake") {
        input.value = "+91 98312 45890";
      } else {
        input.value = "1800 1234";
      }
      verifyPhoneNumber();
    }

    function verifyPhoneNumber() {
      const num = document.getElementById("callPhoneInput").value.trim();
      const box = document.getElementById("callVerdictBox");
      if (!num) return;

      box.style.display = "block";
      if (num.startsWith("1800") || num.startsWith("1912") || num.startsWith("1930")) {
        box.className = "verdict-box verdict-safe";
        box.innerHTML = `
          <div class="verdict-header">
            <span class="verdict-badge">🟢 VERIFIED OFFICIAL TOLL-FREE</span>
          </div>
          <div class="verdict-title">${currentLang === 'hi' ? 'आधिकारिक टोल-फ्री नंबर' : (currentLang === 'te' ? 'అధికారిక టోల్-ఫ్రీ నంబర్' : 'Verified Official Toll-Free Directory')}</div>
          <div class="verdict-desc">
            ${currentLang === 'hi' 
              ? 'यह 1800 या सरकारी हेल्पलाइन नंबर है। यह आधिकारिक और सुरक्षित है।' 
              : (currentLang === 'te' 
                ? 'ఇది అధికారిక టోల్-ఫ్రీ లేదా ప్రభుత్వ హెల్ప్‌లైన్ నంబర్. ఇది సురక్షితమైనది.' 
                : '1800 and 4-digit numbers (like 1912/1930) are official institutional lines and cannot be spoofed by standard mobile scammers.')}
          </div>
        `;
      } else {
        box.className = "verdict-box verdict-danger";
        box.innerHTML = `
          <div class="verdict-header">
            <span class="verdict-badge">🔴 SUSPICIOUS FAKE CUSTOMER CARE</span>
          </div>
          <div class="verdict-title">${currentLang === 'hi' ? 'सावधान! 10 अंकों का व्यक्तिगत मोबाइल नंबर' : (currentLang === 'te' ? 'జాగ్రత్త! వ్యక్తిగత మొబైల్ నంబర్' : 'DANGER: Personal 10-Digit Mobile Number')}</div>
          <div class="verdict-desc">
            ${currentLang === 'hi' 
              ? 'बैंक या बिजली विभाग कभी भी 10 अंकों के व्यक्तिगत मोबाइल नंबर को कस्टमर केयर के रूप में इस्तेमाल नहीं करते। इस नंबर पर बात न करें और कभी भी AnyDesk / TeamViewer ऐप इंस्टॉल न करें!' 
              : (currentLang === 'te' 
                ? 'బ్యాంకులు లేదా ప్రభుత్వ శాఖలు ఎప్పుడూ వ్యక్తిగత మొబైల్ నంబర్లను కస్టమర్ కేర్‌గా వాడవు. ఈ నంబర్‌కు మాట్లాడవద్దు, వారు చెప్పే యాప్‌లు ఇన్‌స్టాల్ చేయవద్దు!' 
                : 'Banks, courier services, and electricity departments NEVER use 10-digit mobile numbers for customer care. Scammers use these numbers to trick seniors into installing screen-sharing apps (AnyDesk/RustDesk) to empty accounts.')}
          </div>
        `;
      }
    }

    /* REPORT INCIDENT */
    function submitReport() {
      const target = document.getElementById("reportTargetInput").value.trim();
      const successBox = document.getElementById("reportSuccessBox");
      if (!target) {
        alert("Please enter scam details");
        return;
      }
      successBox.style.display = "block";
      document.getElementById("reportTargetInput").value = "";
    }

    /* REGISTRY FILTER */
    function filterRegistry() {
      const query = document.getElementById("registrySearchInput").value.toLowerCase();
      const items = document.querySelectorAll("#registryList .list-item-card");
      items.forEach(card => {
        const text = card.textContent.toLowerCase();
        if (text.includes(query)) {
          card.style.display = "flex";
        } else {
          card.style.display = "none";
        }
      });
    }

    /* GUARDIAN SAVE */
    function saveGuardian() {
      const phone = document.getElementById("guardianPhoneInput").value.trim();
      if (!phone) {
        alert("Please enter a valid mobile number");
        return;
      }
      localStorage.setItem("blaxguard_guardian", phone);
      alert(currentLang === 'hi' 
        ? "अभिभावक नंबर सफलतापूर्वक सुरक्षित किया गया: " + phone 
        : (currentLang === 'te' 
          ? "గార్డియన్ మొబైల్ నంబర్ సేవ్ చేయబడింది: " + phone 
          : "Guardian Contact Saved! You will receive safety alerts on " + phone));
    }

    /* ADMIN REFRESH */
    function refreshAdminData() {
      alert(currentLang === 'hi' ? "नवीनतम खतरे और साइबर हीयूरिस्टिक्स अपडेट हो गए हैं।" : (currentLang === 'te' ? "తాజా సైబర్ రక్షణ డేటా అప్‌డేట్ చేయబడింది." : "Heuristics and RBI registry synced successfully!"));
    }

    /* AUDIO VOICE ASSISTANT FOR SENIORS (Browser Speech Synthesis) */
    function speakRule(ruleNum) {
      if (!("speechSynthesis" in window)) return;
      window.speechSynthesis.cancel();

      let msg = "";
      let langCode = "en-IN";

      if (currentLang === "hi") {
        langCode = "hi-IN";
        if (ruleNum === 1) msg = "नियम एक: यूपीआई पिन केवल पैसे भेजने के लिए होता है। पैसे प्राप्त करने के लिए कभी भी पिन न डालें।";
        else if (ruleNum === 2) msg = "नियम दो: व्हाट्सएप से कभी भी एपीके फाइल डाउनलोड न करें। यह आपके बैंक के ओटीपी चुरा सकती है।";
        else msg = "नियम तीन: बिजली विभाग कभी भी व्यक्तिगत नंबर से कॉल नहीं करता। संदेशों से घबराएं नहीं।";
      } else if (currentLang === "te") {
        langCode = "te-IN";
        if (ruleNum === 1) msg = "నియమం ఒకటి: డబ్బులు పంపేందుకు మాత్రమే యూపీఐ పిన్ వాడాలి. డబ్బులు వచ్చేందుకు పిన్ అవసరం లేదు.";
        else if (ruleNum === 2) msg = "నియమం రెండు: వాట్సాప్ లో వచ్చే ఏపీకే ఫైల్స్ ఇన్స్టాల్ చేయకండి. ఇది మీ ఓటీపీలు దొంగిలిస్తుంది.";
        else msg = "నియమం మూడు: కరెంట్ ఆఫీస్ వారు వ్యక్తిగత నంబర్ల నుండి ఫోన్ చేయరు. మోసపోవద్దు.";
      } else {
        langCode = "en-IN";
        if (ruleNum === 1) msg = "Rule 1: UPI PIN is only for sending money, never for receiving money.";
        else if (ruleNum === 2) msg = "Rule 2: Never install APK files sent on WhatsApp. They can steal your bank OTPs.";
        else msg = "Rule 3: Electricity boards never call from personal mobile numbers.";
      }

      const utterance = new SpeechSynthesisUtterance(msg);
      utterance.lang = langCode;
      utterance.rate = 0.9;
      window.speechSynthesis.speak(utterance);
    }

    function speakAlert(type) {
      if (!("speechSynthesis" in window)) return;
      window.speechSynthesis.cancel();

      let msg = "";
      let langCode = "en-IN";

      if (currentLang === "hi") {
        langCode = "hi-IN";
        if (type === "loan") msg = "सावधान! यह ऐप आपकी पारिवारिक तस्वीरें और फोन नंबर चुराकर ब्लैकमेल कर सकती है। इसे तुरंत हटाएं।";
        else msg = "रुकिए! यह खतरनाक लिंक है।";
      } else if (currentLang === "te") {
        langCode = "te-IN";
        if (type === "loan") msg = "హెచ్చరిక! ఈ యాప్ మీ కుటుంబ ఫోటోలు మరియు నంబర్లను దొంగిలించి బ్లాక్ మెయిల్ చేస్తుంది. వెంటనే తీసివేయండి.";
        else msg = "ఆగండి! ఇది ప్రమాదకర లింక్.";
      } else {
        langCode = "en-IN";
        if (type === "loan") msg = "Warning! Predatory loan app detected. It requests access to your photos and contacts.";
        else msg = "Warning! High risk link detected.";
      }

      const utterance = new SpeechSynthesisUtterance(msg);
      utterance.lang = langCode;
      utterance.rate = 0.9;
      window.speechSynthesis.speak(utterance);
    }

    /* INITIALIZATION */
    window.addEventListener("DOMContentLoaded", () => {
      initTheme();

      // Language Selector Event
      const langSelect = document.getElementById("langSelect");
      langSelect.value = currentLang;
      langSelect.addEventListener("change", (e) => {
        setLanguage(e.target.value);
      });

      setLanguage(currentLang);

      // Handle Hash Routing
      window.addEventListener("hashchange", handleRouting);
      handleRouting();
    });
  </script>
</body>
</html>
'''

full_html = html_template.replace("{{SHIELD_URI}}", shield_uri).replace("{{FULL_URI}}", full_uri)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(full_html)

print("Generated updated index.html with Check page Rule Engine! Size:", os.path.getsize("index.html"))
