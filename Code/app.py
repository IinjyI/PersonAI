import streamlit as st
from generation import generate_tweet_and_mbti

mbti = [
    "ISTJ",
    "ISFJ",
    "INFJ",
    "INTJ",
    "ISTP",
    "ISFP",
    "INFP",
    "INTP",
    "ESTP",
    "ESFP",
    "ENFP",
    "ENTP",
    "ESTJ",
    "ESFJ",
    "ENFJ",
    "ENTJ",
]


def guess_page():

    success = False
    error = False

    # Form for guessing the generated tweet's authour's MBTI type
    with st.form(key="mbti_guess_form"):
        st.write("**Can You Guess The MBTI Type Of A Person Based On A Tweet?**")

        # Generate tweet and mbti if not already generated
        if "generated_tweet" not in st.session_state:
            generated_tweet, generated_mbti = generate_tweet_and_mbti()
            st.session_state.generated_tweet = generated_tweet
            st.session_state.generated_mbti = generated_mbti

        # Initialize current guess if not already present
        if "current_guess" not in st.session_state:
            st.session_state.current_guess = None

        # Display generated tweet
        tweet_placeholder = st.empty()
        if st.session_state.generated_tweet:
            tweet_placeholder.caption(f"💬 **{st.session_state.generated_tweet}**")

        # Radio button for selecting guess
        guess = st.selectbox("Your Guess?", options=mbti)

        col1, col2 = st.columns(2)

        with col1:
            # Button to submit guess
            if st.form_submit_button("Guess", type="primary"):
                st.session_state.current_guess = guess
                if guess == st.session_state.generated_mbti:
                    success = True
                else:
                    error = True

        with col2:
            # Button to generate new tweet for a new round
            if st.form_submit_button("New Round"):
                generated_tweet, generated_mbti = generate_tweet_and_mbti()
                st.session_state.generated_tweet = generated_tweet
                st.session_state.generated_mbti = generated_mbti
                tweet_placeholder.caption(f"💬 **{st.session_state.generated_tweet}**")

        # Display success message if guess is correct
        if success:
            st.success(f"Yup! This Person Is An **{st.session_state.generated_mbti}.**")

        # Display error message if guess is incorrect
        if error:
            st.error(f"Oops! This Person Is An **{st.session_state.generated_mbti}.**")


def classify_page():
    classified = False

    # Form for classifying user's tweet
    with st.form(key="classify_tweet"):
        st.write("**Do You Want To Know Your MBTI Type Based On Your Tweets?**")
        tweet = st.text_input("Enter A Tweet:", max_chars=280)

        # Button to classify the tweet
        if st.form_submit_button("Classify", type="primary"):
            classified = True

        if classified:
            # Display result based on tweet classification
            st.write(f"🎭 Your MBTI Type Is **??**")


# Main function
if __name__ == "__main__":
    # Streamlit UI
    st.header("🎭 PersonAI")
    selected_page = st.selectbox(
        "Do You Want To...", ["Guess MBTI Type?", "Classify Tweet?"]
    )

    # Display appropriate section based on selection
    if selected_page == "Guess MBTI Type?":
        guess_page()
    elif selected_page == "Classify Tweet?":
        classify_page()
