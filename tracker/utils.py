import pdfplumber
import re

# -------------------------------------------------
# PDF TEXT EXTRACTION
# -------------------------------------------------
def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text.lower()


# -------------------------------------------------
# BASIC SKILL KEYWORDS (quick match)
# -------------------------------------------------
SKILL_KEYWORDS = {
    "Aptitude": ["aptitude", "quantitative", "math", "percentage", "ratio","aptitude", "quantitative", "probability", "numbers",
        "percentages", "ratio", "time and work","logical", "reasoning", "puzzle","logical reasoning", "analytical thinking", "puzzles",
        "critical thinking", "verbal reasoning","problem solving","logical thinking abilities"],
    "Reasoning": ["logical", "reasoning", "puzzle","logical reasoning", "analytical thinking", "puzzles",
        "critical thinking", "verbal reasoning","problem solving","logical thinking abilities","aptitude", "quantitative", "math", "percentage", "ratio","aptitude", "quantitative", "probability", "numbers",
        "percentages", "ratio", "time and work"],
    "English": ["english", "grammar", "verbal", "communication","verbal ability", "grammar", "vocabulary",
        "communication", "english proficiency","reading comprehension","sentence correction","Listening skills","writing skills"],
    "Coding": [
        "python", "java", "c++", "sql", "django", "oop",
        "data structure", "algorithm","programming language", "python", "java", "c++",
        "data structures", "algorithms", "coding","C#", "javascript","backend","frontend","Sql","NoSQL"
    ]
}


def extract_sections_from_jd(text):
    text = text.lower()
    matched_sections = set()

    for section, keywords in SKILL_KEYWORDS.items():
        for word in keywords:
            if word in text:
                matched_sections.add(section)
                break

    return list(matched_sections)


# -------------------------------------------------
# ADVANCED SECTION SCORING (strong relevance)
# -------------------------------------------------
SECTION_KEYWORDS = {
    "Aptitude": [
        "aptitude", "quantitative", "probability", "numbers",
        "percentages", "ratio", "time and work"
    ],
    "Reasoning": [
        "logical reasoning", "analytical thinking", "puzzles",
        "critical thinking", "verbal reasoning","problem solving","logical thinking abilities"
    ],
    "English": [
        "verbal ability", "grammar", "vocabulary",
        "communication", "english proficiency","reading comprehension","sentence correction","Listening skills","writing skills"
    ],
    "Coding": [
        "programming language", "python", "java", "c++",
        "data structures", "algorithms", "coding","C#", "javascript","backend","frontend","Sql","NoSQL"
    ]
}


def extract_relevant_sections(jd_text):
    jd_text = jd_text.lower()
    section_scores = {}

    for section, keywords in SECTION_KEYWORDS.items():
        score = 0
        for kw in keywords:
            if kw in jd_text:
                score += 1
        section_scores[section] = score

    # Require at least 2 keyword matches
    recommended_sections = [
        section for section, score in section_scores.items()
        if score >= 2
    ]

    return recommended_sections


# -------------------------------------------------
# 🔥 REQUIRED BY VIEWS.PY (DO NOT REMOVE)
# -------------------------------------------------
def map_jd_to_sections(jd_text):
    """
    Unified JD → Section mapper
    Used by views.py
    """

    # First try strong relevance
    sections = extract_relevant_sections(jd_text)

    # Fallback if JD is small or weak
    if not sections:
        sections = extract_sections_from_jd(jd_text)

    return sections
