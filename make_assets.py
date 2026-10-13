import base64

shield_svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">
  <defs>
    <linearGradient id="sGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#4682B4" />
      <stop offset="100%" stop-color="#1F3A60" />
    </linearGradient>
    <linearGradient id="tGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#2DD4BF" />
      <stop offset="100%" stop-color="#0D9488" />
    </linearGradient>
    <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="2" stdDeviation="3" flood-opacity="0.3"/>
    </filter>
  </defs>
  <path d="M50 6 L86 22 V48 C86 70 70 88 50 94 C30 88 14 70 14 48 V22 Z" fill="url(#sGrad)" filter="url(#glow)"/>
  <path d="M50 14 L79 27 V47 C79 64 66 79 50 84 C34 79 21 64 21 47 V27 Z" fill="none" stroke="url(#tGrad)" stroke-width="3.5" stroke-linecap="round"/>
  <circle cx="50" cy="41" r="9" fill="#FFFFFF" fill-opacity="0.95"/>
  <path d="M43 50 L57 50 L59 64 L41 64 Z" fill="#FFFFFF" fill-opacity="0.95"/>
  <path d="M42 44 L48 50 L60 37" fill="none" stroke="#0D9488" stroke-width="3.8" stroke-linecap="round" stroke-linejoin="round"/>
</svg>'''

full_logo_svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 380 95" width="380" height="95">
  <defs>
    <linearGradient id="fsGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#4682B4" />
      <stop offset="100%" stop-color="#1F3A60" />
    </linearGradient>
    <linearGradient id="ftGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#2DD4BF" />
      <stop offset="100%" stop-color="#0D9488" />
    </linearGradient>
    <filter id="fglow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="2" stdDeviation="2.5" flood-opacity="0.25"/>
    </filter>
  </defs>
  <g transform="translate(8, 6)">
    <path d="M42 4 L76 19 V44 C76 64 61 80 42 86 C23 80 8 64 8 44 V19 Z" fill="url(#fsGrad)" filter="url(#fglow)"/>
    <path d="M42 12 L70 24 V43 C70 59 57 72 42 77 C27 72 14 59 14 43 V24 Z" fill="none" stroke="url(#ftGrad)" stroke-width="3" stroke-linecap="round"/>
    <circle cx="42" cy="37" r="8" fill="#FFFFFF"/>
    <path d="M36 45 L48 45 L50 58 L34 58 Z" fill="#FFFFFF"/>
    <path d="M35 40 L40 45 L50 33" fill="none" stroke="#0D9488" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"/>
  </g>
  <text x="102" y="46" font-family="'Montserrat', -apple-system, sans-serif" font-weight="800" font-size="32" fill="#0F172A" letter-spacing="-0.5">Blax<tspan fill="#4682B4">Guard</tspan></text>
  <line x1="102" y1="55" x2="365" y2="55" stroke="url(#ftGrad)" stroke-width="2.5" stroke-linecap="round"/>
  <text x="102" y="73" font-family="'Montserrat', -apple-system, sans-serif" font-weight="600" font-size="11.5" fill="#4682B4" letter-spacing="0.2">Your shield against fake links and loan scams</text>
</svg>'''

s_b64 = base64.b64encode(shield_svg.encode('utf-8')).decode('utf-8')
f_b64 = base64.b64encode(full_logo_svg.encode('utf-8')).decode('utf-8')

with open('b64_assets.json', 'w', encoding='utf-8') as f:
    import json
    json.dump({'shield': s_b64, 'full': f_b64}, f)
print('Done writing b64_assets.json')
