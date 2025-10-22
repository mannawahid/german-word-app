import streamlit as st
from gtts import gTTS
import io
import pandas as pd
import random
import time

# === Vocabulary Database ===
word_bank = {
    "A1.1": {
        "sein": {"bangla": "হওয়া", "sentence_de": "Ich bin Student.", "sentence_bn": "আমি একজন ছাত্র।"},
        "haben": {"bangla": "থাকা / থাকা আছে", "sentence_de": "Ich habe ein Buch.", "sentence_bn": "আমার একটি বই আছে।"},
        "kommen": {"bangla": "আসা", "sentence_de": "Ich komme aus Bangladesch.", "sentence_bn": "আমি বাংলাদেশ থেকে আসি।"},
        "gehen": {"bangla": "যাওয়া", "sentence_de": "Ich gehe zur Arbeit.", "sentence_bn": "আমি কাজে যাচ্ছি।"},
        "machen": {"bangla": "করা", "sentence_de": "Was machst du?", "sentence_bn": "তুমি কী করছো?"},
        "lernen": {"bangla": "শেখা", "sentence_de": "Ich lerne Deutsch.", "sentence_bn": "আমি জার্মান শিখছি।"},
        "sprechen": {"bangla": "কথা বলা", "sentence_de": "Sie spricht gut Englisch.", "sentence_bn": "সে ভালো ইংরেজি বলে।"},
        "wohnen": {"bangla": "বাস করা / থাকা", "sentence_de": "Ich wohne in Bremen.", "sentence_bn": "আমি ব্রেমেনে থাকি।"},
        "essen": {"bangla": "খাওয়া", "sentence_de": "Ich esse einen Apfel.", "sentence_bn": "আমি একটি আপেল খাচ্ছি।"},
        "trinken": {"bangla": "পান করা", "sentence_de": "Er trinkt Wasser.", "sentence_bn": "সে পানি পান করে।"},
        "lesen": {"bangla": "পড়া", "sentence_de": "Ich lese ein Buch.", "sentence_bn": "আমি একটি বই পড়ছি।"},
        "hören": {"bangla": "শোনা", "sentence_de": "Wir hören Musik.", "sentence_bn": "আমরা গান শুনি।"},
        "sehen": {"bangla": "দেখা", "sentence_de": "Ich sehe einen Film.", "sentence_bn": "আমি একটি সিনেমা দেখি।"},
        "schreiben": {"bangla": "লেখা", "sentence_de": "Ich schreibe einen Brief.", "sentence_bn": "আমি একটি চিঠি লিখছি।"},
        "arbeiten": {"bangla": "কাজ করা", "sentence_de": "Mein Vater arbeitet im Büro.", "sentence_bn": "আমার বাবা অফিসে কাজ করেন।"},
        "spielen": {"bangla": "খেলা / বাজানো", "sentence_de": "Die Kinder spielen Fußball.", "sentence_bn": "ছেলেরা ফুটবল খেলে।"},
        "finden": {"bangla": "খুঁজে পাওয়া / মনে করা", "sentence_de": "Ich finde das Buch interessant.", "sentence_bn": "আমি বইটি আকর্ষণীয় মনে করি।"},
        "mögen": {"bangla": "পছন্দ করা", "sentence_de": "Ich mag Schokolade.", "sentence_bn": "আমি চকোলেট পছন্দ করি।"},
        "kaufen": {"bangla": "কেনা", "sentence_de": "Ich kaufe Brot und Milch.", "sentence_bn": "আমি রুটি এবং দুধ কিনি।"},
        "brauchen": {"bangla": "প্রয়োজন হওয়া", "sentence_de": "Ich brauche Hilfe.", "sentence_bn": "আমার সাহায্য দরকার।"},
        "nehmen": {"bangla": "নেওয়া", "sentence_de": "Ich nehme den Bus.", "sentence_bn": "আমি বাসে যাই।"},
        "geben": {"bangla": "দেওয়া", "sentence_de": "Kannst du mir das Buch geben?", "sentence_bn": "তুমি কি আমাকে বইটা দিতে পারো?"},
        "fragen": {"bangla": "প্রশ্ন করা", "sentence_de": "Ich frage den Lehrer.", "sentence_bn": "আমি শিক্ষকের কাছে প্রশ্ন করি।"},
        "antworten": {"bangla": "উত্তর দেওয়া", "sentence_de": "Der Schüler antwortet richtig.", "sentence_bn": "ছাত্রটি সঠিক উত্তর দেয়।"},
        "helfen": {"bangla": "সাহায্য করা", "sentence_de": "Kannst du mir helfen?", "sentence_bn": "তুমি কি আমাকে সাহায্য করতে পারো?"},
        "bleiben": {"bangla": "থাকা / অবস্থান করা", "sentence_de": "Ich bleibe zu Hause.", "sentence_bn": "আমি বাড়িতে থাকি।"},
        "stehen": {"bangla": "দাঁড়ানো", "sentence_de": "Er steht vor der Tür.", "sentence_bn": "সে দরজার সামনে দাঁড়িয়ে আছে।"},
        "sitzen": {"bangla": "বসা", "sentence_de": "Wir sitzen im Park.", "sentence_bn": "আমরা পার্কে বসে আছি।"},
        "laufen": {"bangla": "দৌড়ানো / হাঁটা", "sentence_de": "Das Kind läuft schnell.", "sentence_bn": "বাচ্চাটি দ্রুত দৌড়াচ্ছে।"},
    }
}

