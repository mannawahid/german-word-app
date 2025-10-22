import streamlit as st
import pandas as pd
import random

# === Embedded Vocabulary ===
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

# === Page setup ===
st.set_page_config(page_title="Deutsch Wörter Lernen", page_icon="🇩🇪", layout="centered")
st.title("🇩🇪 Deutsch Wörter Lernen (German ↔ বাংলা)")
st.caption("Persistent multiple-choice quiz with Bangla–German toggle.")

menu = st.sidebar.radio("📚 Menu", ["🏠 Word List", "🎯 Quiz"])

# === Word list page ===
if menu == "🏠 Word List":
    df = pd.DataFrame(
        [{"🇩🇪 German": g, "🇧🇩 Bangla": v["bangla"], "🗣️ Example": v["sentence"]}
         for g, v in vocab.items()]
    )
    st.subheader("📘 German → Bangla Vocabulary")
    st.dataframe(df, use_container_width=True)
    st.success(f"Loaded {len(vocab)} words successfully!")

# === Quiz page ===
elif menu == "🎯 Quiz":
    st.subheader("🎯 Multiple-Choice Quiz")
    mode = st.radio("Quiz Direction:", ["🇩🇪 German → বাংলা", "🇧🇩 বাংলা → German"])
    num_q = st.slider("Number of Questions:", 5, 20, 10)

    # initialize once
    if "quiz_words" not in st.session_state or st.session_state.get("last_mode") != mode:
        pairs = list(vocab.items())
        random.shuffle(pairs)
        st.session_state.quiz_words = pairs[:num_q]
        st.session_state.answers = {}
        st.session_state.submitted = False
        st.session_state.last_mode = mode

    quiz_words = st.session_state.quiz_words

    for i, (german, info) in enumerate(quiz_words, start=1):
        correct_bn = info["bangla"]
        sent = info.get("sentence", "")

        if mode == "🇩🇪 German → বাংলা":
            question = german
            correct_ans = correct_bn
            all_options = [v["bangla"] for v in vocab.values()]
        else:
            question = correct_bn
            correct_ans = german
            all_options = list(vocab.keys())

        wrong = random.sample([o for o in all_options if o != correct_ans],
                              k=min(3, len(all_options) - 1))
        options = wrong + [correct_ans]
        random.shuffle(options)

        st.markdown(f"**{i}. {'Bangla meaning of' if mode == '🇩🇪 German → বাংলা' else 'German word for'} '{question}'?**")
        if sent and mode == "🇩🇪 German → বাংলা":
            st.caption(f"💬 Example: {sent}")

        key = f"q{i}"
        default_index = options.index(st.session_state.answers[key]) if key in st.session_state.answers and st.session_state.answers[key] in options else 0
        choice = st.radio("Select:", options, key=key, index=default_index)
        st.session_state.answers[key] = choice

    st.divider()

    # --- submit ---
    if st.button("✅ Submit Quiz"):
        correct = 0
        table = []
        for i, (german, info) in enumerate(quiz_words, start=1):
            chosen = st.session_state.answers.get(f"q{i}")
            if mode == "🇩🇪 German → বাংলা":
                correct_ans = info["bangla"]
                shown = german
            else:
                correct_ans = german
                shown = info["bangla"]
            ok = chosen == correct_ans
            if ok:
                correct += 1
            table.append({
                "Word": shown,
                "Your Answer": chosen,
                "Correct": correct_ans,
                "Result": "✔️" if ok else "❌"
            })
        st.session_state.submitted = True
        st.session_state.results = table
        st.session_state.score = correct

    # --- show result ---
    if st.session_state.get("submitted"):
        res = st.session_state.results
        score = st.session_state.score / len(res)
        st.success(f"🎯 You got {st.session_state.score} / {len(res)} correct!")
        st.progress(score)
        st.balloons()
        st.dataframe(pd.DataFrame(res))
