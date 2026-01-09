// ==============================
// DOM ELEMENTS
// ==============================
const results = document.getElementById("results");
const loadingOverlay = document.getElementById("loadingOverlay");
const loadingText = document.getElementById("loadingText");

const deepfakeBadge = document.getElementById("deepfakeBadge");
const deepfakeBar = document.getElementById("deepfakeBar");
const deepfakeText = document.getElementById("deepfakeText");

const toxicityBadge = document.getElementById("toxicityBadge");
const toxicityText = document.getElementById("toxicityText");

const finalBadge = document.getElementById("finalBadge");

// ==============================
// UI HELPERS
// ==============================
function showLoading(text = "Processing…") {
  loadingText.textContent = text;
  loadingOverlay.classList.remove("hidden");
  toggleButtons(true);
}

function hideLoading() {
  loadingOverlay.classList.add("hidden");
  toggleButtons(false);
}

function toggleButtons(disabled) {
  document.querySelectorAll("button").forEach(btn => {
    btn.disabled = disabled;
  });
}

function showResults() {
  results.classList.remove("hidden");
}

function setBadge(el, level) {
  const value = level || "Unavailable";
  el.textContent = value;
  el.className = "badge " + value.toLowerCase();
}

// ==============================
// RENDER: INSTAGRAM
// ==============================
function renderInstagramResults(data) {
  showResults();

  const dfScore = data.deepfake_score ?? 0;
  const toxScore = data.toxicity_score ?? 0;
  const risk = data.risk_level ?? "Unavailable";

  // Deepfake (IG = proxy score)
  setBadge(deepfakeBadge, risk);
  deepfakeBar.style.width = Math.round(dfScore * 100) + "%";
  deepfakeText.textContent = `Score: ${dfScore}`;

  // Toxicity
  const toxRisk =
    toxScore > 0.6 ? "High" :
    toxScore > 0.3 ? "Medium" : "Low";

  setBadge(toxicityBadge, toxRisk);
  toxicityText.textContent = `Toxicity score: ${toxScore}`;

  // Final
  setBadge(finalBadge, risk);
}

// ==============================
// RENDER: VIDEO
// ==============================
function renderVideoResults(data) {
  showResults();

  const score = data.deepfake_score ?? 0;
  const risk = data.risk_level ?? "Unavailable";
  const frames = data.frames_analyzed ?? 0;

  setBadge(deepfakeBadge, risk);
  deepfakeBar.style.width = Math.round(score * 100) + "%";
  deepfakeText.textContent = `Frames analyzed: ${frames}`;

  setBadge(toxicityBadge, "Unavailable");
  toxicityText.textContent = "Not applicable for uploaded videos";

  setBadge(finalBadge, risk);
}

// ==============================
// INSTAGRAM ANALYSIS
// ==============================
async function analyzeInstagram() {
  const urlInput = document.getElementById("url");

  if (!urlInput.value.trim()) {
    alert("Please enter an Instagram URL.");
    return;
  }

  results.classList.add("hidden");
  const cleanUrl = urlInput.value.trim().split("?")[0];

  try {
    showLoading("Analyzing Instagram post…");

    const res = await fetch("/api/analyze", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ instagram_url: cleanUrl })
    });

    if (!res.ok) throw new Error(await res.text());

    const data = await res.json();
    renderInstagramResults(data);

  } catch (err) {
    alert("Analysis failed:\n" + err.message);
  } finally {
    hideLoading();
  }
}

// ==============================
// VIDEO ANALYSIS
// ==============================
async function analyzeVideo() {
  const fileInput = document.getElementById("videoFile");

  if (!fileInput.files.length) {
    alert("Please select a .mp4 video.");
    return;
  }

  results.classList.add("hidden");
  const formData = new FormData();
  formData.append("file", fileInput.files[0]);

  try {
    showLoading("Uploading video…");

    const res = await fetch("/api/analyze/video", {
      method: "POST",
      body: formData
    });

    if (!res.ok) throw new Error(await res.text());

    showLoading("Detecting faces & running CNN…");

    const data = await res.json();
    renderVideoResults(data);

  } catch (err) {
    alert("Video analysis failed:\n" + err.message);
  } finally {
    hideLoading();
  }
}
