// Key Dynamics Solutions - Standalone Client-side In-Browser Engine
// Enables 100% serverless Word generation on GitHub Pages and static web hosting!

(function() {
  // Check if we are running in standalone mode (no backend or backend failed)
  window.generateDocxClientSide = async function(resumeData, options = {}) {
    if (!window.docx) {
      throw new Error("docx library not loaded from CDN");
    }

    const { Document, Packer, Paragraph, TextRun, Header, ImageRun, Table, TableRow, TableCell, AlignmentType, WidthType, BorderStyle } = docx;

    const logoB64 = options.custom_logo_data || window.DEFAULT_LOGO_B64;
    const headerAlignment = options.header_alignment || "dual";
    const headerTagline = options.header_tagline || "CONFIDENTIAL CANDIDATE DOSSIER | KEY DYNAMICS SOLUTIONS";
    const logoWidth = parseFloat(options.logo_width || 2.3);

    // Color definitions
    const colors = {
      primary: "18227C",     // Deep Navy
      accent: "00B5B8",      // Vibrant Cyan
      secondary: "475569",   // Slate Grey
      text: "1E293B"         // Charcoal Text
    };

    // Convert base64 logo to Uint8Array
    function b64ToUint8Array(b64) {
      const cleanB64 = b64.includes(",") ? b64.split(",")[1] : b64;
      const binaryString = atob(cleanB64);
      const len = binaryString.length;
      const bytes = new Uint8Array(len);
      for (let i = 0; i < len; i++) {
        bytes[i] = binaryString.charCodeAt(i);
      }
      return bytes;
    }

    const logoBytes = b64ToUint8Array(logoB64);

    // Header Construction
    const headerChildren = [];

    const logoImageRun = new ImageRun({
      data: logoBytes,
      transformation: {
        width: Math.round(logoWidth * 96),
        height: Math.round((logoWidth * 96) / 3.22)
      }
    });

    if (headerAlignment === "dual") {
      headerChildren.push(
        new Table({
          width: { size: 100, type: WidthType.PERCENTAGE },
          borders: {
            top: { style: BorderStyle.NONE },
            bottom: { style: BorderStyle.NONE },
            left: { style: BorderStyle.NONE },
            right: { style: BorderStyle.NONE },
            insideHorizontal: { style: BorderStyle.NONE },
            insideVertical: { style: BorderStyle.NONE }
          },
          rows: [
            new TableRow({
              children: [
                new TableCell({
                  width: { size: 60, type: WidthType.PERCENTAGE },
                  children: [new Paragraph({ children: [logoImageRun] })]
                }),
                new TableCell({
                  width: { size: 40, type: WidthType.PERCENTAGE },
                  children: [
                    new Paragraph({
                      alignment: AlignmentType.RIGHT,
                      children: [
                        new TextRun({
                          text: headerTagline,
                          font: "Calibri",
                          size: 15,
                          bold: true,
                          color: colors.secondary
                        })
                      ]
                    })
                  ]
                })
              ]
            })
          ]
        })
      );
    } else {
      let align = AlignmentType.RIGHT;
      if (headerAlignment === "left") align = AlignmentType.LEFT;
      if (headerAlignment === "center") align = AlignmentType.CENTER;

      headerChildren.push(
        new Paragraph({
          alignment: align,
          children: [logoImageRun]
        })
      );
      if (headerTagline) {
        headerChildren.push(
          new Paragraph({
            alignment: align,
            spacing: { before: 80, after: 100 },
            children: [
              new TextRun({
                text: headerTagline,
                font: "Calibri",
                size: 15,
                bold: true,
                color: colors.secondary
              })
            ]
          })
        );
      }
    }

    // Divider line under header
    headerChildren.push(
      new Paragraph({
        border: {
          bottom: { color: colors.accent, space: 4, value: "single", size: 12 }
        }
      })
    );

    // Document Body
    const bodyChildren = [];

    // Candidate Name
    bodyChildren.push(
      new Paragraph({
        spacing: { before: 120, after: 40 },
        children: [
          new TextRun({
            text: (resumeData.full_name || "CANDIDATE NAME").toUpperCase(),
            font: "Calibri",
            size: 40,
            bold: true,
            color: colors.primary
          })
        ]
      })
    );

    // Target Title
    if (resumeData.target_title) {
      bodyChildren.push(
        new Paragraph({
          spacing: { before: 0, after: 80 },
          children: [
            new TextRun({
              text: resumeData.target_title,
              font: "Calibri",
              size: 24,
              bold: true,
              color: colors.accent
            })
          ]
        })
      );
    }

    // Contact details line
    const contact = resumeData.contact || {};
    const contactParts = [
      contact.email,
      contact.phone,
      contact.location,
      contact.linkedin,
      contact.website
    ].filter(Boolean);

    if (contactParts.length > 0) {
      bodyChildren.push(
        new Paragraph({
          spacing: { before: 0, after: 200 },
          children: [
            new TextRun({
              text: contactParts.join("   |   "),
              font: "Calibri",
              size: 19,
              color: colors.secondary
            })
          ]
        })
      );
    }

    // Helper for Section Headings
    function addSectionHeader(title) {
      bodyChildren.push(
        new Paragraph({
          spacing: { before: 240, after: 100 },
          border: {
            bottom: { color: colors.primary, space: 4, value: "single", size: 12 }
          },
          children: [
            new TextRun({
              text: title.toUpperCase(),
              font: "Calibri",
              size: 23,
              bold: true,
              color: colors.primary
            })
          ]
        })
      );
    }

    // Summary
    if (resumeData.summary) {
      addSectionHeader("Professional Summary");
      bodyChildren.push(
        new Paragraph({
          spacing: { before: 80, after: 160 },
          children: [
            new TextRun({
              text: resumeData.summary,
              font: "Calibri",
              size: 21,
              color: colors.text
            })
          ]
        })
      );
    }

    // Core Skills
    if (resumeData.skills && resumeData.skills.length > 0) {
      addSectionHeader("Core Competencies & Skills");
      const skillsRows = [];
      const cols = 3;
      for (let i = 0; i < resumeData.skills.length; i += cols) {
        const rowCells = [];
        for (let j = 0; j < cols; j++) {
          const sk = resumeData.skills[i + j] || "";
          rowCells.push(
            new TableCell({
              width: { size: 33, type: WidthType.PERCENTAGE },
              borders: {
                top: { style: BorderStyle.NONE },
                bottom: { style: BorderStyle.NONE },
                left: { style: BorderStyle.NONE },
                right: { style: BorderStyle.NONE }
              },
              children: [
                new Paragraph({
                  spacing: { before: 40, after: 40 },
                  children: sk ? [
                    new TextRun({ text: "▪  ", font: "Calibri", size: 19, color: colors.accent }),
                    new TextRun({ text: sk, font: "Calibri", size: 20, color: colors.text })
                  ] : []
                })
              ]
            })
          );
        }
        skillsRows.push(new TableRow({ children: rowCells }));
      }

      bodyChildren.push(
        new Table({
          width: { size: 100, type: WidthType.PERCENTAGE },
          borders: {
            top: { style: BorderStyle.NONE },
            bottom: { style: BorderStyle.NONE },
            left: { style: BorderStyle.NONE },
            right: { style: BorderStyle.NONE },
            insideHorizontal: { style: BorderStyle.NONE },
            insideVertical: { style: BorderStyle.NONE }
          },
          rows: skillsRows
        })
      );
    }

    // Experience
    if (resumeData.experience && resumeData.experience.length > 0) {
      addSectionHeader("Professional Experience");
      resumeData.experience.forEach(exp => {
        bodyChildren.push(
          new Table({
            width: { size: 100, type: WidthType.PERCENTAGE },
            borders: {
              top: { style: BorderStyle.NONE },
              bottom: { style: BorderStyle.NONE },
              left: { style: BorderStyle.NONE },
              right: { style: BorderStyle.NONE },
              insideHorizontal: { style: BorderStyle.NONE },
              insideVertical: { style: BorderStyle.NONE }
            },
            rows: [
              new TableRow({
                children: [
                  new TableCell({
                    width: { size: 70, type: WidthType.PERCENTAGE },
                    children: [
                      new Paragraph({
                        spacing: { before: 80, after: 40 },
                        children: [
                          new TextRun({ text: exp.title || "Professional Role", font: "Calibri", size: 22, bold: true, color: colors.primary }),
                          exp.company ? new TextRun({ text: `  |  ${exp.company}`, font: "Calibri", size: 21, bold: true, color: colors.secondary }) : new TextRun("")
                        ]
                      })
                    ]
                  }),
                  new TableCell({
                    width: { size: 30, type: WidthType.PERCENTAGE },
                    children: [
                      new Paragraph({
                        alignment: AlignmentType.RIGHT,
                        spacing: { before: 80, after: 40 },
                        children: [
                          new TextRun({ text: exp.dates || "", font: "Calibri", size: 19, italics: true, color: colors.secondary })
                        ]
                      })
                    ]
                  })
                ]
              })
            ]
          })
        );

        // Bullets
        (exp.bullets || []).forEach(b => {
          if (!b.trim()) return;
          bodyChildren.push(
            new Paragraph({
              indent: { left: 360 },
              spacing: { before: 30, after: 40 },
              children: [
                new TextRun({ text: "•  ", font: "Calibri", bold: true, color: colors.accent }),
                new TextRun({ text: b.trim(), font: "Calibri", size: 20, color: colors.text })
              ]
            })
          );
        });
      });
    }

    // Education
    if (resumeData.education && resumeData.education.length > 0) {
      addSectionHeader("Education & Credentials");
      resumeData.education.forEach(edu => {
        bodyChildren.push(
          new Paragraph({
            spacing: { before: 60, after: 30 },
            children: [
              new TextRun({ text: edu.degree || "Degree", font: "Calibri", size: 21, bold: true, color: colors.primary }),
              edu.institution ? new TextRun({ text: ` — ${edu.institution}`, font: "Calibri", size: 20, color: colors.secondary }) : new TextRun(""),
              edu.dates ? new TextRun({ text: `   (${edu.dates})`, font: "Calibri", size: 19, italics: true, color: colors.secondary }) : new TextRun("")
            ]
          })
        );
        if (edu.details) {
          bodyChildren.push(
            new Paragraph({
              indent: { left: 240 },
              spacing: { before: 0, after: 40 },
              children: [
                new TextRun({ text: edu.details, font: "Calibri", size: 19, color: colors.text })
              ]
            })
          );
        }
      });
    }

    // Certifications
    if (resumeData.certifications && resumeData.certifications.length > 0) {
      addSectionHeader("Certifications & Honors");
      resumeData.certifications.forEach(cert => {
        bodyChildren.push(
          new Paragraph({
            indent: { left: 240 },
            spacing: { before: 30, after: 40 },
            children: [
              new TextRun({ text: "✔  ", font: "Calibri", color: colors.accent }),
              new TextRun({ text: cert, font: "Calibri", size: 20, color: colors.text })
            ]
          })
        );
      });
    }

    // Assemble Document
    const doc = new Document({
      sections: [
        {
          properties: {
            page: {
              margin: {
                top: 1100,
                bottom: 1100,
                left: 1100,
                right: 1100
              }
            }
          },
          headers: {
            default: new Header({
              children: headerChildren
            })
          },
          children: bodyChildren
        }
      ]
    });

    const blob = await Packer.toBlob(doc);
    return blob;
  };

  // Override or augment app.js Word download function if fetch to server fails (e.g. on GitHub Pages)
  window.addEventListener("DOMContentLoaded", () => {
    const originalBtn = document.getElementById("generateDocxBtn");
    const originalBtnBottom = document.getElementById("generateDocxBtnBottom");
    const modalDownloadLink = document.getElementById("modalDownloadLink");

    // Intercept generation to support pure client-side if running on GitHub Pages
    const isGitHubPages = window.location.hostname.includes("github.io") || window.location.protocol === "file:";

    if (isGitHubPages) {
      console.log("Running in 100% Client-Side Mode (GitHub Pages / Standalone)");
      
      async function handleClientSideDownload() {
        const candidateData = {
          full_name: document.getElementById("candFullName").value.trim() || "Candidate Name",
          target_title: document.getElementById("candTitle").value.trim(),
          contact: {
            email: document.getElementById("candEmail").value.trim(),
            phone: document.getElementById("candPhone").value.trim(),
            location: document.getElementById("candLocation").value.trim(),
            linkedin: document.getElementById("candLinkedin").value.trim()
          },
          summary: document.getElementById("candSummary").value.trim(),
          skills: window.skillsList || [],
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

        const safeName = (candidateData.full_name || "Resume").replace(/\\s+/g, "_").replace(/[^a-zA-Z0-9_]/g, "");
        const docFilename = `${safeName}_KeyDynamics_Resume.docx`;

        try {
          const blob = await window.generateDocxClientSide(candidateData, {
            header_alignment: window.currentAlignment || "dual",
            header_tagline: document.getElementById("headerTaglineInput").value.trim(),
            logo_width: parseFloat(document.getElementById("logoSizeRange").value || 2.3)
          });

          // Trigger download
          saveAs(blob, docFilename);

          document.getElementById("modalDocName").textContent = docFilename;
          document.getElementById("downloadModal").style.display = "flex";
        } catch (err) {
          alert("Error building Word document: " + err.message);
        }
      }

      if (originalBtn) originalBtn.onclick = handleClientSideDownload;
      if (originalBtnBottom) originalBtnBottom.onclick = handleClientSideDownload;
    }
  });

})();
