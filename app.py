import math
import random
from fractions import Fraction

import streamlit as st


st.set_page_config(page_title="Unlimited Limits", page_icon="UL", layout="centered")


AUTHOR_NAME = "Adam Daif"
LINKEDIN_URL = "https://www.linkedin.com/in/adam-daif-71638623a/"
DECIMAL_PLACES = 3
DECIMAL_TOLERANCE = 0.5 * (10 ** -DECIMAL_PLACES)
MAX_A = 13


def find_valid_bc_pairs(max_a=MAX_A):
    """Return valid (b, c, a) triples where the limit simplifies to 1/a."""
    valid = []
    for a in range(1, max_a + 1):
        c = a * a + 2
        b = c - 1
        valid.append((b, c, a))
    return valid


def refill_problem_queue():
    """Shuffle all valid problems so each one appears before any repeat."""
    problems = find_valid_bc_pairs()
    random.shuffle(problems)

    last_problem = st.session_state.get("last_problem")
    if last_problem and len(problems) > 1 and problems[0] == last_problem:
        problems.append(problems.pop(0))

    st.session_state.problem_queue = problems


def generate_problem():
    """Return the next problem from a shuffled queue of all valid triples."""
    if "problem_queue" not in st.session_state or not st.session_state.problem_queue:
        refill_problem_queue()

    problem = st.session_state.problem_queue.pop(0)
    st.session_state.last_problem = problem
    return problem


def classify_answer_format(answer_text):
    cleaned = answer_text.strip().replace(" ", "")
    if "/" in cleaned:
        return "fraction"
    if "." in cleaned:
        return "decimal"
    return "number"


def parse_answer(answer_text):
    """Parse fractions, decimals, and plain integers."""
    cleaned = answer_text.strip().replace(" ", "")
    if not cleaned:
        return None

    try:
        if "/" in cleaned:
            return float(Fraction(cleaned))
        return float(cleaned)
    except (ValueError, ZeroDivisionError):
        return None


def correct_answer_fraction(a):
    return Fraction(1, a)


def format_fraction(value):
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def format_answer_display(value):
    fraction_text = format_fraction(value)
    if value.denominator == 1:
        return fraction_text

    decimal_text = f"{float(value):.{DECIMAL_PLACES}f}"
    return f"{fraction_text} ({decimal_text})"


def reset_problem():
    b, c, a = generate_problem()
    st.session_state.b = b
    st.session_state.c = c
    st.session_state.a = a
    st.session_state.answer_text = ""
    st.session_state.answer_input = ""
    st.session_state.feedback_shown = False


if "b" not in st.session_state or "c" not in st.session_state or "a" not in st.session_state:
    reset_problem()


b = st.session_state.b
c = st.session_state.c
a = st.session_state.a
correct_fraction = correct_answer_fraction(a)
correct_value = float(correct_fraction)

light_mode = st.toggle(
    "Light mode",
    key="light_mode",
    help="Switch to a white background with dark text.",
)

