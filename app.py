import streamlit as st
import sympy as sp

st.set_page_config(page_title="SmartMath AI", page_icon="🤖", layout="centered")

st.title("🤖 SmartMath AI")
st.subheader("Universal Math Solver – from Kindergarten to Masters 🎓")

user_input = st.text_input("🧮 Enter your math question:")
level = st.selectbox(
    "🎓 Select Explanation Level:",
    ["Kindergarten", "School", "College / Masters"]
)

def solve_math(expression):
    try:
        expr = sp.sympify(expression)
        simplified = sp.simplify(expr)
        return f"✅ Simplified Expression: {simplified}"
    except Exception:
        try:
            lhs, rhs = expression.split("=")
            x = sp.symbols('x')
            sol = sp.solve(sp.Eq(sp.sympify(lhs), sp.sympify(rhs)), x)
            return f"✅ Solution: x = {sol}"
        except Exception as e:
            return f"⚠️ Error: Could not understand the question. {e}"

def explain_solution(expr, level):
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
        return "🧸 Imagine a balance! We move numbers to keep it equal — solving equations in a fun way!"
    elif level == "School":
        return "📘 School Level: " + base
    else:
        return "🎓 College Level: " + base

if user_input:
    solution = solve_math(user_input)
    explanation = explain_solution(user_input, level)

    st.success(solution)
    st.info(explanation)

st.markdown("---")
st.caption("Made by Muhammed Rabeeh — Science Exhibition 2025 ✨")
