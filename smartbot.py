import streamlit as st
import sympy as sp

st.set_page_config(page_title="SmartMath AI", page_icon="🤖", layout="centered")
st.title("🤖 SmartMath AI")
st.subheader("Offline Math Solver — Equations, Word Problems, and Puzzles (Class 10)")

# Input
user_input = st.text_input("🧮 Enter your math question:")
level = st.selectbox("🎓 Explanation Level:", ["Kindergarten", "School", "College / Masters"])

# --------------------- PRELOADED 25 CLASS 10 QUESTIONS ---------------------
word_problems = {
    "eight 8": {
        "solution": "888 + 88 + 8 + 8 + 8 = 1000",
        "explanation": "Step-by-step:\n1. Start with 888\n2. Add 88 → 976\n3. Add 8 → 984\n4. Add 8 → 992\n5. Add 8 → 1000"
    },
    "sum of first 10 natural numbers": {
        "solution": "1 + 2 + ... + 10 = 55",
        "explanation": "Use formula n(n+1)/2 → 10*11/2 = 55"
    },
    "pythagorean triplet": {
        "solution": "3² + 4² = 5²",
        "explanation": "Check 3*3 + 4*4 = 9+16=25=5*5"
    },
    "area of triangle": {
        "solution": "Area = 1/2 * base * height",
        "explanation": "Multiply base and height and divide by 2"
    },
    "simple interest": {
        "solution": "SI = P * R * T / 100",
        "explanation": "Multiply principal, rate, and time, then divide by 100"
    },
    "perimeter of square": {
        "solution": "Perimeter = 4 * side",
        "explanation": "Add all sides: 4 times the length of one side"
    },
    "average of numbers": {
        "solution": "Average = sum of numbers / count",
        "explanation": "Add numbers and divide by total count"
    },
    "factorial of 5": {
        "solution": "5! = 120",
        "explanation": "5*4*3*2*1 = 120"
    },
    "sum of angles in triangle": {
        "solution": "180 degrees",
        "explanation": "Sum of interior angles of a triangle = 180"
    },
    "ratio problem": {
        "solution": "Divide quantities in given ratio",
        "explanation": "Use formula: part = (ratio * total)/sum of ratio parts"
    },
    "average marks problem": {
        "solution": "Average = Total marks / Number of students",
        "explanation": "Add marks and divide by number of students"
    },
    "work and time problem": {
        "solution": "Work = Rate * Time",
        "explanation": "Multiply rate of work by time to get total work"
    },
    "speed distance time": {
        "solution": "Speed = Distance / Time",
        "explanation": "Divide distance by time"
    },
    "compound interest": {
        "solution": "A = P*(1 + R/100)^T",
        "explanation": "Use formula to calculate compound interest"
    },
    "sum of squares": {
        "solution": "1²+2²+...+n² = n(n+1)(2n+1)/6",
        "explanation": "Use the formula for sum of squares"
    },
    "quadratic equation": {
        "solution": "x² - 5x + 6 = 0 → x = 2, 3",
        "explanation": "Factorize the equation: (x-2)(x-3)=0"
    },
    "simultaneous equations": {
        "solution": "x + y = 5, x - y = 1 → x=3, y=2",
        "explanation": "Solve two equations using elimination or substitution"
    },
    "profit and loss": {
        "solution": "Profit = Selling Price - Cost Price",
        "explanation": "Subtract cost from selling price"
    },
    "perimeter of rectangle": {
        "solution": "2*(length + breadth)",
        "explanation": "Add length and breadth, multiply by 2"
    },
    "area of circle": {
        "solution": "π * radius²",
        "explanation": "Multiply pi by radius squared"
    },
    "circumference of circle": {
        "solution": "2 * π * radius",
        "explanation": "Multiply 2, pi, and radius"
    },
    "simple riddle": {
        "solution": "9 + 1 = 10 using digits",
        "explanation": "Arrange numbers to make correct sum"
    },
    "percentage problem": {
        "solution": "Percentage = (part/total)*100",
        "explanation": "Divide part by total and multiply by 100"
    },
    "volume of cube": {
        "solution": "side³",
        "explanation": "Multiply side length by itself 3 times"
    },
    "surface area of cube": {
        "solution": "6 * side²",
        "explanation": "6 faces, each with area side²"
    },
    "speed ratio problem": {
        "solution": "Speed ratio = Distance1/Time1 : Distance2/Time2",
        "explanation": "Calculate each speed and form ratio"
    }
}

def solve_word_problem(question):
    q = question.lower()
    for key in word_problems:
        if key in q:
            return word_problems[key]["solution"], word_problems[key]["explanation"]
    return None, None

# --------------------- SOLVE EQUATIONS & EXPRESSIONS ---------------------
def solve_math(expr):
    try:
        simplified = sp.simplify(expr)
        return f"✅ Simplified Expression: {simplified}"
    except Exception:
        try:
            lhs, rhs = expr.split("=")
            x = sp.symbols('x')
            sol = sp.solve(sp.Eq(sp.sympify(lhs), sp.sympify(rhs)), x)
            return f"✅ Solution: x = {sol}"
        except Exception:
            return None

# --------------------- EXPLANATION ---------------------
def explain_solution(expr, level):
    if level == "Kindergarten":
        return "🧸 Easy Explain: Imagine a balance! Move numbers to keep it equal."
    elif level == "School":
        return "📘 School Explain: Apply simple math rules step by step."
    else:
        return "🎓 College Explain: Use algebraic or calculus rules systematically."

# --------------------- MAIN ---------------------
if user_input:
    sol_text, expl_text = solve_word_problem(user_input)
    if sol_text:
        st.success(sol_text)
        st.info(expl_text)
    else:
        sol = solve_math(user_input)
        if sol:
            st.success(sol)
            st.info(explain_solution(user_input, level))
        else:
            st.warning("⚠️ Could not solve this problem. Try a different question.")

st.markdown("---")
st.caption("Made by Muhammed Rabeeh Fysal and Alex Jacob Shaiju — Science Exhibition 2025 ✨")
