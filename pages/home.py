import streamlit as st

from components.Page import Page


class HomePage(Page):

    def __init__(self) -> None:
        super().__init__()

    def render(self):
        st.markdown(
            """
        # Choo Choo Service

        Welcome to the Choo Choo Console. In this area, you'll be able to:
        """
        )

        st.subheader("View Existing Journeys")

        btn_search_by_journey = st.button("Search by Journey")

        if btn_search_by_journey:
            st.switch_page("pages/search-journey.py")

        st.divider()

        st.subheader("Add New Journeys")
        btn_create_new_journey = st.button("Create new Journey")

        if btn_create_new_journey:
            st.switch_page("pages/create-journey.py")


if __name__ == "__main__":
    HomePage().render()
