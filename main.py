import streamlit as st

# ────────────────────────────────────────────────
#   YOUR FUNCTION — define it here
# ────────────────────────────────────────────────
letter_to_number = {
    'A': 1, 'I': 1, 'J': 1, 'Q': 1, 'Y': 1, '1': 1, 'R': 2,
    'B': 2, 'K': 2, '2': 2, 'C': 3, 'S': 3, 'L': 3, 'G': 3,
    '3': 3, 'D': 4, 'M': 4, 'T': 4, '4': 4, 'E': 5, 'H': 5,
    'N': 5, 'X': 5, '5': 5, 'U': 6, 'V': 6, 'W': 6, '6': 6,
    'Z': 7, 'O': 7, '7': 7, 'P': 8, 'F': 8, '8': 8, '9': 9
}

def letter_sum(input_string):
    total_sum = 0
    for char in input_string.upper():  # Convert to uppercase to match dictionary keys
        if char.isalpha():  # Check if the character is a letter
            total_sum += letter_to_number.get(char, 0)  # Get the number from the dictionary, default to 0
        elif char.isdigit():
            total_sum += int(char)

    return total_sum


# ────────────────────────────────────────────────
#   App configuration & session state
# ────────────────────────────────────────────────
st.set_page_config(page_title="Numerology Calculator", layout="centered", initial_sidebar_state="collapsed")
st.markdown("""
    <style>
        .block-container {padding-top: 1.2rem !important;}
        .stApp > header {display: none !important;}
    </style>
""", unsafe_allow_html=True)

if "history" not in st.session_state:
    st.session_state.history = []


# ────────────────────────────────────────────────
#   UI
# ────────────────────────────────────────────────
st.title("Numerology Calculator")
st.caption("Name → Numerological Value")

# st.markdown("---")


st.markdown(
    """
    <style>
        div[data-testid="InputInstructions"] > span {
            visibility: hidden !important;
        }
        div[data-testid="InputInstructions"] > span:nth-child(1) {
            visibility: hidden !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)



# Main input

with st.form(key="calc_form", clear_on_submit=True):
    user_input = st.text_input(
        "Name to calculate:",
        value="",
        placeholder="Type here...",
        help="Enter a name to calculate its numerology value.",
        key="input_field"
    )

    submit_button = st.form_submit_button(
        "Calculate",
        type="primary",
        use_container_width=True
    )

if submit_button:
    cleaned = user_input.strip()
    
    if not cleaned:
        st.warning("Please enter a string first.")
    else:
        with st.spinner("Working..."):
            try:
                result = letter_sum(cleaned)
                
                # Store in history
                st.session_state.history.append((cleaned, result))
                
                # Show result
                st.success(f"**{result}**")
                st.caption(f"for:  {cleaned!r}")
                
            except Exception as e:
                st.error(f"Error: {str(e)}")


# ────────────────────────────────────────────────
#   History
# ────────────────────────────────────────────────

if st.session_state.history:
    # st.markdown("---")
    st.subheader("History")
    
    # Prepare data with explicit S. No. (1 = most recent)
    history_rows = [
        {"S. No.": i + 1, "Input": inp, "Result": res}
        for i, (inp, res) in enumerate(reversed(st.session_state.history))
    ]
    
    st.dataframe(
    history_rows,
    hide_index=True,
    use_container_width=True,
    column_config={
        "S. No.": st.column_config.NumberColumn(
            "S. No.",
            width="small",          # ← narrowest – just enough for 1–2 digits + header
            format="%d"
        ),
        "Input": st.column_config.TextColumn(
            "Input",
            width="large",          # ← takes most of the space (good for longer strings)
        ),
        "Result": st.column_config.NumberColumn(
            "Result",
            width="medium",         # ← medium – enough for typical integers
            format="%d"
        )
    }
)

    # Small utility button
    if st.button("Clear history", use_container_width=False):
        st.session_state.history = []
        st.rerun()


# Footer
st.markdown("---")
st.caption("Simple numerology calculator • Session history only")