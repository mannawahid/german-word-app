import streamlit as st
import pandas as pd
import random

# === Embedded vocabulary (Excel থেকে নেওয়া) ===
vocab = {
    "ansehen": {"bangla": "দেখা", "sentence": "আমি ছবিটা দেখি।"},
    "das Bild, -er": {"bangla": "ছবি", "sentence": "ছবিটা সুন্দর।"},
    "hören": {"bangla": "শোনা", "sentence": "আমি গান শুনি।"},
    "noch einmal": {"bangla": "আবার একবার", "sentence": "অনুগ্রহ করে আবার একবার বলুন।"},
    "ankreuzen": {"bangla": "টিক চিহ্ন দেওয়া", "sentence": "সঠিক উত্তরে টিক দিন।"},
    "zuordnen": {"bangla": "মিলানো", "sentence": "শব্দগুলো মিলিয়ে দিন।"},
    "ergänzen": {"bangla": "পূরণ করা", "sentence": "বাক্যটি পূর্ণ করুন।"},
    "machen": {"bangla": "করা", "sentence": "আমি আমার বাড়ির কাজ করি।"},
    "der Kurs, -e": {"bangla": "কোর্স / ক্লাস", "sentence": "কোর্সটি আকর্ষণীয়।"},
    "sprechen": {"bangla": "কথা বলা", "sentence": "আমরা জার্মান বলি।"},
    "lesen": {"bangla": "পড়া", "sentence": "সে বই পড়ে।"},
    "schreiben": {"bangla": "লেখা", "sentence": "আমি আমার নাম লিখি।"},
    "fragen": {"bangla": "জিজ্ঞেস করা", "sentence": "আমি শিক্ষককে প্রশ্ন করি।"},
    "antworten": {"bangla": "উত্তর দেওয়া", "sentence": "সে আমার প্রশ্নের উত্তর দেয়।"},
    "kommen": {"bangla": "আসা", "sentence": "আমি স্কুলে আসি।"},
    "gehen": {"bangla": "যাওয়া", "sentence": "আমি বিশ্ববিদ্যালয়ে যাই।"},
    "sehen": {"bangla": "দেখা", "sentence": "আমি টেলিভিশন দেখি।"},
    "trinken": {"bangla": "পান করা", "sentence": "আমি পানি পান করি।"},
    "essen": {"bangla": "খাওয়া", "sentence": "আমি আপেল খাই।"},
    "wohnen": {"bangla": "বাস করা", "sentence": "আমি ব্রেমেনে থাকি।"},
}

# === Streamlit config ===
st.set_page_config(page_title="Deutsch Wörter Lernen", page_icon="🇩🇪", layout="centered")
st.title("🇩🇪 Deutsch Wörter Lernen (Fill-in-the-Gap Quiz)")
st.caption("Write the correct answer instead of choosing multiple choice. Answers stay saved until you submit.")

menu = st.sidebar.radio("📚 Menu", ["🏠 Word List", "✍️ Fill-in-the-Gap Quiz"])

# === Word list ===
if menu == "🏠 Word List":
    df = pd.DataFrame(
        [{"🇩🇪 German": g, "🇧🇩 Bangla": v["bangla"], "🗣️ Example": v["sentence"]}
         for g, v in vocab.items()]
    )
    st.subheader("📘 German ↔ Bangla Vocabulary")
    st.dataframe(df, use_container_width=True)
    st.success(f"Loaded {len(vocab)} words successfully!")

# === Quiz ===
elif menu == "✍️ Fill-in-the-Gap Quiz":
    st.subheader("✍️ Fill-in-the-Gap Quiz")

    # Choose mode
    mode = st.radio("Quiz Direction:", ["🇩🇪 German → বাংলা", "🇧🇩 বাংলা → German"])
    num_q = st.slider("Number of Questions:", 5, 20, 10)

    # Initialize session data
    if "quiz_words" not in st.session_state or st.session_state.get("last_mode") != mode:
        pairs = list(vocab.items())
        random.shuffle(pairs)
        st.session_state.quiz_words = pairs[:num_q]
        st.session_state.answers = {}
        st.session_state.submitted = False
        st.session_state.last_mode = mode

    quiz_words = st.session_state.quiz_words

    # Render questions
    for i, (german, info) in enumerate(quiz_words, start=1):
        bangla = info["bangla"]
        sentence = info.get("sentence", "")

        # question/answer direction
        if mode == "🇩🇪 German → বাংলা":
            question = german
            correct = bangla
            q_text = f"{i}. Write the Bangla meaning of '{question}':"
        else:
            question = bangla
            correct = german
            q_text = f"{i}. Write the German word for '{question}':"

        st.markdown(f"**{q_text}**")
        if sentence and mode == "🇩🇪 German → বাংলা":
            st.caption(f"💬 Example: {sentence}")

        key = f"q{i}"
        st.session_state.answers[key] = st.text_input(
            "Your answer:",
            value=st.session_state.answers.get(key, ""),
            key=key
        )

    st.divider()

    # === Submit ===
    if st.button("✅ Submit Quiz"):
        results = []
        correct_count = 0

        for i, (german, info) in enumerate(quiz_words, start=1):
            ans = st.session_state.answers.get(f"q{i}", "").strip()
            if mode == "🇩🇪 German → বাংলা":
                correct = info["bangla"]
                shown = german
            else:
                correct = german
                shown = info["bangla"]

            is_ok = ans == correct
            if is_ok:
                correct_count += 1
            results.append({
                "Word": shown,
                "Your Answer": ans if ans else "—",
                "Correct Answer": correct,
                "Result": "✔️" if is_ok else "❌"
            })

        st.session_state.results = results
        st.session_state.score = correct_count
        st.session_state.submitted = True

    # === Result section ===
    if st.session_state.get("submitted"):
        data = st.session_state.results
        score = st.session_state.score / len(data)
        st.success(f"🎯 You got {st.session_state.score} / {len(data)} correct!")
        st.progress(score)
        st.balloons()
        st.dataframe(pd.DataFrame(data))
