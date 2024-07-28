import streamlit as st

from pages.login import Login


def main():
    st.set_page_config(
        page_title="Choo Choo Console",
        page_icon="🚄",
        layout="centered",
    )

    if "authenticated" not in st.session_state or not st.session_state["authenticated"]:
        st.switch_page("pages/login.py")

    else:
        st.switch_page("pages/home.py")


if __name__ == "__main__":
    main()
