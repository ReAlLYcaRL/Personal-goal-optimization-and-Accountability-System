import streamlit as st

def show():
    st.header("Vision Board")
    st.write("Upload images or add motivational quotes for your goals.")
    uploaded_file = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"])
    quote = st.text_input("Add a motivational quote")

    if uploaded_file:
        st.image(uploaded_file, caption="Goal Image", use_column_width=True)
    if quote:
        st.success(f"Quote added: {quote}")