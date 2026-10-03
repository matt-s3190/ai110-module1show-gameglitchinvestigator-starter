"""Streamlit UI for the Glitchy Guesser.

Everything here only *displays* things or *collects* input.
No game rules live in this file; those are in logic_utils.py.
"""

import streamlit as st


def setup_page():
    st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")
    st.title("🎮 Game Glitch Investigator")
    st.caption("An AI-generated guessing game. Something is off.")


def render_sidebar(difficulties, default_index):
    """Draw the settings sidebar and return the chosen difficulty."""
    st.sidebar.header("Settings")
    return st.sidebar.selectbox(
        "Difficulty",
        difficulties,
        index=default_index,
    )


def render_sidebar_info(low, high, attempt_limit):
    st.sidebar.caption(f"Range: {low} to {high}")
    st.sidebar.caption(f"Attempts allowed: {attempt_limit}")


def render_prompt(attempts_left):
    st.subheader("Make a guess")
    st.info(
        f"Guess a number between 1 and 100. "
        f"Attempts left: {attempts_left}"
    )


def render_debug_info(state, difficulty):
    with st.expander("Developer Debug Info"):
        st.write("Secret:", state.secret)
        st.write("Attempts:", state.attempts)
        st.write("Score:", state.score)
        st.write("Difficulty:", difficulty)
        st.write("History:", state.history)


def render_guess_input(difficulty):
    """Return the raw text the user typed."""
    return st.text_input(
        "Enter your guess:",
        key=f"guess_input_{difficulty}"
    )


def render_controls():
    """Return (submit_clicked, new_game_clicked, show_hint)."""
    col1, col2, col3 = st.columns(3)
    with col1:
        submit = st.button("Submit Guess 🚀")
    with col2:
        new_game = st.button("New Game 🔁")
    with col3:
        show_hint = st.checkbox("Show hint", value=True)
    return submit, new_game, show_hint


def render_new_game_started():
    st.success("New game started.")


def render_game_over(status):
    if status == "won":
        st.success("You already won. Start a new game to play again.")
    else:
        st.error("Game over. Start a new game to try again.")


def render_guess_result(result, show_hint, secret, score):
    """Display the outcome of one turn returned by logic_utils.process_guess."""
    if result["error"]:
        st.error(result["error"])
        return

    if show_hint:
        st.warning(result["message"])

    if result["status"] == "won":
        st.balloons()
        st.success(
            f"You won! The secret was {secret}. "
            f"Final score: {score}"
        )
    elif result["status"] == "lost":
        st.error(
            f"Out of attempts! "
            f"The secret was {secret}. "
            f"Score: {score}"
        )


def render_footer():
    st.divider()
    st.caption("Built by an AI that claims this code is production-ready.")
