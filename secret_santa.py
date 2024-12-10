import streamlit as st
import random

# List of participants
participants = ["Sadia", "Arafat", "Joy", "Fuad", "Sujana", "Marium"]

# Generate pairings
random.seed(42)
shuffled = participants[:]
while True:
    random.shuffle(shuffled)
    if all(p != s for p, s in zip(participants, shuffled)):
        break
assignments = dict(zip(participants, shuffled))

# Initialize session state
if "page" not in st.session_state:
    st.session_state.page = "welcome"
if "tip_selected" not in st.session_state:
    st.session_state.tip_selected = None
if "terms_accepted" not in st.session_state:
    st.session_state.terms_accepted = False
if "assignment_revealed" not in st.session_state:
    st.session_state.assignment_revealed = False  # Track if assignment is revealed
if "selected_name" not in st.session_state:
    st.session_state.selected_name = None  # Store the selected name

# Navigation function to handle page transitions
def go_to_page(page_name):
    st.session_state.page = page_name

# Page: Welcome Screen
if st.session_state.page == "welcome":
    st.title("Welcome to Secret Santa 🎅")
    st.write("Get ready for a fun and festive experience!")
    if st.button("Next"):
        go_to_page("credit_card")

# Page: Fake Credit Card Info with Tips
elif st.session_state.page == "credit_card":
    st.title("We Need Payment Information 🤑")
    st.write("To proceed, age tips de shala 😜")

    # Tips section
    st.subheader("Tips 💸")
    st.write("Please select a tip percentage to proceed:")

    # Tip buttons
    if st.button("15%"):
        st.session_state.tip_selected = "15%"
    if st.button("18%"):
        st.session_state.tip_selected = "18%"
    if st.button("25%"):
        st.session_state.tip_selected = "25%"
    if st.button("Ami Fokinni"):
        st.session_state.tip_selected = "Fokkinira tip deyna"

    # Display selected tip
    if st.session_state.tip_selected:
        st.success(f"Selected Tip: {st.session_state.tip_selected}")

    # Disabled credit card fields
    st.text_input("Enter your credit card number:", value="", disabled=True)
    st.text_input("Enter expiry date (MM/YY):", value="", disabled=True)
    st.text_input("Enter CVC:", value="", disabled=True)

    # "Next" button to move to the Secret Santa page
    if st.button("Next"):
        if st.session_state.tip_selected:
            go_to_page("secret_santa")
        else:
            st.warning("Please select a tip option to proceed!")

# Page: Secret Santa Assignment
elif st.session_state.page == "secret_santa":
    st.title("Secret Santa Assignment 🎄")

    # Show a message if the assignment has already been revealed
    if st.session_state.assignment_revealed:
        st.success(f"You are the Secret Santa for **{assignments[st.session_state.selected_name]}**! 🎁 Don't disappoint.")
        st.stop()  # Stop further interaction

    st.write("Here are the available names:")
    st.write(", ".join(participants))
    
    # Dropdown for name selection
    name = st.selectbox("Select your name from the list:", [""] + participants)
    
    # Terms and Conditions
    st.subheader("Terms and Conditions 🤓")
    st.write("""
    1. The gift must be **reasonable**— Eishob dollarama-r chocolate candy dile mair khabi. 💰
    2. If your gift sucks, gonodholai hobe. 
    3. Re-gifting last year's trash is strictly prohibited. 🙅‍♂️
    4. By clicking 'I Agree,' you pledge your undying loyalty to Secret Santa and agree to **not be a fokinni** as you were with tips. 🛍️
    """)
    
    # Checkbox to accept terms
    st.session_state.terms_accepted = st.checkbox("I agree to the above terms and conditions.")

    # Reveal the assignment
    if st.button("Reveal Your Assignment"):
        if not st.session_state.terms_accepted:
            st.error("You must accept the Terms and Conditions to proceed!")
        elif name in assignments:
            st.session_state.assignment_revealed = True  # Mark the assignment as revealed
            st.session_state.selected_name = name  # Store the selected name
            st.success(f"You are the Secret Santa for **{assignments[name]}**! 🎁 Don't disappoint.")
            st.stop()  # Stop further interaction after revealing the assignment
        else:
            st.error("Name not found! Please check your spelling or contact the organizer.")
