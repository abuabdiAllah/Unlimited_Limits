# Unlimited Limits

`Unlimited Limits` is a Streamlit app for practicing limit problems involving square roots and rational expressions.

## Problem Format and Derivation

The app generates problems of the form:

$$
\lim_{x \to -1} \sqrt{\frac{x+1}{x^2 + cx + b}}
$$

where the values of `b` and `c` are chosen so that:

1. the expression inside the square root gives a `0/0` form at `x = -1`
2. the limit simplifies to `1/a` for some positive integer `a`

Those conditions force a specific pattern for `b` and `c`.

At `x = -1`, the denominator must also equal zero:

$$
(-1)^2 + c(-1) + b = 0
$$

so:

$$
1 - c + b = 0 \Rightarrow b = c - 1
$$

That means the denominator factors as:

$$
x^2 + cx + (c - 1) = (x+1)(x+c-1)
$$

After canceling the common factor, the limit becomes:

$$
\sqrt{\frac{1}{x+c-1}}
$$

Now evaluate at `x = -1`:

$$
\sqrt{\frac{1}{c-2}}
$$

The project requires this to equal `1/a`, so:

$$
\sqrt{\frac{1}{c-2}} = \frac{1}{a}
$$

which implies:

$$
c - 2 = a^2
$$

Therefore:

- `c = a^2 + 2`
- `b = a^2 + 1`

for positive integers `a`.

In this app, `a` is limited to `1` through `13`. That keeps the problems readable, keeps the arithmetic within a familiar multiplication-table range for most students, and still provides enough variety for practice without producing coefficients that feel unnecessarily large.

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

Live app:

`https://unlimitedlimits.streamlit.app/`

GitHub repository:

`https://github.com/abuabdiAllah/Unlimited_Limits`

The app is deployed on Streamlit Community Cloud using `app.py` as the entrypoint.

## Future Improvement Ideas

- Add a pop-up onscreen calculator students could use if they needed
- Add hints if the student gets the answer wrong the first few times before giving the complete walkthrough
