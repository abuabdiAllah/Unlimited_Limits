# Unlimited Limits

`Unlimited Limits` is a Streamlit app for practicing limit problems involving square roots and rational expressions.

It was built for a technical exercise that asked for:

- random equation generation on each run or refresh
- an answer input that accepts fractions, decimals, or simplified numeric expressions
- immediate correctness feedback
- a clean, student-friendly interface
- bonus explanation of the solution steps

## Problem Format

The app generates problems of the form:

$$
\lim_{x \to -1} \sqrt{\frac{x+1}{x^2 + cx + b}}
$$

where the values of `b` and `c` are chosen so that:

1. the expression inside the square root gives a `0/0` form at `x = -1`
2. the limit simplifies to `1/a` for some positive integer `a`

This is done by choosing:

- `c = a^2 + 2`
- `b = a^2 + 1`

for random integers `a` from `1` to `13`.

## Features

- New random problem on app load or refresh
- Shuffled problem cycle so every valid problem appears before any repeat
- `New Problem` button for another equation without reloading
- Answer parsing for inputs such as `1/3`, `0.5`, or `2`
- Immediate feedback for correct and incorrect answers
- Step-by-step walkthrough after submission
- Simple Streamlit interface designed around the provided wireframes

## Local Setup

From the repository root:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run app.py
```

Then open:

`http://localhost:8501`

## Notes

- Main app file: [app.py](./app.py)
- Dependencies: [requirements.txt](./requirements.txt)
- Local-only files such as `.venv/` and Streamlit logs are ignored in `.gitignore`

## Deployment

This app can be deployed on Streamlit Community Cloud by connecting the GitHub repository and using `app.py` as the entrypoint.
