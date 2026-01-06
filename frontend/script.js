async function analyze() {
  const urlInput = document.getElementById("url");
  const output = document.getElementById("output");

  output.textContent = "Analyzing...";

  // Clean Instagram URL
  const cleanUrl = urlInput.value.split("?")[0];

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

    if (!response.ok) {
      output.textContent = "ERROR:\n" + text;
      return;
    }

    output.textContent = JSON.stringify(JSON.parse(text), null, 2);

  } catch (err) {
    output.textContent = "Request failed:\n" + err.message;
  }
}
