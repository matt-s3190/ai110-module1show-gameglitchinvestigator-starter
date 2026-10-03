# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?

  It seemed normal at first. Every widget was aligned as it should, a line edit to place my guess and three consecutive buttons to submit my guess, create a new game, and show me a hint. In addition, the title and instruction of the game is rendered correctly.
- List at least two concrete bugs you noticed at the start
  - Selecting a different diffucilty changes the range shown below the dropdown, but the range shown in the main page stays the same
  - Switching difficulties midway through a game doesn't reset my attempt counter and my guess history.

  

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
| Clicking on new game button after finishing a game | Refresh my screen and reset my attempts | Nothing happens. Screen stays the same and no reset occurs | "None" |
| Repeatedly submitting a invalid guess (i.e "True", -1) | Display a warning message telling me my guess is invalid and not decrement my attempts | Shows a warning message but my "Attempts left: " counter decreases by 1 with each submission | "None" |
| Guessing a number following the hint indicator (i.e. "LOWER" or "HIGHER") | Helps me find the correct number more easier with less attempts | Incorrectly leads me farther away from the correct number | "None" |

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
Claude
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).

  I suspected the wrong-hint bug was in `check_guess`, and Claude confirmed the "Go HIGHER" and "Go LOWER" messages were swapped, but it also found a second cause: `secret_for_comparison` turned the secret into a string on even attempts, so Python compared guesses alphabetically (`"9"` counted as bigger than `"50"`). It was correct because both problems had to be fixed for the hint to be right on every turn, not just odd ones. I verified it with a pytest case that checks guesses like 9, 40, 60, and 50 on both odd and even attempts, and all of them passed.

- Give one example of an AI suggestion you did not accept as written (including what the AI suggested, why you rejected or changed it, and how you verified your version). It does not have to be a suggestion that was wrong: over-engineered, out of scope, harder to read, or a poor fit for this codebase all count.

  While fixing the invalid-guess bug, Claude pointed out two more problems: `initial_state` starts attempts at 1 instead of 0, and the "Attempts left" counter is drawn before the guess is processed, so it updates one click late. I chose not to fix those in the same change because they were out of scope for the bug I was working on, and mixing them in would make it harder to tell which change fixed what. I verified my narrower fix with pytest, which showed invalid inputs like "True" and "-1" no longer change the attempt count while a valid guess still does.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
When it has passed my manual pytest cases and its behavior it shown correctly when running.
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
  Running the game logic and manually pressing a button to see if it elicit the correct response.
- Did AI help you design or understand any tests? How?
Claude help me design several test cases by guiding me by showing me what a correct response should look like from an incorrect one.


---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

  Think of Streamlit as a game of Simon Says where every move starts a brand-new round. Each time you click a button, type in a box, or move a slider, Streamlit refreshes the screen and reruns your whole Python script essentially redrawing everything fresh. This is known as a rerun. That bad thing about reruns is that it also wipes out any regular variables. If you had count variable set to 0 and added 1 when a button was clicked, the next rerun sets count = 0 again, analagous to a game forgetting your score every round. Session state is the scoreboard that survives between rounds. It's a special dictionary (st.session_state) that Streamlit keeps for each user's visit, so anything you store exists after every rerun

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  Commiting every so often with meaningful messages. That way, if I left a project for some time and came back to it, I can read these detailed commits to see not only where I left off, but my original approach to it all.
  
- What is one thing you would do differently next time you work with AI on a coding task?
  Clearly define boundaries around my prompt as Claude was perfoming extra tasks outside of what my prompt requires him to do. 
- In one or two sentences, describe how this project changed the way you think about AI generated code.
I should see AI as a step stool to further enrich my understanding and not as a brain that I should rely on solely.
