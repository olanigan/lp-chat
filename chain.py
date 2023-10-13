from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.llms import Replicate
from langchain.callbacks import get_openai_callback

from store import init_vector_store
from utils import pretty_print_docs

INDEX = "lpnotes"

# Build prompt
template = """Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer. Use six sentences maximum. 
{context}
Question: {question}
Helpful Answer:"""
QA_CHAIN_PROMPT = PromptTemplate.from_template(template)

store = None
chain = None

def chat_chain(input, use_chain):
    get_ops()

    retriever = store.as_retriever()
    # Retreive related search results
    output = retriever.get_relevant_documents(input)
    output =  pretty_print_docs(output)
    if not use_chain:
        return {"summary": output, "sources": output}
    # Call LLMChain
    with get_openai_callback() as cb:
        # Use LLM to summarize/optimize results
        summary = chain({"question": input,
                        "context": output})
        # st.session_state[SUMMARY] = summary['text']
        print(cb)
    print(f"Question: {summary['question']}\n\nAnswer: {summary['text']}")
    return {"summary": summary['text'], "sources": output}


def get_ops():
    global store, chain
    if not store or not chain:
        print("Initializing Store&Chain")
        store, chain = init_ops()
    return store, chain

def init_ops():
    # Initiate/Load Vector store
    store = init_vector_store(INDEX)
    # Initiate LLMChain
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
    chain = LLMChain(llm=llm, prompt=QA_CHAIN_PROMPT)
    return store, chain

def replicate():
    model = 'a16z-infra/llama13b-v2-chat:df7690f1994d94e96ad9d568eac121aecf50684a0b0963b25a41cc40061269e5'
        
    return Replicate(
        model=model,
        input = {"temperature": 0.1, "max_length":1000,"top_p":1})