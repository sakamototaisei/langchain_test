import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
import os
import secret_keys

os.environ['OPENAI_API_KEY']=secret_keys.OpenAIAPI.openai_api_key
chat = ChatOpenAI(model="gpt-3.5-turbo")

# プロンプトのテンプレート
system_template = (
    "あなたは、{source_lang}を{target_lang}に翻訳する優秀な翻訳アシスタントです。翻訳結果以外は出力しないでください"
)
system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)

human_template = "{text}"
human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

chat_prompt = ChatPromptTemplate.from_messages(
    [system_message_prompt, human_message_prompt]
)

if "response" not in st.session_state:
    st.session_state["response"] = ""

# LLMとやりとりする関数
def communicate():
    text = st.session_state["user_input"]
    response = chat(
        chat_prompt.format_prompt(
            text=text,
            source_lang=source_lang,
            target_lang=target_lang
        ).to_messages()
    )
    st.session_state["response"] = response.content

# ユーザーインターフェースの構築
st.title("翻訳アプリ")
st.write("LnagChainを使った翻訳アプリです")

options = ["日本語", "英語", "フランス語", "中国語", "スペイン語", "ドイツ語"]
source_lang = st.selectbox("翻訳元", options=options)
target_lang = st.selectbox("翻訳先", options=options)

st.text_input("翻訳したいテキストを入力してください", key="user_input")
st.button("翻訳", type="primary", on_click=communicate)

if st.session_state["user_input"] != "":
    st.write("翻訳結果：")
    st.write(st.session_state["response"])
