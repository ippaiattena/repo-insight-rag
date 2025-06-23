from repo_insight.embedder import load_embedder
from repo_insight.retriever import setup_retriever
from repo_insight.generator import build_qa_chain

persist_dir = "./chroma_db"

embedder = load_embedder()
retriever = setup_retriever(persist_dir, embedder, reset=False)
qa_chain = build_qa_chain(retriever)

print("✅ セットアップ完了！質問どうぞ（終了は exit）")

while True:
    query = input("\n🧠 質問: ")
    if query.lower() in ["exit", "quit"]:
        break
    print("🤖 回答:", qa_chain.run(query))
