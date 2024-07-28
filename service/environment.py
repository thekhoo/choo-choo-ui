from enum import Enum

import streamlit as st


def is_authenticated():
    return "authenticated" in st.session_state and st.session_state["authenticated"]


def get_db_credentials():
    return {
        "host": st.secrets.db["host"],
        "user": st.secrets.db["user"],
        "port": int(st.secrets.db["port"]),
        "password": st.secrets.db["password"],
        "database": st.secrets.db["database"],
    }


def get_search_cache_key(key: str):
    return f"searchCache__{key}"


def get_search_cache_value(key: str, default=None):
    return st.session_state.get(get_search_cache_key(key), default)


def set_search_cache_state_value(key: str, value):
    st.session_state[get_search_cache_key(key)] = value


class JourneyFormFieldKey(str, Enum):

    NOTIFICATION_GLOBAL_ID = "notificationGlobalId"
    DESCRIPTION = "description"
    DEPARTURE_STN = "departureStn"
    ARRIVAL_STN = "arriveStn"
    START_NOTI_TIME = "startNotiTime"
    END_NOTI_TIME = "endNotiTime"
    TRAIN_DEP_TIME = "trainDepTime"
    NUM_TRAINS = "numTrains"
    EXPIRES_AT = "expiresAt"
    NOTIFICATION_CHANNEL = "notificationChannel"
    COMPANY = "company"
    WEBHOOK = "webhook"
    CHAT_ID = "chatId"
    USE_FANCY_GREETING_MESSAGE = "useFancyGreetingMessage"

    # special case for DaySelection Field
    MONDAY = "useMonday"
    TUESDAY = "useTuesday"
    WEDNESDAY = "useWednesday"
    THURSDAY = "useThursday"
    FRIDAY = "useFriday"
    SATURDAY = "useSaturday"
    SUNDAY = "useSunday"


def get_journey_form_state_key(key: str):
    return f"journeyform__{key}"


def set_journey_form_state_value(key: str, value):
    st.session_state[get_journey_form_state_key(key)] = value


def get_journey_form_state_value(key: str, default=None):
    return st.session_state.get(get_journey_form_state_key(key), default)