st.markdown(
    f"""
    <style>
    .stApp {{
        {"background: #f6f8fc; color: #0f172a;" if light_mode else ""}
    }}
    .stApp [data-testid="block-container"] {{
        padding-top: 1.5rem;
        padding-bottom: 2rem;
    }}
    .helper-note {{
        font-size: 0.95rem;
        margin-top: 0.35rem;
        color: {"#475569" if light_mode else "#94a3b8"};
    }}
    .sidebar-byline {{
        text-align: center;
        font-size: 0.9rem;
        margin-top: 1.5rem;
        color: {"#475569" if light_mode else "#94a3b8"};
    }}
    .sidebar-byline a {{
        color: inherit;
        text-decoration: none;
        border-bottom: 1px solid currentColor;
    }}
    .sidebar-byline a:hover {{
        opacity: 0.8;
    }}
    .stApp [data-testid="stSidebar"] {{
        {"background: #eef2f7;" if light_mode else ""}
    }}
    .stApp [data-testid="stHeader"] {{
        {"background: rgba(246, 248, 252, 0.92);" if light_mode else ""}
    }}
    .stApp [data-testid="stAppViewContainer"] {{
        {"background: #f6f8fc;" if light_mode else ""}
    }}
    .stApp [data-testid="stAppViewContainer"] > .main {{
        {"background: #f6f8fc;" if light_mode else ""}
    }}
    .stApp [data-testid="stToolbar"] {{
        {"color: #0f172a;" if light_mode else ""}
    }}
    .stApp [data-testid="stSidebar"] *,
    .stApp [data-testid="stAppViewContainer"] h1,
    .stApp [data-testid="stAppViewContainer"] h2,
    .stApp [data-testid="stAppViewContainer"] h3,
    .stApp [data-testid="stAppViewContainer"] p,
    .stApp [data-testid="stAppViewContainer"] li,
    .stApp [data-testid="stAppViewContainer"] label,
    .stApp [data-testid="stAppViewContainer"] span,
    .stApp [data-testid="stAppViewContainer"] div {{
        {"color: #0f172a;" if light_mode else ""}
    }}
    .stApp [data-testid="stMarkdownContainer"] code {{
        {"background: #e2e8f0; color: #0f172a;" if light_mode else ""}
    }}
    .stApp div[data-baseweb="input"] {{
        {"background: #ffffff !important; border-radius: 0.5rem;" if light_mode else ""}
    }}
    .stApp div[data-baseweb="input"] > div {{
        {"background: #ffffff !important; border: 1px solid #cbd5e1 !important;" if light_mode else ""}
    }}
    .stApp .stTextInput input {{
        {"background-color: #ffffff !important; color: #0f172a !important; border: 1px solid #cbd5e1 !important;" if light_mode else ""}
    }}
    .stApp button,
    .stApp [data-testid="stBaseButton-secondary"],
    .stApp [data-testid="stBaseButton-primary"],
    .stApp [data-testid="stFormSubmitButton"] button {{
        {"background: #ffffff !important; color: #0f172a !important; border: 1px solid #cbd5e1 !important; box-shadow: none !important;" if light_mode else ""}
    }}
    .stApp button *,
    .stApp [data-testid="stBaseButton-secondary"] *,
    .stApp [data-testid="stBaseButton-primary"] *,
    .stApp [data-testid="stFormSubmitButton"] button * {{
        {"color: #0f172a !important; fill: #0f172a !important;" if light_mode else ""}
    }}
    .stApp button:hover,
    .stApp [data-testid="stBaseButton-secondary"]:hover,
    .stApp [data-testid="stBaseButton-primary"]:hover,
    .stApp [data-testid="stFormSubmitButton"] button:hover {{
        {"background: #e2e8f0 !important; color: #0f172a !important; border-color: #94a3b8 !important;" if light_mode else ""}
    }}
    .stApp button:focus,
    .stApp [data-testid="stBaseButton-secondary"]:focus,
    .stApp [data-testid="stBaseButton-primary"]:focus,
    .stApp [data-testid="stFormSubmitButton"] button:focus {{
        {"outline: none !important; box-shadow: 0 0 0 0.15rem rgba(148, 163, 184, 0.35) !important;" if light_mode else ""}
    }}
    .stApp div[data-testid="stExpander"] {{
        {"background: #ffffff; border: 1px solid #d9e2f2; border-radius: 12px;" if light_mode else ""}
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

st.caption("Student Practice")
st.title("Unlimited Limits", anchor=False)
st.write("Practice evaluating square-root limits involving rational expressions.")
st.subheader("Solve the limit:", anchor=False)

c_sign = f"+ {c}" if c >= 0 else f"- {abs(c)}"
b_sign = f"+ {b}" if b >= 0 else f"- {abs(b)}"
latex_problem = (
    r"\lim_{x \to -1} \sqrt{\dfrac{x + 1}{x^2 "
    + c_sign + r"x "
    + b_sign + r"}}"
)
st.latex(latex_problem)
st.markdown(
    f"""
    <div class="helper-note">
        Enter a simplified answer such as <code>1/3</code>, <code>0.333</code>, or <code>2</code>.
        Decimal answers should be rounded to {DECIMAL_PLACES} decimal places.
    </div>
    """,
    unsafe_allow_html=True,
)


with st.form("answer_form", clear_on_submit=True):
    user_input = st.text_input(
        "Your answer",
        placeholder="Type your answer here",
        key="answer_input",
    )
    left, right = st.columns(2)
    with left:
        submitted = st.form_submit_button("Check Answer", use_container_width=True)
    with right:
        new_problem = st.form_submit_button("New Problem", use_container_width=True)


if new_problem:
    reset_problem()
    st.rerun()


if submitted:
    st.session_state.answer_text = user_input
    st.session_state.feedback_shown = True


if st.session_state.feedback_shown:
    trimmed_answer = st.session_state.answer_text.strip()
    if not trimmed_answer:
        st.warning("Enter an answer first so the app can check your work.")
    else:
        parsed_answer = parse_answer(trimmed_answer)
        if parsed_answer is None:
            st.warning(
                f"I could not parse that answer. Try a fraction, decimal rounded to {DECIMAL_PLACES} places, or a plain number."
            )
        else:
            answer_format = classify_answer_format(trimmed_answer)
            if answer_format == "decimal":
                is_correct = abs(parsed_answer - correct_value) < DECIMAL_TOLERANCE
            else:
                is_correct = abs(parsed_answer - correct_value) < 1e-6
            if is_correct:
                st.success(f"Correct. The limit is {format_answer_display(correct_fraction)}.")
            else:
                st.error("Not quite. Try again if you want, or use the walkthrough below.")

            st.subheader("Solution walkthrough", anchor=False)

            c_minus_1 = c - 1
            cm1_sign = f"+ {c_minus_1}" if c_minus_1 >= 0 else f"- {abs(c_minus_1)}"

            st.markdown("**Step 1. Check the indeterminate form.**")
            st.latex(
                r"\frac{x+1}{x^2 " + c_sign + r"x " + b_sign + r"}\Bigg|_{x=-1} = \frac{0}{0}"
            )

            st.markdown("**Step 2. Factor the denominator.**")
            st.latex(
                r"x^2 " + c_sign + r"x " + b_sign + r" = (x+1)(x " + cm1_sign + r")"
            )

            st.markdown("**Step 3. Cancel the common factor.**")
            st.latex(
                r"\sqrt{\frac{x+1}{(x+1)(x " + cm1_sign + r")}}"
                r" = \sqrt{\frac{1}{x " + cm1_sign + r"}}"
            )

            st.markdown("**Step 4. Evaluate the simplified expression at x = -1.**")
            st.latex(
                r"\sqrt{\frac{1}{-1 + " + str(c_minus_1) + r"}}"
                + r" = \sqrt{\frac{1}{" + str(c - 2) + r"}}"
                + r" = \frac{1}{" + str(a) + r"}"
            )

            st.info(
                f"Final answer: {format_answer_display(correct_fraction)}."
            )


if st.session_state.feedback_shown:
    with st.expander("How to solve using L'Hopital's Rule (optional alternate method)"):
        st.markdown(
            """
            You can also work with the expression inside the square root:
            """
        )
        st.latex(r"\frac{x+1}{x^2 + " + str(c) + r"x + " + str(b) + r"}")
        st.markdown(
            """
            At `x = -1`, this is a `0/0` form, so L'Hopital's Rule applies to the inner fraction.
            Differentiate the numerator and denominator:
            """
        )
        st.latex(r"\frac{d}{dx}(x+1) = 1")
        st.latex(
            r"\frac{d}{dx}(x^2 + " + str(c) + r"x + " + str(b) + r") = 2x + " + str(c)
        )
        st.markdown("That gives:")
        st.latex(
            r"\lim_{x \to -1} \frac{x+1}{x^2 + "
            + str(c)
            + r"x + "
            + str(b)
            + r"} = \frac{1}{2(-1) + "
            + str(c)
            + r"} = \frac{1}{"
            + str(c - 2)
            + r"}"
        )
        st.markdown("Now put that result back under the square root:")
        st.latex(
            r"\sqrt{\frac{1}{" + str(c - 2) + r"}} = \frac{1}{" + str(a) + r"}"
        )
        st.markdown(f"Final answer: `{format_answer_display(correct_fraction)}`.")


with st.expander("How this app chooses valid problems"):
    st.markdown(
        """
        The denominator must equal zero at `x = -1`, which forces `b = c - 1`.
        That lets the denominator factor as `(x + 1)(x + c - 1)`.

        After canceling the common factor, the limit becomes:
        """
    )
    st.latex(r"\sqrt{\frac{1}{x + c - 1}}")
    st.markdown("To make the final answer equal to `1/a`, the value `c - 2` must be a perfect square.")


with st.sidebar:
    st.subheader("Quick help", anchor=False)
    st.markdown(
        f"""
        - Refreshing the page creates a new problem.
        - `New Problem` swaps in another random equation.
        - Submit your answer to check it and reveal the walkthrough.
        - Decimal answers should be rounded to {DECIMAL_PLACES} decimal places.
        """
    )
    st.markdown("---")
    st.markdown(
        f'<div class="sidebar-byline">Built by <a href="{LINKEDIN_URL}" target="_blank" rel="noopener noreferrer">{AUTHOR_NAME}</a></div>',
        unsafe_allow_html=True,
    )
