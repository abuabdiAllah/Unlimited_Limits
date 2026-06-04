import streamlit as st
import random
from fractions import Fraction
import math

st.set_page_config(page_title="Limit Practice", page_icon="∫", layout="centered")

# ─── Math logic ──────────────────────────────────────────────────────────────

def find_valid_bc_pairs(max_range=10):
    """
    Find all (b, c) pairs such that:
      - x+1 / (x^2 + cx + b) gives 0/0 at x = -1  →  b - c + 1 = 0  →  b = c - 1
      - After factoring out (x+1), the limit equals 1/a for some nonzero integer a
      - The denominator after cancellation (evaluated at x=-1) is nonzero

    x^2 + cx + b = x^2 + cx + (c-1)
    Since b = c-1, try to factor: x^2 + cx + (c-1) = (x+1)(x + (c-1))
    Check: (x+1)(x+c-1) = x^2 + (c-1)x + x + (c-1) = x^2 + cx + (c-1) ✓

    So the expression simplifies:
      sqrt((x+1) / ((x+1)(x+c-1))) = sqrt(1/(x+c-1))

    At x = -1:  limit = sqrt(1/(-1 + c - 1)) = sqrt(1/(c-2)) = 1/sqrt(c-2)

    For the limit to be 1/a for integer a:
      1/sqrt(c-2) = 1/a  →  a = sqrt(c-2)  →  c-2 must be a perfect square

    So: c - 2 = k^2  →  c = k^2 + 2  for k = 1, 2, 3, ...
    And b = c - 1 = k^2 + 1
    And a = k
    """
    valid = []
    for k in range(1, max_range):
        c = k * k + 2
        b = k * k + 1
        a = k
        # Extra check: denominator x+c-1 at x=-1 is c-2 = k^2 ≠ 0 ✓
        # And the expression inside sqrt must be positive near x=-1 for real limit
        # (x+1)/((x+1)(x+c-1)) = 1/(x+c-1); near x=-1, x+c-1 ≈ c-2 = k^2 > 0 ✓
        valid.append((b, c, a))
    return valid


def generate_problem():
    """Pick a random valid (b, c, a) triple."""
    pairs = find_valid_bc_pairs(max_range=8)  # a up to 7
    return random.choice(pairs)


def parse_answer(answer_str):
    """
    Parse student answer. Accepts:
      - integers: "3"
      - fractions: "1/3", "2/5"
      - decimals: "0.333", "0.5"
    Returns a Fraction or None on failure.
    """
    s = answer_str.strip().replace(" ", "")
    if not s:
        return None
    try:
        if "/" in s:
            return Fraction(s)
        else:
            # Try float then convert
            f = float(s)
            return Fraction(f).limit_denominator(1000)
    except (ValueError, ZeroDivisionError):
        return None


def correct_answer_fraction(a):
    """Return correct answer as a Fraction."""
    return Fraction(1, a)


def format_fraction(frac):
    """Format a Fraction nicely."""
    if frac.denominator == 1:
        return str(frac.numerator)
    return f"{frac.numerator}/{frac.denominator}"


# ─── Session state ────────────────────────────────────────────────────────────

if "b" not in st.session_state or "c" not in st.session_state:
    b, c, a = generate_problem()
    st.session_state.b = b
    st.session_state.c = c
    st.session_state.a = a
    st.session_state.submitted = False
    st.session_state.answer_text = ""

b = st.session_state.b
c = st.session_state.c
a = st.session_state.a

# ─── UI ───────────────────────────────────────────────────────────────────────

st.title("Limit Practice")
st.markdown("Practice evaluating limits with square roots and rational expressions.")

# Display the problem using LaTeX
c_sign = f"+ {c}" if c >= 0 else f"- {abs(c)}"
b_sign = f"+ {b}" if b >= 0 else f"- {abs(b)}"

latex_problem = (
    r"\lim_{x \to -1} \sqrt{\dfrac{x + 1}{x^2 "
    + c_sign + r"x "
    + b_sign + r"}}"
)

st.markdown("### Solve the limit:")
st.latex(latex_problem)

st.markdown("---")

