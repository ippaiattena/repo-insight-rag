import streamlit as st
from repo_insight.rag_core import answer_query
import shutil

st.set_page_config(page_title="Repo Insight RAG", layout="wide")
st.title("🧠 Repo Insight RAG")

# 初期化
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "user_input" not in st.session_state:
    st.session_state.user_input = ""

# 入力フォーム
with st.sidebar:
    repo_url = st.text_input("GitHubリポジトリURL", "https://github.com/ippaiattena/ai_invest_bot.git")
    pull_latest = st.checkbox("最新の状態を取得する（git pull）", value=True)
    if st.button("初期化（履歴とDB削除）"):
        st.session_state.chat_history = []
        st.session_state.user_input = ""
        shutil.rmtree("./chroma_db", ignore_errors=True)
        st.success("初期化しました（DB削除済み）")

# チャット表示
st.subheader("💬 質問チャット")

for i, (q, a) in enumerate(st.session_state.chat_history):
    st.markdown(f"**🧍 質問{i+1}:** {q}")
    st.markdown(f"**🤖 回答{i+1}:** {a}")

# 新しい質問
st.text_input("質問を入力", value=st.session_state.user_input, key="user_input")
submit = st.button("送信")

if submit and st.session_state.user_input:
    with st.spinner("思考中..."):
        try:
            answer = answer_query(repo_url=repo_url, query=st.session_state.user_input, pull=pull_latest)
            st.session_state.chat_history.append((st.session_state.user_input, answer))
            st.rerun()
        except Exception as e:
            st.error(f"エラーが発生しました: {e}")
