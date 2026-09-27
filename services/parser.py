import re
from typing import Dict, List, Any, Tuple

# Section keyword patterns
SECTION_PATTERNS = {
    "summary": re.compile(r"^(summary|professional summary|executive summary|profile|about me|career profile|objective|career objective)\b", re.IGNORECASE),
    "experience": re.compile(r"^(experience|work experience|professional experience|employment history|work history|career history|relevant experience)\b", re.IGNORECASE),
    "education": re.compile(r"^(education|academic background|qualifications|academic history|educational background)\b", re.IGNORECASE),
    "skills": re.compile(r"^(skills|technical skills|core skills|core competencies|areas of expertise|technologies|key skills|skills & tools)\b", re.IGNORECASE),
    "projects": re.compile(r"^(projects|key projects|personal projects|technical projects|portfolio)\b", re.IGNORECASE),
    "certifications": re.compile(r"^(certifications|certificates|licenses|credentials|awards & achievements|certifications & licenses)\b", re.IGNORECASE),
}

DATE_PATTERN = re.compile(
    r"\b((?:jan|feb|mar|apr|may|jun|jul|aug|sep|sept|oct|nov|dec)[a-z]*\.?\s+\d{4}|\d{1,2}/\d{4}|\d{4})\s*[-–—to]+\s*((?:jan|feb|mar|apr|may|jun|jul|aug|sep|sept|oct|nov|dec)[a-z]*\.?\s+\d{4}|\d{1,2}/\d{4}|\d{4}|present|current)\b",
    re.IGNORECASE
)

EMAIL_PATTERN = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b")
PHONE_PATTERN = re.compile(r"(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}")
LINKEDIN_PATTERN = re.compile(r"(?:https?://)?(?:www\.)?linkedin\.com/in/[\w-]+", re.IGNORECASE)
URL_PATTERN = re.compile(r"(?:https?://)?(?:www\.)?[\w-]+\.(?:com|org|net|io|dev|ai|me)(?:/[\w-]*)*", re.IGNORECASE)

# Dedicated lexical dictionaries to disambiguate Job Titles vs Company Names
TITLE_KEYWORDS = {
    "developer", "engineer", "manager", "director", "lead", "leader", "architect",
    "consultant", "analyst", "specialist", "officer", "executive", "associate",
    "intern", "administrator", "admin", "coordinator", "president", "head",
    "supervisor", "designer", "technician", "scientist", "representative",
    "accountant", "advocate", "professor", "instructor", "assistant", "staff",
    "vp", "svp", "avp", "evp", "ceo", "cto", "coo", "cfo", "cio", "cmo", "ciso",
    "founder", "co-founder", "programmer", "operator", "trainee", "expert",
    "qa", "tester", "sre", "devops", "dba", "strategist", "recruiter", "partner",
    "principal", "junior", "senior", "sr", "jr", "technologist", "auditor",
    "writer", "editor", "producer", "specialist", "agent", "specialist", "advisor",
    "practitioner", "fellow", "worker", "apprentice"
}

COMPANY_KEYWORDS = {
    "inc", "inc.", "llc", "llp", "ltd", "ltd.", "limited", "corp", "corp.",
    "corporation", "technologies", "tech", "technology", "solutions", "systems",
    "services", "enterprises", "enterprise", "group", "holdings", "consulting",
    "labs", "software", "global", "bank", "hospital", "university", "college",
    "institute", "agency", "pvt", "pvt.", "private", "gmbh", "co.", "co", "company",
    "infotech", "studios", "industries", "media", "health", "logistics", "international",
    "dynamics", "associates", "ventures", "capital", "network", "networks", "foundation"
}


def score_title_confidence(text: str) -> int:
    """Scores how likely a piece of text is a Job Title."""
    if not text:
        return 0
    words = re.findall(r"\b[a-zA-Z]+\b", text.lower())
    score = 0
    for w in words:
        if w in TITLE_KEYWORDS:
            score += 4
    if any(w in words for w in ["sr", "jr", "lead", "principal", "chief", "head", "senior", "junior"]):
        score += 3
    return score


