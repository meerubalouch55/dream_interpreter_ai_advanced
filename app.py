
import streamlit as st
import pickle
import json
import os
import pandas as pd

st.set_page_config(page_title="Dream Interpreter", page_icon="🌙")

# Simulated user session
if "history" not in st.session_state:
    st.session_state.history = []

st.title("🌙 Dream Interpreter AI - Advanced")
st.markdown("Login to save your dream interpretations and give feedback.")

# Simple login (not secure, for demonstration)
username = st.text_input("Username")
password = st.text_input("Password", type="password")

if username and password:
    st.success(f"Welcome, {username}!")

    # Load data
    with open("dream_data.json", "r") as f:
        dream_data = json.load(f)
    with open("dream_model.pkl", "rb") as f:
        model = pickle.load(f)
    with open("vectorizer.pkl", "rb") as f:
        vectorizer = pickle.load(f)

    user_input = st.text_area("Describe your dream:", height=150)

    if st.button("Interpret"):
        if user_input.strip() == "":
            st.warning("Please enter a dream description.")
        else:
            vec = vectorizer.transform([user_input])
            prediction = model.predict(vec)[0]
            meaning = dream_data.get(prediction, "No meaning found.")
            result = f"🔮 Interpretation: {meaning}"
            st.session_state.history.append((user_input, result))
            st.success(result)

    st.markdown("### 🕘 Dream History")
    for idx, (dream, interp) in enumerate(st.session_state.history):
        st.markdown(f"**{idx+1}.** _{dream}_ → {interp}")

    st.markdown("### 💬 Feedback")
    feedback = st.text_area("Leave feedback:")
    if st.button("Submit Feedback"):
        with open("feedback_log.txt", "a") as f:
            f.write(f"{username}: {feedback}\n")
        st.success("Thank you for your feedback!")

else:
    st.info("Please log in to use the app.")
