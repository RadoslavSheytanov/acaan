import streamlit as st
import random
import numpy as np
import plotly.graph_objects as go
from stack import STACK
import time

# Streamlit UI - Looks Like a Real Statistics Tool
st.set_page_config(page_title="Card Probability Analyzer", layout="centered")

# Ensure all session state variables are initialized
for key in ["page", "selected_card", "selected_position", "combined_probability", "sample_size", "loading"]:
    if key not in st.session_state:
        st.session_state[key] = None

def go_to_results():
    st.session_state.page = "loading"
    st.rerun()  # Forces the UI to refresh instantly

if st.session_state.page == "input" or st.session_state.page is None:
    # Input Page
    st.title("Card Stats Calculator")
    st.subheader("Probability Analysis of Playing Card Placement")

    # User Input for Card Selection
    ranks = ['Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King']
    suits = ['Spades', 'Hearts', 'Clubs', 'Diamonds']

    selected_rank = st.selectbox("Select Rank", ranks)
    selected_suit = st.selectbox("Select Suit", suits)
    formatted_card = f"{selected_rank} of {selected_suit}"  # Convert to correct format

    # User Input for Position Selection (use session state safely)
    if st.session_state.selected_position is None:
        st.session_state.selected_position = 1  # Default to 1

    selected_position = st.number_input("Enter Position (1-52)", min_value=1, max_value=52, step=1, value=st.session_state.selected_position)

    # 🚨 Extra Safety Check: If somehow an invalid position is still entered, block calculations
    if selected_position > 52:
        st.error("Invalid position! The deck consists of 52 cards. Please enter a number between 1 and 52.")
        st.stop()  # 🚨 This stops execution and prevents calculations

    if st.button("Analyze"):
        # Save selected values safely before navigating
        st.session_state.selected_card = formatted_card
        st.session_state.selected_position = selected_position

        # Check if the selected card is in the hardcoded stack
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

        # Generate Realistic Probability Distribution
        sample_size = random.randint(100000, 200000)
        card_probability = random.randint(50, 150)
        position_probability = random.randint(50, 150)
        combined_probability = (card_probability * position_probability) // 100 * 100 + int(cut_number)

        # Save computed values to session state
        st.session_state.combined_probability = combined_probability
        st.session_state.sample_size = sample_size

        go_to_results()

elif st.session_state.page == "loading":
    # Show Loading Indicator
    st.title("Processing Data...")
    st.subheader("Please wait while we calculate the probability statistics.")

    # Simulate processing time (realistically could be a short delay)
    with st.spinner("Analyzing..."):
        time.sleep(2)  # Simulate loading time

    # Move to results page after loading
    st.session_state.page = "results"
    st.rerun()

elif st.session_state.page == "results":
    # Results Page
    st.title("Card Probability Analysis")
    st.subheader("Here is the statistical analysis of your selection:")

    # Display Fake Results
    st.success(f"Statistical analysis complete.")
    st.info(f"Estimated probability of **{st.session_state.selected_card}** appearing at position **#{st.session_state.selected_position}** is **1 in {st.session_state.combined_probability}**.")

    # --- Generate a More Realistic Probability Distribution ---
    x_positions = np.arange(1, 53)  # 1-52 deck positions
    y_probabilities = np.random.normal(loc=10, scale=5, size=52).clip(1, 25)  # Normal distribution for realism

    # Highlight the spectator's selected position (red)
    y_probabilities[st.session_state.selected_position - 1] = 50  

    # --- Create an Interactive Graph Using Plotly ---
    fig = go.Figure()

    for i in range(52):
        color = 'red' if i == st.session_state.selected_position - 1 else 'blue'
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

    # Button to restart the analysis
    if st.button("Perform Another Analysis"):
        st.session_state.page = "input"
        st.rerun()
