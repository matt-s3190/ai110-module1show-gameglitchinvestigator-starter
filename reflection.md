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
- Give one example of an AI suggestion you did not accept as written (including what the AI suggested, why you rejected or changed it, and how you verified your version). It does not have to be a suggestion that was wrong: over-engineered, out of scope, harder to read, or a poor fit for this codebase all count.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
