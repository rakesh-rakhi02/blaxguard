document.getElementById("btnScan").addEventListener("click", async () => {
  const input = document.getElementById("quickInput").value.trim();
  const resDiv = document.getElementById("resultContainer");
  if (!input) return;

  resDiv.style.display = "block";
  resDiv.className = "card";
  resDiv.innerHTML = "<span>Analyzing with RBI Registry...</span>";

  try {
    const res = await fetch("http://localhost:8080/api/check", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text: input })
    });
    const data = await res.json();

    if (data.verdict === "safe") {
      resDiv.className = "res-safe";
      resDiv.innerHTML = `<strong>✅ Safe (Score: ${data.score}/100)</strong><br>${data.reasons?.[0] || 'Verified clean'}`;
    } else if (data.verdict === "danger") {
      resDiv.className = "res-danger";
      resDiv.innerHTML = `<strong>🚨 High Risk (Score: ${data.score}/100)</strong><br>${data.reasons?.[0] || 'Threat detected'}`;
    } else {
      resDiv.className = "res-caution";
      resDiv.innerHTML = `<strong>⚠️ Caution (Score: ${data.score}/100)</strong><br>${data.reasons?.[0] || 'Unverified'}`;
    }
  } catch (err) {
    resDiv.className = "res-caution";
    resDiv.innerHTML = "BlaxGuard local server not reached. Ensure http://localhost:8080 is running.";
  }
});
