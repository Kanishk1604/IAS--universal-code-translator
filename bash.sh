#!/bin/bash

# Activate the virtual environment
source env/bin/activate
# Run unit tests
python -m unittest test_translator.py
# Run the Streamlit app
streamlit run app.py
