"""Entry point: wires the UI (ui.py) to the game logic (logic_utils.py).

Run with:  python -m streamlit run app.py
"""

import streamlit as st

import logic_utils as game
import ui

ui.setup_page()

# --- Settings -------------------------------------------------------------
difficulty = ui.render_sidebar(game.DIFFICULTIES, game.DEFAULT_DIFFICULTY_INDEX)
attempt_limit = game.get_attempt_limit(difficulty)
low, high = game.get_range_for_difficulty(difficulty)
ui.render_sidebar_info(low, high, attempt_limit)

# --- State ----------------------------------------------------------------
state = st.session_state
game.init_state(state, low, high)

# --- Main screen ----------------------------------------------------------
ui.render_prompt(game.attempts_left(attempt_limit, state.attempts))
ui.render_debug_info(state, difficulty)

raw_guess = ui.render_guess_input(difficulty)
submit, new_game, show_hint = ui.render_controls()

if new_game:
    game.start_new_game(state)
    ui.render_new_game_started()
    st.rerun()

if state.status != "playing":
    ui.render_game_over(state.status)
    st.stop()

if submit:
    result = game.process_guess(state, raw_guess, attempt_limit)
    ui.render_guess_result(result, show_hint, state.secret, state.score)

ui.render_footer()
