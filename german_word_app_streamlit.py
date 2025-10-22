import streamlit as st
import random
import time
import pandas as pd

# === Vocabulary ===
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
    "das Wort, -":er": {"bangla": "শব্দ", "sentence": ""},
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

# === Streamlit Setup ===
st.set_page_config(page_title="🐰 বাংলা → German Game", page_icon="🇩🇪", layout="centered")
st.title("🐰 🇧🇩 ➜ 🇩🇪 বাংলা → জার্মান শেখার গেম 🎮")
st.caption("Level up, no repeats — and see results after every stage!")

# === Initialize State ===
if "init" not in st.session_state:
    st.session_state.init = True
    st.session_state.level = 1
    st.session_state.score = 0
    st.session_state.correct = 0
    st.session_state.wrong = 0
    st.session_state.used_words = set()  # Already correct words
    st.session_state.retry_words = []    # Wrong ones for next level
    st.session_state.results = []
    st.session_state.current_questions = []
    st.session_state.current_index = 0
    st.session_state.hint_used = False

# === Helper Functions ===
def level_target(level):
    """Return how many questions this level should have"""
    return 2 + level  # level 1→3, level 2→4, level 3→5 ...

def load_next_level():
    """Load new questions (retry + new ones)"""
    all_items = list(vocab.items())
    remaining = [(g, v) for g, v in all_items if g not in st.session_state.used_words]

    new_set = st.session_state.retry_words.copy()
    st.session_state.retry_words = []

    needed = level_target(st.session_state.level)
    fresh = [item for item in remaining if item not in new_set]
    random.shuffle(fresh)
    new_set.extend(fresh[:max(0, needed - len(new_set))])

    st.session_state.current_questions = new_set
    st.session_state.current_index = 0
    st.session_state.hint_used = False
    st.session_state.level_start = time.time()

def remaining_time(start, total=15):
    return max(0, int(total - (time.time() - start)))

# Load first level if empty
if not st.session_state.current_questions:
    load_next_level()

# === GAME LOOP ===
if st.session_state.current_index < len(st.session_state.current_questions):
    german, info = st.session_state.current_questions[st.session_state.current_index]
    bangla = info["bangla"]
    sentence = info["sentence"]

    st.markdown(f"### 🎯 Level {st.session_state.level}")
    st.info(f"Question {st.session_state.current_index + 1}/{len(st.session_state.current_questions)}")
    st.markdown(f"**'{bangla}' শব্দটির জার্মান অনুবাদ লিখুন:**")

    if st.session_state.hint_used:
        st.caption(f"💡 Hint: {sentence}")

    ans_key = f"ans_{st.session_state.level}_{st.session_state.current_index}"
    ans = st.text_input("✍️ Type your German answer:", key=ans_key)

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("💡 Hint"):
            st.session_state.hint_used = True
            st.rerun()

    with col2:
        if st.button("✅ Submit"):
            correct_ans = german.lower()
            given = ans.strip().lower()
            is_correct = given == correct_ans

            if is_correct:
                st.success("✅ Correct! Well done!")
                st.image("https://media.tenor.com/5nZqVYpE6m4AAAAi/cute-rabbit-thumbs-up.gif",
                         caption="🐰 Thumbs Up!")
                st.session_state.score += 10
                st.session_state.correct += 1
                st.session_state.used_words.add(german)
            else:
                st.error(f"❌ Wrong! Correct answer: {german}")
                st.image("https://media.tenor.com/bTFeixbXb2kAAAAi/sad-rabbit-no.gif",
                         caption="🐰 Thumbs Down!")
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
            st.session_state.hint_used = False
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
            st.session_state.hint_used = False
            st.rerun()

# === LEVEL COMPLETE ===
else:
    total_words = len(vocab)
    remaining_words = total_words - len(st.session_state.used_words)

    st.balloons()
    st.success(f"🎉 Level {st.session_state.level} Complete!")
    st.metric("Score", st.session_state.score)
    st.metric("Correct", st.session_state.correct)
    st.metric("Wrong", st.session_state.wrong)
    st.metric("Words Remaining", remaining_words)

    st.write("### 📋 Level Results:")
    level_df = pd.DataFrame(
        [r for r in st.session_state.results if r["Level"] == st.session_state.level]
    )
    st.dataframe(level_df)

    # Continue or End
    if st.session_state.retry_words or remaining_words > 0:
        next_level = st.session_state.level + 1
        if st.button(f"🚀 Start Level {next_level} ({level_target(next_level)} Questions)"):
            st.session_state.level = next_level
            load_next_level()
            st.rerun()
    else:
        st.success("🏁 Game Over — All Words Mastered! 🎓")
        st.metric("Final Score", st.session_state.score)
        st.metric("Total Correct", st.session_state.correct)
        st.metric("Total Wrong", st.session_state.wrong)
        st.write("### 🧾 Full Game Summary:")
        st.dataframe(pd.DataFrame(st.session_state.results))
        if st.button("🔁 Restart Game"):
            for k in list(st.session_state.keys()):
                del st.session_state[k]
            st.rerun()



