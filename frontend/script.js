async function analyze() {
  const urlInput = document.getElementById("url");
  const output = document.getElementById("output");

  // Basic validation
  if (!urlInput.value.trim()) {
    output.textContent = "⚠️ Please enter an Instagram URL.";
    return;
  }

  // Show processing state
  output.textContent = "⏳ Analyzing Instagram post...";

  // Remove tracking parameters (?utm_*)
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

    // Read raw response text first (safer for debugging)
    const text = await response.text();

    // Handle API-level errors
    if (!response.ok) {
      output.textContent =
        "❌ API Error\n" +
        "Status: " + response.status + "\n\n" +
        text;
      return;
    }

    // Parse and pretty-print JSON
    const data = JSON.parse(text);
    output.textContent = JSON.stringify(data, null, 2);

  } catch (err) {
    output.textContent =
      "❌ Request failed.\n" +
      "Reason: " + err.message;
  }
}
