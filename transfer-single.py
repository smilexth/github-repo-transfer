import requests
import os
import argparse
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configuration from environment variables
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
PERSONAL_USERNAME = os.getenv("PERSONAL_USERNAME")
TARGET_ORG = os.getenv("TARGET_ORG")
DEFAULT_REPO = os.getenv("REPO_NAME")  # Default repository name from .env

# GitHub API headers
HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

# Base URL for GitHub API
BASE_URL = "https://api.github.com"

def transfer_repo(owner, repo_name, new_owner):
    """
    Transfer a repository to a new owner (organization).
    """
    url = f"{BASE_URL}/repos/{owner}/{repo_name}/transfer"
    data = {"new_owner": new_owner}
    response = requests.post(url, json=data, headers=HEADERS)
    if response.status_code in [202, 201]:
        print(f"Repository '{repo_name}' transfer initiated successfully.")
        return True
    else:
        print(f"Failed to transfer repository '{repo_name}': {response.status_code} {response.text}")
        return False

def verify_repo_exists(owner, repo_name):
    """
    Verify that the repository exists before attempting to transfer it.
    """
    url = f"{BASE_URL}/repos/{owner}/{repo_name}"
    response = requests.get(url, headers=HEADERS)
    return response.status_code == 200

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Transfer a single GitHub repository to an organization')
    parser.add_argument('--repo', '-r', type=str, help='Repository name to transfer', default=DEFAULT_REPO)
    args = parser.parse_args()
    
    repo_name = args.repo
    
    if not repo_name:
        print("Error: Repository name not provided. Please specify it with --repo flag or in .env file.")
        return
    
    if not verify_repo_exists(PERSONAL_USERNAME, repo_name):
        print(f"Error: Repository '{repo_name}' does not exist or you don't have access to it.")
        return
    
    print(f"Transferring repository: {repo_name} from {PERSONAL_USERNAME} to {TARGET_ORG}")
    transfer_repo(PERSONAL_USERNAME, repo_name, TARGET_ORG)

if __name__ == "__main__":
    main()
