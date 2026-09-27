import json
import os
from pathlib import Path
from google import genai
from google.genai import types

RESUME_SCHEMA = {
    "type": "OBJECT",
    "properties": {
        "full_name": {"type": "STRING"},
        "target_title": {"type": "STRING"},
        "contact": {
            "type": "OBJECT",
            "properties": {
                "email": {"type": "STRING"},
                "phone": {"type": "STRING"},
                "location": {"type": "STRING"},
                "linkedin": {"type": "STRING"},
                "website": {"type": "STRING"}
            }
        },
        "summary": {"type": "STRING"},
        "skills": {
            "type": "ARRAY",
            "items": {"type": "STRING"}
        },
        "experience": {
            "type": "ARRAY",
            "items": {
                "type": "OBJECT",
                "properties": {
                    "title": {"type": "STRING"},
                    "company": {"type": "STRING"},
                    "location": {"type": "STRING"},
                    "dates": {"type": "STRING"},
                    "bullets": {
                        "type": "ARRAY",
                        "items": {"type": "STRING"}
                    }
                },
                "required": ["title", "company"]
            }
        },
        "education": {
            "type": "ARRAY",
            "items": {
                "type": "OBJECT",
                "properties": {
                    "degree": {"type": "STRING"},
                    "institution": {"type": "STRING"},
                    "location": {"type": "STRING"},
                    "dates": {"type": "STRING"},
                    "details": {"type": "STRING"}
                },
                "required": ["degree", "institution"]
            }
        },
        "certifications": {
            "type": "ARRAY",
            "items": {"type": "STRING"}
        },
        "projects": {
            "type": "ARRAY",
            "items": {
                "type": "OBJECT",
                "properties": {
                    "name": {"type": "STRING"},
                    "description": {"type": "STRING"},
                    "bullets": {
                        "type": "ARRAY",
                        "items": {"type": "STRING"}
                    }
                }
            }
        }
    },
    "required": ["full_name", "experience"]
}

def parse_document_with_ai(file_path: str, api_key: str, mime_type: str = None) -> dict:
    """
    Uses Gemini Multimodal to inspect and parse a document (image, PDF, etc.) into structured resume JSON.
    """
    filename = Path(file_path).name
    try:
        client = genai.Client(api_key=api_key)
        
        with open(file_path, "rb") as f:
            file_bytes = f.read()

        if not mime_type:
            ext = Path(file_path).suffix.lower()
            if ext == ".pdf":
                mime_type = "application/pdf"
            elif ext in [".png"]:
                mime_type = "image/png"
            elif ext in [".jpg", ".jpeg"]:
                mime_type = "image/jpeg"
            elif ext in [".webp"]:
                mime_type = "image/webp"
            else:
                mime_type = "application/octet-stream"

        prompt = (
            "You are an expert executive resume parser. Analyze this resume document carefully. "
            "Extract all information with maximum accuracy: Candidate full name, professional title, contact details, "
            "summary, core skills, comprehensive work experience with roles, companies, dates, and bulleted achievements, "
            "education degrees, dates, and certifications. Return structured JSON matching the exact schema.\n"
            "CRITICAL REQUIREMENT: For each experience item, ensure 'title' contains strictly the Job Position/Role "
            "(e.g., Senior Systems Engineer, Operations Director) and 'company' contains strictly the Employer/Organization name "
            "(e.g., Key Dynamics Solutions, Amazon, Tata Consultancy Services). NEVER put company name in title or title in company."
        )

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[
                types.Part.from_bytes(data=file_bytes, mime_type=mime_type),
                prompt
            ],
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=RESUME_SCHEMA,
                temperature=0.1
            )
        )

        parsed_json = json.loads(response.text)
        
        # Disambiguate title vs company for all experience entries
        from services.parser import classify_title_and_company
        for exp in parsed_json.get("experience", []):
            t, c = classify_title_and_company(exp.get("title", ""), exp.get("company", ""))
            exp["title"] = t
            exp["company"] = c

        # Build raw text fallback from parsed data
        raw_text_parts = [
            parsed_json.get("full_name", ""),
            parsed_json.get("target_title", ""),
            " ".join(v for v in parsed_json.get("contact", {}).values() if v),
            "\nSUMMARY\n" + parsed_json.get("summary", ""),
            "\nEXPERIENCE"
        ]
        for exp in parsed_json.get("experience", []):
            raw_text_parts.append(f"{exp.get('title')} at {exp.get('company')} ({exp.get('dates', '')})")
            for b in exp.get("bullets", []):
                raw_text_parts.append(f"• {b}")

        return {
            "success": True,
            "filename": filename,
            "file_type": Path(file_path).suffix.lower(),
            "raw_text": "\n".join(raw_text_parts),
            "page_count": 1,
            "ai_parsed": True,
            "structured_data": parsed_json
        }
    except Exception as e:
        return {
            "success": False,
            "filename": filename,
            "file_type": Path(file_path).suffix.lower(),
            "error": f"AI Parsing failed: {str(e)}"
        }