# === Streamlit UI Config ===
st.set_page_config(page_title="Deutsch Lernen A1.1", page_icon="🇩🇪", layout="wide")
st.title("🐰 Deutsch Lernen 🇩🇪 — A1.1 Vocabulary + Quiz")
st.caption("Learn German Words (with Audio) and Practice with Quizzes 🎯")

# === Sidebar Menu ===
menu = st.sidebar.radio("📚 Menu", ["🏠 Home", "📖 Vocabulary", "🎯 Quiz Game"])

# === 🏠 HOME ===
if menu == "🏠 Home":
    st.header("🎯 Willkommen zur Deutsch Lern-App!")
    st.markdown("""
    👉 **এই অ্যাপে তুমি শিখতে পারবে:**
    - 🇩🇪 জার্মান শব্দ ও অর্থ  
    - 🔊 শব্দ ও বাক্যের নেটিভ উচ্চারণ  
    - 🎯 Bangla → German কুইজ গেম  
    - 🐰 লেভেলভিত্তিক স্কোর ও অগ্রগতি  

    📘 **Level:** A1.1 (Beginner)
    """)
    st.image("https://media.tenor.com/POOQOjE2aYcAAAAi/bunny-hello.gif", width=200)

# === 📖 VOCABULARY ===
elif menu == "📖 Vocabulary":
    st.header("📘 A1.1 Vocabulary with Pronunciation 🔊")
    level = "A1.1"
    words = word_bank[level]

    for word, info in words.items():
        st.markdown(f"### 🇩🇪 {word} — 🇧🇩 {info['bangla']}")
        st.write(f"🗣️ *{info['sentence_de']}*")
        st.write(f"🗨️ {info['sentence_bn']}")

        col1, col2 = st.columns([1, 3])
        with col1:
            if st.button(f"🔊 Word", key=f"word_{word}"):
                tts = gTTS(text=word, lang='de')
                mp3_fp = io.BytesIO()
                tts.write_to_fp(mp3_fp)
                st.audio(mp3_fp.getvalue(), format="audio/mp3")
        with col2:
            if st.button(f"🎧 Sentence", key=f"sent_{word}"):
                tts = gTTS(text=info["sentence_de"], lang='de')
                mp3_fp = io.BytesIO()
                tts.write_to_fp(mp3_fp)
                st.audio(mp3_fp.getvalue(), format="audio/mp3")
        st.markdown("---")

# === 🎯 QUIZ GAME ===
elif menu == "🎯 Quiz Game":
    st.header("🎮 Bangla → German Quiz (A1.1 Level)")
    all_words = word_bank["A1.1"]

    # === Initialize Session ===
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

    # === Helper ===
    def level_target(level):
        return 2 + level

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

    # === Load first level ===
    if not st.session_state.current_questions:
        load_next_level()

    # === Quiz Body ===
    if st.session_state.current_index < len(st.session_state.current_questions):
        german, info = st.session_state.current_questions[st.session_state.current_index]
        bangla = info["bangla"]

        st.markdown(f"### 🎯 Level {st.session_state.level}")
        st.info(f"Question {st.session_state.current_index + 1}/{len(st.session_state.current_questions)}")
        st.markdown(f"**'{bangla}' শব্দটির জার্মান অনুবাদ লিখো:**")

        ans = st.text_input("✍️ Your German Answer:", key=f"ans_{st.session_state.level}_{st.session_state.current_index}")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ Submit"):
                correct_ans = german.strip().lower()
                is_correct = ans.strip().lower() == correct_ans

                if is_correct:
                    st.success("✅ Correct! Great Job!")
                    st.image("https://media.tenor.com/5nZqVYpE6m4AAAAi/cute-rabbit-thumbs-up.gif")
                    st.session_state.score += 10
                    st.session_state.correct += 1
                    st.session_state.used_words.add(german)
                else:
                    st.error(f"❌ Wrong! Correct: {german}")
                    st.image("https://media.tenor.com/bTFeixbXb2kAAAAi/sad-rabbit-no.gif")
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

        with col2:
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

    else:
        st.success(f"🎉 Level {st.session_state.level} Complete!")
        df = pd.DataFrame([r for r in st.session_state.results if r["Level"] == st.session_state.level])
        st.dataframe(df)
        remaining = len(all_words) - len(st.session_state.used_words)
        if st.session_state.retry_words or remaining > 0:
            next_level = st.session_state.level + 1
            if st.button(f"🚀 Start Level {next_level} ({level_target(next_level)} questions)"):
                st.session_state.level = next_level
                load_next_level()
                st.rerun()
        else:
            st.balloons()
            st.success("🏁 All Words Mastered! 🎓")
            st.dataframe(pd.DataFrame(st.session_state.results))
            if st.button("🔁 Restart Game"):
                for k in list(st.session_state.keys()):
                    del st.session_state[k]
                st.rerun()
