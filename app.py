import streamlit as st
from store import init_vector_store
from utils import pretty_print_docs

SEMANTIC = 'semantic'
CHUNKS = 'chunks'

def init_state():
    if 'semantic' not in st.session_state:
        st.session_state[SEMANTIC] = ''

    if CHUNKS not in st.session_state:
        st.session_state[CHUNKS] = ''

def display_form(store):
    query_container = st.container()
    semantic_container = st.container()
    summary_container = st.container()

    with query_container:
        with st.form(key='my_form', clear_on_submit=True):
            user_input = st.text_input("Question:", value="What is the ruling of using Siwak", key='input')
            submit_button = st.form_submit_button(label='Send')

        if submit_button and user_input:
            # output = store.max_marginal_relevance_search(user_input)

            retriever = store.as_retriever()
            output = retriever.get_relevant_documents(user_input)
            
            st.session_state[SEMANTIC] =  pretty_print_docs(output)      

    with semantic_container:
       st.text_area(label="Summary:",
                    height=400,
                    value=st.session_state[SEMANTIC])
 

    # with summary_container:
    #     st.text_area(label="Summary:",value=summarize(user_input))

def parse_output(output):
    result = ""

    for el in output:
        result = f"{result}\n\n{el.page_content}[{el.metadata}]"
    return result

def main():
    init_state()
    store = init_vector_store("first2")
    display_form(store)

if __name__ == "__main__":
    main()