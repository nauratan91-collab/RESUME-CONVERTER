// Key Dynamics Solutions - Resume Studio Client Application

document.addEventListener("DOMContentLoaded", () => {
  // Elements
  const dropzone = document.getElementById("dropzone");
  const resumeFileInput = document.getElementById("resumeFileInput");
  const browseFileBtn = document.getElementById("browseFileBtn");
  const dropzoneContent = document.getElementById("dropzoneContent");
  const processingState = document.getElementById("processingState");
  const activeFileStrip = document.getElementById("activeFileStrip");
  const activeFileName = document.getElementById("activeFileName");
  const activeFileType = document.getElementById("activeFileType");
  const clearFileBtn = document.getElementById("clearFileBtn");
  const ocrAlert = document.getElementById("ocrAlert");

  // Header Styler Elements
  const headerMockup = document.getElementById("headerMockup");
  const headerMockupImg = document.getElementById("headerMockupImg");
  const mockupTaglineText = document.getElementById("mockupTaglineText");
  const mockupDivider = document.getElementById("mockupDivider");
  const headerAlignSegment = document.getElementById("headerAlignSegment");
  const headerTaglineInput = document.getElementById("headerTaglineInput");
  const themeSelect = document.getElementById("themeSelect");
  const logoSizeRange = document.getElementById("logoSizeRange");
  const logoSizeLabel = document.getElementById("logoSizeLabel");
  const customLogoInput = document.getElementById("customLogoInput");
  const resetLogoBtn = document.getElementById("resetLogoBtn");

  // Editor Form Fields
  const candFullName = document.getElementById("candFullName");
  const candTitle = document.getElementById("candTitle");
  const candEmail = document.getElementById("candEmail");
  const candPhone = document.getElementById("candPhone");
  const candLocation = document.getElementById("candLocation");
  const candLinkedin = document.getElementById("candLinkedin");
  const candSummary = document.getElementById("candSummary");
  const skillsContainer = document.getElementById("skillsContainer");
  const newSkillInput = document.getElementById("newSkillInput");
  const confirmAddSkillBtn = document.getElementById("confirmAddSkillBtn");
  const experienceContainer = document.getElementById("experienceContainer");
  const addExpBtn = document.getElementById("addExpBtn");
  const educationContainer = document.getElementById("educationContainer");
  const addEduBtn = document.getElementById("addEduBtn");
  const certsContainer = document.getElementById("certsContainer");
  const addCertBtn = document.getElementById("addCertBtn");
  const rawExtractedText = document.getElementById("rawExtractedText");

  // Buttons & Modals
  const generateDocxBtn = document.getElementById("generateDocxBtn");
  const generateDocxBtnBottom = document.getElementById("generateDocxBtnBottom");
  const downloadModal = document.getElementById("downloadModal");
  const closeModalBtn = document.getElementById("closeModalBtn");
  const modalDismissBtn = document.getElementById("modalDismissBtn");
  const modalDownloadLink = document.getElementById("modalDownloadLink");
  const modalDocName = document.getElementById("modalDocName");

  const settingsModal = document.getElementById("settingsModal");
  const openSettingsBtn = document.getElementById("openSettingsBtn");
  const closeSettingsBtn = document.getElementById("closeSettingsBtn");
  const cancelSettingsBtn = document.getElementById("cancelSettingsBtn");
  const saveSettingsBtn = document.getElementById("saveSettingsBtn");
  const geminiApiKeyInput = document.getElementById("geminiApiKeyInput");
  const loadSampleBtn = document.getElementById("loadSampleBtn");

  // State
  let currentAlignment = "dual";
  let customLogoBase64 = null;
  let skillsList = [];

  // Init Gemini API Key from localStorage
  const savedApiKey = localStorage.getItem("GEMINI_API_KEY") || "";
  if (geminiApiKeyInput) geminiApiKeyInput.value = savedApiKey;

  // 1. HEADER CONTROLS & LIVE PREVIEW
  function updateHeaderMockup() {
    headerMockup.className = `word-header-mockup align-${currentAlignment}`;
    mockupTaglineText.textContent = headerTaglineInput.value || "";

    // Adjust theme color on divider
    const theme = themeSelect.value;
    if (theme === "key_dynamics") {
      mockupDivider.style.backgroundColor = "#00b5b8";
    } else if (theme === "modern_teal") {
      mockupDivider.style.backgroundColor = "#06b6d4";
    } else if (theme === "classic_blue") {
      mockupDivider.style.backgroundColor = "#3b82f6";
    } else {
      mockupDivider.style.backgroundColor = "#64748b";
    }

    // Logo size
    const inches = parseFloat(logoSizeRange.value);
    logoSizeLabel.textContent = `${inches.toFixed(1)}"`;
    headerMockupImg.style.width = `${inches * 42}px`;
  }

  // Segmented control click
  headerAlignSegment.querySelectorAll(".seg-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      headerAlignSegment.querySelectorAll(".seg-btn").forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      currentAlignment = btn.dataset.align;
      updateHeaderMockup();
    });
  });

  headerTaglineInput.addEventListener("input", updateHeaderMockup);
  themeSelect.addEventListener("change", updateHeaderMockup);
  logoSizeRange.addEventListener("input", updateHeaderMockup);

  // Custom Logo upload & preview
  customLogoInput.addEventListener("change", (e) => {
    const file = e.target.files[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = (event) => {
      customLogoBase64 = event.target.result;
      headerMockupImg.src = customLogoBase64;
    };
    reader.readAsDataURL(file);
  });

  resetLogoBtn.addEventListener("click", () => {
    customLogoBase64 = null;
    headerMockupImg.src = "/static/images/company_logo.png";
    customLogoInput.value = "";
  });

  updateHeaderMockup();

  // 2. FILE UPLOAD HANDLING
  browseFileBtn.addEventListener("click", (e) => {
    e.stopPropagation();
    resumeFileInput.click();
  });

  dropzone.addEventListener("click", () => {
    resumeFileInput.click();
  });

  dropzone.addEventListener("dragover", (e) => {
    e.preventDefault();
    dropzone.classList.add("drag-active");
  });

  dropzone.addEventListener("dragleave", () => {
    dropzone.classList.remove("drag-active");
  });

  dropzone.addEventListener("drop", (e) => {
    e.preventDefault();
    dropzone.classList.remove("drag-active");
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      handleFileUpload(e.dataTransfer.files[0]);
    }
  });

  resumeFileInput.addEventListener("change", (e) => {
    if (e.target.files && e.target.files.length > 0) {
      handleFileUpload(e.target.files[0]);
    }
  });

  clearFileBtn.addEventListener("click", () => {
    resumeFileInput.value = "";
    activeFileStrip.style.display = "none";
    dropzoneContent.style.display = "block";
    processingState.style.display = "none";
  });

  async function handleFileUpload(file) {
    dropzoneContent.style.display = "none";
    processingState.style.display = "block";
    activeFileStrip.style.display = "none";
    ocrAlert.style.display = "none";

    const formData = new FormData();
    formData.append("file", file);

    const apiKey = localStorage.getItem("GEMINI_API_KEY") || "";
    if (apiKey) {
      formData.append("gemini_api_key", apiKey);
    }

    try {
      const response = await fetch("/api/upload", {
        method: "POST",
        body: formData
      });

      const data = await response.json();
      processingState.style.display = "none";

      if (!response.ok || !data.success) {
        alert("Upload error: " + (data.error || "Failed to process resume file"));
        dropzoneContent.style.display = "block";
        return;
      }

      // Show active file badge
      activeFileName.textContent = file.name;
      activeFileType.textContent = `${(file.size / 1024).toFixed(1)} KB • ${file.type || "Document"}`;
      activeFileStrip.style.display = "flex";

      if (data.requires_ocr && !data.ai_parsed) {
        ocrAlert.style.display = "flex";
      }

      // Populate structured resume
      populateEditor(data.structured_data, data.raw_text);

    } catch (err) {
      processingState.style.display = "none";
      dropzoneContent.style.display = "block";
      alert("Error uploading file: " + err.message);
    }
  }

  // 3. POPULATE RESUME EDITOR
  function populateEditor(res, rawText = "") {
    if (!res) return;

    candFullName.value = res.full_name || "";
    candTitle.value = res.target_title || "";

    const contact = res.contact || {};
    candEmail.value = contact.email || "";
    candPhone.value = contact.phone || "";
    candLocation.value = contact.location || "";
    candLinkedin.value = contact.linkedin || "";

    candSummary.value = res.summary || "";

    // Skills
    skillsList = res.skills || [];
    renderSkills();

    // Experiences
    renderExperienceList(res.experience || []);

    // Education
    renderEducationList(res.education || []);

    // Certifications
    renderCertificationsList(res.certifications || []);

    // Raw text
    if (rawExtractedText) {
      rawExtractedText.value = rawText || "";
    }
  }

  // SKILLS TAGS
  function renderSkills() {
    skillsContainer.innerHTML = "";
    skillsList.forEach((skill, idx) => {
      const tag = document.createElement("span");
      tag.className = "skill-tag";
      tag.innerHTML = `
        <span>${escapeHtml(skill)}</span>
        <button type="button" data-idx="${idx}" title="Remove skill">&times;</button>
      `;
      tag.querySelector("button").addEventListener("click", () => {
        skillsList.splice(idx, 1);
        renderSkills();
      });
      skillsContainer.appendChild(tag);
    });
  }

  function addSkill(skillName) {
    const trimmed = skillName.trim();
    if (trimmed && !skillsList.includes(trimmed)) {
      skillsList.push(trimmed);
      renderSkills();
    }
  }

  confirmAddSkillBtn.addEventListener("click", () => {
    addSkill(newSkillInput.value);
    newSkillInput.value = "";
  });

  newSkillInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter") {
      e.preventDefault();
      addSkill(newSkillInput.value);
      newSkillInput.value = "";
    }
  });

  // WORK EXPERIENCE BUILDER
  function renderExperienceList(expList) {
    experienceContainer.innerHTML = "";
    if (!expList || expList.length === 0) {
      addExperienceItem({ title: "", company: "", dates: "", location: "", bullets: [""] });
      return;
    }
    expList.forEach(exp => addExperienceItem(exp));
  }

  function addExperienceItem(exp = {}) {
    const itemCard = document.createElement("div");
    itemCard.className = "item-card exp-card";
    
    const bulletsHtml = (exp.bullets && exp.bullets.length > 0 ? exp.bullets : [""])
      .map(b => `
        <div class="bullet-item-row">
          <input type="text" class="form-input bullet-input" value="${escapeHtml(b)}" placeholder="Describe accomplishment or responsibility...">
          <button type="button" class="bullet-remove-btn" title="Remove bullet"><i class="fa-solid fa-trash-can"></i></button>
        </div>
      `).join("");

    itemCard.innerHTML = `
      <button type="button" class="item-delete-btn" title="Delete job"><i class="fa-solid fa-trash-can"></i></button>
      <div class="grid-2-swap">
        <div class="form-group flex-1">
          <label><i class="fa-solid fa-briefcase text-cyan"></i> Job Title / Role</label>
          <input type="text" class="form-input exp-title" value="${escapeHtml(exp.title || '')}" placeholder="e.g. Director of Operations">
        </div>
        <button type="button" class="btn-swap-single" title="Swap Title ⇄ Company"><i class="fa-solid fa-right-left"></i></button>
        <div class="form-group flex-1">
          <label><i class="fa-solid fa-building text-indigo"></i> Company / Organization</label>
          <input type="text" class="form-input exp-company" value="${escapeHtml(exp.company || '')}" placeholder="e.g. Key Dynamics Solutions">
        </div>
      </div>
      <div class="grid-2 mt-2">
        <div class="form-group">
          <label>Dates / Duration</label>
          <input type="text" class="form-input exp-dates" value="${escapeHtml(exp.dates || '')}" placeholder="e.g. 2021 - Present">
        </div>
        <div class="form-group">
          <label>Location</label>
          <input type="text" class="form-input exp-location" value="${escapeHtml(exp.location || '')}" placeholder="e.g. Dallas, TX">
        </div>
      </div>
      <div class="mt-3">
        <label>Key Responsibilities & Achievements</label>
        <div class="bullets-container">
          ${bulletsHtml}
        </div>
        <button type="button" class="add-bullet-link"><i class="fa-solid fa-plus"></i> Add Bullet Point</button>
      </div>
    `;

    // Hook up single swap button
    const swapBtn = itemCard.querySelector(".btn-swap-single");
    if (swapBtn) {
      swapBtn.addEventListener("click", () => {
        const titleInput = itemCard.querySelector(".exp-title");
        const compInput = itemCard.querySelector(".exp-company");
        const temp = titleInput.value;
        titleInput.value = compInput.value;
        compInput.value = temp;
        titleInput.classList.add("input-swapped");
        compInput.classList.add("input-swapped");
        setTimeout(() => {
          titleInput.classList.remove("input-swapped");
          compInput.classList.remove("input-swapped");
        }, 500);
      });
    }

    // Hook up delete job
    itemCard.querySelector(".item-delete-btn").addEventListener("click", () => {
      itemCard.remove();
    });

    // Hook up add bullet
    const bulletsWrap = itemCard.querySelector(".bullets-container");
    itemCard.querySelector(".add-bullet-link").addEventListener("click", () => {
      const row = document.createElement("div");
      row.className = "bullet-item-row";
      row.innerHTML = `
        <input type="text" class="form-input bullet-input" placeholder="Describe accomplishment...">
        <button type="button" class="bullet-remove-btn" title="Remove bullet"><i class="fa-solid fa-trash-can"></i></button>
      `;
      row.querySelector(".bullet-remove-btn").addEventListener("click", () => row.remove());
      bulletsWrap.appendChild(row);
      row.querySelector("input").focus();
    });

    // Hook up remove bullet buttons
    itemCard.querySelectorAll(".bullet-remove-btn").forEach(btn => {
      btn.addEventListener("click", (e) => {
        e.target.closest(".bullet-item-row").remove();
      });
    });

    experienceContainer.appendChild(itemCard);
  }

  addExpBtn.addEventListener("click", () => {
    addExperienceItem({ title: "", company: "", dates: "", location: "", bullets: [""] });
  });

  // Global Swap all roles Title <-> Company
  const swapAllExpBtn = document.getElementById("swapAllExpBtn");
  if (swapAllExpBtn) {
    swapAllExpBtn.addEventListener("click", () => {
      const cards = document.querySelectorAll(".exp-card");
      if (cards.length === 0) return;
      cards.forEach(card => {
        const titleInput = card.querySelector(".exp-title");
        const compInput = card.querySelector(".exp-company");
        if (titleInput && compInput) {
          const temp = titleInput.value;
          titleInput.value = compInput.value;
          compInput.value = temp;
          titleInput.classList.add("input-swapped");
          compInput.classList.add("input-swapped");
          setTimeout(() => {
            titleInput.classList.remove("input-swapped");
            compInput.classList.remove("input-swapped");
          }, 500);
        }
      });
    });
  }

  // Swap Name <-> Title
  const swapNameTitleBtn = document.getElementById("swapNameTitleBtn");
  if (swapNameTitleBtn) {
    swapNameTitleBtn.addEventListener("click", () => {
      const temp = candFullName.value;
      candFullName.value = candTitle.value;
      candTitle.value = temp;
      candFullName.classList.add("input-swapped");
      candTitle.classList.add("input-swapped");
      setTimeout(() => {
        candFullName.classList.remove("input-swapped");
        candTitle.classList.remove("input-swapped");
      }, 500);
    });
  }

  // EDUCATION BUILDER
  function renderEducationList(eduList) {
    educationContainer.innerHTML = "";
    if (!eduList || eduList.length === 0) {
      addEducationItem({ degree: "", institution: "", dates: "", details: "" });
      return;
    }
    eduList.forEach(edu => addEducationItem(edu));
  }

  function addEducationItem(edu = {}) {
    const itemCard = document.createElement("div");
    itemCard.className = "item-card edu-card";
    itemCard.innerHTML = `
      <button type="button" class="item-delete-btn" title="Delete degree"><i class="fa-solid fa-trash-can"></i></button>
      <div class="grid-2">
        <div class="form-group">
          <label>Degree / Qualification</label>
          <input type="text" class="form-input edu-degree" value="${escapeHtml(edu.degree || '')}" placeholder="e.g. B.S. in Computer Science">
        </div>
        <div class="form-group">
          <label>Institution / University</label>
          <input type="text" class="form-input edu-inst" value="${escapeHtml(edu.institution || '')}" placeholder="e.g. University of Texas">
        </div>
      </div>
      <div class="grid-2 mt-2">
        <div class="form-group">
          <label>Graduation Year / Dates</label>
          <input type="text" class="form-input edu-dates" value="${escapeHtml(edu.dates || '')}" placeholder="e.g. 2016 - 2020">
        </div>
        <div class="form-group">
          <label>Honors / Details</label>
          <input type="text" class="form-input edu-details" value="${escapeHtml(edu.details || '')}" placeholder="e.g. Summa Cum Laude, GPA 3.9">
        </div>
      </div>
    `;

    itemCard.querySelector(".item-delete-btn").addEventListener("click", () => {
      itemCard.remove();
    });

    educationContainer.appendChild(itemCard);
  }

  addEduBtn.addEventListener("click", () => {
    addEducationItem({ degree: "", institution: "", dates: "", details: "" });
  });

  // CERTIFICATIONS BUILDER
  function renderCertificationsList(certs) {
    certsContainer.innerHTML = "";
    certs.forEach(cert => addCertItem(cert));
  }

  function addCertItem(certText = "") {
    const row = document.createElement("div");
    row.className = "bullet-item-row";
    row.innerHTML = `
      <input type="text" class="form-input cert-input" value="${escapeHtml(certText)}" placeholder="e.g. AWS Certified Solutions Architect">
      <button type="button" class="bullet-remove-btn" title="Remove certification"><i class="fa-solid fa-trash-can"></i></button>
    `;
    row.querySelector(".bullet-remove-btn").addEventListener("click", () => row.remove());
    certsContainer.appendChild(row);
  }

  addCertBtn.addEventListener("click", () => {
    addCertItem("");
  });

  // 4. GENERATE WORD (.DOCX) DOCUMENT
  async function triggerDocxGeneration() {
    // Collect data from form
    const candidateData = {
      full_name: candFullName.value.trim() || "Candidate Name",
      target_title: candTitle.value.trim(),
      contact: {
        email: candEmail.value.trim(),
        phone: candPhone.value.trim(),
        location: candLocation.value.trim(),
        linkedin: candLinkedin.value.trim()
      },
      summary: candSummary.value.trim(),
      skills: skillsList,
      experience: [],
      education: [],
      certifications: []
    };

    // Collect Experience
    document.querySelectorAll(".exp-card").forEach(card => {
      const title = card.querySelector(".exp-title").value.trim();
      const company = card.querySelector(".exp-company").value.trim();
      const dates = card.querySelector(".exp-dates").value.trim();
      const location = card.querySelector(".exp-location").value.trim();
      const bullets = [];
      card.querySelectorAll(".bullet-input").forEach(b => {
        if (b.value.trim()) bullets.push(b.value.trim());
      });
      if (title || company) {
        candidateData.experience.push({ title, company, dates, location, bullets });
      }
    });

    // Collect Education
    document.querySelectorAll(".edu-card").forEach(card => {
      const degree = card.querySelector(".edu-degree").value.trim();
      const institution = card.querySelector(".edu-inst").value.trim();
      const dates = card.querySelector(".edu-dates").value.trim();
      const details = card.querySelector(".edu-details").value.trim();
      if (degree || institution) {
        candidateData.education.push({ degree, institution, dates, details });
      }
    });

    // Collect Certifications
    document.querySelectorAll(".cert-input").forEach(input => {
      if (input.value.trim()) candidateData.certifications.push(input.value.trim());
    });

    const payload = {
      resume_data: candidateData,
      header_alignment: currentAlignment,
      header_tagline: headerTaglineInput.value.trim(),
      palette_name: themeSelect.value,
      logo_width: parseFloat(logoSizeRange.value),
      custom_logo_data: customLogoBase64
    };

    const originalText = generateDocxBtn.innerHTML;
    generateDocxBtn.innerHTML = `<i class="fa-solid fa-spinner fa-spin"></i> Building .docx...`;
    generateDocxBtn.disabled = true;
    generateDocxBtnBottom.innerHTML = `<i class="fa-solid fa-spinner fa-spin"></i> Building .docx...`;
    generateDocxBtnBottom.disabled = true;

    try {
      const res = await fetch("/api/generate-docx", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });

      const result = await res.json();
      generateDocxBtn.innerHTML = originalText;
      generateDocxBtn.disabled = false;
      generateDocxBtnBottom.innerHTML = `<i class="fa-solid fa-file-word"></i> Generate & Download Word Document`;
      generateDocxBtnBottom.disabled = false;

      if (!res.ok || !result.success) {
        alert("Failed to create Word document: " + (result.error || "Unknown error"));
        return;
      }

      // Show download modal
      modalDocName.textContent = result.filename;
      modalDownloadLink.href = result.download_url;
      modalDownloadLink.setAttribute("download", result.filename);
      downloadModal.style.display = "flex";

      // Also trigger automatic download
      const tempLink = document.createElement("a");
      tempLink.href = result.download_url;
      tempLink.download = result.filename;
      document.body.appendChild(tempLink);
      tempLink.click();
      document.body.removeChild(tempLink);

    } catch (err) {
      generateDocxBtn.innerHTML = originalText;
      generateDocxBtn.disabled = false;
      generateDocxBtnBottom.innerHTML = `<i class="fa-solid fa-file-word"></i> Generate & Download Word Document`;
      generateDocxBtnBottom.disabled = false;
      alert("Error: " + err.message);
    }
  }

  generateDocxBtn.addEventListener("click", triggerDocxGeneration);
  generateDocxBtnBottom.addEventListener("click", triggerDocxGeneration);

  // Modal close
  closeModalBtn.addEventListener("click", () => downloadModal.style.display = "none");
  modalDismissBtn.addEventListener("click", () => downloadModal.style.display = "none");
  downloadModal.addEventListener("click", (e) => {
    if (e.target === downloadModal) downloadModal.style.display = "none";
  });

  // Settings modal
  openSettingsBtn.addEventListener("click", () => settingsModal.style.display = "flex");
  closeSettingsBtn.addEventListener("click", () => settingsModal.style.display = "none");
  cancelSettingsBtn.addEventListener("click", () => settingsModal.style.display = "none");
  saveSettingsBtn.addEventListener("click", () => {
    localStorage.setItem("GEMINI_API_KEY", geminiApiKeyInput.value.trim());
    settingsModal.style.display = "none";
    alert("Settings saved! Any uploaded scanned images or complex resumes will now use your Gemini API key.");
  });

  // LOAD SAMPLE DATA
  loadSampleBtn.addEventListener("click", () => {
    const sample = {
      full_name: "ALEXANDER MORGAN",
      target_title: "Senior Solutions Architect & Operations Director",
      contact: {
        email: "alex.morgan@keydynamics.example",
        phone: "+1 (555) 382-9910",
        location: "Dallas, TX",
        linkedin: "linkedin.com/in/alexandermorgan"
      },
      summary: "Accomplished Solutions Architect and Business Operations Leader with 12+ years of experience spearheading digital transformations, enterprise cloud migrations, and workflow automation. Expert at aligning operational processes with cutting-edge IT infrastructure to boost scalability and cut downtime.",
      skills: [
        "Cloud Architecture (AWS/GCP)", "Process Automation", "Enterprise ERP Systems",
        "DevOps & CI/CD", "Strategic Operations", "Cross-Functional Leadership",
        "Python & Go", "Cybersecurity Governance", "Agile / Scrum Master"
      ],
      experience: [
        {
          title: "Principal Solutions Architect",
          company: "Global Tech Innovations",
          dates: "2021 - Present",
          location: "Dallas, TX",
          bullets: [
            "Led end-to-end modernization of legacy infrastructure, reducing operational overhead by 34% across 8 business units.",
            "Orchestrated cross-functional teams of 25+ engineers, ensuring 99.99% system availability and strict SLA compliance.",
            "Designed automated CI/CD deployment pipelines cutting release cycles from 3 weeks to 2 hours."
          ]
        },
        {
          title: "Senior Systems Engineer",
          company: "Apex Dynamic Systems",
          dates: "2016 - 2021",
          location: "Austin, TX",
          bullets: [
            "Implemented multi-region hybrid cloud solutions handling 10M+ daily transactions with zero critical incidents.",
            "Authored operational playbooks and conducted disaster recovery drills for mission-critical distributed databases.",
            "Mentored junior architects and spearheaded cloud cost-optimization initiatives yielding $420K annual savings."
          ]
        }
      ],
      education: [
        {
          degree: "M.S. in Computer Engineering",
          institution: "University of Texas at Austin",
          dates: "2014 - 2016",
          details: "Graduated Magna Cum Laude"
        },
        {
          degree: "B.S. in Electrical & Computer Engineering",
          institution: "Texas A&M University",
          dates: "2010 - 2014",
          details: "Dean's Honor List"
        }
      ],
      certifications: [
        "AWS Certified Solutions Architect - Professional",
        "Certified Information Systems Security Professional (CISSP)",
        "TOGAF 9.2 Enterprise Architect"
      ]
    };

    populateEditor(sample, "Loaded interactive sample resume for Key Dynamics Solutions.");
    activeFileName.textContent = "sample_executive_resume.pdf";
    activeFileType.textContent = "Pre-loaded Sample Data";
    activeFileStrip.style.display = "flex";
  });

  // Helper
  function escapeHtml(text) {
    if (!text) return "";
    return String(text)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#039;");
  }

});