def score_company_confidence(text: str) -> int:
    """Scores how likely a piece of text is an Employer / Company Name."""
    if not text:
        return 0
    words = re.findall(r"\b[a-zA-Z]+\b", text.lower())
    score = 0
    for w in words:
        if w in COMPANY_KEYWORDS:
            score += 4
    return score


def classify_title_and_company(text1: str, text2: str) -> Tuple[str, str]:
    """
    Intelligently determines which string is the Job Title and which is the Company Name.
    Guarantees: Returns (job_title, company_name) in correct order.
    """
    t1 = (text1 or "").strip()
    t2 = (text2 or "").strip()

    if not t1:
        return t2, ""
    if not t2:
        return t1, ""

    t1_title_score = score_title_confidence(t1)
    t2_title_score = score_title_confidence(t2)
    t1_comp_score = score_company_confidence(t1)
    t2_comp_score = score_company_confidence(t2)

    # Score if order is (t1=title, t2=company)
    normal_score = t1_title_score + t2_comp_score
    # Score if order is (t2=title, t1=company)
    swapped_score = t2_title_score + t1_comp_score

    if swapped_score > normal_score:
        return t2, t1
    elif normal_score > swapped_score:
        return t1, t2

    # Tie-breaking rules
    # If t1 has company keyword and t2 does not
    if t1_comp_score > 0 and t2_comp_score == 0:
        return t2, t1
    # If t2 has title keyword and t1 does not
    if t2_title_score > 0 and t1_title_score == 0:
        return t2, t1

    # Default: maintain existing order
    return t1, t2


def parse_resume_text(raw_text: str) -> Dict[str, Any]:
    """
    Parses raw resume text into structured components.
    """
    lines = [line.strip() for line in raw_text.splitlines()]
    cleaned_lines = [l for l in lines if l]
    
    result = {
        "full_name": "",
        "target_title": "",
        "contact": {
            "email": "",
            "phone": "",
            "location": "",
            "linkedin": "",
            "website": ""
        },
        "summary": "",
        "skills": [],
        "experience": [],
        "education": [],
        "certifications": [],
        "projects": []
    }

    if not cleaned_lines:
        return result

    # 1. Contact Info Extraction
    emails = EMAIL_PATTERN.findall(raw_text)
    if emails:
        result["contact"]["email"] = emails[0]
    
    phones = PHONE_PATTERN.findall(raw_text)
    if phones:
        result["contact"]["phone"] = phones[0]

    linkedin = LINKEDIN_PATTERN.findall(raw_text)
    if linkedin:
        result["contact"]["linkedin"] = linkedin[0]

    # 2. Extract Candidate Name and Title (Top lines)
    header_lines = cleaned_lines[:6]
    candidate_name = ""
    candidate_title = ""

    for line in header_lines:
        # Ignore lines with email, phone, or links
        if EMAIL_PATTERN.search(line) or PHONE_PATTERN.search(line) or "http" in line.lower() or "www." in line.lower():
            continue
        # Skip section titles
        if any(pat.match(line) for pat in SECTION_PATTERNS.values()):
            break
        # Ignore obvious company names (e.g. at the top of a document)
        if score_company_confidence(line) >= 4 and score_title_confidence(line) == 0:
            continue
        
        # First plausible line is candidate name
        if not candidate_name and len(line.split()) <= 5 and not any(char.isdigit() for char in line):
            candidate_name = line
            continue
        # Second plausible line is target title
        if candidate_name and not candidate_title and len(line.split()) <= 7:
            candidate_title = line
            break

    result["full_name"] = candidate_name or "Candidate Name"
    result["target_title"] = candidate_title

    # 3. Partition document into sections
    sections = {}
    current_sec = "header"
    sections[current_sec] = []

    for line in cleaned_lines:
        matched_sec = None
        for sec_name, pattern in SECTION_PATTERNS.items():
            if len(line.split()) <= 4 and pattern.match(line):
                matched_sec = sec_name
                break
        
        if matched_sec:
            current_sec = matched_sec
            if current_sec not in sections:
                sections[current_sec] = []
        else:
            sections[current_sec].append(line)

    # 4. Parse Summary
    if "summary" in sections:
        result["summary"] = " ".join(sections["summary"]).strip()

    # 5. Parse Skills
    if "skills" in sections:
        skills_lines = sections["skills"]
        skills_set = []
        for s_line in skills_lines:
            s_line = re.sub(r"^[•\-\*\—\–]\s*", "", s_line)
            if ":" in s_line:
                s_line = s_line.split(":", 1)[1]
            parts = re.split(r"[,|•;]", s_line)
            for p in parts:
                cleaned = p.strip()
                if cleaned and len(cleaned) <= 40:
                    skills_set.append(cleaned)
        result["skills"] = skills_set

    # 6. Parse Work Experience (With title vs company disambiguation)
    if "experience" in sections:
        result["experience"] = parse_experience_section(sections["experience"])

    # 7. Parse Education
    if "education" in sections:
        result["education"] = parse_education_section(sections["education"])

    # 8. Parse Certifications
    if "certifications" in sections:
        certs = []
        for line in sections["certifications"]:
            cleaned = re.sub(r"^[•\-\*\—\–]\s*", "", line).strip()
            if cleaned:
                certs.append(cleaned)
        result["certifications"] = certs

    # 9. Parse Projects
    if "projects" in sections:
        result["projects"] = parse_projects_section(sections["projects"])

    return result


