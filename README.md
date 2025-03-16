# GitHub Repository Transfer Script

A Python utility script to list and manage GitHub repositories, particularly for transferring repositories between personal accounts and organizations.

## Features

- List all repositories owned by a GitHub user
- Display repository details including name, visibility, and description
- Transfer single repository or bulk repositories to an organization

## Prerequisites

- Python 3.x
- `requests` library
- `python-dotenv` library
- GitHub Personal Access Token (PAT) with appropriate permissions

## Setup

1. Clone this repository or download the script files

2. Create and activate a virtual environment (recommended):
   ```bash
   # Create a virtual environment
   python -m venv venv

   # Activate the virtual environment
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. Install required dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Create a Personal Access Token on GitHub:
   - Go to [GitHub Settings > Developer settings > Personal access tokens](https://github.com/settings/tokens)
   - Generate a new token with at least the following scopes:
     - `repo` (Full control of private repositories) - **Required to see private repositories**
     - `admin:org` (If transferring to organizations)
   
   - **Important:** When selecting repository permissions, you'll need to choose the appropriate access level:
     - **No access**: The token won't have any repository permissions
     - **Access: Public repositories only**: Only allows operations on public repositories
     - **Access: All repositories**: Grants access to both public and private repositories
   
   - For this script to work properly with private repositories, select **"Access: All repositories"**
   - If you only need to transfer public repositories, you can select **"Access: Public repositories only"**
   
   - Copy the generated token

5. Create a `.env` file in the project root directory with the following content:
   ```
   GITHUB_TOKEN=your_github_token_here
   PERSONAL_USERNAME=your_github_username
   TARGET_ORG=target_organization_name
   REPO_NAME=optional_default_repo_name_for_single_transfer
   ```
   
   Replace the values with your actual GitHub token, username, and target organization name.

## Available Scripts

This repository includes several Python scripts for different purposes:

1. `list-repos.py` - Lists all repositories owned by your GitHub account
2. `transfer-single.py` - Transfers a single repository to an organization
3. `transfer-bulk.py` - Transfers all repositories to an organization

## Usage

Ensure your virtual environment is activated before running any commands:

### Listing Your Repositories

To list all your repositories with details (visibility, description, URL):

```bash
python list-repos.py
```

This will display:
- Total number of repositories found
- Count of public and private repositories
- A detailed list of all repositories

### Transferring a Single Repository

To transfer a specific repository to your target organization:

```bash
# Method 1: Use command line argument
python transfer-single.py --repo your-repo-name

# Method 2: Use short flag
python transfer-single.py -r your-repo-name

# Method 3: Use default from .env file (if REPO_NAME is set)
python transfer-single.py
```

### Transferring All Repositories

To transfer all repositories you own to your target organization:

```bash
python transfer-bulk.py
```

**Warning**: This will attempt to transfer ALL repositories you own to the target organization!

## Troubleshooting

### Cannot See Private Repositories

If the script only shows public repositories:

1. Verify your Personal Access Token has the full `repo` scope with "Access: All repositories" permission
2. Generate a new token if necessary with the correct permissions
3. Update your `.env` file with the new token

### Unable to Transfer Repositories

When transferring repositories fails:
1. Ensure you have the appropriate permissions on both the source repository and target organization
2. Verify your PAT has both `repo` (with all repositories access) and `admin:org` scopes
3. Check if there are any organization restrictions that prevent repository transfers

## Security Note

Always keep your GitHub Personal Access Token secure and never commit it to version control. This project includes a `.gitignore` file that prevents the `.env` file from being committed. If you're not using Git, make sure to exclude the `.env` file from any form of sharing.

## License

[MIT License](LICENSE)
