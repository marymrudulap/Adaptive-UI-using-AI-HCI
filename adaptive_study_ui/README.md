# Adaptive Study UI

A local Python/Tkinter HCI quiz with AI-based presentation adaptation. Original project created for this assignment with ChatGPT assistance; no external sample repository was copied.

## Run on Windows
1. Install Python 3.10 or newer with Tcl/Tk support (official desktop installers normally include it).
2. Extract the ZIP fully. Open PowerShell in the extracted `adaptive_study_ui` folder.
3. Check GUI support: `python -m tkinter` (or `py -m tkinter`). Close the test window.
4. Run `python app.py` (or `py app.py`). No pip packages, account, or API keys are required.
5. Run checks: `python -m unittest -v test_model.py`.

macOS/Linux: use `python3`; Tkinter may require a separate OS package from the Python distributor. A graphical desktop is required.

## Demonstration
- Reset. Submit three wrong answers without hints; move to question four. Support displays a study guide automatically.
- Reset. Correct answers for questions 1–3 are options 1, 2, 3. Move to question four; Challenge displays a self-explanation prompt.
- Choose Support or Standard from Interface mode. The manual choice overrides the model. Choose Auto to resume.
- Hint remains accessible in every mode. Submit without choosing an answer to verify validation.
- Complete all six questions. Reset starts a fresh session and clears interaction history.

## How adaptation works
`model.py` loads 12 explicitly synthetic labeled rows from `training_data.csv`. A custom k-nearest-neighbors classifier (k=3) compares two normalized features: recent answer accuracy and the fraction of questions with an explicit hint request. Training consists of retaining labeled examples (instance-based learning); no neural model or remote AI service is used. The model is fixed during a session; only the five-answer rolling user model changes. Three submitted answers are required before automatic inference. Squared Euclidean distance ranks examples. Majority label wins; label ties prefer Standard, then Support, then Challenge. Distance ties preserve CSV row order.

Automatic adaptation is applied on Next question, not while a person is answering. Support includes the current question's conceptual hint automatically; Standard offers optional help; Challenge offers a self-explanation prompt. Question order, correctness, and available answers stay fixed. Vote share is shown but is not a calibrated probability. Automatic Support guidance does not count as an explicit hint request, a limitation of the feature definition.

History is RAM-only; no files are written at runtime, and no network requests are made. Closing or resetting discards history. Manual mode still records interaction events and resumes inference when Auto is selected.

## Files
- app.py: six-question desktop interface and callbacks
- model.py: nearest-neighbor classifier and rolling session state
- training_data.csv: 12 synthetic examples, four per mode
- test_model.py: 10 automated checks
- TEST_RESULTS.md: verification and remaining manual checks
- REFERENCES.md: research and software attribution
- AI_DISCLOSURE.md: scope of AI assistance
- requirements.txt: no third-party Python dependencies

## GitHub submission
Publication is pending. Repository access through the connected account returned Not Found on November 15, 2026; this does not prove the repository is absent.
Intended existing course repository, to verify: https://github.com/marymrudulap/AI-HCI-Course
Upload this entire folder as `adaptive-study-ui` in your actual course repository. Update the report with the confirmed repository or folder URL. Grant your instructor access if private. Do not submit a pending URL as proof of uploaded code.

PowerShell example from an existing local course-repository checkout after copying the folder:
```powershell
git add adaptive-study-ui
git commit -m "Add adaptive HCI study interface"
git push
```
Run `git remote -v` first to verify the destination and branch. If this is not your repository, use your own course repository and replace the URL in the report.


## Updated professional styling

This is a Python Tkinter desktop app. Styling is implemented in `app.py`
(`configure_styles`) and `ui_components.py`, rather than CSS. Both files are included.
The interface includes a navy sidebar, violet accents, rounded cards, keyboard
answer navigation, answer feedback colors, and a scrolling study panel.

### Run

Install Python 3.11 or newer with Tkinter support. Extract the complete ZIP,
open a terminal in the `adaptive_study_ui` folder, and run:

```sh
python app.py
```

No third-party Python packages are required.