def parse_experience_section(lines: List[str]) -> List[Dict[str, Any]]:
    experiences = []
    current_job = None

    def finalize_job(job):
        """Disambiguates and classifies job title and company before saving."""
        if not job:
            return None
        t, c = classify_title_and_company(job.get("title", ""), job.get("company", ""))
        job["title"] = t or "Professional Role"
        job["company"] = c or ""
        return job

    for idx, line in enumerate(lines):
        is_bullet = bool(re.match(r"^[•\-\*\—\–\d+\.]\s+", line))
        date_match = DATE_PATTERN.search(line)
        cleaned_bullet = re.sub(r"^[•\-\*\—\–\d+\.]\s*", "", line).strip()
        next_line = lines[idx + 1] if idx + 1 < len(lines) else ""

        # If date match found on a non-bullet line, start a new job entry
        if date_match and not is_bullet:
            dates = date_match.group(0)
            rest_of_line = line.replace(dates, "").strip(" ,|-–—()[]")

            # If current_job exists but was only an incomplete predecessor line (no dates, no bullets), merge with it!
            if current_job and not current_job.get("dates") and len(current_job.get("bullets", [])) == 0:
                prev_text = current_job.get("title", "")
                if not rest_of_line:
                    current_job["dates"] = dates
                    continue
                else:
                    correct_title, correct_company = classify_title_and_company(rest_of_line, prev_text)
                    current_job["title"] = correct_title
                    current_job["company"] = correct_company
                    current_job["dates"] = dates
                    continue

            if current_job:
                experiences.append(finalize_job(current_job))
            
            raw_title = rest_of_line
            raw_company = ""

            if " at " in rest_of_line:
                raw_title, raw_company = rest_of_line.split(" at ", 1)
            elif " - " in rest_of_line or " | " in rest_of_line:
                parts = re.split(r"\s+[-|]\s+", rest_of_line)
                raw_title = parts[0]
                if len(parts) > 1:
                    raw_company = parts[1]
            elif "," in rest_of_line:
                parts = rest_of_line.split(",", 1)
                raw_title = parts[0]
                raw_company = parts[1]

            # Use intelligent classifier to place title in title, and company in company!
            correct_title, correct_company = classify_title_and_company(raw_title, raw_company)

            current_job = {
                "title": correct_title,
                "company": correct_company,
                "dates": dates,
                "location": "",
                "bullets": []
            }
        elif is_bullet:
            if current_job:
                current_job["bullets"].append(cleaned_bullet)
            else:
                current_job = {
                    "title": "Professional Experience",
                    "company": "",
                    "dates": "",
                    "location": "",
                    "bullets": [cleaned_bullet]
                }
        else:
            # Regular text line (could be title, company name, or location)
            # Detect if this short line is actually the beginning of a NEW job
            is_new_job_start = False
            if current_job and (current_job.get("dates") or len(current_job.get("bullets", [])) > 0):
                if len(line.split()) <= 7 and not is_bullet:
                    if next_line and DATE_PATTERN.search(next_line):
                        is_new_job_start = True
                    elif score_title_confidence(line) > 0 or score_company_confidence(line) > 0:
                        is_new_job_start = True

            if is_new_job_start:
                experiences.append(finalize_job(current_job))
                current_job = {
                    "title": line,
                    "company": "",
                    "dates": "",
                    "location": "",
                    "bullets": []
                }
            elif current_job is None:
                current_job = {
                    "title": line,
                    "company": "",
                    "dates": "",
                    "location": "",
                    "bullets": []
                }
            elif not current_job["company"] and not current_job.get("dates") and len(line.split()) <= 6:
                # Disambiguate existing title vs incoming line
                correct_title, correct_company = classify_title_and_company(current_job["title"], line)
                current_job["title"] = correct_title
                current_job["company"] = correct_company
            else:
                # Add as bullet / detail
                current_job["bullets"].append(line)

    if current_job:
        experiences.append(finalize_job(current_job))

    return experiences


