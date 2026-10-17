/**
 * SamjhautaCheck: AI Fine-Print Trap Detector & Negotiation Coach
 * Frontend Controller & Audio Player Engine
 */

document.addEventListener("DOMContentLoaded", () => {
  // DOM Elements
  const dropzone = document.getElementById("dropzone");
  const fileInput = document.getElementById("fileInput");
  const fileBadge = document.getElementById("fileBadge");
  const fileNameDisplay = document.getElementById("fileNameDisplay");
  const textToggleBtn = document.getElementById("textToggleBtn");
  const contractDrawer = document.getElementById("contractDrawer");
  const contractText = document.getElementById("contractText");
  const languageSelect = document.getElementById("languageSelect");
  const loadDemoBtn = document.getElementById("loadDemoBtn");
  const auditBtn = document.getElementById("auditBtn");
  const auditSpinner = document.getElementById("auditSpinner");
  const auditBtnText = document.getElementById("auditBtnText");
  const auditBtnIcon = document.getElementById("auditBtnIcon");
  
  // Results Elements
  const resultsSection = document.getElementById("resultsSection");
  const gaugeCircle = document.getElementById("gaugeCircle");
  const gaugeScore = document.getElementById("gaugeScore");
  const verdictBadge = document.getElementById("verdictBadge");
  const docTypeTag = document.getElementById("docTypeTag");
  
  // Audio Player Elements
  const audioElement = document.getElementById("audioElement");
  const playPauseBtn = document.getElementById("playPauseBtn");
  const playIcon = document.getElementById("playIcon");
  const pauseIcon = document.getElementById("pauseIcon");
  const waveformContainer = document.getElementById("waveformContainer");
  const timelineSlider = document.getElementById("timelineSlider");
  const currentTimeDisplay = document.getElementById("currentTime");
  const totalTimeDisplay = document.getElementById("totalTime");
  const speedBtn = document.getElementById("speedBtn");
  const transcriptToggleBtn = document.getElementById("transcriptToggleBtn");
  const transcriptDrawer = document.getElementById("transcriptDrawer");
  const transcriptText = document.getElementById("transcriptText");
  const ttsBadgeLanguage = document.getElementById("ttsBadgeLanguage");
  
  // Tabs & Lists
  const tabButtons = document.querySelectorAll(".tab-btn");
  const tabPanels = document.querySelectorAll(".tab-panel");
  const flagCountBadge = document.getElementById("flagCountBadge");
  const missingCountBadge = document.getElementById("missingCountBadge");
  const flagsContainer = document.getElementById("flagsContainer");
  const missingContainer = document.getElementById("missingContainer");
  const negotiationMessageBox = document.getElementById("negotiationMessageBox");
  const copyNegotiationBtn = document.getElementById("copyNegotiationBtn");
  const openWhatsAppBtn = document.getElementById("openWhatsAppBtn");
  const summaryLeadText = document.getElementById("summaryLeadText");
  const takeawaysList = document.getElementById("takeawaysList");
  const toastNotification = document.getElementById("toastNotification");
  const toastMessage = document.getElementById("toastMessage");
  const apiStatusText = document.getElementById("apiStatusText");

  // State
  let currentFile = null;
  let currentReport = null;
  let isPlaying = false;
  let playbackRate = 1.0;
  let useSpeechSynthFallback = false;
  let fallbackUtterance = null;

  // Initialize Waveform Bars (24 bars)
  for (let i = 0; i < 28; i++) {
    const bar = document.createElement("div");
    bar.className = "wave-bar";
    bar.style.height = `${8 + Math.sin(i * 0.4) * 12 + Math.random() * 8}px`;
    waveformContainer.appendChild(bar);
  }

  // Check Backend Status
  fetch("/api/status")
    .then(res => res.json())
    .then(data => {
      if (data.sarvam_configured) {
        apiStatusText.textContent = `Sarvam AI Active (${data.api_key_masked})`;
      } else {
        apiStatusText.textContent = `Sarvam Demo Mode (Local Heuristics)`;
      }
    })
    .catch(() => {
      apiStatusText.textContent = `SamjhautaCheck Ready`;
    });

  // Drag and Drop Handling
  ["dragenter", "dragover"].forEach(eventName => {
    dropzone.addEventListener(eventName, (e) => {
      e.preventDefault();
      e.stopPropagation();
      dropzone.classList.add("drag-active");
    });
  });

  ["dragleave", "drop"].forEach(eventName => {
    dropzone.addEventListener(eventName, (e) => {
      e.preventDefault();
      e.stopPropagation();
      dropzone.classList.remove("drag-active");
    });
  });

  dropzone.addEventListener("drop", (e) => {
    const files = e.dataTransfer.files;
    if (files.length > 0) {
      handleSelectedFile(files[0]);
    }
  });

  fileInput.addEventListener("change", (e) => {
    if (e.target.files.length > 0) {
      handleSelectedFile(e.target.files[0]);
    }
  });

  function handleSelectedFile(file) {
    currentFile = file;
    fileNameDisplay.textContent = `📄 ${file.name} (${(file.size / 1024).toFixed(1)} KB)`;
    fileBadge.style.display = "inline-block";
    
    // If text file, preview in drawer
    if (file.name.endsWith(".txt") || file.name.endsWith(".md")) {
      const reader = new FileReader();
      reader.onload = (e) => {
        contractText.value = e.target.result;
        contractDrawer.classList.add("open");
      };
      reader.readAsText(file);
    }
  }

  // Toggle raw text drawer
  textToggleBtn.addEventListener("click", () => {
    contractDrawer.classList.toggle("open");
    if (contractDrawer.classList.contains("open")) {
      contractText.focus();
    }
  });

  // Load Demo Rental Agreement
  loadDemoBtn.addEventListener("click", async () => {
    try {
      loadDemoBtn.disabled = true;
      loadDemoBtn.textContent = "Loading Demo...";
      
      const res = await fetch("/api/demo");
      const data = await res.json();
      
      contractText.value = data.text;
      contractDrawer.classList.add("open");
      currentFile = null;
      fileNameDisplay.textContent = "📄 Bangalore_Rental_Agreement_Demo.pdf";
      fileBadge.style.display = "inline-block";
      
      showToast("Realistic predatory rental agreement loaded!");
      
      // Auto run audit for instant gratification
      executeAudit("Bangalore_Rental_Agreement_Demo.pdf", data.text);
    } catch (err) {
      showToast("Error loading demo agreement", true);
    } finally {
      loadDemoBtn.disabled = false;
      loadDemoBtn.innerHTML = `
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/></svg>
        Load Demo Rental Agreement
      `;
    }
  });

  // Audit Trigger Button
  auditBtn.addEventListener("click", () => {
    const textVal = contractText.value.trim();
    const filename = currentFile ? currentFile.name : (textVal ? "Pasted_Contract.txt" : "Document.txt");
    executeAudit(filename, textVal);
  });

  // Core Audit Execution
  async function executeAudit(filename, textContent) {
    const selectedLang = languageSelect.value;
    
    // Validation
    if (!currentFile && (!textContent || textContent.length < 30)) {
      showToast("Please select a file or paste contract text first", true);
      contractDrawer.classList.add("open");
      contractText.focus();
      return;
    }

    setAuditLoading(true);

    try {
      const formData = new FormData();
      formData.append("language", selectedLang);
      formData.append("filename", filename);

      if (currentFile) {
        formData.append("file", currentFile);
      }
      if (textContent) {
        formData.append("text", textContent);
      }

      const response = await fetch("/api/audit", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || `Server returned error ${response.status}`);
      }

      const result = await response.json();
      currentReport = result;
      renderAuditResults(result);

      if (result.cached) {
        showToast("⚡ Served instantaneously from SQLite cache!");
      } else {
        showToast("✅ Forensic trap audit complete!");
      }
    } catch (err) {
      console.error("Audit error:", err);
      showToast(err.message || "Failed to audit contract", true);
    } finally {
      setAuditLoading(false);
    }
  }

  function setAuditLoading(isLoading) {
    if (isLoading) {
      auditBtn.disabled = true;
      auditSpinner.style.display = "inline-block";
      auditBtnIcon.style.display = "none";
      auditBtnText.textContent = "Auditing Contract...";
    } else {
      auditBtn.disabled = false;
      auditSpinner.style.display = "none";
      auditBtnIcon.style.display = "inline-block";
      auditBtnText.textContent = "Run Forensic Trap Audit";
    }
  }

  // Render Audit Results
  function renderAuditResults(data) {
    const report = data.report;
    const score = report.fairness_score;

    // Reveal Results Section
    resultsSection.classList.add("visible");
    resultsSection.scrollIntoView({ behavior: "smooth", block: "start" });

    // 1. Animate Gauge (Circumference for r=85 is 2 * PI * 85 = 534.07)
    const circumference = 2 * Math.PI * 85;
    const offset = circumference - (score / 100) * circumference;
    
    gaugeCircle.style.strokeDasharray = `${circumference}`;
    gaugeCircle.style.strokeDashoffset = `${offset}`;

    // Color code and verdict
    if (score < 40) {
      gaugeCircle.style.stroke = "#ef4444";
      gaugeCircle.style.filter = "drop-shadow(0 0 12px rgba(239, 68, 68, 0.4))";
      verdictBadge.className = "verdict-badge verdict-critical";
      verdictBadge.textContent = "🔴 PREDATORY & HIGH RISK";
    } else if (score < 72) {
      gaugeCircle.style.stroke = "#f59e0b";
      gaugeCircle.style.filter = "drop-shadow(0 0 12px rgba(245, 158, 11, 0.4))";
      verdictBadge.className = "verdict-badge verdict-unbalanced";
      verdictBadge.textContent = "🟡 UNBALANCED — REVISE";
    } else {
      gaugeCircle.style.stroke = "#10b981";
      gaugeCircle.style.filter = "drop-shadow(0 0 12px rgba(16, 185, 129, 0.4))";
      verdictBadge.className = "verdict-badge verdict-fair";
      verdictBadge.textContent = "🟢 REASONABLY FAIR";
    }

    // Number counting animation
    animateScoreNumber(score);

    // Document classification tag
    docTypeTag.textContent = `Type: ${report.document_type}`;

    // 2. Audio Setup
    setupAudioPlayer(data);

    // 3. Populate Tab 1: Red Flags
    flagCountBadge.textContent = report.red_flags ? report.red_flags.length : 0;
    renderRedFlags(report.red_flags || []);

    // 4. Populate Tab 2: Missing Protections
    missingCountBadge.textContent = report.missing_protections ? report.missing_protections.length : 0;
    renderMissingProtections(report.missing_protections || []);

    // 5. Populate Tab 3: WhatsApp Negotiation Draft
    negotiationMessageBox.textContent = report.whatsapp_negotiation_draft || "";
    openWhatsAppBtn.href = `https://api.whatsapp.com/send?text=${encodeURIComponent(report.whatsapp_negotiation_draft || "")}`;

    // 6. Populate Tab 4: Executive Summary
    summaryLeadText.textContent = report.summary || "";
    takeawaysList.innerHTML = (report.key_takeaways || []).map(item => `
      <li>
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>
        <span>${escapeHtml(item)}</span>
      </li>
    `).join("");
  }

  function animateScoreNumber(targetScore) {
    let current = 0;
    const duration = 1000;
    const startTime = performance.now();

    function updateScore(timestamp) {
      const elapsed = timestamp - startTime;
      const progress = Math.min(elapsed / duration, 1);
      // easeOutCubic
      const easeProgress = 1 - Math.pow(1 - progress, 3);
      current = Math.round(easeProgress * targetScore);
      gaugeScore.textContent = current;

      if (progress < 1) {
        requestAnimationFrame(updateScore);
      } else {
        gaugeScore.textContent = targetScore;
      }
    }
    requestAnimationFrame(updateScore);
  }

  function renderRedFlags(flags) {
    if (!flags.length) {
      flagsContainer.innerHTML = `<p style="color:var(--text-secondary); padding:20px;">No critical red flags detected.</p>`;
      return;
    }

    flagsContainer.innerHTML = flags.map((flag, idx) => `
      <div class="glass-card flag-card severity-${flag.severity_level}">
        <div class="flag-header">
          <div class="flag-title-area">
            <strong>Trap #${idx + 1}</strong>
            <span class="severity-pill pill-${flag.severity_level}">${flag.severity_level} Risk</span>
          </div>
        </div>

        <div class="flag-details-grid">
          <div class="flag-box">
            <div class="flag-box-label label-quote">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 21c3 0 7-1 7-8V5c0-1.25-.756-2.017-2-2H4c-1.25 0-2 .75-2 1.972V11c0 1.25.75 2 2 2 1 0 1 0 1 1v1c0 1-1 2-2 2s-1 .008-1 1.031V20c0 1 0 1 1 1z"/></svg>
              Original Trap Clause (Verbatim)
            </div>
            <div class="flag-box-content quote-text">${escapeHtml(flag.clause_quote)}</div>
          </div>

          <div class="flag-box">
            <div class="flag-box-label label-risk">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
              Plain-English Risk & Legal Exposure
            </div>
            <div class="flag-box-content" style="color: #fca5a5;">${escapeHtml(flag.plain_english_risk)}</div>
          </div>
        </div>

        <div class="counter-proposal-box">
          <div class="flag-box-label label-proposal">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg>
            Recommended Counter-Proposal (Substitute Clause)
          </div>
          <div class="flag-box-content" style="color: #6ee7b7;">${escapeHtml(flag.counter_proposal_text)}</div>
        </div>
      </div>
    `).join("");
  }

  function renderMissingProtections(missing) {
    if (!missing.length) {
      missingContainer.innerHTML = `<p style="color:var(--text-secondary); padding:20px;">All standard protections are present.</p>`;
      return;
    }

    missingContainer.innerHTML = missing.map((item, idx) => `
      <div class="glass-card missing-card">
        <div class="missing-icon">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
        </div>
        <div class="missing-text">
          <strong>Missing Protection #${idx + 1}:</strong><br>
          ${escapeHtml(item)}
        </div>
      </div>
    `).join("");
  }

  // Audio Player Engine
  function setupAudioPlayer(data) {
    const lang = data.spoken_language || "en";
    const script = data.translated_script || data.report.spoken_briefing_script;

    transcriptText.textContent = script;
    
    // Set language label on player
    const langNames = {
      en: "English (Indian) • Meera",
      hi: "हिन्दी • Meera",
      hinglish: "Hinglish • Arvind",
      te: "తెలుగు • Meera",
      ta: "தமிழ் • Meera"
    };
    ttsBadgeLanguage.textContent = langNames[lang] || `${lang.toUpperCase()} • Bulbul`;

    // Reset playback state
    stopAudio();

    if (data.audio_base64 && data.audio_base64.length > 50) {
      useSpeechSynthFallback = false;
      audioElement.src = `data:audio/wav;base64,${data.audio_base64}`;
      audioElement.load();
    } else {
      // Offline fallback: Use browser Web Speech API for seamless demo
      useSpeechSynthFallback = true;
      totalTimeDisplay.textContent = "00:45";
    }
  }

  // Play / Pause Toggle
  playPauseBtn.addEventListener("click", () => {
    if (isPlaying) {
      pauseAudio();
    } else {
      playAudio();
    }
  });

  function playAudio() {
    isPlaying = true;
    playIcon.style.display = "none";
    pauseIcon.style.display = "inline-block";
    waveformContainer.classList.add("playing");

    if (useSpeechSynthFallback) {
      playWebSpeech();
    } else {
      audioElement.playbackRate = playbackRate;
      audioElement.play().catch(e => {
        console.warn("Audio autoplay blocked or failed, falling back to speech synth:", e);
        playWebSpeech();
      });
    }
  }

  function pauseAudio() {
    isPlaying = false;
    playIcon.style.display = "inline-block";
    pauseIcon.style.display = "none";
    waveformContainer.classList.remove("playing");

    if (useSpeechSynthFallback && window.speechSynthesis) {
      window.speechSynthesis.pause();
    } else {
      audioElement.pause();
    }
  }

  function stopAudio() {
    isPlaying = false;
    playIcon.style.display = "inline-block";
    pauseIcon.style.display = "none";
    waveformContainer.classList.remove("playing");
    timelineSlider.value = 0;
    currentTimeDisplay.textContent = "00:00";

    if (window.speechSynthesis) {
      window.speechSynthesis.cancel();
    }
    audioElement.pause();
    audioElement.currentTime = 0;
  }

  // Web Speech Fallback Engine
  function playWebSpeech() {
    if (!("speechSynthesis" in window)) {
      showToast("Speech synthesis not supported in this browser.", true);
      return;
    }

    window.speechSynthesis.cancel();
    const script = transcriptText.textContent;
    fallbackUtterance = new SpeechSynthesisUtterance(script);
    fallbackUtterance.rate = playbackRate;
    
    const selectedLang = languageSelect.value;
    if (selectedLang === "hi" || selectedLang === "hinglish") {
      fallbackUtterance.lang = "hi-IN";
    } else if (selectedLang === "te") {
      fallbackUtterance.lang = "te-IN";
    } else if (selectedLang === "ta") {
      fallbackUtterance.lang = "ta-IN";
    } else {
      fallbackUtterance.lang = "en-IN";
    }

    fallbackUtterance.onend = () => {
      pauseAudio();
      timelineSlider.value = 100;
    };

    fallbackUtterance.onerror = () => {
      pauseAudio();
    };

    window.speechSynthesis.speak(fallbackUtterance);

    // Simulate progress bar for speech synth
    const estimatedDuration = Math.max(15, script.length / 15);
    const start = Date.now();
    const interval = setInterval(() => {
      if (!isPlaying) {
        clearInterval(interval);
        return;
      }
      const elapsed = (Date.now() - start) / 1000;
      const progress = Math.min((elapsed / estimatedDuration) * 100, 100);
      timelineSlider.value = progress;
      currentTimeDisplay.textContent = formatTime(elapsed);
      totalTimeDisplay.textContent = formatTime(estimatedDuration);
      if (progress >= 100) {
        clearInterval(interval);
      }
    }, 200);
  }

  // Audio Element Listeners
  audioElement.addEventListener("timeupdate", () => {
    if (!useSpeechSynthFallback && audioElement.duration) {
      const progress = (audioElement.currentTime / audioElement.duration) * 100;
      timelineSlider.value = progress;
      currentTimeDisplay.textContent = formatTime(audioElement.currentTime);
      totalTimeDisplay.textContent = formatTime(audioElement.duration);
    }
  });

  audioElement.addEventListener("ended", () => {
    pauseAudio();
  });

  // Timeline Scrubbing
  timelineSlider.addEventListener("input", (e) => {
    if (!useSpeechSynthFallback && audioElement.duration) {
      const seekTime = (e.target.value / 100) * audioElement.duration;
      audioElement.currentTime = seekTime;
    }
  });

  // Speed Multiplier
  speedBtn.addEventListener("click", () => {
    if (playbackRate === 1.0) playbackRate = 1.25;
    else if (playbackRate === 1.25) playbackRate = 1.5;
    else playbackRate = 1.0;

    speedBtn.textContent = `${playbackRate.toFixed(1)}x`;
    audioElement.playbackRate = playbackRate;
    if (useSpeechSynthFallback && fallbackUtterance) {
      fallbackUtterance.rate = playbackRate;
    }
  });

  // Transcript Drawer Toggle
  transcriptToggleBtn.addEventListener("click", () => {
    transcriptDrawer.classList.toggle("open");
  });

  // Tab Switching
  tabButtons.forEach(btn => {
    btn.addEventListener("click", () => {
      tabButtons.forEach(b => b.classList.remove("active"));
      tabPanels.forEach(p => p.classList.remove("active"));

      btn.classList.add("active");
      const targetId = btn.getAttribute("data-tab");
      document.getElementById(targetId).classList.add("active");
    });
  });

  // Copy Negotiation Draft
  copyNegotiationBtn.addEventListener("click", () => {
    const text = negotiationMessageBox.textContent;
    navigator.clipboard.writeText(text).then(() => {
      showToast("Negotiation draft copied to clipboard!");
    }).catch(() => {
      showToast("Failed to copy text", true);
    });
  });

  // Helpers
  function formatTime(seconds) {
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  }

  function showToast(message, isError = false) {
    toastMessage.textContent = message;
    toastNotification.style.borderColor = isError ? "rgba(239, 68, 68, 0.4)" : "rgba(16, 185, 129, 0.4)";
    toastNotification.classList.add("show");
    setTimeout(() => {
      toastNotification.classList.remove("show");
    }, 3200);
  }

  function escapeHtml(str) {
    if (!str) return "";
    return str
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#039;");
  }
});
