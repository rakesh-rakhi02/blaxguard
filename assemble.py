import json
import os

with open("uris.json", "r", encoding="utf-8") as f:
    uris = json.load(f)

shield_uri = uris["shield"]
full_uri = uris["full"]

with open("template.html", "r", encoding="utf-8") as f:
    template = f.read()

output = template.replace("{{SHIELD_URI}}", shield_uri).replace("{{FULL_URI}}", full_uri)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(output)

print(f"Successfully generated index.html! Size: {os.path.getsize('index.html')} bytes")
