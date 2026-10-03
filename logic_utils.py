"""Core game logic for the Glitchy Guesser.

Nothing in this file imports Streamlit. Every function takes plain values
(or a dict-like `state`) and returns plain values, so it can be unit tested
with pytest without running the UI.

NOTE: This is a pure refactor. Behavior was moved here unchanged from app.py,
bugs included, so they can be isolated and fixed one at a time.
"""

import random


# ---------------------------------------------------------------------------
# Difficulty settings
# ---------------------------------------------------------------------------

DIFFICULTIES = ["Easy", "Normal", "Hard"]
DEFAULT_DIFFICULTY_INDEX = 1

ATTEMPT_LIMITS = {
    "Easy": 6,
    "Normal": 8,
    "Hard": 5,
}


def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        return 1, 50
    return 1, 100


def get_attempt_limit(difficulty: str):
    """Return how many attempts are allowed for a given difficulty."""
    return ATTEMPT_LIMITS[difficulty]


# ---------------------------------------------------------------------------
# Secret number / game state
# ---------------------------------------------------------------------------

def generate_secret(low: int, high: int):
    """Pick a random secret number in [low, high]."""
    return random.randint(low, high)


def initial_state(low: int, high: int):
    """Default values for a brand-new session."""
    return {
        "secret": generate_secret(low, high),
        "attempts": 1,
        "score": 0,
        "status": "playing",
        "history": [],
    }


def init_state(state, low: int, high: int):
    """Fill in any missing keys in `state` with their defaults."""
    for key, value in initial_state(low, high).items():
        if key not in state:
            state[key] = value


def start_new_game(state):
    """Reset `state` when the player clicks New Game."""
    state["attempts"] = 0
    state["secret"] = generate_secret(1, 100)


def attempts_left(attempt_limit: int, attempts: int):
    """Number of attempts remaining."""
    return attempt_limit - attempts


# ---------------------------------------------------------------------------
# Guess handling
# ---------------------------------------------------------------------------

def parse_guess(raw: str, low: int = None, high: int = None):
    """
    Parse user input into an int guess.

    If `low` and `high` are given, guesses outside [low, high] are rejected.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    if raw is None:
        return False, None, "Enter a guess."

    raw = raw.strip()
    if raw == "":
        return False, None, "Enter a guess."

    try:
        if "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)
    except Exception:
        return False, None, "That is not a number."

    # FIX: Claude traced the "invalid guess uses an attempt" bug here; out-of-range guesses like -1 were accepted. Added a range check; verified with pytest.
    if low is not None and high is not None and not (low <= value <= high):
        return False, None, f"Guess must be between {low} and {high}."

    return True, value, None


# FIX: Claude found this second cause of the wrong-hint bug while checking my FIXME; secret became a string on even attempts. Now always an int.
def secret_for_comparison(secret, attempts: int):
    """Return the secret value used when checking a guess on this attempt.

    Always returns the secret as an int so guesses are compared numerically.
    (Previously it returned str(secret) on even attempts, which caused
    alphabetical comparisons like "9" > "50".)
    """
    return int(secret)

# FIX: I flagged this function with a FIXME; Claude confirmed the HIGHER/LOWER messages were swapped, fixed them, and removed the string-compare fallback.
def check_guess(guess, secret):
    """
    Compare guess to secret and return (outcome, message).

    outcome examples: "Win", "Too High", "Too Low"
    """
    if guess == secret:
        return "Win", "🎉 Correct!"

    if guess > secret:
        return "Too High", "📉 Go LOWER!"
    return "Too Low", "📈 Go HIGHER!"


def update_score(current_score: int, outcome: str, attempt_number: int):
    """Update score based on outcome and attempt number."""
    if outcome == "Win":
        points = 100 - 10 * (attempt_number + 1)
        if points < 10:
            points = 10
        return current_score + points

    if outcome == "Too High":
        if attempt_number % 2 == 0:
            return current_score + 5
        return current_score - 5

    if outcome == "Too Low":
        return current_score - 5

    return current_score


def process_guess(state, raw_guess: str, attempt_limit: int, low: int = None, high: int = None):
    """
    Run one full turn: parse the guess, and only if it is valid, count the
    attempt, check it, and update score/history/status in `state`.
    Invalid guesses return an error and leave `state` untouched.

    Returns a result dict the UI can render:
        {
            "error":   str | None,   # invalid input message
            "outcome": str | None,   # "Win" / "Too High" / "Too Low"
            "message": str | None,   # hint text
            "status":  str,          # "playing" / "won" / "lost"
        }
    """
    result = {"error": None, "outcome": None, "message": None, "status": state["status"]}

    ok, guess_int, err = parse_guess(raw_guess, low, high)

    if not ok:
        result["error"] = err
        return result

    # FIX: Claude found attempts were counted before validation; moved the increment here so only a valid guess costs an attempt. Verified with pytest.
    state["attempts"] += 1
    state["history"].append(guess_int)

    secret = secret_for_comparison(state["secret"], state["attempts"])
    outcome, message = check_guess(guess_int, secret)
    result["outcome"] = outcome
    result["message"] = message

    state["score"] = update_score(
        current_score=state["score"],
        outcome=outcome,
        attempt_number=state["attempts"],
    )

    if outcome == "Win":
        state["status"] = "won"
    elif state["attempts"] >= attempt_limit:
        state["status"] = "lost"

    result["status"] = state["status"]
    return result
