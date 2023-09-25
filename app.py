import streamlit as st

SEMANTIC = 'semantic'

def init_state():
    if 'semantic' not in st.session_state:
        st.session_state[SEMANTIC] = ''

def display_form():
    query_container = st.container()
    semantic_container = st.container()
    summary_container = st.container()

    with query_container:
        with st.form(key='my_form', clear_on_submit=True):
            user_input = st.text_input("Question:", placeholder="What is the ruling of using Siwak", key='input')
            submit_button = st.form_submit_button(label='Send')

        if submit_button and user_input:
            st.session_state[SEMANTIC] = "You typed:\n\n" + user_input       

    with semantic_container:
       st.text_area(label="Summary:",value=st.session_state[SEMANTIC])
 

    # with summary_container:
    #     st.text_area(label="Summary:",value=summarize(user_input))

def main():
    init_state()
    display_form()

if __name__ == "__main__":
    main()