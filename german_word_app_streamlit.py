import streamlit as st
import pandas as pd
import random
import time

# === Vocabulary Database (Level wise) ===
word_bank = {
    "A1.1": {
        "ansehen": {"bangla": "দেখা", "sentence_de": "Ich sehe das Bild.", "sentence_bn": "আমি ছবিটা দেখি।"},
        "das Bild, -er": {"bangla": "ছবি", "sentence_de": "Das Bild ist schön.", "sentence_bn": "ছবিটা সুন্দর।"},
        "hören": {"bangla": "শোনা", "sentence_de": "Ich höre Musik.", "sentence_bn": "আমি গান শুনি।"},
    },
    "A1.2": {
        "lesen": {"bangla": "পড়া", "sentence_de": "Er liest ein Buch.", "sentence_bn": "সে বই পড়ে।"},
        "essen": {"bangla": "খাওয়া", "sentence_de": "Ich esse einen Apfel.", "sentence_bn": "আমি আপেল খাই।"},
        "gehen": {"bangla": "যাওয়া", "sentence_de": "Ich gehe zur Uni.", "sentence_bn": "আমি বিশ্ববিদ্যালয়ে যাই।"},
    },
    "A2.1": {
        "sprechen": {"bangla": "কথা বলা", "sentence_de": "Wir sprechen Deutsch.", "sentence_bn": "আমরা জার্মান বলি।"},
        "wohnen": {"bangla": "বাস করা", "sentence_de": "Ich wohne in Bremen.", "sentence_bn": "আমি ব্রেমেনে থাকি।"},
    },
    "A2.2": {
        "machen": {"bangla": "করা", "sentence_de": "Ich mache meine Hausaufgaben.", "sentence_bn": "আমি আমার বাড়ির কাজ করি।"},
        "zuordnen": {"bangla": "মিলানো", "sentence_de": "Ordnen Sie die Wörter zu.", "sentence_bn": "শব্দগুলো মিলিয়ে দিন।"},
        "ankreuzen": {"bangla": "টিক চিহ্ন দেওয়া", "sentence_de": "Kreuzen Sie die richtige Antwort an.", "sentence_bn": "সঠিক উত্তরে টিক দিন।"},
    },
}

# === Streamlit Config ===
st.set_page_config(page_title="🇩🇪 Deutsch Lernen App", page_icon="🐰", layout="wide")
st.title("🐰 Deutsch Lernen 🇩🇪")
st.caption("Bangla → German quiz + Level-wise vocabulary lists 🎯")

# Sidebar Menu
menu = st.sidebar.radio("📚 Menu", ["🏠 Home", "📖 Vocabulary Levels", "🎯 Quiz Game"])

# === HOME PAGE ===
if menu == "🏠 Home":
    st.header("🎯 Willkommen!")
    st.write("""
    এই অ্যাপে তুমি তিনভাবে জার্মান শিখতে পারবে:  
    1️⃣ Level-wise শব্দ তালিকা দেখতে পারবে (A1 → B2 পর্যন্ত)।  
    2️⃣ প্রতিটি শব্দের জার্মান ও বাংলা বাক্য পাবে।  
    3️⃣ 🎮 Quiz Game এর মাধ্যমে অনুশীলন করতে পারবে (Bangla → German)।
    """)
    st.image("https://media.tenor.com/POOQOjE2aYcAAAAi/bunny-hello.gif", width=200)

# === VOCABULARY PAGE ===
elif menu == "📖 Vocabulary Levels":
    st.header("📘 German Vocabulary by Levels")
    selected_level = st.selectbox("📖 Choose your level:", list(word_bank.keys()))

    level_words = word_bank[selected_level]
    st.subheader(f"🇩🇪 Level {selected_level} Vocabulary")

    data = []
    for word, info in level_words.items():
        data.append({
            "🇩🇪 German": word,
            "🇧🇩 Bangla": info["bangla"],
            "🗣️ German Sentence": info["sentence_de"],
            "🗨️ Bangla Sentence": info["sentence_bn"]
        })
    df = pd.DataFrame(data)
    st.dataframe(df, use_container_width=True)

