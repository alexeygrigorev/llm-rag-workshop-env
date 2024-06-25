import streamlit as st

from rag import rag


# https://chatgpt.com/share/53192091-232a-491d-9cd3-aa510390dc1a

# Streamlit UI
st.title("RAG Function Invoker")

# Input box for user query
user_query = st.text_input("Enter your query:")

# Button to invoke the function
if st.button("Run RAG Function"):
    with st.spinner('Processing...'):
        result = rag(user_query)
        st.success("Done!")
        # Output for showing the results
        st.write(result)
