import streamlit as st
import asyncio
from trip_planner import main as plan_trip

# Page config
st.set_page_config(
    page_title="AI Trip Planner",
    page_icon="✈️",
    layout="wide"
)

st.title("✈️ AI Trip Planner")
st.markdown("Plan your perfect trip using AI agents!")

# Create a form for user input
with st.form("trip_planner_form"):
    prompt = st.text_area(
        "Describe your trip:",
        placeholder="e.g., 4 day trip to Malaysia with a budget of $400, give me a day by day breakdown?",
        height=100
    )
    
    submitted = st.form_submit_button("Plan My Trip", use_container_width=True)

if submitted:
    if not prompt.strip():
        st.error("Please enter a trip description!")
    else:
        try:
            with st.spinner("🤔 Planning your trip..."):
                # Run the async function
                result = asyncio.run(plan_trip(prompt))
            
            st.success("Trip planned successfully!")
            st.markdown("### Your Trip Plan:")
            st.markdown(result)
            
        except Exception as e:
            st.error(f"Error planning trip: {str(e)}")
            st.write("Make sure you have the required agents configured in the notebook.")
