import calendar
from datetime import date, time

import streamlit as st

from components.common.toasts import SuccessToast
from service.constants import NotificationChannel, Station
from service.environment import (
    JourneyFormFieldKey,
    get_db_credentials,
    get_search_cache_key,
    get_search_cache_value,
    set_journey_form_state_value,
)
from service.sql import ChooChooDatabase
from service.types import TrainNotifyRequest


# helper components
def TrainJourneyHeader(
    dep_stn: Station, arr_stn: Station, schedule_id: str, description: str
):
    st.subheader(f"🚄 {dep_stn.value} > {arr_stn.value}")
    st.caption(f"{schedule_id} | {description}")


def TrainJourneyInfoDropdownTextGroup(caption: str, text: str):
    st.caption(caption)
    st.write(text)


def TrainJourneyInfoDropdown(
    start_noti_time: time,
    end_noti_time: time,
    train_departure_time: time,
    number_of_trains: str,
    days_to_notify: str,
    notification_channel: NotificationChannel,
    chat_id: str,
):
    with st.expander("Additional Details"):
        left_col, right_col = st.columns(2)
        with left_col:
            TrainJourneyInfoDropdownTextGroup(
                "Train Departure Time", train_departure_time.strftime("%I:%M %p")
            )

            TrainJourneyInfoDropdownTextGroup("Days to Notify", days_to_notify)

            TrainJourneyInfoDropdownTextGroup(
                "Notification Channel", notification_channel.value.capitalize()
            )

        with right_col:
            TrainJourneyInfoDropdownTextGroup(
                "Notification Timings",
                f"{start_noti_time.strftime('%I:%M %p')} - {end_noti_time.strftime('%I:%M %p')}",
            )

            TrainJourneyInfoDropdownTextGroup(
                "Number of Trains",
                f"{number_of_trains} train" + "s" if number_of_trains != 1 else "",
            )

            TrainJourneyInfoDropdownTextGroup("Chat ID", str(chat_id))


def edit_journey(
    notification_global_id: str,
    description: str,
    dep_stn: str,
    arr_stn: str,
    noti_start_time: time,
    noti_end_time: time,
    train_dep_time: time,
    number_of_trains: int,
    expires_at: date,
    days_to_notify_str: str,
    notification_channel: str,
    chat_id: str,
    use_fancy_greeting_message: bool,
):
    # save journey to cache
    set_journey_form_state_value(
        JourneyFormFieldKey.NOTIFICATION_GLOBAL_ID, notification_global_id
    )
    set_journey_form_state_value(JourneyFormFieldKey.DESCRIPTION, description)
    set_journey_form_state_value(JourneyFormFieldKey.DEPARTURE_STN, dep_stn)
    set_journey_form_state_value(JourneyFormFieldKey.ARRIVAL_STN, arr_stn)
    set_journey_form_state_value(JourneyFormFieldKey.START_NOTI_TIME, noti_start_time)
    set_journey_form_state_value(JourneyFormFieldKey.END_NOTI_TIME, noti_end_time)
    set_journey_form_state_value(JourneyFormFieldKey.TRAIN_DEP_TIME, train_dep_time)
    set_journey_form_state_value(JourneyFormFieldKey.NUM_TRAINS, number_of_trains)
    set_journey_form_state_value(JourneyFormFieldKey.EXPIRES_AT, expires_at)

    # days to notify tuple
    set_journey_form_state_value(
        JourneyFormFieldKey.MONDAY,
        calendar.day_name[calendar.MONDAY] in days_to_notify_str,
    )
    set_journey_form_state_value(
        JourneyFormFieldKey.TUESDAY,
        calendar.day_name[calendar.TUESDAY] in days_to_notify_str,
    )
    set_journey_form_state_value(
        JourneyFormFieldKey.WEDNESDAY,
        calendar.day_name[calendar.WEDNESDAY] in days_to_notify_str,
    )
    set_journey_form_state_value(
        JourneyFormFieldKey.THURSDAY,
        calendar.day_name[calendar.THURSDAY] in days_to_notify_str,
    )
    set_journey_form_state_value(
        JourneyFormFieldKey.FRIDAY,
        calendar.day_name[calendar.FRIDAY] in days_to_notify_str,
    )
    set_journey_form_state_value(
        JourneyFormFieldKey.SATURDAY,
        calendar.day_name[calendar.SATURDAY] in days_to_notify_str,
    )
    set_journey_form_state_value(
        JourneyFormFieldKey.SUNDAY,
        calendar.day_name[calendar.SUNDAY] in days_to_notify_str,
    )

    # notification_channels
    set_journey_form_state_value(
        JourneyFormFieldKey.NOTIFICATION_CHANNEL, notification_channel
    )
    set_journey_form_state_value(JourneyFormFieldKey.CHAT_ID, chat_id)
    set_journey_form_state_value(
        JourneyFormFieldKey.USE_FANCY_GREETING_MESSAGE, use_fancy_greeting_message
    )

    # change page
    st.switch_page("pages/edit-journey.py")


def delete_journey(notification_global_id: str):
    db = ChooChooDatabase(**get_db_credentials())
    db.soft_delete_schedule_by_id(notification_global_id)
    SuccessToast("Nuked!")


def Journey(idx: int, train_journey: TrainNotifyRequest):

    with st.container():
        dep_stn: Station = train_journey.get("departure_station", None)
        arr_stn: Station = train_journey.get("arrival_station", None)
        schedule_id: str = train_journey.get("notification_schedule_global_id", None)
        description: str = train_journey.get("description", None)

        start_noti_time: time = train_journey.get("start_notification_time", None)
        end_noti_time: time = train_journey.get("end_notification_time", None)
        train_departure_time: time = train_journey.get("train_departure_time")
        expires_at: date = train_journey.get("expires_at")
        number_of_trains = train_journey.get("number_of_trains")
        days_to_notify = ", ".join(
            calendar.day_name[day - 1] for day in train_journey.get("days_to_notify")
        )
        notification_channel = train_journey.get("notification_channel")
        chat_id = train_journey.get("chat_id")
        use_fancy_greeting_message = train_journey.get("use_fancy_greeting_message")

        # render it!
        TrainJourneyHeader(dep_stn, arr_stn, schedule_id, description)
        TrainJourneyInfoDropdown(
            start_noti_time,
            end_noti_time,
            train_departure_time,
            number_of_trains,
            days_to_notify,
            notification_channel,
            chat_id,
        )

        left_col, right_col = st.columns([0.25, 1])

        edit_button_key = f"editButton-{idx}"
        with left_col:
            edit_button = st.button(
                label="Edit Schedule",
                key=get_search_cache_key(edit_button_key),
            )

            if get_search_cache_value(edit_button_key):
                edit_journey(
                    schedule_id,
                    description,
                    dep_stn.value,
                    arr_stn.value,
                    start_noti_time,
                    end_noti_time,
                    train_departure_time,
                    number_of_trains,
                    expires_at,
                    days_to_notify,
                    notification_channel.value,
                    chat_id,
                    use_fancy_greeting_message,
                )

        with right_col:
            with st.popover("Delete Schedule"):
                st.write("Are you sure you want to delete?")

                delete_button = st.button(
                    label="Nuke it with fire 🔥",
                    type="primary",
                    key=get_search_cache_key(f"deleteButton-{idx}"),
                    on_click=delete_journey,
                    args=[schedule_id],
                )


def JourneyGroup(train_journeys: list[TrainNotifyRequest], use_divider: bool = True):
    for idx, journey in enumerate(train_journeys):
        Journey(idx, journey)
        if use_divider:
            st.divider()
