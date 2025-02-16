import streamlit as st
import random
import numpy as np
import plotly.graph_objects as go
from stack import STACK
import time

# Streamlit UI - Looks Like a Real Statistics Tool
st.set_page_config(page_title="Card Probability Analyzer", layout="centered")

# Ensure all session state variables are initialized
for key in ["page", "selected_rank", "selected_suit", "selected_card", "selected_position", "entered_number"]:
    if key not in st.session_state:
        st.session_state[key] = None  # Ensure no placeholders are shown before selection

# Function to move between pages
def go_to(page_name):
    st.session_state.page = page_name
    st.rerun()

### 🎴 PAGE 1: Card Selection ###
if st.session_state.page is None or st.session_state.page == "card_selection":
    st.title("Select Your Card")
    
    # --- Rank Selection Section ---
    st.write("### 1️⃣ Select a Rank")
    ranks = ['Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King']
    
    rank_cols = st.columns(7)
    for i, rank in enumerate(ranks[:7]):
        if rank_cols[i].button(rank, use_container_width=True, key=f"rank_{rank}"):
            st.session_state.selected_rank = rank

    rank_cols2 = st.columns(6)
    for i, rank in enumerate(ranks[7:]):
        if rank_cols2[i].button(rank, use_container_width=True, key=f"rank_{rank}"):
            st.session_state.selected_rank = rank

    # --- Suit Selection Section ---
    st.write("### 2️⃣ Select a Suit")
    suits = ['Spades', 'Hearts', 'Clubs', 'Diamonds']
    suit_cols = st.columns(4)

    for i, suit in enumerate(suits):
        if suit_cols[i].button(suit, use_container_width=True, key=f"suit_{suit}"):
            st.session_state.selected_suit = suit

    # Show the selected card properly formatted only after selection
    if st.session_state.selected_rank and st.session_state.selected_suit:
        selected_card = f"{st.session_state.selected_rank} of {st.session_state.selected_suit}"
        st.session_state.selected_card = selected_card
        st.subheader(f"Selected Card: **{selected_card}**")
        st.write("")  # Add spacing
        if st.button("Next", use_container_width=True):
            go_to("position_selection")  # Move to next page
    else:
        st.warning("Please select both a rank and a suit.")

### 🔢 PAGE 2: Position Selection (0-9 Number Entry) ###
elif st.session_state.page == "position_selection":
    st.title("Enter a Position")
    
    st.write("### 3️⃣ Construct a Number (1-52)")

    # Initialize entered number only when the page loads
    if "entered_number" not in st.session_state or st.session_state.entered_number is None:
        st.session_state.entered_number = ""

    # --- Number Entry Grid (0-9) ---
    num_cols = st.columns(10)
    for i in range(10):
        if num_cols[i].button(str(i), use_container_width=True, key=f"num_{i}"):
            st.session_state.entered_number += str(i)

    # Ensure a valid number is entered
    valid_number = None
    if st.session_state.entered_number:
        try:
            entered_number = int(st.session_state.entered_number)
            if 1 <= entered_number <= 52:
                valid_number = entered_number
                st.session_state.selected_position = entered_number
            else:
                st.session_state.entered_number = ""  # Reset if invalid
                st.warning("Please enter a number between 1 and 52.")
        except ValueError:
            st.session_state.entered_number = ""  # Reset if not valid

    # Show selected position only if valid
    if valid_number:
        st.subheader(f"Selected Position: **#{valid_number}**")
        st.write("")  # Add spacing
        if st.button("Next", use_container_width=True):
            go_to("results")  # Move to results page
    else:
        st.warning("Please construct a valid number between 1 and 52.")

### 📊 PAGE 3: Results Page ###
elif st.session_state.page == "results":
    st.title("Card Probability Analysis")
    st.subheader("Here is the statistical analysis of your selection:")

    # --- Probability Calculation ---
    formatted_card = st.session_state.selected_card
    selected_position = st.session_state.selected_position

    if formatted_card in STACK:
        current_position = STACK.index(formatted_card) + 1
    else:
        st.error("Invalid card selection!")
        st.stop()

    # ✅ **Fix: Ensure "00" is shown when CP == NP**
    if current_position == selected_position:
        cut_number = "00"
    elif current_position > selected_position:
        cut_number = current_position - selected_position
    else:
        cut_number = 52 - (selected_position - current_position)

    # Generate Fake Probability Data
    sample_size = random.randint(100000, 200000)
    card_probability = random.randint(50, 150)
    position_probability = random.randint(50, 150)
    combined_probability = (card_probability * position_probability) // 100 * 100 + int(cut_number)

    # Display Fake Results
    st.success(f"Statistical analysis complete.")
    st.info(f"Estimated probability of **{formatted_card}** appearing at position **#{selected_position}** is **1 in {combined_probability}** based on a sample size of {sample_size}.")

    # --- Generate a More Realistic Probability Distribution ---
    x_positions = np.arange(1, 53)  # 1-52 deck positions
    y_probabilities = np.random.normal(loc=10, scale=5, size=52).clip(1, 25)  # Normal distribution for realism

    # Highlight the spectator's selected position (red)
    y_probabilities[selected_position - 1] = 50  

    # --- Create an Interactive Graph Using Plotly ---
    fig = go.Figure()

    for i in range(52):
        color = 'red' if i == selected_position - 1 else 'blue'
        fig.add_trace(go.Bar(
            x=[x_positions[i]],
            y=[y_probabilities[i]],
            marker_color=color,
            hovertext=f"Position {i+1}, Probability: {y_probabilities[i]:.2f}%",
            name=f"Position {i+1}"
        ))

    fig.update_layout(
        title="Probability Distribution",
        xaxis_title="Position in Deck",
        yaxis_title="Probability (%)",
        showlegend=False
    )

    # Display the interactive plot
    st.plotly_chart(fig)

    # Restart the analysis
    if st.button("Perform Another Analysis", use_container_width=True):
        go_to("card_selection")
