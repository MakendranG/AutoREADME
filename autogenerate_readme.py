
import requests
import os

from jinja2 import Template

def fetch_repo_details(repo_url):
    """
    Extracts the repository owner and name from the given URL,
    then fetches repository details using the GitHub API.
    """
    parts = repo_url.rstrip('/').split('/')
    if len(parts) < 2:
        raise ValueError("Invalid GitHub URL")
    owner, repo = parts[-2], parts[-1]
    api_url = f"https://api.github.com/repos/{owner}/{repo}"
    response = requests.get(api_url)
    response.raise_for_status()  # Ensure the API call was successful
    return response.json()

def generate_readme(repo_data):
    """
    Generates a well-formatted README using a Jinja2 template
    based on the repository data fetched from GitHub.
    """
    readme_template = """
# {{ name }}

{{ description }}

## Repository Details

- **Primary Language:** {{ language }}
- **Stars:** {{ stargazers_count }}
- **Forks:** {{ forks_count }}
- **Open Issues:** {{ open_issues_count }}
{% if license %}
- **License:** {{ license.name }}
{% endif %}

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Installation

Clone the repository:

~~~bash
git clone {{ html_url }}
~~~

## Usage

Follow the usage instructions provided in the project documentation.

## Contributing

Feel free to fork the project and submit pull requests. For major changes, please open an issue first.

## License

{% if license %}
This project is licensed under the {{ license.name }} license.
{% else %}
No license information provided.
{% endif %}
    """
    template = Template(readme_template)
    return template.render(
        name=repo_data.get("name", "Project Name"),
        description=repo_data.get("description", "No description provided."),
        language=repo_data.get("language", "N/A"),
        stargazers_count=repo_data.get("stargazers_count", 0),
        forks_count=repo_data.get("forks_count", 0),
        open_issues_count=repo_data.get("open_issues_count", 0),
        license=repo_data.get("license", None),
        html_url=repo_data.get("html_url", "")
    )

if __name__ == "__main__":
    repo_url = os.getenv("REPO_URL") or input("Enter the GitHub repository URL: ")
    try:
        repo_data = fetch_repo_details(repo_url)
        readme_content = generate_readme(repo_data)
        with open("README.md", "w") as file:
            file.write(readme_content)
        print("README.md generated successfully!")
    except Exception as e:
        print("Error:", e)
