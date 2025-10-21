# SmartMath-AI
Smart Bot created to help solve complex math question from KG-1 to Masters
import streamlit as st
import sympy as sp
import openai
import os

# -------------------- CONFIG --------------------
st.set_page_config(page_title="SmartMath AI", page_icon="🤖", layout="centered")

# -------------------- APP HEADER --------------------
st.title("🤖 SmartMath AI")
st.subheader("Universal Math Solver – from Kindergarten to Masters 🎓")

st.markdown("""
Welcome to **SmartMath AI**, an intelligent assistant that solves and explains math
problems at any level.  
Type a question like:
- `solve 2x + 3 = 9`
- `integrate x^2 + 3x + 5`
- `differentiate sin(x) + x^3`
""")

# -------------------- INPUT SECTION --------------------
user_input = st.text_input("🧮 Enter your math question:")
level = st.selectbox(
    "🎓 Select Explanation Level:",
    ["Kindergarten", "School", "College / Masters"]
)

use_gpt = st.toggle("💬 Use AI (GPT) for Natural Explanations", value=False)

if use_gpt:
    openai.api_key = st.text_input("Enter your OpenAI API key:", type="password")

# -------------------- CORE MATH LOGIC --------------------
def solve_math(expression):
    try:
        # Try to parse and simplify expression
        expr = sp.sympify(expression)
        simplified = sp.simplify(expr)
        return f"✅ Simplified Expression: {simplified}"
    except Exception:
        # Try to solve equations
        try:
            lhs, rhs = expression.split("=")
            x = sp.symbols('x')
            sol = sp.solve(sp.Eq(sp.sympify(lhs), sp.sympify(rhs)), x)
            return f"✅ Solution: x = {sol}"
        except Exception as e:
            return f"⚠️ Error: Could not understand the question. {e}"

# -------------------- EXPLANATION LOGIC --------------------
def basic_explanation(expr, level):
    expr_lower = expr.lower()
    if "solve" in expr_lower or "=" in expr_lower:
        base = "We solve equations by isolating the variable, moving constants to the other side, and dividing by the coefficient."
    elif "integrate" in expr_lower:
        base = "Integration means finding the area under a curve. Increase the power by 1 and divide by the new power."
    elif "differentiate" in expr_lower or "derivative" in expr_lower:
        base = "Differentiation finds the rate of change. Multiply by the exponent and reduce the power by one."
    else:
        base = "We simplify the expression using standard algebraic rules."

    if level == "Kindergarten":
        return "🧸 Imagine a balance! We move numbers to keep it equal — that’s solving equations in a fun way!"
    elif level == "School":
        return "📘 School Level: " + base
    else:
        return "🎓 College Level: " + base + " It follows formal calculus and algebraic operations."

# -------------------- GPT EXPLANATION (OPTIONAL) --------------------
def gpt_explanation(expr, level, solution):
    try:
        prompt = f"Explain the following math solution for a {level} student:\n\nProblem: {expr}\nSolution: {solution}\n\nStep-by-step explanation:"
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": "You are a math tutor."},
                      {"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"⚠️ Could not generate AI explanation: {e}"

# -------------------- MAIN APP --------------------
if user_input:
    with st.spinner("🧠 Thinking..."):
        solution = solve_math(user_input)
        if use_gpt and openai.api_key:
            explanation = gpt_explanation(user_input, level, solution)
        else:
            explanation = basic_explanation(user_input, level)

    st.success(solution)
    st.info(explanation)

st.markdown("---")
st.caption("Made by **Muhammed Rabeeh** — College Science Exhibition 2025 ✨")
