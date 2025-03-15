import requests
from jinja2 import Template

def fetch_repo_details(repo_url):
    # Extract owner and repository name from the URL
    parts = repo_url.rstrip('/').split('/')
    if len(parts) < 2:
        raise ValueError("Invalid GitHub URL")
    owner, repo = parts[-2], parts[-1]
    api_url = f"https://api.github.com/repos/{owner}/{repo}"
    response = requests.get(api_url)
    response.raise_for_status()
    return response.json()

def generate_readme(repo_data):
    # Simple README template
    readme_template = """
# {{ name }}

{{ description }}

## Primary Language
- {{ language }}

<!-- You can add more sections here -->
    """
    template = Template(readme_template)
    return template.render(
        name=repo_data.get("name", "Project Name"),
        description=repo_data.get("description", "No description provided."),
        language=repo_data.get("language", "N/A")
    )

if __name__ == "__main__":
    repo_url = input("Enter the GitHub repository URL: ")
    try:
        repo_data = fetch_repo_details(repo_url)
        readme_content = generate_readme(repo_data)
        with open("README.md", "w") as file:
            file.write(readme_content)
        print("README.md generated successfully!")
    except Exception as e:
        print("Error:", e)
