import streamlit as st
from parse_ast import translate_code


# Streamlit App Title
st.title("Code Translator")

# Sidebar for selecting the target language
st.sidebar.header("Translator Settings")
target_language = st.sidebar.selectbox("Select Target Language", ["JavaScript", "C++"," Java"])

# Text area for inputting Python code
st.subheader("Input Python Code")
python_code = st.text_area("Write your Python code here:", height=200)

# Button to trigger translation
if st.button("Translate"):
    if python_code.strip():
        # Call the translator function
        translated_code = translate_code(python_code, target_language)
        
        # Display the translated code
        st.subheader(f"Translated Code ({target_language})")
        st.code(translated_code, language=target_language.lower())
    else:
        st.warning("Please enter Python code to translate.")

uploaded_file = st.sidebar.file_uploader("Upload a Python File", type=["py"])
if uploaded_file is not None:
    python_code = uploaded_file.read().decode("utf-8")
# st.text_area("Uploaded Python Code", python_code, height=200)


#file download
# st.download_button(
#     label="Download Translated Code",
#     data=translated_code,
#     file_name=f"translated.{target_language.lower()}",
#     mime="text/plain",
# )

