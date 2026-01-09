async function analyze() {
  const urlInput = document.getElementById("url");
  const output = document.getElementById("output");

  // ----------------------------
  // Basic validation
  // ----------------------------
  if (!urlInput.value.trim()) {
    output.textContent = "⚠️ Please enter an Instagram URL.";
    return;
  }

  // ----------------------------
  // Processing state
  // ----------------------------
  output.textContent = "⏳ Analyzing Instagram post...";

  // Clean Instagram URL (remove tracking params)
  const cleanUrl = urlInput.value.trim().split("?")[0];

  try {
    const response = await fetch("/api/analyze", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        instagram_url: cleanUrl
      })
    });

    // ----------------------------
    // Read raw response text first
    // ----------------------------
    const text = await response.text();

    // ----------------------------
    // API-level error handling
    // ----------------------------
    if (!response.ok) {
      output.textContent =
        "❌ API Error\n" +
        "Status: " + response.status + "\n\n" +
        text;
      return;
    }

    // ----------------------------
    // Parse and pretty-print JSON
    // ----------------------------
    const data = JSON.parse(text);
    output.textContent = JSON.stringify(data, null, 2);

  } catch (err) {
    // ----------------------------
    // Network / JS error handling
    // ----------------------------
    output.textContent =
      "❌ Request failed.\n" +
      "Reason: " + err.message;
  }
}
