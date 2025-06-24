import streamlit as st
from repo_insight.rag_core import answer_query

st.set_page_config(page_title="Repo Insight RAG", layout="wide")
st.title("🧠 Repo Insight RAG")

# 初期化
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# 入力フォーム
with st.sidebar:
    repo_url = st.text_input("GitHubリポジトリURL", "https://github.com/ippaiattena/ai_invest_bot.git")
    pull_latest = st.checkbox("最新の状態を取得する（git pull）", value=True)
    if st.button("初期化（履歴とDB削除）"):
        st.session_state.chat_history = []
        st.success("初期化しました（※DB削除は今後対応）")

# チャット表示
st.subheader("💬 質問チャット")

for i, (q, a) in enumerate(st.session_state.chat_history):
    st.markdown(f"**🧍 質問{i+1}:** {q}")
    st.markdown(f"**🤖 回答{i+1}:** {a}")

# 新しい質問
query = st.text_input("質問を入力", key="user_input")

if query:
    with st.spinner("思考中..."):
        try:
            answer = answer_query(repo_url=repo_url, query=query, pull=pull_latest)
            st.session_state.chat_history.append((query, answer))
            st.rerun()
        except Exception as e:
            st.error(f"エラーが発生しました: {e}")