# Input + Submit
with st.form("answer_form", clear_on_submit=False):
    user_input = st.text_input(
        "Your answer (e.g. `1/3`, `0.5`, `2`):",
        value=st.session_state.answer_text,
        placeholder="Enter your answer here",
    )
    col1, col2 = st.columns([1, 1])
    with col1:
        submitted = st.form_submit_button("Submit Answer", use_container_width=True)
    with col2:
        new_problem = st.form_submit_button("New Problem", use_container_width=True)

if new_problem:
    b_new, c_new, a_new = generate_problem()
    st.session_state.b = b_new
    st.session_state.c = c_new
    st.session_state.a = a_new
    st.session_state.submitted = False
    st.session_state.answer_text = ""
    st.rerun()

if submitted and user_input.strip():
    st.session_state.answer_text = user_input
    st.session_state.submitted = True

# ─── Feedback ────────────────────────────────────────────────────────────────

if st.session_state.submitted and st.session_state.answer_text.strip():
    parsed = parse_answer(st.session_state.answer_text)
    correct = correct_answer_fraction(a)

    if parsed is None:
        st.warning("⚠️ Couldn't parse your answer. Try formats like `1/3`, `0.5`, or `2`.")
    else:
        # Allow small floating-point tolerance
        is_correct = abs(float(parsed) - float(correct)) < 1e-6

        if is_correct:
            st.success(f"✅ Correct! The limit is **{format_fraction(correct)}**.")
        else:
            st.error(
                f"❌ Not quite. You entered **{format_fraction(parsed)}**, "
                f"but the correct answer is **{format_fraction(correct)}**."
            )

        # ── Explanation (always shown after submission) ──────────────────────
        st.markdown("---")
        st.markdown("#### 📖 Solution walkthrough")

        c_sign_ex = f"+ {c}" if c >= 0 else f"- {abs(c)}"
        b_sign_ex = f"+ {b}" if b >= 0 else f"- {abs(b)}"
        c_minus_1 = c - 1
        cm1_sign = f"+ {c_minus_1}" if c_minus_1 >= 0 else f"- {abs(c_minus_1)}"

        st.markdown(
            f"**Step 1 – Check the indeterminate form.**  \n"
            f"Substituting $x = -1$:"
        )
        st.latex(
            r"\frac{x+1}{x^2 " + c_sign_ex + r"x " + b_sign_ex + r"}"
            r"\bigg|_{x=-1} = \frac{0}{0}"
        )

        st.markdown(
            f"**Step 2 – Factor the denominator.**  \n"
            f"Since $b = c - 1 = {b}$, the denominator factors as:"
        )
        st.latex(
            r"x^2 " + c_sign_ex + r"x " + b_sign_ex
            + r" = (x+1)(x " + cm1_sign + r")"
        )

        st.markdown("**Step 3 – Cancel the common factor $(x+1)$.**")
        st.latex(
            r"\sqrt{\frac{x+1}{(x+1)(x " + cm1_sign + r")}}"
            r" = \sqrt{\frac{1}{x " + cm1_sign + r"}}"
        )

        st.markdown("**Step 4 – Evaluate at $x = -1$.**")
        denom_val = c - 2  # = k^2 = a^2
        denom_sign = f"+ {denom_val}" if denom_val >= 0 else f"- {abs(denom_val)}"
        st.latex(
            r"\sqrt{\frac{1}{-1 " + denom_sign + r"}}"
            + r" = \sqrt{\frac{1}{" + str(denom_val) + r"}}"
            + r" = \frac{1}{" + str(a) + r"}"
        )

        st.markdown(
            f"**Result:** The limit equals $\\dfrac{{1}}{{{a}}}$."
        )

# ─── Sidebar ────────────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown("### About this app")
    st.markdown(
        "This app generates limit problems of the form:\n\n"
        r"$$\lim_{x \to -1} \sqrt{\frac{x+1}{x^2 + cx + b}}$$"
        "\n\nThe denominator always has $(x+1)$ as a factor, "
        "so the $\\frac{0}{0}$ form resolves by cancellation."
    )
    st.markdown("**Accepted answer formats:**")
    st.markdown("- Fractions: `1/3`, `2/5`\n- Decimals: `0.333`\n- Integers: `2`")
    st.markdown("---")
    st.markdown("Click **New Problem** to get a fresh equation.")
