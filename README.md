# Obsidian GitHub Sync

A simple CLI tool to sync your Obsidian vault with GitHub, allowing you to keep your notes synchronized across multiple devices.

## Prerequisites

- Python 3.7 or higher
- Git installed on your system
- A GitHub account and repository for your Obsidian vault
- Your Obsidian vault

## Installation

1. Clone this repository or download the files
2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### First-time setup

Before you can start syncing, you need to run the setup command to configure your vault and GitHub repository:

```bash
python obsidian_sync.py setup --vault-path "path/to/your/vault" --repo-url "https://github.com/username/repo.git"
```

### Syncing your vault

To sync your vault with GitHub, simply run:

```bash
python obsidian_sync.py sync
```

You can also add a custom commit message:

```bash
python obsidian_sync.py sync --message "Updated notes on topic X"
```

## How it works

The tool will:
1. Initialize a Git repository in your Obsidian vault (if not already initialized)
2. Track all changes in your vault
3. Pull any changes from the remote repository
4. Commit your local changes with a timestamp or custom message
5. Push the changes to GitHub

## Tips

1. Make sure to create a `.gitignore` file in your vault to exclude unnecessary files
2. Run the sync command periodically to keep your vaults in sync
3. If you encounter conflicts, resolve them manually in your preferred text editor

## Troubleshooting

If you encounter any issues:
1. Ensure you have the correct permissions for the GitHub repository
2. Check if your Git credentials are properly configured
3. Make sure your vault path is correct
4. Verify that you have an active internet connection 