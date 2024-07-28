from datetime import time, timedelta
from typing import Optional

import streamlit as st

from components.common.forms import (
    DateInputField,
    DropdownInputField,
    SliderInputField,
    TextInputField,
)
from service.constants import NotificationChannel, Station
from service.environment import (
    JourneyFormFieldKey,
    get_journey_form_state_key,
    get_journey_form_state_value,
    set_journey_form_state_value,
)
from service.locales import t


# customised input fields
def TimeSliderInputField(
    label: str,
    help: Optional[str] = None,
    key: Optional[str] = None,
    value: Optional[time] = None,
):
    return SliderInputField(
        label=label,
        min_value=time(0, 0, 0),
        max_value=time(23, 59, 59),
        help=help,
        step=timedelta(minutes=5),
        key=key,
        value=value,
    )


def StationDropdownInputField(
    label: str,
    help: Optional[str] = None,
    key: Optional[str] = None,
    index_val: Optional[str] = None,
):
    stn_arr = [stn.value for stn in Station]
    return DropdownInputField(
        label=label,
        dropdown_options=stn_arr,
        key=key,
        index=stn_arr.index(index_val) if index_val else 0,
        format_func=lambda s: t(s),
        help=help,
    )


def DaySelectionInputField():
    with st.container():

        left_col, mid_col, right_col = st.columns(3)
        with left_col:
            use_mon = st.checkbox(
                label="Monday",
                key=get_journey_form_state_key(JourneyFormFieldKey.MONDAY),
            )
            use_tue = st.checkbox(
                label="Tuesday",
                key=get_journey_form_state_key(JourneyFormFieldKey.TUESDAY),
            )
            use_wed = st.checkbox(
                label="Wednesday",
                key=get_journey_form_state_key(JourneyFormFieldKey.WEDNESDAY),
            )

        with mid_col:
            use_thu = st.checkbox(
                label="Thursday",
                key=get_journey_form_state_key(JourneyFormFieldKey.THURSDAY),
            )
            use_fri = st.checkbox(
                label="Friday",
                key=get_journey_form_state_key(JourneyFormFieldKey.FRIDAY),
            )
        with right_col:
            use_sat = st.checkbox(
                label="Saturday",
                key=get_journey_form_state_key(JourneyFormFieldKey.SATURDAY),
            )
            use_sun = st.checkbox(
                label="Sunday",
                key=get_journey_form_state_key(JourneyFormFieldKey.SUNDAY),
            )


# main component
def JourneyForm():
    with st.container():
        st.markdown("#### 📖 Journey Information")

        if not get_journey_form_state_value(JourneyFormFieldKey.NOTIFICATION_CHANNEL):
            set_journey_form_state_value(
                JourneyFormFieldKey.NOTIFICATION_CHANNEL,
                NotificationChannel.TELEGRAM.value,
            )

        if get_journey_form_state_value(JourneyFormFieldKey.NOTIFICATION_GLOBAL_ID):
            notiifcation_schedule_global_id = TextInputField(
                label="Journey ID",
                value=get_journey_form_state_value(
                    JourneyFormFieldKey.NOTIFICATION_GLOBAL_ID
                ),
                disabled=True,
            )

        description = TextInputField(
            label="Journey Description",
            placeholder="Describe your journey",
            key=get_journey_form_state_key(JourneyFormFieldKey.DESCRIPTION),
        )

        dep_stn = StationDropdownInputField(
            label="Departure Station",
            help="The station the train will depart from",
            key=get_journey_form_state_key(JourneyFormFieldKey.DEPARTURE_STN),
        )
        arr_stn = StationDropdownInputField(
            label="Arrival Station",
            help="The station the train will arrive at",
            key=get_journey_form_state_key(JourneyFormFieldKey.ARRIVAL_STN),
        )

        st.divider()
        st.markdown("#### 🕰️ Timings")

        notification_start_time = TimeSliderInputField(
            label="Start Notifying At",
            help="The time to start sending notifications about your trains",
            key=get_journey_form_state_key(JourneyFormFieldKey.START_NOTI_TIME),
        )
        notification_end_time = TimeSliderInputField(
            label="Stop Notifying At",
            help="The time to stop sending notifications about your trains",
            key=get_journey_form_state_key(JourneyFormFieldKey.END_NOTI_TIME),
        )
        train_departure_time = TimeSliderInputField(
            label="Train Departs At",
            help="The time that you want your trains to depart at. "
            + "Returns all trains after this time",
            key=get_journey_form_state_key(JourneyFormFieldKey.TRAIN_DEP_TIME),
        )

        number_of_trains = SliderInputField(
            label="Number of Trains",
            min_value=1,
            max_value=10,
            help="The number of available trains to return",
            key=get_journey_form_state_key(JourneyFormFieldKey.NUM_TRAINS),
        )

        expires_at = DateInputField(
            label="Stop Notifying On",
            help="The last day to be notified for this journey.",
            key=get_journey_form_state_key(JourneyFormFieldKey.EXPIRES_AT),
        )

        st.divider()
        st.markdown("#### 📅 Days to Notify")

        day_selection_bool_tup = DaySelectionInputField()

        st.divider()
        st.markdown("#### 📱 Notification Method")

        notification_channel_arr = [channel.value for channel in NotificationChannel]
        notification_channel_state_val = get_journey_form_state_value(
            JourneyFormFieldKey.NOTIFICATION_CHANNEL
        )

        notification_channel = DropdownInputField(
            "Notification Channel",
            notification_channel_arr,
            help="The channel you want to be notified with",
            key=get_journey_form_state_key(JourneyFormFieldKey.NOTIFICATION_CHANNEL),
            index=(
                notification_channel_arr.index(notification_channel_state_val)
                if notification_channel_state_val
                else 0
            ),
            format_func=lambda s: t(s),
        )

        if notification_channel_state_val == NotificationChannel.MS_TEAMS:

            chat_id = (
                TextInputField(
                    label="Chat ID",
                    placeholder="Enter the SSM Path",
                    max_chars=128,
                    help="The SSM Path to the Webhook",
                    key=get_journey_form_state_key(JourneyFormFieldKey.CHAT_ID),
                    disabled=True,
                ),
            )

            st.markdown(
                """
                For Microsoft Teams, some additional steps are required, please contact 
                an administrator.
                """
            )

        if notification_channel_state_val == NotificationChannel.TELEGRAM:

            chat_id = TextInputField(
                label="Telegram Chat ID",
                placeholder="Enter the Telegram Chat ID",
                max_chars=128,
                key=get_journey_form_state_key(JourneyFormFieldKey.CHAT_ID),
            )

            use_fancy_greeting_message = st.checkbox(
                label="Send Fancy Greeting Message",
                help="Sends a fancy (sometimes vulgar) greeting message to the telegram group before the train records",
                key=get_journey_form_state_key(
                    JourneyFormFieldKey.USE_FANCY_GREETING_MESSAGE
                ),
            )

            st.markdown(
                """
                For telegram, see how to get your chat 
                ID [here](https://medium.com/@2mau/how-to-get-a-chat-id-in-telegram-1861a33ca1de).    
                """
            )

        st.divider()
