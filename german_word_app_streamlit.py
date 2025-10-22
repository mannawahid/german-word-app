import streamlit as st
import json
import random
import matplotlib.pyplot as plt

VOCAB_FILE = "german_vocab.json"

def load_vocab():
    try:
        with open(VOCAB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_vocab(vocab):
    with open(VOCAB_FILE, "w", encoding="utf-8") as f:
        json.dump(vocab, f, ensure_ascii=False, indent=4)

# App title
st.set_page_config(page_title="Deutsch Wörter Lernen", page_icon="🇩🇪", layout="centered")
st.title("🇩🇪 Deutsch Wörter Lernen (German ↔ বাংলা)")
st.caption("Learn German words with Bangla meanings, practice quizzes, and track your progress!")

# Sidebar navigation
menu = st.sidebar.radio("📚 Menu", ["🏠 Home", "➕ Add Word", "🎯 Quiz", "📊 Progress"])

# === Page 1: Home ===
if menu == "🏠 Home":
    vocab = load_vocab()
    st.subheader("📘 Your Vocabulary List")
    if vocab:
        st.table({"🇩🇪 German Word": vocab.keys(), "🇧🇩 Bangla Meaning": vocab.values()})
    else:
        st.info("No words added yet. Go to ➕ Add Word.")

# === Page 2: Add Word ===
elif menu == "➕ Add Word":
    st.subheader("➕ Add a New Word")
    german = st.text_input("🇩🇪 German Word")
    bangla = st.text_input("🇧🇩 Bangla Meaning")
    if st.button("Save Word"):
        if german and bangla:
            vocab = load_vocab()
            vocab[german] = bangla
            save_vocab(vocab)
            st.success(f"✅ '{german}' added successfully!")
        else:
            st.warning("Please enter both German and Bangla words.")

# === Page 3: Quiz ===
elif menu == "🎯 Quiz":
    st.subheader("🎯 Take a Quiz")
    vocab = load_vocab()
    if not vocab:
        st.warning("No words available. Please add some first!")
    else:
        mode = st.radio("Select Quiz Mode:", ["German → Bangla", "Bangla → German"])
        num_questions = st.slider("Number of Questions:", 5, 20, 10)

        if st.button("Start Quiz"):
            quiz_words = list(vocab.items())
            random.shuffle(quiz_words)
            quiz_words = quiz_words[:num_questions]

            score = 0
            for german, bangla in quiz_words:
                if mode == "German → Bangla":
                    ans = st.text_input(f"What is the Bangla meaning of '{german}'?", key=german)
                    if st.button(f"Check {german}", key=german+"_btn"):
                        if ans.strip() == bangla:
                            st.success("✅ Correct!")
                            score += 1
                        else:
                            st.error(f"❌ Wrong! Correct: {bangla}")
                else:
                    ans = st.text_input(f"What is the German word for '{bangla}'?", key=bangla)
                    if st.button(f"Check {bangla}", key=bangla+"_btn"):
                        if ans.strip() == german:
                            st.success("✅ Correct!")
                            score += 1
                        else:
                            st.error(f"❌ Wrong! Correct: {german}")
            st.success(f"🎯 Your total score: {score}/{num_questions}")

# === Page 4: Progress ===
elif menu == "📊 Progress":
    st.subheader("📈 Your Learning Progress")
    try:
        with open("quiz_history.json", "r", encoding="utf-8") as f:
            history = json.load(f)
    except FileNotFoundError:
        history = []

    if st.button("Simulate Last 10 Quiz Scores"):
        history = [random.randint(5, 20) for _ in range(10)]
        with open("quiz_history.json", "w", encoding="utf-8") as f:
            json.dump(history, f, ensure_ascii=False, indent=4)

    if history:
        fig, ax = plt.subplots()
        ax.plot(range(1, len(history)+1), history, marker="o", color="green")
        ax.set_title("Quiz Score History")
        ax.set_xlabel("Attempt Number")
        ax.set_ylabel("Score (out of 20)")
        st.pyplot(fig)
    else:
        st.info("No quiz history yet.")
