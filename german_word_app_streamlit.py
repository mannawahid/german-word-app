# --- Imports ---
import streamlit as st
import random
import time
import pandas as pd

# === Embedded Vocabulary ===
vocab = {
    "ansehen": {"bangla": "দেখা", "sentence": "Ich sehe das Bild."},
    "das Bild, -er": {"bangla": "ছবি", "sentence": "Das Bild ist schön."},
    "hören": {"bangla": "শোনা", "sentence": "Ich höre Musik."},
    "lesen": {"bangla": "পড়া", "sentence": "Er liest ein Buch."},
    "essen": {"bangla": "খাওয়া", "sentence": "Ich esse einen Apfel."},
    "gehen": {"bangla": "যাওয়া", "sentence": "Ich gehe zur Uni."},
    "sprechen": {"bangla": "কথা বলা", "sentence": "Wir sprechen Deutsch."},
    "wohnen": {"bangla": "বাস করা", "sentence": "Ich wohne in Bremen."},
}

# === Streamlit Page Setup ===
st.set_page_config(page_title="বাংলা → German Game", page_icon="🇩🇪", layout="centered")
st.title("🇧🇩 ➜ 🇩🇪 🎮")
st.caption("Type the correct German word, get applause if right, or see 😴 if wrong!")

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
    st.session_state.results = []

# === Timer Function ===
def remaining_time(start_time, total_time=15):
    elapsed = time.time() - start_time
    return max(0, int(total_time - elapsed))

# === Game Loop ===
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

    # Timer
    remain = remaining_time(st.session_state.start_time)
    timer_box = st.empty()
    timer_box.warning(f"⏱️ Time left: {remain}s")

    # Input
    ans_key = f"ans_{st.session_state.current_index}"
    ans = st.text_input("✍️ Type your German answer:", key=ans_key)

    # Buttons
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("💡 Show Hint"):
            st.session_state.hint_used = True
            st.rerun()

    with col2:
        if st.button("✅ Submit"):
            # Evaluate
            is_correct = ans.strip().lower() == german.lower()
            if is_correct:
                st.success("🎉 ✅ Correct! Great Job!")
                st.session_state.score += 10
                st.session_state.correct += 1
                st.image(
                    "https://media.tenor.com/2roX3uxz_68AAAAC/clapping-hands-joypixels.gif",
                    caption="👏 Applause!"
                )
            else:
                st.error(f"😴 ❌ Wrong! Correct answer: {german}")
                st.session_state.wrong += 1
                st.image(
                    "https://media.tenor.com/Fo9vS7UwTtcAAAAd/sleepy-cat.gif",
                    caption="😴 Try Again!"
                )

            st.session_state.results.append({
                "Bangla": bangla,
                "Your Answer": ans if ans else "—",
                "Correct German": german,
                "Result": "✅" if is_correct else "❌"
            })

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
            st.session_state.results.append({
                "Bangla": bangla,
                "Your Answer": "Skipped",
                "Correct German": german,
                "Result": "❌"
            })
            st.session_state.current_index += 1
            st.session_state.start_time = time.time()
            st.session_state.hint_used = False
            st.rerun()

# === Game Over ===
else:
    st.balloons()
    st.success("🏁 Game Over!")
    st.metric("Total Score", st.session_state.score)
    st.metric("Correct Answers", st.session_state.correct)
    st.metric("Wrong Answers", st.session_state.wrong)

    st.write("### 📋 Review Your Answers:")
    st.dataframe(pd.DataFrame(st.session_state.results))

    if st.button("🔁 Restart Game"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()


