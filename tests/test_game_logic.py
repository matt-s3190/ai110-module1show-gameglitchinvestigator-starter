import pytest

from logic_utils import check_guess, process_guess

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"


def make_state(secret=50, attempts=0):
    """A fresh, plain-dict game state for testing process_guess."""
    return {
        "secret": secret,
        "attempts": attempts,
        "score": 0,
        "status": "playing",
        "history": [],
    }


# ---------------------------------------------------------------------------
# Bug 1: hint pointed the wrong way (swapped messages in check_guess, and
# secret_for_comparison turning the secret into a string on even attempts).
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("starting_attempts", [0, 1])  # next attempt is odd, then even
@pytest.mark.parametrize(
    "guess, expected_outcome, expected_hint",
    [
        ("9", "Too Low", "HIGHER"),    # "9" > "50" alphabetically: used to fail on even attempts
        ("40", "Too Low", "HIGHER"),
        ("60", "Too High", "LOWER"),
        ("50", "Win", "Correct"),
    ],
)
def test_hint_points_toward_secret(starting_attempts, guess, expected_outcome, expected_hint):
    state = make_state(secret=50, attempts=starting_attempts)

    result = process_guess(state, guess, attempt_limit=8, low=1, high=100)

    assert result["outcome"] == expected_outcome
    assert expected_hint in result["message"]


# ---------------------------------------------------------------------------
# Bug 2: invalid submissions used up an attempt and were added to history.
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("bad_input", ["True", "-1", "0", "101", "", "   ", "abc"])
def test_invalid_guess_does_not_use_attempt(bad_input):
    state = make_state(attempts=0)

    # Submit the same invalid guess several times in a row.
    for _ in range(3):
        result = process_guess(state, bad_input, attempt_limit=8, low=1, high=100)
        assert result["error"] is not None

    assert state["attempts"] == 0
    assert state["history"] == []
    assert state["score"] == 0
    assert state["status"] == "playing"


def test_valid_guess_still_uses_attempt():
    # Guard against over-correcting: a valid guess must still count.
    state = make_state(attempts=0)

    result = process_guess(state, "40", attempt_limit=8, low=1, high=100)

    assert result["error"] is None
    assert state["attempts"] == 1
    assert state["history"] == [40]
