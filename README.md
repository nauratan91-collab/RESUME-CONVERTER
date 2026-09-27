# 📄 Key Dynamics Solutions - Resume to Word (.docx) Converter

![Python](https://img.shields.io/badge/Python-3.11%2B-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.1-black.svg)
![python-docx](https://img.shields.io/badge/python--docx-1.2-brightgreen.svg)
![License](https://img.shields.io/badge/License-Proprietary-navy.svg)

An enterprise web software that ingests any resume format (**PDF, PowerPoint PPT/PPTX, Images PNG/JPG, Word DOCX**), extracts and structures candidate profile details, applies the **Key Dynamics Solutions** official logo in the Word header, and exports professionally styled Word (`.docx`) documents.

---

## ✨ Features

- **Multi-Format Ingestion**:
  - **PDF Documents (`.pdf`)**: Direct text and layout extraction using `pypdf`.
  - **PowerPoint Presentations (`.pptx`, `.ppt`)**: Slide shapes and table text extraction via `python-pptx`.
  - **Images & Scans (`.png`, `.jpg`, `.jpeg`, `.webp`)**: Direct image inspection + optional Gemini 2.5 Flash Vision OCR.
  - **Word Files (`.docx`)**: Re-branding and re-formatting existing documents.
- **Corporate Header with Logo**:
  - The official **Key Dynamics Solutions** logo is embedded directly into the Word document header on every page.
  - Customizable header layouts:
    - **Dual (Recommended)**: Logo on Left + Confidential Tagline on Right.
    - **Right**: Logo placed at top right.
    - **Left**: Logo placed at top left.
    - **Center**: Logo centered horizontally.
  - Brand color palette matching Key Dynamics Solutions: Deep Navy (`#18227C`), Vibrant Cyan (`#00B5B8`), and Slate (`#475569`).
- **Smart Disambiguation & 1-Click Swapping**:
  - Built-in lexical classifier prevents job title and company name from being inverted.
  - 1-Click `⇄ Swap Title & Company` buttons on every job card and candidate profile.
- **Interactive Review & Editor**:
  - Live in-browser editing of Name, Title, Contact Info, Executive Summary, Skills Tags, Work History (with bullet points), Education, and Certifications.
  - Pre-loaded "Load Sample Data" button to test and export in 1 click.
- **One-Click Word Export**:
  - Generates downloadable `.docx` file with custom margins, styled dividers, bullets, and page numbering.

---

## 🚀 Quick Start

### 1. Prerequisites
- Python 3.10+ installed
- Windows / macOS / Linux

### 2. Installation
Clone the repository:
```bash
git clone https://github.com/nauratan91-collab/resume-converter.git
cd resume-converter
```

Install dependencies:
```bash
pip install -r requirements.txt
```

### 3. Run Application
```bash
python app.py
```
*(Or on Windows, simply double-click `run.bat`).*

Open your browser and visit:
👉 **http://localhost:5055**

---

## 📁 Project Structure

```text
resume_converter_app/
├── app.py                      # Flask backend & REST endpoints
├── run.bat                     # 1-Click Windows launcher
├── requirements.txt            # Dependency manifest
├── services/
│   ├── extractor.py            # PDF, PPTX, DOCX & Image text extractor
│   ├── parser.py               # Resume section parser & Title/Company classifier
│   ├── docx_builder.py         # Word (.docx) builder with header logo
│   └── ai_enhancer.py          # Gemini 2.5 Flash multimodal vision parser
├── static/
│   ├── images/
│   │   └── company_logo.png    # Key Dynamics Solutions official logo
│   ├── css/
│   │   └── style.css           # Modern corporate styling
│   └── js/
│       └── app.js              # Client reactivity, drag & drop, editor & download
├── templates/
│   └── index.html              # Main web application dashboard
├── uploads/                    # Staged incoming files
└── output/                     # Generated Word documents (.docx)
```

---

## 🔒 Confidentiality & Branding
Developed for **Key Dynamics Solutions**  
*Transform Your Operation*
