import streamlit as st
import json
import random
import pandas as pd

# === File paths ===
VOCAB_FILE = "german_vocab.json"
EXCEL_FILE = "Meine_Woerter_im_Kurs_Bangla.xlsx"

# === Load Excel and initialize ===
def load_excel():
    try:
        df = pd.read_excel(EXCEL_FILE)
        df = df.dropna(subset=["German", "Bangla"])
        vocab = {row["German"]: row["Bangla"] for _, row in df.iterrows()}
        save_vocab(vocab)
        return vocab
    except Exception as e:
        st.error(f"⚠️ Could not load Excel file: {e}")
        return {}

def load_vocab():
    try:
        with open(VOCAB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_vocab(vocab):
    with open(VOCAB_FILE, "w", encoding="utf-8") as f:
        json.dump(vocab, f, ensure_ascii=False, indent=4)

# === Streamlit Config ===
st.set_page_config(page_title="Deutsch Wörter Lernen", page_icon="🇩🇪", layout="centered")
st.title("🇩🇪 Deutsch Wörter Lernen (German ↔ বাংলা)")
st.caption("Learn German words from Excel, take a multiple-choice quiz, and see your result below!")

# === Sidebar Menu ===
menu = st.sidebar.radio("📚 Menu", ["🏠 Home", "🎯 Quiz", "🗑️ Delete Word"])

# === Load Data ===
vocab = load_excel()
if not vocab:
    st.warning("⚠️ No data loaded. Please make sure the Excel file exists and has columns: German | Bangla | Sentence.")
    st.stop()

# === Page 1: Home ===
if menu == "🏠 Home":
    st.subheader("📘 Word List (from Excel)")
    st.dataframe(pd.DataFrame(list(vocab.items()), columns=["🇩🇪 German", "🇧🇩 Bangla"]))
    st.success(f"✅ Loaded {len(vocab)} words from Excel successfully!")

# === Page 2: Quiz ===
elif menu == "🎯 Quiz":
    st.subheader("🎯 Multiple Choice Quiz")

    num_questions = st.slider("Number of Questions:", 5, 20, 10)
    quiz_words = list(vocab.items())
    random.shuffle(quiz_words)
    quiz_words = quiz_words[:num_questions]

    answers = {}
    for idx, (german, bangla) in enumerate(quiz_words, start=1):
        options = [bangla]  # correct
        wrong_opts = random.sample(
            [b for b in vocab.values() if b != bangla],
            min(3, len(vocab) - 1)
        )
        options.extend(wrong_opts)
        random.shuffle(options)

        st.markdown(f"**{idx}. What is the Bangla meaning of '{german}'?**")
        selected = st.radio(
            "Select your answer:",
            options,
            key=f"q_{idx}"
        )
        answers[german] = (selected, bangla)

    st.divider()

    # === Submit button ===
    if st.button("✅ Submit Quiz"):
        correct = 0
        for german, (chosen, actual) in answers.items():
            if chosen == actual:
                correct += 1

        st.success(f"🎯 Your total score: {correct}/{len(answers)} ✅")
        st.progress(correct / len(answers))
        st.balloons()

        # Show result table
        result_table = []
        for german, (chosen, actual) in answers.items():
            result_table.append({
                "🇩🇪 German": german,
                "Your Answer": chosen,
                "Correct Answer": actual,
                "Result": "✔️" if chosen == actual else "❌"
            })
        st.dataframe(pd.DataFrame(result_table))

# === Page 3: Delete Word ===
elif menu == "🗑️ Delete Word":
    st.subheader("🗑️ Delete a Word from Vocabulary")
    vocab = load_vocab()

    if not vocab:
        st.warning("No words found in JSON file.")
    else:
        word_to_delete = st.selectbox("Select a German word to delete:", list(vocab.keys()))
        if st.button("Delete"):
            del vocab[word_to_delete]
            save_vocab(vocab)
            st.success(f"❌ '{word_to_delete}' deleted successfully!")
