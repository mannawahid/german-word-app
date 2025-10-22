import streamlit as st
import pandas as pd
import random
import time

# === Vocabulary ===
vocab = {
    "ansehen": {"bangla": "দেখা", "sentence": "আমি ছবিটা দেখি।"},
    "das Bild, -er": {"bangla": "ছবি", "sentence": "ছবিটা সুন্দর।"},
    "hören": {"bangla": "শোনা", "sentence": "আমি গান শুনি।"},
    "ankreuzen": {"bangla": "টিক চিহ্ন দেওয়া", "sentence": "সঠিক উত্তরে টিক দিন।"},
    "zuordnen": {"bangla": "মিলানো", "sentence": "শব্দগুলো মিলিয়ে দিন।"},
    "machen": {"bangla": "করা", "sentence": "আমি আমার বাড়ির কাজ করি।"},
    "lesen": {"bangla": "পড়া", "sentence": "সে বই পড়ে।"},
    "essen": {"bangla": "খাওয়া", "sentence": "আমি আপেল খাই।"},import streamlit as st
import random, time, pandas as pd

# === Vocabulary ===
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
    "wohnen": {"bangla": "বাস করা", "sentence": "Ich wohne in Bremen."},
}

# === Page setup ===
st.set_page_config(page_title="বাংলা → German Game", page_icon="🇩🇪", layout="centered")
st.title("🇧🇩 ➜ 🇩🇪 বাংলা থেকে German শেখার গেম")
st.caption("Type the correct German word within time, gain XP, and level up!")

# === Initialize session ===
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

# === Helper: timer ===
def remaining_time(start, total=15):
    return max(0, int(total - (time.time() - start)))

# === Game loop ===
if st.session_state.current_index < len(st.session_state.quiz_order):
    german, info = st.session_state.quiz_order[st.session_state.current_index]
    bangla = info["bangla"]
    sentence = info["sentence"]

    st.markdown(f"### 🎯 Level {st.session_state.level}")
    st.progress(min(1.0, st.session_state.correct / 5))
    st.info(f"Question {st.session_state.current_index + 1}/{len(st.session_state.quiz_order)}")

    st.markdown(f"**'{bangla}' শব্দটির জার্মান অনুবাদ লিখুন:**")

    if st.session_state.hint_used:
        st.caption(f"💡 Hint: {sentence}")

    # Timer display
    remain = remaining_time(st.session_state.start_time)
    t = st.empty()
    t.warning(f"⏱️ Time left: {remain}s")

    time.sleep(0.2)
    remain = remaining_time(st.session_state.start_time)
    t.warning(f"⏱️ Time left: {remain}s")

    # User input
    ans = st.text_input("✍️ Type your German answer:", key=f"ans_{st.session_state.current_index}")

    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("💡 Show Hint"):
            st.session_state.hint_used = True
            st.rerun()

    with c2:
        if st.button("✅ Submit"):
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

            # Level Up
            if st.session_state.correct % 5 == 0 and st.session_state.correct != 0:
                st.session_state.level += 1
                st.balloons()
                st.success(f"🏆 Level Up! You reached Level {st.session_state.level}!")
            st.rerun()

    with c3:
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

    "gehen": {"bangla": "যাওয়া", "sentence": "আমি বিশ্ববিদ্যালয়ে যাই।"},
    "sprechen": {"bangla": "কথা বলা", "sentence": "আমরা জার্মান বলি।"},
    "wohnen": {"bangla": "বাস করা", "sentence": "আমি ব্রেমেনে থাকি।"},
}

# === Config ===
st.set_page_config(page_title="Deutsch Wörter Game", page_icon="🎮", layout="centered")
st.title("🎮 Deutsch Wörter Lernen: Game Mode")
st.caption("Fill in the blanks, beat the timer, and level up!")

# === Initialize Session ===
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

# === Helper: Timer ===
def get_remaining_time(start_time, total_time=15):
    elapsed = time.time() - start_time
    return max(0, int(total_time - elapsed))

# === Current question ===
if st.session_state.current_index < len(st.session_state.quiz_order):
    german, info = st.session_state.quiz_order[st.session_state.current_index]
    correct_ans = info["bangla"]
    sentence = info["sentence"]

    st.markdown(f"### Level {st.session_state.level}")
    st.progress(min(1.0, st.session_state.correct / 5))
    st.info(f"Question {st.session_state.current_index + 1}/{len(st.session_state.quiz_order)}")

    st.markdown(f"**What's the Bangla meaning of:** `{german}`")
    if st.session_state.hint_used:
        st.caption(f"💬 Hint: {sentence}")

    # Timer
    remaining = get_remaining_time(st.session_state.start_time)
    timer_placeholder = st.empty()
    timer_placeholder.warning(f"⏱️ Time left: {remaining}s")

    # Continuously update timer
    time.sleep(0.2)
    remaining = get_remaining_time(st.session_state.start_time)
    timer_placeholder.warning(f"⏱️ Time left: {remaining}s")

    # User input
    ans = st.text_input("✍️ Type your answer here:", key=f"ans_{st.session_state.current_index}")

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("💡 Show Hint"):
            st.session_state.hint_used = True
            st.rerun()
    with col2:
        if st.button("✅ Submit"):
            if ans.strip() == correct_ans:
                st.success("✅ Correct!")
                st.session_state.score += 10
                st.session_state.correct += 1
            else:
                st.error(f"❌ Wrong! Correct answer: {correct_ans}")
                st.session_state.wrong += 1

            st.session_state.current_index += 1
            st.session_state.start_time = time.time()
            st.session_state.hint_used = False

            # Level up after every 5 correct answers
            if st.session_state.correct % 5 == 0 and st.session_state.correct != 0:
                st.session_state.level += 1
                st.balloons()
                st.success(f"🎉 Level Up! You reached Level {st.session_state.level}!")
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
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

