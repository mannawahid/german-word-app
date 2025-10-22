import streamlit as st
import random
import pandas as pd

# === Built-in Vocabulary (from Meine_Woerter_im_Kurs_Bangla.xlsx) ===
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

# === Streamlit Config ===
st.set_page_config(page_title="Deutsch Wörter Lernen", page_icon="🇩🇪", layout="centered")
st.title("🇩🇪 Deutsch Wörter Lernen (German ↔ বাংলা)")
st.caption("Learn German vocabulary with Bangla meanings and example sentences.")

menu = st.sidebar.radio("📚 Menu", ["🏠 Word List", "🎯 Quiz"])

# === Word List Page ===
if menu == "🏠 Word List":
    st.subheader("📘 German → Bangla Word List")
    df = pd.DataFrame(
        [{"🇩🇪 German": g, "🇧🇩 Bangla": v["bangla"], "🗣️ Example": v["sentence"]}
         for g, v in vocab.items()]
    )
    st.dataframe(df, use_container_width=True)
    st.success(f"Loaded {len(vocab)} words successfully!")

# === Quiz Page ===
elif menu == "🎯 Quiz":
    st.subheader("🎯 Multiple-Choice Quiz")

    # Mode selector
    mode = st.radio("Choose Quiz Mode:", ["🇩🇪 German → বাংলা", "🇧🇩 বাংলা → German"])

    num_questions = st.slider("Number of Questions:", 5, 20, 10)

    # Create randomized question set
    quiz_words = list(vocab.items())
    random.shuffle(quiz_words)
    quiz_words = quiz_words[:num_questions]

    # Keep answers persistent
    if "answers" not in st.session_state:
        st.session_state.answers = {}

    # Display questions
    for idx, (german, info) in enumerate(quiz_words, start=1):
        correct = info["bangla"]
        sentence = info.get("sentence", "")

        if mode == "🇩🇪 German → বাংলা":
            question = german
            correct_option = correct
            all_options = [v["bangla"] for v in vocab.values()]
        else:
            question = info["bangla"]
            correct_option = german
            all_options = list(vocab.keys())

        # Pick 3 wrong options
        wrong_opts = random.sample([opt for opt in all_options if opt != correct_option],
                                   k=min(3, len(all_options) - 1))
        options = wrong_opts + [correct_option]
        random.shuffle(options)

        st.markdown(f"**{idx}. {'What is the Bangla meaning of' if mode == '🇩🇪 German → বাংলা' else 'What is the German word for'} '{question}'?**")
        if sentence and mode == "🇩🇪 German → বাংলা":
            st.caption(f"💬 Example: {sentence}")

        # Radio button with persistent state
        key = f"q_{idx}"
        selected = st.radio("Select your answer:", options,
                            key=key,
                            index=options.index(st.session_state.answers[key])
                            if key in st.session_state.answers and st.session_state.answers[key] in options
                            else None)

        st.session_state.answers[key] = selected

    st.divider()

    # === Submit button ===
    if st.button("✅ Submit Quiz"):
        correct_count = 0
        result_data = []

        # Evaluate answers
        for idx, (german, info) in enumerate(quiz_words, start=1):
            key = f"q_{idx}"
            chosen = st.session_state.answers.get(key)
            if mode == "🇩🇪 German → বাংলা":
                correct_ans = info["bangla"]
                word_shown = german
            else:
                correct_ans = german
                word_shown = info["bangla"]

            is_correct = chosen == correct_ans
            if is_correct:
                correct_count += 1

            result_data.append({
                "Word": word_shown,
                "Your Answer": chosen if chosen else "❌ Not answered",
                "Correct Answer": correct_ans,
                "Result": "✔️" if is_correct else "❌"
            })

        score = correct_count / len(result_data)
        st.success(f"🎯 You got {correct_count} / {len(result_data)} correct!")
        st.progress(score)
        st.balloons()
        st.dataframe(pd.DataFrame(result_data))
