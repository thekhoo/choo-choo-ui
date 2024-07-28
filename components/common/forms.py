from datetime import time
from enum import Enum
from typing import Callable, Optional

import streamlit as st


# base components
def TextInputField(
    label: str,
    placeholder: Optional[str] = None,
    max_chars: int = 256,
    help: Optional[str] = None,
    disabled: bool = False,
    value: Optional[str] = None,
    key: Optional[str] = None,
):
    return st.text_input(
        label=label,
        placeholder=placeholder,
        max_chars=max_chars,
        help=help,
        disabled=disabled,
        value=value,
        key=key,
    )


def DropdownInputField(
    label: str,
    dropdown_options: list,
    key: Optional[str] = None,
    help: Optional[str] = None,
    index: Optional[int] = None,
    format_func: Optional[Callable] = lambda s: None,
):
    return st.selectbox(
        label=label,
        options=dropdown_options,
        key=key,
        format_func=format_func,
        help=help,
        index=index,
    )


def SliderInputField(
    label: str,
    min_value: int | time,
    max_value: int | time,
    help: Optional[str] = None,
    step: Optional[int | time] = None,
    key: Optional[str] = None,
    value: Optional[int | time] = None,
):
    return st.slider(
        label=label,
        min_value=min_value,
        max_value=max_value,
        help=help,
        step=step,
        key=key,
        value=value,
    )


def DateInputField(
    label: str,
    help: Optional[str] = None,
    key: Optional[str] = None,
    value: Optional[str] = None,
):
    return st.date_input(label=label, help=help, key=key, value=value)
