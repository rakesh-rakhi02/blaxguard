import base64
import json

with open("shield_128.png", "rb") as f:
    shield_b64 = "data:image/png;base64," + base64.b64encode(f.read()).decode("utf-8")

with open("full_logo_opt.jpg", "rb") as f:
    full_b64 = "data:image/jpeg;base64," + base64.b64encode(f.read()).decode("utf-8")

print(f"Shield URI length: {len(shield_b64)}")
print(f"Full URI length: {len(full_b64)}")

with open("uris.json", "w", encoding="utf-8") as f:
    json.dump({"shield": shield_b64, "full": full_b64}, f)
print("Saved uris.json successfully")
