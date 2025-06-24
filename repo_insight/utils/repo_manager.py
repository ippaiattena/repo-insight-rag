import os
from git import Repo

REPO_ROOT = "repos"

def get_repo_name_from_url(repo_url: str) -> str:
    return repo_url.rstrip("/").split("/")[-1].replace(".git", "")

def get_local_path(user: str, repo: str) -> str:
    return os.path.join(REPO_ROOT, user, repo)

def clone_or_pull_repo_from_url(repo_url: str, pull: bool = False) -> str:
    user = repo_url.split("/")[-2]
    repo = get_repo_name_from_url(repo_url)
    local_path = get_local_path(user, repo)

    os.makedirs(os.path.dirname(local_path), exist_ok=True)

    if os.path.exists(local_path):
        if pull:
            print(f"🔄 Pulling latest changes in {local_path}...")
            repo_obj = Repo(local_path)
            repo_obj.remotes.origin.pull()
        else:
            print(f"📂 Repo already exists at {local_path}")
    else:
        print(f"⬇️ Cloning {repo_url} into {local_path}...")
        Repo.clone_from(repo_url, local_path)
    return local_path