# === QUIZ PAGE ===
elif menu == "🎯 Quiz Game":
    st.header("🎮 Bangla → German Quiz")

    # Merge all levels
    all_words = {}
    for lvl in word_bank.values():
        all_words.update(lvl)

    # Initialize session state
    if "level" not in st.session_state:
        st.session_state.level = 1
        st.session_state.score = 0
        st.session_state.correct = 0
        st.session_state.wrong = 0
        st.session_state.used_words = set()
        st.session_state.retry_words = []
        st.session_state.results = []
        st.session_state.current_questions = []
        st.session_state.current_index = 0

    # Helper functions
    def level_target(level):
        return 2 + level  # Level 1 → 3, Level 2 → 4, etc.

    def load_next_level():
        remaining = [(g, v) for g, v in all_words.items() if g not in st.session_state.used_words]
        new_set = st.session_state.retry_words.copy()
        st.session_state.retry_words = []
        need = level_target(st.session_state.level)
        fresh = [item for item in remaining if item not in new_set]
        random.shuffle(fresh)
        new_set.extend(fresh[:max(0, need - len(new_set))])
        st.session_state.current_questions = new_set
        st.session_state.current_index = 0
        st.session_state.hint_used = False

    # Load first level
    if not st.session_state.current_questions:
        load_next_level()

    # Game logic
    if st.session_state.current_index < len(st.session_state.current_questions):
        german, info = st.session_state.current_questions[st.session_state.current_index]
        bangla = info["bangla"]

        st.markdown(f"### 🎯 Level {st.session_state.level}")
        st.info(f"Question {st.session_state.current_index + 1}/{len(st.session_state.current_questions)}")
        st.markdown(f"**'{bangla}' শব্দটির জার্মান অনুবাদ লিখো:**")

        ans = st.text_input("✍️ Your German Answer:", key=f"ans_{st.session_state.level}_{st.session_state.current_index}")

        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("✅ Submit"):
                correct_ans = german.strip().lower()
                is_correct = ans.strip().lower() == correct_ans

                if is_correct:
                    st.success("✅ Correct!")
                    st.image("https://media.tenor.com/5nZqVYpE6m4AAAAi/cute-rabbit-thumbs-up.gif", caption="🐰 Thumbs Up!")
                    st.session_state.score += 10
                    st.session_state.correct += 1
                    st.session_state.used_words.add(german)
                else:
                    st.error(f"❌ Wrong! Correct: {german}")
                    st.image("https://media.tenor.com/bTFeixbXb2kAAAAi/sad-rabbit-no.gif", caption="🐰 Thumbs Down!")
                    st.session_state.retry_words.append((german, info))
                    st.session_state.wrong += 1

                st.session_state.results.append({
                    "Level": st.session_state.level,
                    "Bangla": bangla,
                    "Your Answer": ans if ans else "—",
                    "Correct German": german,
                    "Result": "✅" if is_correct else "❌"
                })

                st.session_state.current_index += 1
                st.rerun()

        with col3:
            if st.button("⏭️ Skip"):
                st.session_state.retry_words.append((german, info))
                st.session_state.results.append({
                    "Level": st.session_state.level,
                    "Bangla": bangla,
                    "Your Answer": "Skipped",
                    "Correct German": german,
                    "Result": "❌"
                })
                st.session_state.wrong += 1
                st.session_state.current_index += 1
                st.rerun()

    # === Level complete ===
    else:
        st.success(f"🎉 Level {st.session_state.level} Complete!")
        level_df = pd.DataFrame([r for r in st.session_state.results if r["Level"] == st.session_state.level])
        st.dataframe(level_df)
        total_words = len(all_words)
        remaining = total_words - len(st.session_state.used_words)

        if st.session_state.retry_words or remaining > 0:
            next_level = st.session_state.level + 1
            if st.button(f"🚀 Start Level {next_level} ({level_target(next_level)} questions)"):
                st.session_state.level = next_level
                load_next_level()
                st.rerun()
        else:
            st.balloons()
            st.success("🏁 Game Over — All Words Mastered! 🎓")
            st.dataframe(pd.DataFrame(st.session_state.results))
            if st.button("🔁 Restart Game"):
                for k in list(st.session_state.keys()):
                    del st.session_state[k]
                st.rerun()
