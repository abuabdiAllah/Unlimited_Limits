import ast
import math
import operator
import random
from fractions import Fraction

import streamlit as st


st.set_page_config(page_title="Unlimited Limits", page_icon="UL", layout="centered")


SAFE_BINARY_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
}

SAFE_UNARY_OPS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

SAFE_FUNCTIONS = {
    "sqrt": math.sqrt,
}


def find_valid_bc_pairs(max_a=7):
    """Return valid (b, c, a) triples where the limit simplifies to 1/a."""
    valid = []
    for a in range(1, max_a + 1):
        c = a * a + 2
        b = c - 1
        valid.append((b, c, a))
    return valid


def generate_problem():
    """Pick a random valid (b, c, a) triple."""
    return random.choice(find_valid_bc_pairs())


def evaluate_numeric_expression(expression):
    """Safely evaluate simple numeric expressions such as 1/3 or sqrt(1/9)."""
    normalized = expression.strip().replace("^", "**")
    if not normalized:
        raise ValueError("Empty expression")

    node = ast.parse(normalized, mode="eval")

    def _eval(current):
        if isinstance(current, ast.Expression):
            return _eval(current.body)
        if isinstance(current, ast.Constant) and isinstance(current.value, (int, float)):
            return float(current.value)
        if isinstance(current, ast.BinOp) and type(current.op) in SAFE_BINARY_OPS:
            left = _eval(current.left)
            right = _eval(current.right)
            return SAFE_BINARY_OPS[type(current.op)](left, right)
        if isinstance(current, ast.UnaryOp) and type(current.op) in SAFE_UNARY_OPS:
            return SAFE_UNARY_OPS[type(current.op)](_eval(current.operand))
        if isinstance(current, ast.Call) and isinstance(current.func, ast.Name):
            func_name = current.func.id
            if func_name not in SAFE_FUNCTIONS or len(current.args) != 1:
                raise ValueError("Unsupported function")
            return SAFE_FUNCTIONS[func_name](_eval(current.args[0]))
        raise ValueError("Unsupported expression")

    value = _eval(node)
    if not math.isfinite(value):
        raise ValueError("Non-finite value")
    return value


def parse_answer(answer_text):
    """Parse user input into a numeric value."""
    try:
        return evaluate_numeric_expression(answer_text)
    except (SyntaxError, ValueError, ZeroDivisionError, OverflowError):
        return None


def correct_answer_fraction(a):
    return Fraction(1, a)


def format_fraction(value):
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def reset_problem():
    b, c, a = generate_problem()
    st.session_state.b = b
    st.session_state.c = c
    st.session_state.a = a
    st.session_state.answer_text = ""
    st.session_state.feedback_shown = False


if "b" not in st.session_state or "c" not in st.session_state or "a" not in st.session_state:
    reset_problem()


b = st.session_state.b
c = st.session_state.c
a = st.session_state.a
correct_fraction = correct_answer_fraction(a)
correct_value = float(correct_fraction)


st.markdown(
    """
    <style>
    .app-shell {
        max-width: 720px;
        margin: 0 auto;
        padding: 0.5rem 0 2rem 0;
    }
    .hero-card {
        background: linear-gradient(180deg, #f6f8fc 0%, #ffffff 100%);
        border: 1px solid #d9e2f2;
        border-radius: 20px;
        padding: 2rem 1.5rem;
        box-shadow: 0 18px 45px rgba(15, 23, 42, 0.08);
    }
    .eyebrow {
        color: #4b5563;
        font-size: 0.95rem;
        letter-spacing: 0.04em;
        text-transform: uppercase;
        margin-bottom: 0.35rem;
    }
    .hero-title {
        color: #0f172a;
        font-size: 2.35rem;
        font-weight: 700;
        margin-bottom: 0.35rem;
    }
    .hero-copy {
        color: #475569;
        font-size: 1.05rem;
        margin-bottom: 1.25rem;
    }
    .equation-label {
        color: #0f172a;
        font-size: 1.2rem;
        font-weight: 600;
        text-align: center;
        margin-top: 0.75rem;
    }
    .helper-note {
        color: #64748b;
        font-size: 0.95rem;
        text-align: center;
        margin-top: 0.75rem;
    }
    .section-title {
        color: #0f172a;
        font-size: 1.05rem;
        font-weight: 600;
        margin-bottom: 0.35rem;
    }
    </style>
    <div class="app-shell">
        <div class="hero-card">
            <div class="eyebrow">Student Practice</div>
            <div class="hero-title">Unlimited Limits</div>
            <div class="hero-copy">
                Practice evaluating square-root limits that simplify after factoring and cancellation.
            </div>
            <div class="equation-label">Solve the limit:</div>
    """,
    unsafe_allow_html=True,
)


c_sign = f"+ {c}" if c >= 0 else f"- {abs(c)}"
b_sign = f"+ {b}" if b >= 0 else f"- {abs(b)}"
latex_problem = (
    r"\lim_{x \to -1} \sqrt{\dfrac{x + 1}{x^2 "
    + c_sign + r"x "
    + b_sign + r"}}"
)
st.latex(latex_problem)
st.markdown(
    """
            <div class="helper-note">
                Enter a fraction, decimal, or simple numeric expression such as <code>1/3</code>,
                <code>0.5</code>, or <code>sqrt(1/9)</code>.
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


with st.form("answer_form", clear_on_submit=False):
    user_input = st.text_input(
        "Your answer",
        value=st.session_state.answer_text,
        placeholder="Type your answer here",
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
                "I could not parse that answer. Try a fraction, decimal, or simple numeric expression."
            )
        else:
            is_correct = abs(parsed_answer - correct_value) < 1e-6
            if is_correct:
                st.success(f"Correct. The limit is {format_fraction(correct_fraction)}.")
            else:
                st.error(
                    f"Not quite yet. Try again if you want, or use the walkthrough below. "
                    f"The correct limit is {format_fraction(correct_fraction)}."
                )

            st.markdown("### Solution walkthrough")

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
                f"Final answer: {format_fraction(correct_fraction)}. "
                f"Here, b = {b}, c = {c}, and c - 2 = {a}^2."
            )


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
    st.markdown("## Quick help")
    st.markdown(
        """
        - Refreshing the page creates a new problem.
        - `New Problem` swaps in another random equation.
        - Accepted answers: fractions, decimals, and simple numeric expressions.
        """
    )
    st.markdown("### Examples")
    st.code("1/3\n0.333333\nsqrt(1/9)")
