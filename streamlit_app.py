import streamlit as st
import requests

st.title("Funny Jokes Quiz Game")

if 'score' not in st.session_state:
    st.session_state['score'] = 0

response = requests.get("http://127.0.0.1:5000/get_joke")
joke = response.json()

st.write(joke['question'])

options = joke['options']
selected_option = st.radio("Choose your punchline:", options)

if st.button("Submit Answer"):
    result = requests.post("http://127.0.0.1:5000/submit_answer", json={"answer": selected_option})
    if result.json()['correct']:
        st.session_state['score'] += 1
        st.success("Correct!")
    else:
        st.error("Wrong!")
    st.write(f"Your Score: {st.session_state['score']}")

st.write("---")
st.write("Leaderboard (Coming Soon!)")
