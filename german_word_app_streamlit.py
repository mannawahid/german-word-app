import streamlit as st
import random, time, pandas as pd

# === Vocabulary ===
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

# === Streamlit setup ===
st.set_page_config(page_title="🐰 বাংলা → German Game", page_icon="🇩🇪", layout="centered")
st.title(🇧🇩 🎮 🇩🇪)
st.caption("No repeats! Only wrong words come again — finish all to win 🏁")

# === Initialize session ===
if "init" not in st.session_state:
    st.session_state.init = True
    st.session_state.level = 1
    st.session_state.score = 0
    st.session_state.correct = 0
    st.session_state.wrong = 0
    st.session_state.used_words = set()   # already answered correctly
    st.session_state.retry_words = []     # wrong ones, will repeat
    st.session_state.results = []
    st.session_state.current_questions = []
    st.session_state.current_index = 0
    st.session_state.hint_used = False

# === Helper ===
def load_next_level():
    """Load new questions for next level"""
    all_items = list(vocab.items())
    remaining = [(g, v) for g, v in all_items if g not in st.session_state.used_words]

    # If previous level had wrongs, include them first
    new_set = st.session_state.retry_words.copy()
    st.session_state.retry_words = []

    # Fill with fresh unseen words
    extra_needed = 3 + st.session_state.level  # grows each level
    fresh = [item for item in remaining if item not in new_set]
    random.shuffle(fresh)
    new_set.extend(fresh[:extra_needed])

    st.session_state.current_questions = new_set
    st.session_state.current_index = 0
    st.session_state.hint_used = False

def remaining_time(start, total=15):
    return max(0, int(total - (time.time() - start)))

# === Load first level if empty ===
if not st.session_state.current_questions:
    load_next_level()
    st.session_state.level_start = time.time()

# === Game loop ===
if st.session_state.current_index < len(st.session_state.current_questions):
    german, info = st.session_state.current_questions[st.session_state.current_index]
    bangla = info["bangla"]
    sentence = info["sentence"]

    st.markdown(f"### 🎯 Level {st.session_state.level}")
    st.info(f"Question {st.session_state.current_index + 1}/{len(st.session_state.current_questions)}")
    st.markdown(f"**'{bangla}' শব্দটির জার্মান অনুবাদ লিখুন:**")
    if st.session_state.hint_used:
        st.caption(f"💡 Hint: {sentence}")

    # Timer
    tbox = st.empty()
    remain = remaining_time(st.session_state.level_start)
    tbox.warning(f"⏱️ Time left: {remain}s")

    ans_key = f"ans_{st.session_state.level}_{st.session_state.current_index}"
    ans = st.text_input("✍️ Type your German answer:", key=ans_key)

    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("💡 Hint"):
            st.session_state.hint_used = True
            st.rerun()

    with c2:
        if st.button("✅ Submit"):
            correct_ans = german.lower()
            given = ans.strip().lower()
            is_correct = given == correct_ans

            if is_correct:
                st.success("✅ Correct! Well done!")
                st.session_state.score += 10
                st.session_state.correct += 1
                st.image("https://media.tenor.com/5nZqVYpE6m4AAAAi/cute-rabbit-thumbs-up.gif",
                         caption="🐰 Thumbs Up!")
                st.session_state.used_words.add(german)
            else:
                st.error(f"❌ Wrong! Correct answer: {german}")
                st.session_state.wrong += 1
                st.image("https://media.tenor.com/bTFeixbXb2kAAAAi/sad-rabbit-no.gif",
                         caption="🐰 Thumbs Down!")
                # only wrongs go to retry list
                st.session_state.retry_words.append((german, info))

            st.session_state.results.append({
                "Level": st.session_state.level,
                "Bangla": bangla,
                "Your Answer": ans if ans else "—",
                "Correct German": german,
                "Result": "✅" if is_correct else "❌"
            })

            st.session_state.current_index += 1
            st.session_state.level_start = time.time()
            st.session_state.hint_used = False
            st.rerun()

    with c3:
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
            st.session_state.level_start = time.time()
            st.session_state.hint_used = False
            st.rerun()

# === Level complete ===
else:
    total_words = len(vocab)
    remaining_words = total_words - len(st.session_state.used_words)

    st.balloons()
    st.success(f"🎉 Level {st.session_state.level} Complete!")
    st.metric("Score", st.session_state.score)
    st.metric("Correct", st.session_state.correct)
    st.metric("Wrong", st.session_state.wrong)
    st.metric("Words Remaining", remaining_words)

    if st.session_state.retry_words:
        st.warning(f"⏩ {len(st.session_state.retry_words)} wrong words will repeat in next level.")
    else:
        st.info("✅ No mistakes in this level!")

    if remaining_words > 0 or st.session_state.retry_words:
        if st.button(f"🚀 Next Level {st.session_state.level + 1}"):
            st.session_state.level += 1
            load_next_level()
            st.rerun()
    else:
        st.balloons()
        st.success("🏁 Game Over! All words mastered! 🥇")
        df = pd.DataFrame(st.session_state.results)
        st.dataframe(df)
        st.metric("Final Score", st.session_state.score)
        st.metric("Total Correct", st.session_state.correct)
        st.metric("Total Wrong", st.session_state.wrong)
        if st.button("🔁 Restart Game"):
            for k in list(st.session_state.keys()):
                del st.session_state[k]
            st.rerun()

