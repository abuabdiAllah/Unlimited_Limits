# Unlimited Limits App

Unlimited Limits is a Streamlit application that helps students practice evaluating limits involving square roots and rational expressions.T

## The Problem

The app presents limits of the form:

$$\lim_{x \to -1} \sqrt{\frac{x+1}{x^2 + cx + b}}$$

where `b` and `c` are randomly chosen integers satisfying:

1. The expression inside the square root evaluates to **0/0** at x = −1 (indeterminate form requiring simplification).
2. After simplification, the limit equals **1/a** for some positive integer **a**.

### How the math works

For condition 1 (0/0 form at x = −1):
- Numerator: x + 1 = 0 at x = −1 ✓
- Denominator: x² + cx + b = 0 at x = −1 → 1 − c + b = 0 → **b = c − 1**

With b = c − 1, the denominator factors as:
```
x² + cx + (c−1) = (x+1)(x + c−1)
```

Cancelling the (x+1) factor:
```
sqrt((x+1) / ((x+1)(x+c−1))) = sqrt(1 / (x+c−1))
```

At x = −1: `sqrt(1/(c−2))`. For this to equal `1/a` (an integer reciprocal), we need `c − 2 = a²`, so:
- **c = a² + 2**, **b = a² + 1** for any positive integer **a**

The app generates problems for a ∈ {1, 2, 3, 4, 5, 6, 7}.

## Setup & Running Locally

### Prerequisites
- Python 3.9+

### Installation

```bash
# Clone the repo
git clone <your-repo-url>
cd limit_app

# Create a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Run the app

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`.

## Deployment (Streamlit Community Cloud)

1. Push this repo to GitHub.
2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in.
3. Click **New app**, select your repo and `app.py` as the entry point.
4. Click **Deploy**.

## Features

- **Random problem generation** — new (b, c) pair each session, or click "New Problem"
- **Flexible answer parsing** — accepts fractions (`1/3`), decimals (`0.333`), and integers
- **Immediate feedback** — correct/incorrect with the right answer shown
- **Step-by-step explanation** — full solution walkthrough after every submission
- **Sidebar help** — quick reference for accepted answer formats

## Notes

- Only the Python standard library (`fractions`, `math`, `random`) and `streamlit` are required — no heavy math packages needed.
- The LaTex rendering is handled natively by Streamlit's `st.latex()`.

