import streamlit as st


def ErrorToast(label: str, icon: str = "😵"):
    st.toast(label, icon=icon)


def WarningToast(label: str, icon: str = "⚠️"):
    st.toast(label, icon=icon)


def SuccessToast(label: str, icon: str = "✅"):
    st.toast(label, icon=icon)
