import os
import sys
from pathlib import Path
from datetime import datetime
import typer
from git import Repo
from git.exc import GitCommandError
from rich.console import Console
from rich.progress import Progress
from dotenv import load_dotenv

# Initialize Typer app and Rich console
app = typer.Typer()
console = Console()

def init_repo(vault_path: Path, repo_url: str) -> Repo:
    """Initialize or get the Git repository."""
    try:
        if not (vault_path / '.git').exists():
            console.print(f"Initializing new Git repository in {vault_path}", style="yellow")
            repo = Repo.init(vault_path)
            repo.create_remote('origin', repo_url)
        else:
            repo = Repo(vault_path)
        return repo
    except Exception as e:
        console.print(f"Error initializing repository: {str(e)}", style="red")
        sys.exit(1)

def sync_changes(repo: Repo, commit_message: str = None):
    """Sync changes with remote repository."""
    try:
        # Add all changes
        repo.git.add('.')
        
        # Create commit message
        if not commit_message:
            commit_message = f"Vault sync: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        # Ensure we're on main branch
        if 'main' not in repo.heads:
            # If main branch doesn't exist locally, create it
            console.print("Creating main branch...", style="yellow")
            repo.git.checkout('-b', 'main')
        else:
            repo.heads.main.checkout()
        
        # Only commit if there are changes
        if repo.is_dirty() or len(repo.untracked_files) > 0:
            repo.index.commit(commit_message)
            console.print("Changes committed successfully", style="green")
        
        try:
            # Check if remote main branch exists
            remote_main_exists = 'main' in [ref.name for ref in repo.remotes.origin.refs]
            
            if remote_main_exists:
                # Pull changes from remote if main branch exists
                console.print("Pulling changes from remote...", style="yellow")
                repo.remotes.origin.pull('main')
            else:
                # If main branch doesn't exist, just push to create it
                console.print("Initializing remote repository...", style="yellow")
                repo.git.push('--set-upstream', 'origin', 'main')
        except GitCommandError:
            # If checking remote refs fails, assume branch doesn't exist and create it
            console.print("Initializing remote repository...", style="yellow")
            repo.git.push('--set-upstream', 'origin', 'main')
        
        # Push changes to remote
        console.print("Pushing changes to remote...", style="yellow")
        repo.remotes.origin.push('main')
        
        console.print("Sync completed successfully! ✨", style="green bold")
    except GitCommandError as e:
        console.print(f"Git error: {str(e)}", style="red")
        sys.exit(1)
    except Exception as e:
        console.print(f"Error during sync: {str(e)}", style="red")
        sys.exit(1)

@app.command()
def setup(
    vault_path: str = typer.Option(..., "--vault-path", "-v", help="Path to your Obsidian vault"),
    repo_url: str = typer.Option(..., "--repo-url", "-r", help="GitHub repository URL")
):
    """Setup the Obsidian vault for syncing."""
    vault_path = Path(vault_path).resolve()
    if not vault_path.exists():
        console.print(f"Error: Vault path {vault_path} does not exist!", style="red")
        sys.exit(1)
    
    # Save configuration
    with open(".env", "w") as f:
        f.write(f"VAULT_PATH={vault_path}\n")
        f.write(f"REPO_URL={repo_url}\n")
    
    repo = init_repo(vault_path, repo_url)
    console.print("Setup completed successfully! 🎉", style="green bold")

@app.command()
def sync(
    commit_message: str = typer.Option(None, "--message", "-m", help="Custom commit message")
):
    """Sync your Obsidian vault with GitHub."""
    load_dotenv()
    
    vault_path = os.getenv("VAULT_PATH")
    repo_url = os.getenv("REPO_URL")
    
    if not vault_path or not repo_url:
        console.print("Error: Please run setup first!", style="red")
        sys.exit(1)
    
    vault_path = Path(vault_path)
    repo = init_repo(vault_path, repo_url)
    sync_changes(repo, commit_message)

if __name__ == "__main__":
    app() 