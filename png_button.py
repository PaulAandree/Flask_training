import streamlit as st
import pandas as pd
import altair as alt
import altair_saver
import tempfile

# Your data
data = {
    'x': [1, 2, 3, 4, 5],
    'y': [5, 4, 3, 2, 1]
}

# Convert data to a Pandas DataFrame
df = pd.DataFrame(data)

# Your Altair chart code
chart = alt.Chart(df).mark_line().encode(
    x='x',
    y='y'
)

# Streamlit app code
st.altair_chart(chart)  # Display the Altair chart

# Save Altair chart as PNG
with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as f:
    altair_saver.save(chart, f.name)
    st.markdown(f"## Download Altair Chart as PNG")
    st.markdown(f'<a href="{f.name}" download>Click here to download the PNG file</a>', unsafe_allow_html=True)
