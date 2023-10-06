import streamlit as st
from store import init_vector_store
from utils import pretty_print_docs
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from langchain.callbacks import get_openai_callback
from flask import Flask, request

app = Flask(__name__)

SEMANTIC = 'semantic'
CHUNKS = 'chunks'
SUMMARY = 'summary'
INDEX = "first2"

STATES = [SEMANTIC, CHUNKS, SUMMARY]

store = None
chain = None

# Build prompt
template = """Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer. Use six sentences maximum. 
{context}
Question: {question}
Helpful Answer:"""
QA_CHAIN_PROMPT = PromptTemplate.from_template(template)

st.set_page_config(layout="wide")
st.title("🧠📚📈 Logical Progression")
st.markdown("## Class Notes from Year 1 - 10!")

def init_state():
    for state in STATES:
        if state not in st.session_state:
            st.session_state[state] = ''

def display_form(store, chain):
    # query_container = st.container()
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
            chat_chain(sample_input)
        elif input_submit_button and user_input:
            chat_chain(user_input)

    with summary_container:
        st.text_area(label="Summary:",
                     height=200,
                     value=st.session_state[SUMMARY])
    
    with semantic_container:
       st.text_area(label="Sources:",
                    height=400,
                    value=st.session_state[SEMANTIC])

def chat_chain(input):
    retriever = store.as_retriever()
    # Retreive related search results
    output = retriever.get_relevant_documents(input)
    output =  pretty_print_docs(output)
    st.session_state[SEMANTIC] =  output
    # Call LLMChain
    with get_openai_callback() as cb:
        # Use LLM to summarize/optimize results
        summary = chain({"question": input,
                        "context": output})
        st.session_state[SUMMARY] = summary['text']
        print(cb)
    print(f"Question: {summary['question']}\n\nAnswer: {summary['text']}")
    return {"summary": summary, "sources": output}

@app.route('/')
def home():
    return "Welcome to LP Chat API", 200

@app.route('/api', methods=['GET', 'POST'])
def index():
    """Prints the POST request message."""
    message = request.get_json()
    message = message['message']
    print(f"Received message: {message}")
    # return "Welcome to LP Chat API", 200
    print('Loading Store&Chain for HTTP')
    return chat_chain(message), 200

def main():
    print('Loading Store&Chain for UI')
    store, chain = get_ops()
    # Show Q&A Form
    display_form(store, chain)

def get_ops():
    global store, chain
    if not store or not chain:
        print("Initializing Store&Chain")
        store, chain = init_ops()
    return store, chain

def init_ops():
      # Initiate session states
    init_state()
    # Initiate/Load Vector store
    store = init_vector_store(INDEX)
    # Initiate LLMChain
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
    chain = LLMChain(llm=llm, prompt=QA_CHAIN_PROMPT)
    return store, chain

if __name__ == "__main__":
    main()
    app.run(port=5001)