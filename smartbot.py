import streamlit as st
import sympy as sp
from sympy.parsing.sympy_parser import (
    parse_expr,
    standard_transformations,
    implicit_multiplication_application,
    convert_xor,
)
from sympy import SympifyError

# ...existing code...
st.set_page_config(page_title="SmartMath AI", page_icon="🤖", layout="centered")

st.title("🤖 SmartMath AI")
st.subheader("Universal Math Solver – from Kindergarten to Masters 🎓")

user_input = st.text_input("🧮 Enter your math question:")
level = st.selectbox(
    "🎓 Select Explanation Level:",
    ["Kindergarten", "School", "College / Masters"]
)

# parsing config (allows implicit multiplication like 2x and ^ as power)
TRANSFORMATIONS = standard_transformations + (
    implicit_multiplication_application,
    convert_xor,
)

def safe_parse(expr_str):
    if not expr_str or len(expr_str) > 400:
        raise ValueError("Expression empty or too long.")
    return parse_expr(expr_str, transformations=TRANSFORMATIONS, evaluate=True)

def solve_math(expression):
    try:
        # detect equation
        if "=" in expression:
            lhs_str, rhs_str = map(str.strip, expression.split("=", 1))
            lhs = safe_parse(lhs_str)
            rhs = safe_parse(rhs_str)
            eq = sp.Eq(lhs, rhs)
            # choose symbol(s) to solve for (prefer single symbol)
            syms = sorted(eq.free_symbols, key=lambda s: s.name)
            if not syms:
                # maybe numeric equality -> evaluate truth
                return f"✅ Result: {sp.simplify(eq)}"
            var = syms[0]
            sol = sp.solve(eq, var)
            return {"type": "equation", "var": var, "solution": sol, "eq": eq}
        # detect integration
        elif expression.lower().startswith(("integrate ", "∫")) or "integrate(" in expression.lower():
            # allow syntax: integrate(x**2, x) or integrate x^2 wrt x
            # try to split by comma if present
            if "," in expression:
                f_str, var_str = map(str.strip, expression.split(",", 1))
                f = safe_parse(f_str.replace("integrate", "", 1))
                var = safe_parse(var_str)
            else:
                # assume integrate <f> wrt x
                f = safe_parse(expression.replace("integrate", "", 1))
                var = list(f.free_symbols)
                var = var[0] if var else sp.Symbol("x")
            antider = sp.integrate(f, var)
            return {"type": "integral", "integrand": f, "var": var, "result": antider}
        # detect differentiation
        elif expression.lower().startswith(("differentiate ", "derivative ")) or "d/d" in expression.lower() or "diff(" in expression.lower():
            # common forms: diff(x**2, x) or differentiate x^2 wrt x
            if "," in expression:
                f_str, var_str = map(str.strip, expression.split(",", 1))
                f = safe_parse(f_str.replace("diff", "").replace("differentiate", ""))
                var = safe_parse(var_str)
            else:
                f = safe_parse(expression.replace("diff", "").replace("differentiate", "").replace("derivative", ""))
                syms = list(f.free_symbols)
                var = syms[0] if syms else sp.Symbol("x")
            deriv = sp.diff(f, var)
            return {"type": "derivative", "func": f, "var": var, "result": deriv}
        else:
            # try to simplify / evaluate expression
            expr = safe_parse(expression)
            simplified = sp.simplify(expr)
            # numeric evaluation if purely numeric
            if simplified.is_Number:
                return {"type": "number", "result": float(simplified)}
            return {"type": "simplify", "expr": expr, "result": simplified}
    except (SympifyError, ValueError) as e:
        return {"type": "error", "message": f"Could not parse expression: {e}"}
    except Exception as e:
        return {"type": "error", "message": f"Computation error: {e}"}

def explain_solution(original, result_obj, level):
    base = ""
    if result_obj["type"] == "equation":
        base = "We isolate the chosen variable and solve the resulting polynomial/transcendental equation."
    elif result_obj["type"] == "integral":
        base = "Find an antiderivative such that its derivative gives the integrand."
    elif result_obj["type"] == "derivative":
        base = "Apply power and chain/product/quotient rules to compute the rate of change."
    elif result_obj["type"] == "simplify":
        base = "We apply algebraic identities and simplification rules."
    elif result_obj["type"] == "number":
        base = "This is a numeric result after simplification."
    else:
        base = result_obj.get("message", "Unable to produce an explanation.")

    if level == "Kindergarten":
        return "🧸 Math is like balancing a seesaw — we move things so both sides are fair!"
    if level == "School":
        return "📘 " + base
    return "🎓 " + base

if user_input:
    res = solve_math(user_input)
    explanation = explain_solution(user_input, res, level)

    if res["type"] == "error":
        st.error(res["message"])
    elif res["type"] == "equation":
        st.success(f"✅ Solution for {res['var']}: {res['solution']}")
        st.latex(sp.latex(res["eq"]))
        st.info(explanation)
    elif res["type"] == "integral":
        st.success("✅ Integral computed")
        st.latex(r"\int " + sp.latex(res["integrand"]) + r"\,d" + sp.latex(res["var"]) + " = " + sp.latex(res["result"]))
        st.info(explanation)
    elif res["type"] == "derivative":
        st.success("✅ Derivative computed")
        st.latex("d/d" + sp.latex(res["var"]) + " " + sp.latex(res["func"]) + " = " + sp.latex(res["result"]))
        st.info(explanation)
    elif res["type"] == "simplify":
        st.success("✅ Simplified Expression:")
        st.latex(sp.latex(res["result"]))
        st.info(explanation)
    elif res["type"] == "number":
        st.success(f"✅ Result: {res['result']}")
        st.info(explanation)

st.markdown("---")
st.caption("Made by Muhammed Rabeeh — Science Exhibition 2025 ✨")
# ...existing code...
