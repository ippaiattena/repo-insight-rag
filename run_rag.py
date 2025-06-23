import argparse
import os
from git import Repo
from repo_insight.embedder import load_embedder
from repo_insight.retriever import setup_retriever
from repo_insight.generator import build_qa_chain

REPO_ROOT = "repos"

def clone_or_pull_repo(repo_url: str, repo_name: str, pull: bool = False) -> str:
    local_path = os.path.join(REPO_ROOT, repo_name)
    if os.path.exists(local_path):
        if pull:
            print(f"🔄 Pulling latest changes in {local_path}...")
            repo = Repo(local_path)
            repo.remotes.origin.pull()
        else:
            print(f"📂 Repo already exists at {local_path}")
    else:
        print(f"⬇️ Cloning {repo_url} into {local_path}...")
        Repo.clone_from(repo_url, local_path)
    return local_path

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-url", type=str, required=True, help="GitHub repo URL")
    parser.add_argument("--pull", action="store_true", help="Pull latest changes if repo exists")
    return parser.parse_args()

def main():
    args = parse_args()
    repo_url = args.repo_url
    repo_name = repo_url.rstrip("/").split("/")[-1].replace(".git", "")
    local_path = clone_or_pull_repo(repo_url, repo_name, pull=args.pull)

    persist_dir = os.path.join("./chroma_db", repo_name)

    embedder = load_embedder()
    retriever = setup_retriever(persist_dir, embedder, local_path=local_path, reset=False)
    qa_chain = build_qa_chain(retriever)

    print("✅ セットアップ完了！質問どうぞ（終了は exit）")
    while True:
        query = input("\n🧠 質問: ")
        if query.lower() in ["exit", "quit"]:
            break
        print("🤖 回答:", qa_chain.run(query))

if __name__ == "__main__":
    os.makedirs(REPO_ROOT, exist_ok=True)
    main()
