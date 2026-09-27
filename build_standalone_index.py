import os
from pathlib import Path

# Load base64 logo
with open('static/images/logo_b64.txt', 'r', encoding='utf-8') as f:
    LOGO_B64 = f.read().strip()

HTML_CONTENT = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Key Dynamics Solutions | Enterprise Resume to Word (.docx) Converter</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
  
  <!-- Client-side Document Processing CDNs -->
  <script src="https://unpkg.com/docx@8.5.0/build/index.umd.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/FileSaver.js/2.0.5/FileSaver.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/mammoth/1.6.0/mammoth.browser.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/jszip/3.10.1/jszip.min.js"></script>

  <style>
    :root {{
      --primary: #18227c;
      --primary-dark: #0f1754;
      --primary-light: #2c3ca8;
      --cyan: #00b5b8;
      --cyan-dark: #008f91;
      --cyan-light: #e0f9f9;
      --orange: #f7941d;
      --bg-main: #f8fafc;
      --bg-card: #ffffff;
      --border-color: #e2e8f0;
      --border-focus: #00b5b8;
      --text-main: #0f172a;
      --text-muted: #64748b;
      --radius-sm: 6px;
      --radius-md: 10px;
      --radius-lg: 16px;
      --radius-xl: 24px;
      --shadow-sm: 0 1px 3px rgba(0,0,0,0.06);
      --shadow-md: 0 4px 14px rgba(0,0,0,0.08);
      --font-sans: 'Plus Jakarta Sans', system-ui, -apple-system, sans-serif;
      --font-mono: 'JetBrains Mono', monospace;
    }}

    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{ font-family: var(--font-sans); background-color: var(--bg-main); color: var(--text-main); line-height: 1.5; }}

    /* NAVBAR */
    .app-navbar {{ background: #ffffff; border-bottom: 1px solid var(--border-color); position: sticky; top: 0; z-index: 100; box-shadow: var(--shadow-sm); }}
    .nav-container {{ max-width: 1440px; margin: 0 auto; padding: 0.75rem 1.5rem; display: flex; align-items: center; justify-content: space-between; }}
    .brand-group {{ display: flex; align-items: center; gap: 1rem; }}
    .nav-logo {{ height: 42px; width: auto; object-fit: contain; }}
    .brand-divider {{ width: 1px; height: 32px; background-color: var(--border-color); }}
    .app-title {{ font-size: 1.1rem; font-weight: 800; color: var(--primary); letter-spacing: -0.02em; display: block; }}
    .app-subtitle {{ font-size: 0.75rem; color: var(--text-muted); font-weight: 500; display: block; }}
    .nav-actions {{ display: flex; align-items: center; gap: 0.75rem; }}

    /* BUTTONS */
    button {{ font-family: var(--font-sans); cursor: pointer; transition: all 0.2s ease; }}
    .btn-primary {{ background: linear-gradient(135deg, var(--primary) 0%, #1e3a8a 100%); color: #ffffff; border: none; padding: 0.65rem 1.25rem; border-radius: var(--radius-md); font-weight: 600; font-size: 0.9rem; display: inline-flex; align-items: center; gap: 0.5rem; box-shadow: 0 4px 12px rgba(24, 34, 124, 0.25); }}
    .btn-primary:hover {{ background: linear-gradient(135deg, var(--primary-light) 0%, var(--primary) 100%); transform: translateY(-1px); }}
    .btn-secondary {{ background: #f1f5f9; color: var(--text-main); border: 1px solid var(--border-color); padding: 0.6rem 1.1rem; border-radius: var(--radius-md); font-weight: 600; font-size: 0.85rem; display: inline-flex; align-items: center; gap: 0.5rem; }}
    .btn-secondary:hover {{ background: #e2e8f0; }}
    .btn-ghost {{ background: transparent; color: var(--text-muted); border: 1px solid transparent; padding: 0.6rem 1rem; border-radius: var(--radius-md); font-weight: 500; font-size: 0.85rem; display: inline-flex; align-items: center; gap: 0.5rem; }}
    .btn-ghost:hover {{ background: #f1f5f9; color: var(--primary); }}
    .btn-lg {{ padding: 0.85rem 1.6rem; font-size: 1rem; }}
    .btn-xs {{ background: #f8fafc; border: 1px solid var(--border-color); color: var(--primary); padding: 0.25rem 0.65rem; border-radius: var(--radius-sm); font-size: 0.75rem; font-weight: 600; }}
    .btn-xs:hover {{ background: var(--cyan-light); border-color: var(--cyan); }}
    .btn-link {{ background: none; border: none; color: var(--cyan-dark); font-size: 0.8rem; font-weight: 600; text-decoration: underline; cursor: pointer; }}
    .btn-icon {{ background: #f1f5f9; border: none; width: 32px; height: 32px; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: var(--text-muted); }}

    /* SWAP BUTTONS */
    .grid-2-swap {{ display: flex; align-items: flex-end; gap: 0.6rem; }}
    .btn-swap-single {{ background: #f1f5f9; border: 1px solid var(--border-color); color: var(--primary); height: 38px; width: 38px; border-radius: var(--radius-md); display: flex; align-items: center; justify-content: center; margin-bottom: 2px; cursor: pointer; flex-shrink: 0; transition: all 0.2s ease; }}
    .btn-swap-single:hover {{ background: var(--cyan-light); border-color: var(--cyan); color: var(--cyan-dark); transform: rotate(180deg); }}
    .input-swapped {{ background-color: #ecfeff !important; border-color: #06b6d4 !important; transition: background-color 0.4s ease; }}
    .section-actions-row {{ display: flex; align-items: center; gap: 0.5rem; }}

    /* MAIN LAYOUT */
    .main-content {{ max-width: 1440px; margin: 0 auto; padding: 2rem 1.5rem 4rem; }}
    .hero-section {{ text-align: center; margin-bottom: 2.2rem; }}
    .badge-pill {{ display: inline-flex; align-items: center; gap: 0.5rem; background: #ffffff; border: 1px solid #cbd5e1; padding: 0.35rem 1rem; border-radius: 999px; font-size: 0.8rem; font-weight: 600; color: var(--primary); margin-bottom: 1rem; box-shadow: var(--shadow-sm); }}
    .badge-dot {{ width: 8px; height: 8px; background: var(--cyan); border-radius: 50%; box-shadow: 0 0 8px var(--cyan); }}
    .hero-section h1 {{ font-size: 2.2rem; font-weight: 800; color: var(--primary); letter-spacing: -0.03em; margin-bottom: 0.5rem; }}
    .hero-section h1 span {{ color: var(--cyan-dark); background: linear-gradient(135deg, var(--cyan-dark) 0%, var(--primary) 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
    .hero-section p {{ color: var(--text-muted); font-size: 1rem; max-width: 760px; margin: 0 auto; }}

    .workflow-grid {{ display: grid; grid-template-columns: 460px 1fr; gap: 1.75rem; align-items: start; }}
    @media (max-width: 1100px) {{ .workflow-grid {{ grid-template-columns: 1fr; }} }}

    .card {{ background: var(--bg-card); border: 1px solid var(--border-color); border-radius: var(--radius-lg); box-shadow: var(--shadow-sm); overflow: hidden; margin-bottom: 1.75rem; }}
    .card-header {{ padding: 1.1rem 1.4rem; border-bottom: 1px solid var(--border-color); display: flex; align-items: center; justify-content: space-between; background: #ffffff; }}
    .card-title {{ font-size: 1.05rem; font-weight: 700; color: var(--primary); display: flex; align-items: center; gap: 0.6rem; }}
    .file-badge, .badge-status {{ font-size: 0.75rem; font-weight: 600; padding: 0.2rem 0.6rem; border-radius: var(--radius-sm); background: #f1f5f9; color: var(--text-muted); }}
    .badge-status {{ background: var(--cyan-light); color: var(--cyan-dark); }}

    /* UPLOAD ZONE */
    .dropzone {{ margin: 1.4rem; border: 2px dashed #cbd5e1; border-radius: var(--radius-md); padding: 2.2rem 1.5rem; text-align: center; background: #fafcff; cursor: pointer; transition: all 0.2s ease; }}
    .dropzone:hover, .dropzone.drag-active {{ border-color: var(--cyan); background: #f0fdfe; }}
    .upload-icon-circle {{ width: 56px; height: 56px; background: var(--cyan-light); color: var(--cyan-dark); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 1.5rem; margin: 0 auto 1rem; }}
    .dropzone h3 {{ font-size: 1.05rem; font-weight: 700; color: var(--text-main); margin-bottom: 0.35rem; }}
    .dropzone p {{ font-size: 0.85rem; color: var(--text-muted); margin-bottom: 1.2rem; }}
    .link-btn {{ background: none; border: none; color: var(--primary); font-weight: 700; text-decoration: underline; cursor: pointer; }}
    .supported-formats {{ display: flex; justify-content: center; gap: 0.8rem; flex-wrap: wrap; }}
    .supported-formats span {{ font-size: 0.72rem; font-weight: 600; color: var(--text-muted); background: #ffffff; border: 1px solid var(--border-color); padding: 0.25rem 0.55rem; border-radius: var(--radius-sm); display: flex; align-items: center; gap: 0.3rem; }}

    .active-file-strip {{ margin: 0 1.4rem 1.4rem; padding: 0.75rem 1rem; background: #f8fafc; border: 1px solid var(--border-color); border-radius: var(--radius-md); display: flex; align-items: center; justify-content: space-between; }}
    .file-info-col {{ display: flex; align-items: center; gap: 0.75rem; }}
    .file-icon {{ font-size: 1.4rem; color: var(--primary); }}
    .file-info-col strong {{ display: block; font-size: 0.85rem; color: var(--text-main); }}
    .file-info-col span {{ font-size: 0.75rem; color: var(--text-muted); }}

    .processing-state {{ padding: 1.5rem 0; }}
    .spinner {{ width: 44px; height: 44px; border: 4px solid var(--cyan-light); border-top-color: var(--cyan); border-radius: 50%; animation: spin 0.8s linear infinite; margin: 0 auto 1rem; }}
    @keyframes spin {{ to {{ transform: rotate(360deg); }} }}

    /* HEADER STYLER CARD & LIVE PREVIEW */
    .header-preview-container {{ padding: 1.4rem 1.4rem 0.5rem; }}
    .preview-label {{ font-size: 0.75rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; color: var(--text-muted); margin-bottom: 0.6rem; display: flex; align-items: center; gap: 0.4rem; }}
    .word-header-mockup {{ background: #ffffff; border: 1px solid #cbd5e1; box-shadow: 0 2px 10px rgba(0,0,0,0.06); border-radius: var(--radius-sm); padding: 1rem 1.25rem 0.75rem; position: relative; min-height: 90px; }}
    .mockup-logo-wrap {{ display: flex; margin-bottom: 0.35rem; }}
    .mockup-logo-wrap img {{ height: 38px; width: auto; object-fit: contain; transition: all 0.2s; }}
    .mockup-tagline {{ font-size: 0.68rem; font-weight: 700; color: var(--text-muted); letter-spacing: 0.03em; text-align: right; margin-bottom: 0.4rem; }}
    .mockup-divider {{ height: 2px; background-color: var(--cyan); width: 100%; }}

    .word-header-mockup.align-right .mockup-logo-wrap {{ justify-content: flex-end; }}
    .word-header-mockup.align-left .mockup-logo-wrap {{ justify-content: flex-start; }}
    .word-header-mockup.align-center .mockup-logo-wrap {{ justify-content: center; }}
    .word-header-mockup.align-center .mockup-tagline {{ text-align: center; }}
    .word-header-mockup.align-left .mockup-tagline {{ text-align: left; }}
    .word-header-mockup.align-dual {{ display: flex; flex-direction: column; }}

    .controls-form {{ padding: 1.4rem; }}
    .control-group {{ margin-bottom: 1.1rem; }}
    .control-group label {{ display: block; font-size: 0.8rem; font-weight: 600; color: var(--text-main); margin-bottom: 0.4rem; }}
    .control-row {{ display: flex; gap: 1rem; }}
    .flex-1 {{ flex: 1; }}

    .segmented-control {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 0.4rem; }}
    .seg-btn {{ background: #f1f5f9; border: 1px solid var(--border-color); padding: 0.5rem 0.6rem; font-size: 0.75rem; font-weight: 600; border-radius: var(--radius-sm); color: var(--text-muted); display: flex; align-items: center; justify-content: center; gap: 0.4rem; }}
    .seg-btn:hover {{ background: #e2e8f0; }}
    .seg-btn.active {{ background: var(--primary); border-color: var(--primary); color: #ffffff; box-shadow: 0 2px 6px rgba(24, 34, 124, 0.2); }}

    .form-input, .form-select, .form-textarea {{ width: 100%; padding: 0.6rem 0.85rem; border: 1px solid var(--border-color); border-radius: var(--radius-md); font-family: var(--font-sans); font-size: 0.88rem; color: var(--text-main); background: #ffffff; transition: border-color 0.2s; }}
    .form-input:focus, .form-select:focus, .form-textarea:focus {{ outline: none; border-color: var(--border-focus); box-shadow: 0 0 0 3px rgba(0, 181, 184, 0.15); }}
    .form-range {{ width: 100%; accent-color: var(--cyan); }}

    .logo-swap-row {{ display: flex; align-items: center; justify-content: space-between; margin-top: 1rem; padding-top: 0.85rem; border-top: 1px solid var(--border-color); }}
    .custom-logo-label {{ font-size: 0.8rem; font-weight: 600; color: var(--primary); cursor: pointer; display: inline-flex; align-items: center; gap: 0.4rem; }}
    .custom-logo-label:hover {{ color: var(--cyan-dark); }}

    /* RIGHT COLUMN: RESUME EDITOR */
    .editor-card {{ min-height: 800px; }}
    .editor-header {{ background: #fafcff; }}
    .editor-body {{ padding: 1.4rem; }}
    .form-section {{ padding-bottom: 1.5rem; margin-bottom: 1.5rem; border-bottom: 1px solid var(--border-color); }}
    .form-section:last-child {{ border-bottom: none; }}
    .section-header-row {{ display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.85rem; }}
    .section-title {{ font-size: 0.95rem; font-weight: 700; color: var(--primary); display: flex; align-items: center; gap: 0.5rem; }}

    .grid-2 {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 1rem; }}
    .grid-4 {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 0.75rem; }}
    @media (max-width: 768px) {{ .grid-2, .grid-4, .grid-2-swap {{ grid-template-columns: 1fr; flex-direction: column; }} }}
    .mt-2 {{ margin-top: 0.5rem; }}
    .mt-3 {{ margin-top: 0.75rem; }}

    .skills-tags-container {{ display: flex; flex-wrap: wrap; gap: 0.5rem; margin-bottom: 0.85rem; min-height: 40px; }}
    .skill-tag {{ background: #f1f5f9; border: 1px solid #cbd5e1; color: var(--text-main); padding: 0.25rem 0.7rem; border-radius: 999px; font-size: 0.8rem; font-weight: 600; display: inline-flex; align-items: center; gap: 0.4rem; }}
    .skill-tag button {{ background: none; border: none; color: var(--text-muted); cursor: pointer; padding: 0; font-size: 0.75rem; }}
    .skill-tag button:hover {{ color: #ef4444; }}
    .quick-add-skill-row {{ display: flex; gap: 0.6rem; max-width: 450px; }}

    .item-card {{ background: #f8fafc; border: 1px solid var(--border-color); border-radius: var(--radius-md); padding: 1rem; margin-bottom: 1rem; position: relative; }}
    .item-delete-btn {{ position: absolute; top: 0.75rem; right: 0.75rem; background: none; border: none; color: #94a3b8; cursor: pointer; font-size: 0.9rem; }}
    .item-delete-btn:hover {{ color: #ef4444; }}
    .bullet-item-row {{ display: flex; align-items: center; gap: 0.5rem; margin-top: 0.4rem; }}
    .bullet-item-row input {{ flex: 1; }}
    .bullet-remove-btn {{ background: none; border: none; color: #cbd5e1; cursor: pointer; }}
    .bullet-remove-btn:hover {{ color: #ef4444; }}
    .add-bullet-link {{ background: none; border: none; color: var(--cyan-dark); font-size: 0.75rem; font-weight: 600; margin-top: 0.5rem; cursor: pointer; display: inline-flex; align-items: center; gap: 0.3rem; }}

    .card-footer {{ padding: 1.25rem 1.4rem; background: #f8fafc; border-top: 1px solid var(--border-color); display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 1rem; }}
    .footer-hint {{ font-size: 0.82rem; color: var(--text-muted); display: flex; align-items: center; gap: 0.4rem; }}

    /* MODAL */
    .modal-backdrop {{ position: fixed; inset: 0; background: rgba(15, 23, 42, 0.6); backdrop-filter: blur(4px); display: flex; align-items: center; justify-content: center; z-index: 1000; padding: 1rem; }}
    .modal-dialog {{ background: #ffffff; border-radius: var(--radius-xl); max-width: 520px; width: 100%; box-shadow: var(--shadow-md); overflow: hidden; }}
    .modal-header {{ padding: 1.1rem 1.4rem; border-bottom: 1px solid var(--border-color); display: flex; align-items: center; justify-content: space-between; }}
    .modal-title {{ font-size: 1.05rem; font-weight: 700; color: var(--primary); display: flex; align-items: center; gap: 0.5rem; }}
    .modal-close {{ background: none; border: none; font-size: 1.1rem; color: var(--text-muted); cursor: pointer; }}
    .modal-body {{ padding: 1.75rem 1.4rem; text-align: center; }}
    .modal-file-icon {{ font-size: 3.5rem; color: #2563eb; margin-bottom: 1rem; }}
    .modal-body h3 {{ font-size: 1.15rem; font-weight: 700; color: var(--primary); margin-bottom: 0.5rem; word-break: break-all; }}
    .modal-desc {{ font-size: 0.9rem; color: var(--text-muted); margin-bottom: 1.5rem; }}
    .modal-actions {{ display: flex; justify-content: center; gap: 0.75rem; }}

    .text-cyan {{ color: var(--cyan); }}
    .text-indigo {{ color: var(--primary); }}
  </style>
</head>
<body>

  <!-- Top Navigation Bar -->
  <header class="app-navbar">
    <div class="nav-container">
      <div class="brand-group">
        <img src="{LOGO_B64}" alt="Key Dynamics Solutions" class="nav-logo" id="navLogoImg">
        <div class="brand-divider"></div>
        <div class="brand-title-box">
          <span class="app-title">Resume Studio</span>
          <span class="app-subtitle">Corporate Word Converter & Header Styler</span>
        </div>
      </div>
      <div class="nav-actions">
        <button class="btn-secondary" id="loadSampleBtn" title="Load sample resume to test immediately">
          <i class="fa-solid fa-wand-magic-sparkles"></i> Load Sample Data
        </button>
      </div>
    </div>
  </header>

  <!-- Main Container -->
  <main class="main-content">
    
    <!-- Hero Banner -->
    <section class="hero-section">
      <div class="hero-content">
        <div class="badge-pill">
          <span class="badge-dot"></span>
          <span>Enterprise Word Resume Styler • Key Dynamics Solutions</span>
        </div>
        <h1>Convert Resumes to Branded <span>Word Documents</span></h1>
        <p>Upload PDF, PowerPoint presentations, Word docs or images. Automatically parse candidate details, review in the live editor, and download executive Word (.docx) resumes with your official company logo in the header.</p>
      </div>
    </section>

    <!-- Two-Column Workflow Section -->
    <div class="workflow-grid">
      
      <!-- LEFT COLUMN: Upload & Document Header Configuration -->
      <div class="config-column">
        
        <!-- Upload Card -->
        <div class="card upload-card">
          <div class="card-header">
            <div class="card-title">
              <i class="fa-solid fa-cloud-arrow-up text-cyan"></i>
              <span>1. Upload Resume</span>
            </div>
            <span class="file-badge">PDF, PPTX, PNG, JPG, DOCX</span>
          </div>

          <div class="dropzone" id="dropzone">
            <input type="file" id="resumeFileInput" accept=".pdf,.pptx,.ppt,.png,.jpg,.jpeg,.webp,.docx,.txt" hidden>
            <div class="dropzone-inner" id="dropzoneContent">
              <div class="upload-icon-circle">
                <i class="fa-solid fa-file-arrow-up"></i>
              </div>
              <h3>Drag & drop resume here</h3>
              <p>or <button type="button" class="link-btn" id="browseFileBtn">browse from your computer</button></p>
              <div class="supported-formats">
                <span><i class="fa-regular fa-file-pdf"></i> PDF</span>
                <span><i class="fa-regular fa-file-powerpoint"></i> PPT / PPTX</span>
                <span><i class="fa-regular fa-file-image"></i> Images</span>
                <span><i class="fa-regular fa-file-word"></i> Word DOCX</span>
              </div>
            </div>

            <div class="processing-state" id="processingState" style="display: none;">
              <div class="spinner"></div>
              <h4 id="processingTitle">Extracting resume structure...</h4>
              <p id="processingSubtitle">Analyzing text, dates, roles and competencies</p>
            </div>
          </div>

          <div class="active-file-strip" id="activeFileStrip" style="display: none;">
            <div class="file-info-col">
              <i class="fa-solid fa-file-lines file-icon"></i>
              <div>
                <strong id="activeFileName">resume.pdf</strong>
                <span id="activeFileType">Document</span>
              </div>
            </div>
            <button class="btn-icon" id="clearFileBtn" title="Remove file"><i class="fa-solid fa-xmark"></i></button>
          </div>
        </div>

        <!-- Word Document Header Styler Card -->
        <div class="card header-styler-card">
          <div class="card-header">
            <div class="card-title">
              <i class="fa-solid fa-stamp text-indigo"></i>
              <span>2. Word Header & Branding</span>
            </div>
            <span class="badge-status">Active Header</span>
          </div>

          <!-- Live Header Preview -->
          <div class="header-preview-container">
            <div class="preview-label"><i class="fa-solid fa-eye"></i> Word Document Header Preview</div>
            <div class="word-header-mockup align-dual" id="headerMockup">
              <div class="mockup-logo-wrap" id="mockupLogoWrap">
                <img src="{LOGO_B64}" alt="Company Logo" id="headerMockupImg">
              </div>
              <div class="mockup-tagline" id="mockupTaglineText">
                CONFIDENTIAL CANDIDATE DOSSIER | KEY DYNAMICS SOLUTIONS
              </div>
              <div class="mockup-divider" id="mockupDivider"></div>
            </div>
          </div>

          <!-- Styler Controls -->
          <div class="controls-form">
            <div class="control-group">
              <label><i class="fa-solid fa-arrows-left-right"></i> Header Layout & Alignment</label>
              <div class="segmented-control" id="headerAlignSegment">
                <button type="button" class="seg-btn active" data-align="dual">
                  <i class="fa-solid fa-table-columns"></i> Dual (Logo + Tagline)
                </button>
                <button type="button" class="seg-btn" data-align="right">
                  <i class="fa-solid fa-align-right"></i> Right Logo
                </button>
                <button type="button" class="seg-btn" data-align="left">
                  <i class="fa-solid fa-align-left"></i> Left Logo
                </button>
                <button type="button" class="seg-btn" data-align="center">
                  <i class="fa-solid fa-align-center"></i> Center Logo
                </button>
              </div>
            </div>

            <div class="control-group">
              <label for="headerTaglineInput"><i class="fa-solid fa-heading"></i> Header Tagline / Watermark Text</label>
              <input type="text" id="headerTaglineInput" class="form-input" value="CONFIDENTIAL CANDIDATE DOSSIER | KEY DYNAMICS SOLUTIONS">
            </div>

            <div class="control-row">
              <div class="control-group flex-1">
                <label for="themeSelect"><i class="fa-solid fa-palette"></i> Palette & Theme</label>
                <select id="themeSelect" class="form-select">
                  <option value="key_dynamics" selected>Key Dynamics (Navy & Cyan)</option>
                  <option value="modern_teal">Modern Teal & Cyan</option>
                  <option value="classic_blue">Corporate Royal Blue</option>
                  <option value="sleek_dark">Sleek Charcoal & Platinum</option>
                </select>
              </div>

              <div class="control-group flex-1">
                <label for="logoSizeRange"><i class="fa-solid fa-ruler-horizontal"></i> Logo Width: <span id="logoSizeLabel">2.3"</span></label>
                <input type="range" id="logoSizeRange" min="1.6" max="3.0" step="0.1" value="2.3" class="form-range">
              </div>
            </div>

            <div class="logo-swap-row">
              <label class="custom-logo-label" for="customLogoInput">
                <i class="fa-solid fa-upload"></i> Change / Upload Different Logo
              </label>
              <input type="file" id="customLogoInput" accept="image/*" hidden>
              <button type="button" class="btn-link" id="resetLogoBtn">Reset to Default Logo</button>
            </div>
          </div>
        </div>

      </div>

      <!-- RIGHT COLUMN: Parsed Resume Editor & Live Document Structure -->
      <div class="editor-column">
        
        <div class="card editor-card">
          <div class="card-header editor-header">
            <div class="card-title">
              <i class="fa-solid fa-pen-to-square text-cyan"></i>
              <span>3. Review & Edit Structured Resume</span>
            </div>
            <div class="editor-actions">
              <button class="btn-primary" id="generateDocxBtn">
                <i class="fa-solid fa-file-word"></i> Download Word (.docx)
              </button>
            </div>
          </div>

          <div class="editor-body">
            
            <!-- Candidate Identity -->
            <div class="form-section">
              <div class="section-header-row">
                <h4 class="section-title"><i class="fa-solid fa-user"></i> Candidate Profile</h4>
                <button type="button" class="btn-xs" id="swapNameTitleBtn" title="Swap Full Name and Professional Title"><i class="fa-solid fa-right-left"></i> Swap Name ⇄ Title</button>
              </div>
              <div class="grid-2">
                <div class="form-group">
                  <label>Full Name</label>
                  <input type="text" id="candFullName" class="form-input" placeholder="e.g. John Doe">
                </div>
                <div class="form-group">
                  <label>Professional Title</label>
                  <input type="text" id="candTitle" class="form-input" placeholder="e.g. Principal Operations Manager">
                </div>
              </div>

              <div class="grid-4 mt-2">
                <div class="form-group">
                  <label>Email</label>
                  <input type="email" id="candEmail" class="form-input" placeholder="john@example.com">
                </div>
                <div class="form-group">
                  <label>Phone</label>
                  <input type="text" id="candPhone" class="form-input" placeholder="+1 (555) 000-0000">
                </div>
                <div class="form-group">
                  <label>Location</label>
                  <input type="text" id="candLocation" class="form-input" placeholder="Dallas, TX">
                </div>
                <div class="form-group">
                  <label>LinkedIn</label>
                  <input type="text" id="candLinkedin" class="form-input" placeholder="linkedin.com/in/johndoe">
                </div>
              </div>
            </div>

            <!-- Professional Summary -->
            <div class="form-section">
              <h4 class="section-title"><i class="fa-solid fa-align-left"></i> Executive Summary</h4>
              <textarea id="candSummary" class="form-textarea" rows="4" placeholder="Brief executive summary highlighting background, leadership experience, and major career achievements..."></textarea>
            </div>

            <!-- Core Skills -->
            <div class="form-section">
              <div class="section-header-row">
                <h4 class="section-title"><i class="fa-solid fa-bolt"></i> Core Competencies & Skills</h4>
                <button type="button" class="btn-xs" id="addSkillBtn"><i class="fa-solid fa-plus"></i> Add Skill</button>
              </div>
              <div class="skills-tags-container" id="skillsContainer"></div>
              <div class="quick-add-skill-row">
                <input type="text" id="newSkillInput" class="form-input" placeholder="Type a skill and press Enter...">
                <button type="button" class="btn-secondary" id="confirmAddSkillBtn">Add</button>
              </div>
            </div>

            <!-- Work Experience -->
            <div class="form-section">
              <div class="section-header-row">
                <h4 class="section-title"><i class="fa-solid fa-briefcase"></i> Work Experience</h4>
                <div class="section-actions-row">
                  <button type="button" class="btn-xs" id="swapAllExpBtn" title="Swap Job Title and Company Name for all roles"><i class="fa-solid fa-right-left"></i> Swap All Title ⇄ Company</button>
                  <button type="button" class="btn-xs" id="addExpBtn"><i class="fa-solid fa-plus"></i> Add Experience</button>
                </div>
              </div>
              <div class="dynamic-items-container" id="experienceContainer"></div>
            </div>

            <!-- Education -->
            <div class="form-section">
              <div class="section-header-row">
                <h4 class="section-title"><i class="fa-solid fa-graduation-cap"></i> Education</h4>
                <button type="button" class="btn-xs" id="addEduBtn"><i class="fa-solid fa-plus"></i> Add Degree</button>
              </div>
              <div class="dynamic-items-container" id="educationContainer"></div>
            </div>

            <!-- Certifications -->
            <div class="form-section">
              <div class="section-header-row">
                <h4 class="section-title"><i class="fa-solid fa-certificate"></i> Certifications & Honors</h4>
                <button type="button" class="btn-xs" id="addCertBtn"><i class="fa-solid fa-plus"></i> Add Certification</button>
              </div>
              <div class="certs-list-container" id="certsContainer"></div>
            </div>

          </div>

          <div class="card-footer">
            <div class="footer-hint">
              <i class="fa-solid fa-circle-check text-cyan"></i> Generates official Word (.docx) document with Key Dynamics Solutions header logo.
            </div>
            <button class="btn-primary btn-lg" id="generateDocxBtnBottom">
              <i class="fa-solid fa-file-word"></i> Generate & Download Word Document
            </button>
          </div>
        </div>

      </div>

    </div>

  </main>

  <!-- Download Ready Modal -->
  <div class="modal-backdrop" id="downloadModal" style="display: none;">
    <div class="modal-dialog">
      <div class="modal-header">
        <div class="modal-title">
          <i class="fa-solid fa-circle-check text-cyan"></i>
          <span>Document Successfully Converted!</span>
        </div>
        <button class="modal-close" id="closeModalBtn"><i class="fa-solid fa-xmark"></i></button>
      </div>
      <div class="modal-body">
        <div class="modal-file-icon">
          <i class="fa-solid fa-file-word"></i>
        </div>
        <h3 id="modalDocName">Alexander_Morgan_KeyDynamics_Resume.docx</h3>
        <p class="modal-desc">Your branded Word document has been generated with the <strong>Key Dynamics Solutions</strong> header logo, typography, and styling.</p>
        
        <div class="modal-actions">
          <button type="button" class="btn-primary btn-lg" id="modalDownloadLink">
            <i class="fa-solid fa-download"></i> Download Word File (.docx)
          </button>
          <button type="button" class="btn-secondary" id="modalDismissBtn">Done</button>
        </div>
      </div>
    </div>
  </div>

  <script>
    const DEFAULT_LOGO_B64 = "{LOGO_B64}";
  </script>
  <script src="/static/js/app.js"></script>
  <!-- Fallback standalone bundle script in case running as static file on GitHub Pages -->
  <script src="standalone_app.js"></script>
</body>
</html>
'''

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(HTML_CONTENT)

print('Successfully generated root index.html!')
