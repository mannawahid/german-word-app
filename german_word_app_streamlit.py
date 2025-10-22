# --- imports always at the very top ---
import streamlit as st
import pandas as pd
import random
import time

# === Embedded Vocabulary (Excel-free) ===
# NOTE: শেষ আইটেমের পর আর কোন 'import' লিখবে না—এখানেই ডিকশনারি শেষ হবে।
vocab = {
    "ansehen": {"bangla": "দেখা", "sentence": "Ich sehe das Bild."},
    "das Bild, -er": {"bangla": "ছবি", "sentence": "Das Bild ist schön."},
    "hören": {"bangla": "শোনা", "sentence": "Ich höre Musik."},
    "ankreuzen": {"bangla": "টিক চিহ্ন দেওয়া", "sentence": "Kreuzen Sie die richtige Antwort an."},
    "zuordnen": {"bangla": "মিলানো", "sentence": "Ordnen Sie die Wörter zu."},
    "machen": {"bangla": "করা", "sentence": "Ich mache meine Hausaufgaben."},
    "lesen": {"bangla": "পড়া", "sentence": "Er liest ein Buch."},
    "essen": {"bangla": "খাওয়া", "sentence": "Ich esse einen Apfel."},
    "gehen": {"bangla": "যাওয়া", "sentence": "Ich gehe zur Uni."},
    "sprechen": {"bangla": "কথা বলা", "sentence": "Wir sprechen Deutsch."},
    "wohnen": {"bangla": "বাস করা", "sentence": "Ich wohne in Bremen."}
}  # <-- ডিকশনারি এখানেই শেষ

# === Page setup ===
st.set_page_config(page_title="বাংলা → German Game", page_icon="🇩🇪", layout="centered")
st.title("🇧🇩 ➜ 🇩🇪 বাংলা থেকে German শেখার গেম")
st.caption("Type the correct German word, beat the timer, gain XP, and level up!")

# === Initialize session (runs once) ===
if "level" not in st.session_state:
    st.session_state.level = 1
    st.session_state.score = 0
    st.session_state.correct = 0
    st.session_state.wrong = 0
    st.session_state.current_index = 0
    st.session_state.quiz_order = list(vocab.items())
    random.shuffle(st.session_state.quiz_order)
    st.session_state.start_time = time.time()
    st.session_state.hint_used = False

def remaining_time(start, total=15):
    return max(0, int(total - (time.time() - start)))

# === Game loop ===
if st.session_state.current_index < len(st.session_state.quiz_order):
    german, info = st.session_state.quiz_order[st.session_state.current_index]
    bangla = info["bangla"]
    sentence = info.get("sentence", "")

    st.markdown(f"### 🎯 Level {st.session_state.level}")
    st.progress(min(1.0, st.session_state.correct / 5))
    st.info(f"Question {st.session_state.current_index + 1}/{len(st.session_state.quiz_order)}")

    st.markdown(f"**'{bangla}' শব্দটির জার্মান অনুবাদ লিখুন:**")

    if st.session_state.hint_used:
        st.caption(f"💡 Hint (German sentence): {sentence}")

    # Timer display (simple pulse)
    tbox = st.empty()
    tbox.warning(f"⏱️ Time left: {remaining_time(st.session_state.start_time)}s")

    # User input (persistent per question)
    ans_key = f"ans_{st.session_state.current_index}"
    default_val = st.session_state.get(ans_key, "")
    ans = st.text_input("✍️ Type your German answer:", value=default_val, key=ans_key)

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("💡 Show Hint"):
            st.session_state.hint_used = True
            st.rerun()
    with col2:
        if st.button("✅ Submit"):
            # save latest value explicitly
            st.session_state[ans_key] = ans
            if ans.strip().lower() == german.lower():
                st.success("✅ Correct!")
                st.session_state.score += 10
                st.session_state.correct += 1
            else:
                st.error(f"❌ Wrong! Correct answer: {german}")
                st.session_state.wrong += 1

            st.session_state.current_index += 1
            st.session_state.start_time = time.time()
            st.session_state.hint_used = False

            if st.session_state.correct % 5 == 0 and st.session_state.correct != 0:
                st.session_state.level += 1
                st.balloons()
                st.success(f"🏆 Level Up! You reached Level {st.session_state.level}!")
            st.rerun()
    with col3:
        if st.button("⏭️ Skip"):
            st.session_state.current_index += 1
            st.session_state.start_time = time.time()
            st.session_state.hint_used = False
            st.rerun()

else:
    st.balloons()
    st.success("🏁 Game Over!")
    st.metric("Total Score", st.session_state.score)
    st.metric("Correct Answers", st.session_state.correct)
    st.metric("Wrong Answers", st.session_state.wrong)
    if st.button("🔁 Restart Game"):
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.rerun()
