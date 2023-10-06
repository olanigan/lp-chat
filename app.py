import streamlit as st
from chain import chat_chain

SEMANTIC = 'semantic'
CHUNKS = 'chunks'
SUMMARY = 'summary'
INDEX = "lpnotes"

STATES = [SEMANTIC, CHUNKS, SUMMARY]

st.set_page_config(layout="wide")
st.title("🧠📚📈 Logical Progression")
st.markdown("### 🔍 Search tool for Class Notes from Year 1 - 10!")

def init_state():
    for state in STATES:
        if state not in st.session_state:
            st.session_state[state] = ''

def display_form():
    col1, col2 = st.columns(2)
    summary_container = st.container()
    semantic_container = st.container()

    with col1:
        with st.form(key='select_form'):
            sample_input = st.selectbox(
                "Select example questions?",
                ("What is the ruling on using the Siwak?", "What is Logical Progression?", "Importance of seeking knowledge", "How to handle pig impurities","Wearing gold silver for men"),
                index=0,
                placeholder="Select sample question...",
                )
            select_submit_button = st.form_submit_button(label='Send')
    
    with col2:
        with st.form(key='input_form', clear_on_submit=False):
            user_input = st.text_input("Question:", placeholder="What is the ruling of using Siwak", key='input')
            input_submit_button = st.form_submit_button(label='Send')

        if select_submit_button and sample_input:
            chain(sample_input)
        elif input_submit_button and user_input:
            chain(user_input)

    with summary_container:
        st.text_area(label="Summary:",
                     height=200,
                     value=st.session_state[SUMMARY])
    
    with semantic_container:
       st.text_area(label="Sources:",
                    height=400,
                    value=st.session_state[SEMANTIC])

def chain(input, use_chain=True):
    response = chat_chain(input, use_chain)

    st.session_state[SEMANTIC] =  response['sources']
    st.session_state[SUMMARY] = response['summary']

    return {"summary": response["summary"], "sources": response["sources"]}

def main():
    init_state()
    display_form()

if __name__ == "__main__":
    main()