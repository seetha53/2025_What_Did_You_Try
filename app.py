import streamlit as st
from openai import OpenAI
from openai import OpenAIError

# --------------------------------------------------
# BASIC SESSION SAFETY
# --------------------------------------------------

if "calls" not in st.session_state:
    st.session_state.calls = 0

MAX_CALLS_PER_SESSION = 10

# --------------------------------------------------
# OPENAI CLIENT
# --------------------------------------------------

# Uses OPENAI_API_KEY from environment variable
client = OpenAI()

# --------------------------------------------------
# AI FUNCTION (SINGLE CALL)
# --------------------------------------------------

@st.cache_data(show_spinner=False)
def reflect_on_experience(text: str) -> str:
    prompt = f"""
    You are an energetic, reflective narrator celebrating someone's rare achievement.

    The user did this:
    \"\"\"{experience}\"\"\"

    Your task, in **one response**, is to:

    1. Provide a short title for this experience in a separate line
    2. Estimate a **soft, symbolic rarity number** for this experience (e.g., "about 1 in 50 people", "fewer than 1 in 10,000"). This is not exact statistics — it should give the reader a sense of how uncommon the experience is.  
    3. Provide a **short breakdown / explanation** of why this number is reasonable (1–2 sentences).  
    4. Provide **2–3 short upbeat, reflective lines** celebrating the experience and encouraging the reader to continue seeking meaningful experiences.

    Tone:
    - Warm, celebratory, human
    - Upbeat and motivating
    - Concise, readable at a glance
    - Rarity is the focus, reflections wrap around it

    Examples:

    Input: "Learnt to play the piano"
    Output:
    Title: "The Beginning of a perfect note!"
    Soft rarity: "Only about 1 in 100 people learn to play the piano in their lifetime."
    Explanation: Piano is a widely loved instrument, but relatively few dedicate the time to become proficient.
    Reflection:
    You’ve joined a special group pursuing curiosity and growth.  
    Keep this amazing momentum going into 2026 — more adventures await!

    Input: "Climbed Mount Everest"
    Output:
    Title: "The Pinnacle of hard work and growth!"
    Soft rarity: "Fewer than 1 in 10,000 people have ever stood atop Everest."
    Explanation: Everest is extremely difficult to climb and only a tiny fraction of people attempt it each year.
    Reflection:
    What an extraordinary accomplishment — you’re in a tiny, elite group.  
    Let this rare triumph fuel even bolder adventures in 2026!

    Now, using this format, generate the **soft rarity, explanation, and 2–3 line upbeat reflection** for the experience above.
    Don't display headers like title, soft rarity, explanation - just these 2-3 lines as one cohesive paragraph is sufficient.
    For responses that are very commonplace, 1 in 10 or more, ignore the numbers and focus on how it is still a big deal.
    """
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.8,
    )

    return response.choices[0].message.content


# --------------------------------------------------
# STREAMLIT UI
# --------------------------------------------------

st.set_page_config(page_title="A Year Worth Remembering", page_icon="🎉")

st.markdown("<h2 style='text-align: center; color: #4CAF50;'>🎉 Tell me one thing you did this year that you loved doing.</h2>", unsafe_allow_html=True)

st.markdown("<h3 style='text-align: center;'> Small, big, anything at all! </h3>", unsafe_allow_html=True)

experience = st.text_area(
    "",
    placeholder="e.g. Learnt a new language, Took a solo trip, Started journaling",
)

if st.button("There you go!"):
    if not experience.strip():
        st.warning("Tell me something first 🙂")
        st.stop()

    if st.session_state.calls >= MAX_CALLS_PER_SESSION:
        st.error(
            "You've reflected a few times already. "
            "Take a pause and come back later 🙂"
        )
        st.stop()

    st.session_state.calls += 1

    with st.spinner("Reflecting on this..."):
        try:
            reflection = reflect_on_experience(experience)
            st.write(reflection)
            with st.container():
                st.image("images/experiences.jpg", width=300)

        except OpenAIError:
            st.error(
                "The reflection service is temporarily unavailable. "
                "Please try again in a moment."
            )

        except Exception as e:
            st.error("Something unexpected went wrong.")
            st.write(str(e))
