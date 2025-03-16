import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configuration from environment variables
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
PERSONAL_USERNAME = os.getenv("PERSONAL_USERNAME")
TARGET_ORG = os.getenv("TARGET_ORG")

# GitHub API headers
HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

# Base URL for GitHub API
BASE_URL = "https://api.github.com"

def get_personal_repos():
    """
    Retrieve all repositories owned by the authenticated user,
    including private repositories.
    """
    repos = []
    page = 1
    per_page = 100
    while True:
        # Use /user/repos instead of /users/{username}/repos to get private repos
        url = f"{BASE_URL}/user/repos?per_page={per_page}&page={page}&affiliation=owner"
        response = requests.get(url, headers=HEADERS)
        if response.status_code != 200:
            print(f"Error fetching repositories: {response.status_code} {response.text}")
            break

        page_repos = response.json()
        if not page_repos:
            break
        repos.extend(page_repos)
        page += 1
    return repos

def main():
    # Get a list of personal repositories (including private ones)
    repos = get_personal_repos()
    if not repos:
        print("No repositories found or an error occurred.")
        return

    print(f"Found {len(repos)} repositories in {PERSONAL_USERNAME}'s account.")
    print("\nRepository List:")
    print("-" * 80)
    
    # Count public and private repositories
    private_count = sum(1 for repo in repos if repo.get("private", False))
    public_count = len(repos) - private_count
    
    print(f"Public repositories: {public_count}")
    print(f"Private repositories: {private_count}")
    print("-" * 80)
    
    # Loop through each repository and display information
    for i, repo in enumerate(repos, 1):
        repo_name = repo["name"]
        visibility = "Private" if repo.get("private", False) else "Public"
        description = repo.get("description", "No description")
        repo_url = repo.get("html_url", "")
        
        print(f"{i}. {repo_name}")
        print(f"   Visibility: {visibility}")
        print(f"   Description: {description}")
        print(f"   URL: {repo_url}")
        print("-" * 80)

if __name__ == "__main__":
    main()
