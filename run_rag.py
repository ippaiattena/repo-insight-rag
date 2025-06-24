import argparse
import os
from repo_insight.utils.repo_manager import clone_or_pull_repo_from_url, get_repo_name_from_url
from repo_insight.embedder import load_embedder
from repo_insight.retriever import setup_retriever
from repo_insight.generator import build_qa_chain

REPO_ROOT = "repos"

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-url", type=str, required=True, help="GitHub repo URL")
    parser.add_argument("--pull", action="store_true", help="Pull latest changes if repo exists")
    return parser.parse_args()

def main():
    args = parse_args()
    repo_url = args.repo_url
    local_path = clone_or_pull_repo_from_url(repo_url, pull=args.pull)
    repo_name = get_repo_name_from_url(repo_url)

    persist_dir = os.path.join("./chroma_db", repo_name)

    embedder = load_embedder()
    retriever = setup_retriever(persist_dir, embedder, local_path=local_path, reset=True)
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
