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
    "machen": {"bangla": "করা", "sentence": "Ich mache meine Hausaufgaben."},
    "zuordnen": {"bangla": "মিলানো", "sentence": "Ordnen Sie die Wörter zu."},
    "ankreuzen": {"bangla": "টিক চিহ্ন দেওয়া", "sentence": "Kreuzen Sie die richtige Antwort an."},
}

# === Streamlit Config ===
st.set_page_config(page_title="🐰 বাংলা → German Game", page_icon="🇩🇪", layout="centered")
st.title("🐰 🇧🇩 ➜ 🇩🇪 বাংলা → জার্মান শেখার গেম 🎮")
st.caption("Type the correct German word — unlock higher levels as you progress!")

# === Initialize Session ===
if "initialized" not in st.session_state:
    st.session_state.initialized = True
    st.session_state.level = 1
    st.session_state.score = 0
    st.session_state.correct = 0
    st.session_state.wrong = 0
    st.session_state.results = []
    st.session_state.total_questions_answered = 0
    st.session_state.level_targets = {1: 3, 2: 4, 3: 5, 4: 6, 5: 7}
    st.session_state.current_level_target = st.session_state.level_targets.get(1, 3)
    st.session_state.current_questions = []
    st.session_state.current_index = 0
    st.session_state.hint_used = False

# === Helper Functions ===
def load_new_level():
    """Load questions for the current level"""
    all_items = list(vocab.items())
    random.shuffle(all_items)
    st.session_state.current_questions = all_items[:st.session_state.current_level_target]
    st.session_state.current_index = 0
    st.session_state.hint_used = False
    st.session_state.level_start = time.time()

def remaining_time(start, total=15):
    return max(0, int(total - (time.time() - start)))

# Load initial questions if empty
if not st.session_state.current_questions:
    load_new_level()

# === GAME LOOP ===
if st.session_state.current_index < len(st.session_state.current_questions):
    german, info = st.session_state.current_questions[st.session_state.current_index]
    bangla = info["bangla"]
    sentence = info["sentence"]

    st.markdown(f"### 🎯 Level {st.session_state.level}")
    st.info(f"Question {st.session_state.current_index + 1}/{len(st.session_state.current_questions)} for this level")

    st.markdown(f"**'{bangla}' শব্দটির জার্মান অনুবাদ লিখুন:**")

    if st.session_state.hint_used:
        st.caption(f"💡 Hint: {sentence}")

    remain = remaining_time(st.session_state.level_start)
    timer_box = st.empty()
    timer_box.warning(f"⏱️ Time left: {remain}s")

    ans_key = f"ans_{st.session_state.level}_{st.session_state.current_index}"
    ans = st.text_input("✍️ Type your German answer:", key=ans_key)

    c1, c2, c3 = st.columns(3)

    # Hint button
    with c1:
        if st.button("💡 Hint"):
            st.session_state.hint_used = True
            st.rerun()

    # Submit button
    with c2:
        if st.button("✅ Submit"):
            is_correct = ans.strip().lower() == german.lower()

            if is_correct:
                st.success("✅ Correct! Well done!")
                st.session_state.score += 10
                st.session_state.correct += 1
                st.image("https://media.tenor.com/5nZqVYpE6m4AAAAi/cute-rabbit-thumbs-up.gif", caption="🐰 Thumbs Up!")
            else:
                st.error(f"❌ Wrong! Correct answer: {german}")
                st.session_state.wrong += 1
                st.image("https://media.tenor.com/bTFeixbXb2kAAAAi/sad-rabbit-no.gif", caption="🐰 Thumbs Down!")

            st.session_state.results.append({
                "Level": st.session_state.level,
                "Bangla": bangla,
                "Your Answer": ans if ans else "—",
                "Correct German": german,
                "Result": "✅" if is_correct else "❌"
            })

            st.session_state.total_questions_answered += 1
            st.session_state.current_index += 1
            st.session_state.hint_used = False
            st.session_state.level_start = time.time()
            st.rerun()

    # Skip button
    with c3:
        if st.button("⏭️ Skip"):
            st.session_state.results.append({
                "Level": st.session_state.level,
                "Bangla": bangla,
                "Your Answer": "Skipped",
                "Correct German": german,
                "Result": "❌"
            })
            st.session_state.wrong += 1
            st.session_state.current_index += 1
            st.session_state.hint_used = False
            st.session_state.level_start = time.time()
            st.rerun()

# === LEVEL COMPLETE ===
else:
    st.balloons()
    st.success(f"🎉 Level {st.session_state.level} complete!")
    st.metric("Score", st.session_state.score)
    st.metric("Correct", st.session_state.correct)
    st.metric("Wrong", st.session_state.wrong)

    next_level = st.session_state.level + 1
    next_target = st.session_state.level_targets.get(next_level, st.session_state.current_level_target + 1)

    if st.button(f"🚀 Start Level {next_level} ({next_target} questions)"):
        st.session_state.level = next_level
        st.session_state.current_level_target = next_target
        load_new_level()
        st.rerun()

    st.write("### 📋 Review This Level's Answers:")
    df = pd.DataFrame([r for r in st.session_state.results if r["Level"] == st.session_state.level])
    st.dataframe(df)

    if st.button("🏁 End Game"):
        st.success("Game Over! 🏆 See Final Results Below 👇")
        st.write("### 🧾 Final Results:")
        st.dataframe(pd.DataFrame(st.session_state.results))
        st.metric("Total Score", st.session_state.score)
        st.metric("Total Correct", st.session_state.correct)
        st.metric("Total Wrong", st.session_state.wrong)
        if st.button("🔁 Restart Game"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
