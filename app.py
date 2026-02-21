import streamlit as st
import json
import random
import unicodedata
import difflib  # ingebou in Python, geen installasie nodig

# Laai jou JSON databasis
with open("spaans_afrikaans_engels.json", "r", encoding="utf-8") as f:
    vocabulary = json.load(f)

st.title("Taaltoets: Spaans ⇄ Afrikaans ⇄ Engels")

# Normaliseer Unicode (sodat á ≠ a)
def normalize(word):
    return unicodedata.normalize("NFC", word.strip().lower())

# Bereken similarity tussen antwoorde
def similarity(a, b):
    return difflib.SequenceMatcher(None, a, b).ratio()

# Kies toets rigting
direction = st.selectbox(
    "Kies toets rigting:",
    ["Afrikaans → Spaans", "Spaans → Afrikaans", "Engels → Spaans", "Spaans → Engels"]
)

# Kies hoeveel woorde jy wil toets
num_words = st.slider("Hoeveel woorde wil jy toets?", 5, 50, 20)

quiz_words = random.sample(vocabulary, num_words)

score = 0
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
