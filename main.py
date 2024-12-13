import streamlit as st
from scrape import (
    scrape_website,
    extract_body_content,
    clean_body_content,
    split_dom_content,
)
from parse import parse_with_ollama
from langchain_ollama import OllamaLLM


st.title("AI Web Scraper")
url = st.text_input("Enter Website URL")

# Step 1: Scrape the Website
if st.button("Scrape Website"):
    st.write("Scraping the website...")

    result = scrape_website(url)
    if result:
        body_content = result  # Assuming the result is already cleaned and split
        st.session_state.dom_content = "\n".join(body_content)  # Store in session_state

        st.write("Content scraped successfully!")
        with st.expander("View DOM Content"):
            st.text_area("DOM Content", st.session_state.dom_content, height=900)

        # Add a download button for the DOM content
        st.download_button(
            label="Download DOM Content as .txt",
            data=st.session_state.dom_content,
            file_name="dom_content.txt",
            mime="text/plain",
        )
    else:
        st.write("Failed to scrape the website.")
