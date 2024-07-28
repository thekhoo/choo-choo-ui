import streamlit as st


class Page:

    def __init__(
        self,
        is_login_page: bool = False,
        default_login_page: str = "pages/login.py",
        previous_page: str = "pages/home.py",
    ) -> None:
        self.default_login_page = default_login_page
        self.previous_page = previous_page

        if not is_login_page:
            self.return_to_login_if_not_authenticated()

        self.set_page_config()

    def set_page_config(self):
        st.set_page_config(
            page_title="Choo Choo Console",
            page_icon="🚄",
            layout="centered",
        )

    def render_footer(self):
        st.caption("Copyright of Christopher Khoo 2024 (khoojinnwei@gmail.com)")

    def return_to_login_if_not_authenticated(self):
        if (
            "authenticated" not in st.session_state
            or not st.session_state["authenticated"]
        ):
            st.switch_page(self.default_login_page)

    def render_back_button(self, clear_keys: list = []):
        go_back_button = st.button(
            label="< Back",
        )

        if go_back_button:
            # clear cached results
            for key in clear_keys:
                if key in st.session_state:
                    del st.session_state[key]

            st.switch_page(self.previous_page)