def parse_education_section(lines: List[str]) -> List[Dict[str, Any]]:
    educations = []
    current_edu = None

    degree_indicators = ["bachelor", "master", "phd", "b.s", "b.a", "m.s", "m.a", "bba", "mba", "diploma", "associate", "degree", "b.tech", "m.tech", "bsc", "msc"]

    for line in lines:
        date_match = DATE_PATTERN.search(line)
        cleaned = re.sub(r"^[•\-\*\—\–]\s*", "", line).strip()
        lower = cleaned.lower()

        is_degree = any(deg in lower for deg in degree_indicators)

        if is_degree or (date_match and current_edu is None):
            if current_edu:
                educations.append(current_edu)
            
            dates = date_match.group(0) if date_match else ""
            degree_text = cleaned.replace(dates, "").strip(" ,|-–—")
            
            institution = ""
            if " from " in degree_text.lower():
                parts = re.split(r"\s+from\s+", degree_text, flags=re.IGNORECASE)
                degree_text = parts[0]
                institution = parts[1]
            elif " - " in degree_text or " | " in degree_text:
                parts = re.split(r"\s+[-|]\s+", degree_text)
                degree_text = parts[0]
                institution = parts[1] if len(parts) > 1 else ""

            current_edu = {
                "degree": degree_text or "Degree / Qualification",
                "institution": institution,
                "dates": dates,
                "details": ""
            }
        elif current_edu:
            if not current_edu["institution"]:
                current_edu["institution"] = cleaned
            elif not current_edu["dates"] and date_match:
                current_edu["dates"] = date_match.group(0)
            else:
                current_edu["details"] = (current_edu["details"] + " " + cleaned).strip()
        else:
            current_edu = {
                "degree": cleaned,
                "institution": "",
                "dates": date_match.group(0) if date_match else "",
                "details": ""
            }

    if current_edu:
        educations.append(current_edu)

    return educations


def parse_projects_section(lines: List[str]) -> List[Dict[str, Any]]:
    projects = []
    curr_proj = None

    for line in lines:
        is_bullet = bool(re.match(r"^[•\-\*\—\–]\s+", line))
        cleaned = re.sub(r"^[•\-\*\—\–]\s*", "", line).strip()

        if not is_bullet and len(cleaned.split()) <= 6:
            if curr_proj:
                projects.append(curr_proj)
            curr_proj = {
                "name": cleaned,
                "description": "",
                "bullets": []
            }
        elif is_bullet:
            if curr_proj:
                curr_proj["bullets"].append(cleaned)
            else:
                curr_proj = {"name": "Project", "description": "", "bullets": [cleaned]}
        else:
            if curr_proj:
                curr_proj["bullets"].append(cleaned)

    if curr_proj:
        projects.append(curr_proj)

    return projects
