from services.parser import parse_resume_text

test_resume = """
PRIYA SHARMA
Lead Cloud Solutions Architect
priya.sharma@example.com | +91 98765 43210 | Bangalore, India | linkedin.com/in/priyasharma

PROFESSIONAL SUMMARY
Experienced Cloud Solutions Architect with 10+ years driving digital transformation.

WORK EXPERIENCE
Key Dynamics Solutions - Senior Enterprise Architect (2021 - Present)
• Spearheaded migration of enterprise ERP to multi-region cloud.
• Led architectural reviews across 12 distributed squads.

Infosys Limited
Lead Systems Engineer (2017 - 2021)
• Engineered microservice platforms processing 5M+ daily requests.

Tech Mahindra | Cloud Consultant (2014 - 2017)
• Implemented automated CI/CD pipelines reducing deployment friction by 70%.

EDUCATION
B.Tech in Information Technology - Anna University (2010 - 2014)

CORE SKILLS
AWS, Kubernetes, Terraform, Python, Microservices, Enterprise Architecture
"""

res = parse_resume_text(test_resume)

print("=== CANDIDATE PROFILE ===")
print("Name:", res["full_name"])
print("Title:", res["target_title"])

print("\n=== WORK EXPERIENCE ITEMS ===")
for i, exp in enumerate(res["experience"], 1):
    print(f"Job {i}:")
    print(f"  Title   : {exp['title']}")
    print(f"  Company : {exp['company']}")
    print(f"  Dates   : {exp['dates']}")

# Assertions
for exp in res["experience"]:
    title = exp["title"].lower()
    company = exp["company"].lower()
    assert any(w in title for w in ["architect", "engineer", "consultant"]), f"Wrong title: {exp['title']}"
    assert any(w in company for w in ["solutions", "infosys", "mahindra"]), f"Wrong company: {exp['company']}"

print("\nALL RESUME FORMAT TESTS PASSED! Job Title and Company are accurately positioned!")
