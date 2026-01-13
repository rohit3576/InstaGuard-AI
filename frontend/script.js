// ==============================
// DOM ELEMENTS
// ==============================
const urlInput = document.getElementById("url");
const videoInput = document.getElementById("videoFile");
const videoPreview = document.getElementById("videoPreview");
const faceCanvas = document.getElementById("faceCanvas");

const loadingOverlay = document.getElementById("loadingOverlay");
const loadingText = document.getElementById("loadingText");

const results = document.getElementById("results");

// Result elements
const deepfakeBadge = document.getElementById("deepfakeBadge");
const deepfakeBar = document.getElementById("deepfakeBar");
const deepfakeText = document.getElementById("deepfakeText");

const toxicityBadge = document.getElementById("toxicityBadge");
const toxicityText = document.getElementById("toxicityText");

const finalBadge = document.getElementById("finalBadge");

// ==============================
// UTILS — UI HELPERS
// ==============================
function showLoading(text = "Processing...") {
  loadingText.textContent = text;
  loadingOverlay.classList.remove("hidden");
}

function hideLoading() {
  loadingOverlay.classList.add("hidden");
}

function showResults() {
  results.classList.remove("hidden");
}

function resetResults() {
  showResults();

  deepfakeBadge.className = "badge unavailable";
  deepfakeBadge.textContent = "—";
  deepfakeBar.style.width = "0%";
  deepfakeText.textContent = "—";

  toxicityBadge.className = "badge unavailable";
  toxicityBadge.textContent = "—";
  toxicityText.textContent = "—";

  finalBadge.className = "badge large unavailable";
  finalBadge.textContent = "—";
}

function setBadge(el, level) {
  el.className = "badge " + level.toLowerCase();
  el.textContent = level;
}

// ==============================
// VIDEO PREVIEW + CANVAS SYNC
// ==============================
videoInput.addEventListener("change", () => {
  const file = videoInput.files[0];
  if (!file) return;

  const url = URL.createObjectURL(file);
  videoPreview.src = url;
  videoPreview.load();

  videoPreview.onloadedmetadata = () => {
    faceCanvas.width = videoPreview.videoWidth;
    faceCanvas.height = videoPreview.videoHeight;
  };
});

// ==============================
// FAKE FACE SCANNING (RED BOXES)
// ==============================
let scanInterval = null;

function startFakeFaceScan() {
  const ctx = faceCanvas.getContext("2d");
  stopFakeFaceScan();

  scanInterval = setInterval(() => {
    if (videoPreview.paused || videoPreview.ended) return;

    ctx.clearRect(0, 0, faceCanvas.width, faceCanvas.height);

    const boxW = faceCanvas.width * 0.3;
    const boxH = faceCanvas.height * 0.35;

    const x = Math.random() * (faceCanvas.width - boxW);
    const y = Math.random() * (faceCanvas.height - boxH);

    ctx.strokeStyle = "red";
    ctx.lineWidth = 3;
    ctx.strokeRect(x, y, boxW, boxH);

    ctx.font = "16px Arial";
    ctx.fillStyle = "red";
    ctx.fillText("Scanning face...", x, y - 8);
  }, 400);
}

function stopFakeFaceScan() {
  if (scanInterval) {
    clearInterval(scanInterval);
    scanInterval = null;
  }
  const ctx = faceCanvas.getContext("2d");
  ctx.clearRect(0, 0, faceCanvas.width, faceCanvas.height);
}

// ==============================
// MODE A — INSTAGRAM ANALYSIS
// ==============================
async function analyzeInstagram() {
  if (!urlInput.value.trim()) {
    alert("Please enter an Instagram URL");
    return;
  }

  resetResults();
  showLoading("Analyzing Instagram post...");

  const cleanUrl = urlInput.value.trim().split("?")[0];

  try {
    const res = await fetch("/api/analyze", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ instagram_url: cleanUrl })
    });

    const data = await res.json();

    // Deepfake not available
    deepfakeBadge.textContent = "Unavailable";
    deepfakeBadge.className = "badge unavailable";
    deepfakeText.textContent = "Video analysis not allowed for Instagram URLs";

    // Toxicity
    setBadge(toxicityBadge, data.toxicity_score.level);
    toxicityText.textContent =
      `Toxic comments: ${data.toxicity_score.toxic_percentage}%`;

    // Final Risk
    setBadge(finalBadge, data.risk_level);

  } catch (err) {
    alert("Instagram analysis failed");
    console.error(err);
  } finally {
    hideLoading();
  }
}

// ==============================
// MODE B — VIDEO UPLOAD ANALYSIS
// ==============================
async function analyzeVideo() {
  const file = videoInput.files[0];
  if (!file) {
    alert("Please upload a video file");
    return;
  }

  resetResults();
  showLoading("Scanning video for deepfake artifacts...");
  startFakeFaceScan();

  const formData = new FormData();
  formData.append("video", file);

  try {
    const res = await fetch("/api/analyze/video", {
      method: "POST",
      body: formData
    });

    const data = await res.json();

    // Deepfake Result
    const score = Math.round(data.deepfake_score * 100);
    deepfakeBar.style.width = score + "%";
    deepfakeText.textContent =
      `Frames analyzed: ${data.frames_analyzed}`;

    setBadge(deepfakeBadge, data.risk_level);

    // Toxicity not applicable
    toxicityBadge.textContent = "N/A";
    toxicityBadge.className = "badge unavailable";
    toxicityText.textContent = "Not applicable for uploaded videos";

    // Final Risk
    setBadge(finalBadge, data.risk_level);

  } catch (err) {
    alert("Video analysis failed");
    console.error(err);
  } finally {
    stopFakeFaceScan();
    hideLoading();
  }
}
