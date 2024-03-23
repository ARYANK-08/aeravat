import fitz  # PyMuPDF
import re

def extract_text_from_pdf(pdf_path):
    """Extracts text from a PDF file."""
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text()
    return text

def find_information(text):
    """Finds specific information based on patterns."""
    info = {
        'name': None,
        'skills': [],
        'projects': [],
        'linkedin_profile': None,
        'email': None
    }
    
    # Regular expressions for matching patterns
    name_pattern = re.compile(r"NAME\s*:\s*(.*)", re.IGNORECASE)
    skills_pattern = re.compile(r"EDUCATION[\s\S]+?([\w\s,]+)\s*(?:\n|$)", re.IGNORECASE)
    projects_pattern = re.compile(r"Developed\s+(.*?)(?:Tech\s+Stack\s*:\s*(.*?))?\s*(?:$|\n)", re.IGNORECASE | re.DOTALL)
    # Adjusted regular expressions for matching patterns
    linkedin_pattern = re.compile(r"Linkedin\s*:\s*(https?://[www\.]?linkedin\.com/in/[\w-]+/?\b)", re.IGNORECASE)

    # Searching for matches in the text
    email_pattern = re.compile(r"Email\s*:\s*([\w\.-]+@[\w\.-]+)", re.IGNORECASE)

    # Searching for matches in the text
    name_match = name_pattern.search(text)
    skills_match = skills_pattern.search(text)
    projects_matches = projects_pattern.findall(text)
    linkedin_match = linkedin_pattern.search(text)
    email_match = email_pattern.search(text)

    # Assigning matched information to the info dictionary
    if name_match:
        info['name'] = name_match.group(1).strip()
    if skills_match:
        info['skills'] = [skill.strip() for skill in skills_match.group(1).split(',')]
    for project, tech_stack in projects_matches:
        info['projects'].append({'name': project.strip(), 'tech_stack': tech_stack.strip()})
    if linkedin_match:
        info['linkedin_profile'] = linkedin_match.group(1).strip()
    if email_match:
        info['email'] = email_match.group(1).strip()

    return info

# Main code to extract information from a PDF
if __name__ == "__main__":
    pdf_path = 'C:/Users/kyath/OneDrive/Desktop/Aeravat/code/test.pdf'
  # Update this to your PDF file path
    text = extract_text_from_pdf(pdf_path)
    extracted_info = find_information(text)
    
    print("Extracted Information:")
    print(f"Name: {extracted_info['name']}")
    print(f"Skills: {', '.join(extracted_info['skills'])}")
    print("Projects:")
    for project in extracted_info['projects']:
        print(f"  - {project['name']}: {project['tech_stack']}")
    print(f"LinkedIn Profile: {extracted_info['linkedin_profile']}")
    print(f"Email: {extracted_info['email']}")

# Path to your PDF file
