import streamlit as st
from calc_core import eval_expr
import urllib.parse

st.set_page_config(page_title="Kawaii Calculator", layout="centered")

if "expr" not in st.session_state:
    st.session_state.expr = ""
if "result" not in st.session_state:
    st.session_state.result = ""
if "deg_mode" not in st.session_state:
    st.session_state.deg_mode = False

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400..900&display=swap');
                        
.stApp {
    background-color: #f3e8ff;
    max-width: 480px;       
    margin: auto;
}
            

div[data-testid="stButton"] button {
    width: 100%;
    max-width: 70px;
    min-width: 50px;        
    aspect-ratio: 1 / 1;
    border-radius: 50%;
    border: 1px solid #4b0082;
    background-color: #e9d5ff;
    font-size: 1.1rem;
    font-weight: 600;
}
    
div[data-testid="stButton"] button:hover {
    background-color: #d8b4fe;
}

/* Special style for = button */
div[data-testid="stButton"][key="btn_%3D"] button {
    background-color: #f9a8d4 !important;
    color: white;
}
div[data-testid="stButton"][key="btn_%2B"] button,
div[data-testid="stButton"][key="btn_%2D"] button,
div[data-testid="stButton"][key="btn_%2A"] button,
div[data-testid="stButton"][key="btn_%2F"] button,
div[data-testid="stButton"][key="btn_%3D"] button {
    font-weight: 700;
    color: black;
}

div[data-testid="stButton"][key="btn_%E2%8C%AB"] button, /* ⌫ */
div[data-testid="stButton"][key="btn_CE"] button {
    height: 130px;  /* taller button */
    writing-mode: vertical-rl;
    font-size: 16px;
}

div[data-testid="stButton"][key="btn_eq_side"] button {
    height: 195px;
    width: 100%;
    border-radius: 20px;
    background-color: #f9a8d4 !important;
    color: white !important;
    font-size: 22px;
    font-weight: bold;
}
             
/* Display box with wrapping */
.display {
    background-color: white;
    color: black;
    font-size: 20px;
    padding: 12px 16px;
    border-radius: 10px;
    font-family: 'Courier New', monospace;
    text-align: right;
    word-wrap: break-word;
    overflow-wrap: break-word;
    max-width: 100%;
    margin-bottom: 10px;
}
            
                        
.calc-display {
    background-color: white;
    border-radius: 10px;
    padding: 12px 16px;
    font-family: "Orbitron", sans-serif;
    text-align: right;
    margin-bottom: 10px;
    max-width: 100%;
    word-wrap: break-word;
    overflow-wrap: break-word;
}

.calc-input {
    font-size: 20px;
    color: #333;
    font-weight: 400;
}

.calc-output {
    font-size: 32px;
    font-weight: 700;
    color: black;
    margin-top: 4px;
}
            
/* Responsive Grid */

div[data-testid="stButton"] button {
    background-color: #e9d5ff;
    color: black;
    border: 2px solid #4b0082;
    border-radius: 50%;
    aspect-ratio: 1 / 1;
    font-weight: 600;
    font-size: 1.2em;
    width: 100%;
    max-width: 60px;
    min-width: 40px;
    flex: 1;
    transition: all 0.2s ease;
}
</style>
""", unsafe_allow_html=True)

def render_button(label):
    btn = st.button(label, key=label, help=label)
    if btn:
        handle_input(label)

# i/o Handling 
def handle_input(val):
    expr = st.session_state.expr

    if val in {"AC", "CE"}:
        st.session_state.expr = ""
        st.session_state.result = ""

    elif val == "=" or val == "＝":
        result = eval_expr(expr)
        st.session_state.result = "Error" if result.startswith("Error") else result

    elif val == "π":
        st.session_state.expr += "pi"

    elif val == "√x":
        st.session_state.expr += "sqrt("

    elif val == "∛x":
        st.session_state.expr += "root(3,"

    elif val == "xʸ":
        st.session_state.expr += "**"

    elif val == "log":
        st.session_state.expr += "log("

    elif val == "±":
        if expr:
            st.session_state.expr = f"-({expr})"

    elif val == "%":
        st.session_state.expr += "%"

    elif val in {"sin", "cos", "tan"}:
            st.session_state.expr += f"{val}("

    elif val in {"＋", "+"}:
        st.session_state.expr += "+"

    elif val in {"−", "-"}:
        st.session_state.expr += "-"

    elif val == "⌫":
        st.session_state.expr = expr[:-1]

    elif val == "÷":
        st.session_state.expr += "/"

    elif val == "×":
        st.session_state.expr += "*"

    else:
        st.session_state.expr += val

    st.rerun()

st.markdown(f"""
<div class="calc-display">
  <div class="calc-input">{st.session_state.expr or "0"}</div>
  <div class="calc-output">{'= ' + str(st.session_state.result) if st.session_state.result else ''}</div>
</div>
""", unsafe_allow_html=True)

button_rows = [
    ["CE", "sin","cos", "tan", "⌫"],
    ["log", "xʸ", "√x", "∛x", "%"],
    ["7", "8", "9","(", ")"],
    ["4", "5", "6", "÷", "−"],
    ["1", "2", "3", "×", "＋"],
    ["±", "0", ".","π", "＝"]]

for row in button_rows:
    cols = st.columns(len(row))
    for i, label in enumerate(row):
        with cols[i]:
            if label.strip():
                safe_key = f"btn_{urllib.parse.quote(label)}"
                if st.button(label, key=safe_key):
                    handle_input(label)
