import streamlit as st
import json
import random
import unicodedata
import difflib  # ingebou in Python

# Laai jou JSON databasis
with open(r"C:\Users\moste\OneDrive\Documents\spaans_afrikaans_engels.json", "r", encoding="utf-8") as f:
    vocabulary = json.load(f)

st.title("Taaltoets: Spaans ⇄ Afrikaans ⇄ Engels")

def normalize(word):
    return unicodedata.normalize("NFC", word.strip().lower())

def similarity(a, b):
    return difflib.SequenceMatcher(None, a, b).ratio()

direction = st.selectbox(
    "Kies toets rigting:",
    ["Afrikaans → Spaans", "Spaans → Afrikaans", "Engels → Spaans", "Spaans → Engels"]
)

num_words = st.slider("Hoeveel woorde wil jy toets?", 5, 50, 10)

quiz_words = random.sample(vocabulary, num_words)

# Gebruik 'n form sodat die app nie elke keer refresh nie
with st.form(key="quiz_form"):
    answers = []
    for i, entry in enumerate(quiz_words, start=1):
        if direction == "Afrikaans → Spaans":
            st.write(f"{i}. 🇿🇦 Afrikaans: {entry['afrikaans'][0]}")
            answer = st.text_input("Tik die Spaanse vertaling in:", key=f"q{i}")
            correct_word = entry["spanish"]

        elif direction == "Spaans → Afrikaans":
            st.write(f"{i}. 🇪🇸 Spaans: {entry['spanish']}")
            answer = st.text_input("Tik die Afrikaanse vertaling in:", key=f"q{i}")
            correct_word = entry["afrikaans"][0]

        elif direction == "Engels → Spaans":
            st.write(f"{i}. 🇬🇧 Engels: {entry['english'][0]}")
            answer = st.text_input("Tik die Spaanse vertaling in:", key=f"q{i}")
            correct_word = entry["spanish"]

        elif direction == "Spaans → Engels":
            st.write(f"{i}. 🇪🇸 Spaans: {entry['spanish']}")
            answer = st.text_input("Tik die Engelse vertaling in:", key=f"q{i}")
            correct_word = entry["english"][0]

        answers.append((answer, correct_word))

    submitted = st.form_submit_button("Klaar")

    if submitted:
        score = 0
        for answer, correct_word in answers:
            if answer:
                ans_norm = normalize(answer)
                corr_norm = normalize(correct_word)
                sim = similarity(ans_norm, corr_norm)

                if sim == 1.0:
                    st.success("✅ Perfek gespeld!")
                    score += 1
                elif sim >= 0.8:
                    st.warning(f"⚠️ Klein foutjies, maar aanvaarbaar ({round(sim*100)}% reg).")
                    score += 1
                else:
                    st.error(f"❌ Verkeerd. Regte antwoord: {correct_word}")

        st.write(f"Jou totaal: {score} / {num_words}")

# Knoppie om nuwe toets te begin
if st.button("Nuwe toets begin"):
    st.experimental_rerun()
