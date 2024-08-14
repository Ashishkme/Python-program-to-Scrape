# !pip install requests beautifulsoup4
import requests
from bs4 import BeautifulSoup

# URL of the website
url = "https://hprera.nic.in/PublicDashboard"

# Send a GET request to fetch the HTML content
response = requests.get(url, verify=False) # Disable SSL certificate verification
soup = BeautifulSoup(response.content, "html.parser")

# Find the Registered Projects section
registered_projects_section = soup.find("div", {"id": "collapseOne"})

# Extract first 6 Project
if registered_projects_section:
    projects = registered_projects_section.find_all("tr")[1:7]  # Skipping header row

    project_data = []

    for project in projects:
        # Extract RERA number link
        rera_link = project.find("a")["href"]
        rera_url = f"https://hprera.nic.in/{rera_link}"

        # Fetch project details by visiting the RERA number page
        project_response = requests.get(rera_url)
        project_soup = BeautifulSoup(project_response.content, "html.parser")

        # Extract project details
        gstin = project_soup.find("span", {"id": "lblGSTIN"}).text.strip()
        pan = project_soup.find("span", {"id": "lblPAN"}).text.strip()
        name = project_soup.find("span", {"id": "lblProjectName"}).text.strip()
        address = project_soup.find("span", {"id": "lblAddress"}).text.strip()

        project_data.append({
            "GSTIN": gstin,
            "PAN": pan,
            "Name": name,
            "Permanent Address": address
        })
else:
    print("Element with ID 'collapseOne' not found. Please check the HTML structure.")

# Print Project Details
project_data = []

for idx, data in enumerate(project_data, 1):
    print(f"Project {idx}:")
    print(f"  GSTIN: {data['GSTIN']}")
    print(f"  PAN: {data['PAN']}")
    print(f"  Name: {data['Name']}")
    print(f"  Permanent Address: {data['Permanent Address']}\n")