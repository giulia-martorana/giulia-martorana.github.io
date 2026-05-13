# Updating submodules ---------------------------------------------------
import os
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path


# --- Functions ---

def run_command(command):
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
    print(f"STDOUT: {result.stdout.strip()}")
    print(f"STDERR: {result.stderr.strip()}")  # <-- add these two lines
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        sys.exit(result.returncode)
    return result.stdout.strip()
    
def git_add():
    print("Adding changes...")
    run_command("git add index.html")

def has_changes():
    result = subprocess.run("git status --porcelain index.html", stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
    return bool(result.stdout.strip())  # <-- added

def git_commit():
    print("Committing changes...")
    dt = datetime.now() - timedelta(days=1)
    commit_message = f"Automated commit: {dt.strftime('%d%b%y')} data loaded"
    run_command(f'git commit -m "{commit_message}"')

def git_push():
    print("Pushing changes to GitLab...")
    run_command("git push origin main")
    
def git_automation():
    try:
        run_command(f'git config user.name "{GITHUB_USERNAME}"')
        run_command(f'git remote set-url origin https://{GITHUB_USERNAME}:{GITHUB_TOKEN}@github.com/{GITHUB_USERNAME}/{GITHUB_USERNAME}.github.io.git')
        git_add()
        if not has_changes():  # <-- added
            print("No changes to commit. Exiting.")
            return
        git_commit()
        git_push()
        print("Changes have been pushed to the remote repository.")
    except Exception as e:
        print("An error occurred:")
        print(e)
        
# --- MAIN ---
GITHUB_TOKEN = os.environ.get('GITHUB_ACCESS_TOKEN')
GITHUB_USERNAME = 'giulia-martorana'

# Change to working directory that contains the Git repo and MATLAB script
os.chdir('/home/cdsw/giulia-martorana.github.io') # To reach any Git parent folder
print("Current working directory:", os.getcwd())
script_dir = Path('/home/cdsw/giulia-martorana.github.io') 

# Push updated results to GitLab
git_automation()