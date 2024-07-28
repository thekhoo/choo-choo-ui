import hashlib
import hmac

import streamlit as st

from components.Page import Page


def hashed_password(username: str, password: str):
    return hashlib.md5(username.encode() + password.encode()).hexdigest()


def authenticate_user():
    if st.session_state["username"] in st.secrets["passwords"] and hmac.compare_digest(
        hashed_password(st.session_state["username"], st.session_state["password"]),
        st.secrets.passwords[st.session_state["username"]],
    ):
        st.session_state["authenticated"] = True
        del st.session_state["password"]
        del st.session_state["username"]
        st.toast("Authenticated", icon="✅")

    else:
        st.session_state["authenticated"] = False
        st.toast("Sorry, the username and/or password is incorrect", icon="💀")


class Login(Page):

    def __init__(self) -> None:
        super().__init__(is_login_page=True)

    def render(self):
        st.subheader("Welcome back, traveller.")

        st.text_input("Username", key="username")
        st.text_input("Password", key="password", type="password")

        login_button = st.button(
            "Login",
            use_container_width=True,
            on_click=authenticate_user,
            type="primary",
        )

        request_access = st.button(
            "Request Access to Choo Choo Console",
            use_container_width=True,
            type="secondary",
        )

        if "authenticated" in st.session_state and st.session_state["authenticated"]:
            st.switch_page("pages/home.py")

        self.render_footer()


if __name__ == "__main__":
    Login().render()
