import re
from bs4 import BeautifulSoup
import pandas as pd
import requests

def extract_courses(html_content):
    """Extract course information from HTML content using the actual UW CSE HTML structure"""
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Find all <a> tags with 'name' attributes starting with 'cse'
    course_anchors = soup.find_all('a', attrs={'name': re.compile(r'cse\d+')})
    
    courses = []
    
    for anchor in course_anchors:
        # Get the course code from the name attribute
        course_code = anchor['name'].upper()
        
        # The anchor contains a paragraph with the course info
        p_tag = anchor.find('p')
        if not p_tag:
            continue
            
        # Get the course name which is inside a <b> tag
        b_tag = p_tag.find('b')
        if not b_tag:
            continue
            
        course_name = b_tag.text.strip()
        
        # Extract credits and designations
        match = re.search(r'\(([\d\-, max\.\s]+)(?:\s+([A-Za-z&/]+))?\)', course_name)
        
        credits = ""
        designations = ""
        if match:
            credits = match.group(1).strip() if match.group(1) else ""
            designations = match.group(2).strip() if match.group(2) else ""
        
        # Clean up the course name (remove credits and designations)
        clean_name = re.sub(r'\s*\([\d\-, max\.\s]+(?:\s+[A-Za-z&/]+)?\)\s*$', '', course_name).strip()
        
        # The description is the text after the course name
        description_text = p_tag.get_text()
        
        # Remove the course name part
        description = description_text.replace(course_name, '', 1).strip()
        
        # Remove the "View course details in MyPlan" text
        description = re.sub(r'View course details in MyPlan: CSE \d+\.?', '', description).strip()
        
        courses.append({
            'Course Code': course_code,
            'Course Name': clean_name,
            'Credits': credits,
            'Designations': designations,
            'Description': description
        })
    
    return courses

def main():
    print(f"Fetching data from https://www.washington.edu/students/crscat/cse.html")
    response = requests.get("https://www.washington.edu/students/crscat/cse.html")
    html_content = response.text
        
    courses = extract_courses(html_content)
    
    if not courses:
        print("No courses found. Check if the HTML structure matches expectations.")
        return
        
    # Create DataFrame
    df = pd.DataFrame(courses)
    
    # Display stats
    print(f"\nTotal courses found: {len(df)}")
    print("\nSample of first 5 courses:")
    print(df[['Course Code', 'Course Name', 'Credits']].head())
    
    # Save to CSV
    df.to_csv('uw_cse_courses.csv', index=False)
    print(f"\nData saved to uw_cse_courses.csv")
    

if __name__ == "__main__":
    main()