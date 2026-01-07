async function analyze() {
  const urlInput = document.getElementById("url");
  const output = document.getElementById("output");

  // Basic validation
  if (!urlInput.value.trim()) {
    output.textContent = "⚠️ Please enter an Instagram URL.";
    return;
  }

  output.textContent = "⏳ Analyzing...";

  // Remove tracking parameters
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

    const text = await response.text();

    // Handle API errors gracefully
    if (!response.ok) {
      output.textContent = "❌ ERROR:\n" + text;
      return;
    }

    // Pretty print JSON response
    const data = JSON.parse(text);
    output.textContent = JSON.stringify(data, null, 2);

  } catch (err) {
    output.textContent =
      "❌ Request failed.\n" +
      "Reason: " + err.message;
  }
}
