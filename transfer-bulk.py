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

def transfer_repo(owner, repo_name, new_owner):
    """
    Transfer a repository to a new owner (organization).
    """
    url = f"{BASE_URL}/repos/{owner}/{repo_name}/transfer"
    data = {"new_owner": new_owner}
    response = requests.post(url, json=data, headers=HEADERS)
    if response.status_code in [202, 201]:
        print(f"Repository '{repo_name}' transfer initiated successfully.")
    else:
        print(f"Failed to transfer repository '{repo_name}': {response.status_code} {response.text}")

def main():
    # Get a list of personal repositories
    repos = get_personal_repos()
    if not repos:
        print("No repositories found or an error occurred.")
        return

    print(f"Found {len(repos)} repositories in {PERSONAL_USERNAME}'s account.")

    # Loop through each repository and transfer it
    for repo in repos:
        repo_name = repo["name"]
        print(f"Transferring repository: {repo_name}")
        transfer_repo(PERSONAL_USERNAME, repo_name, TARGET_ORG)

if __name__ == "__main__":
    main()
