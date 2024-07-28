from datetime import date, datetime

import streamlit as st

from components.common.toasts import ErrorToast, SuccessToast
from components.JourneyForm import JourneyForm
from components.Page import Page
from service.environment import (
    JourneyFormFieldKey,
    get_db_credentials,
    get_journey_form_state_key,
    get_journey_form_state_value,
)
from service.journey import validate_journey
from service.sql import ChooChooDatabase


class EditJourneyFormPage(Page):

    def __init__(self) -> None:
        self.db = ChooChooDatabase(**get_db_credentials())
        super().__init__(previous_page="pages/search-journey.py")

    def update_journey(self):
        notification_global_id = get_journey_form_state_value(
            JourneyFormFieldKey.NOTIFICATION_GLOBAL_ID
        )
        description = get_journey_form_state_value(JourneyFormFieldKey.DESCRIPTION)
        dep_stn = get_journey_form_state_value(JourneyFormFieldKey.DEPARTURE_STN)
        arr_stn = get_journey_form_state_value(JourneyFormFieldKey.ARRIVAL_STN)
        noti_start_time = get_journey_form_state_value(
            JourneyFormFieldKey.START_NOTI_TIME
        )
        noti_end_time = get_journey_form_state_value(JourneyFormFieldKey.END_NOTI_TIME)
        train_dep_time = get_journey_form_state_value(
            JourneyFormFieldKey.TRAIN_DEP_TIME
        )
        number_of_trains = get_journey_form_state_value(JourneyFormFieldKey.NUM_TRAINS)
        expires_at = get_journey_form_state_value(JourneyFormFieldKey.EXPIRES_AT)
        days_to_notify_tup = (
            get_journey_form_state_value(JourneyFormFieldKey.MONDAY),
            get_journey_form_state_value(JourneyFormFieldKey.TUESDAY),
            get_journey_form_state_value(JourneyFormFieldKey.WEDNESDAY),
            get_journey_form_state_value(JourneyFormFieldKey.THURSDAY),
            get_journey_form_state_value(JourneyFormFieldKey.FRIDAY),
            get_journey_form_state_value(JourneyFormFieldKey.SATURDAY),
            get_journey_form_state_value(JourneyFormFieldKey.SUNDAY),
        )
        notification_channel = get_journey_form_state_value(
            JourneyFormFieldKey.NOTIFICATION_CHANNEL
        )
        chat_id = get_journey_form_state_value(JourneyFormFieldKey.CHAT_ID)
        use_fancy_greeting_message = get_journey_form_state_value(
            JourneyFormFieldKey.USE_FANCY_GREETING_MESSAGE
        )

        baseline_date = date(2024, 1, 1)
        baseline_noti_start_time = datetime.combine(baseline_date, noti_start_time)
        baseline_noti_end_time = datetime.combine(baseline_date, noti_end_time)
        baseline_train_dep_time = datetime.combine(baseline_date, train_dep_time)

        # validate the inputs
        is_input_valid = validate_journey(
            description=description,
            dep_stn=dep_stn,
            arr_stn=arr_stn,
            baseline_noti_start_time=baseline_noti_start_time,
            baseline_noti_end_time=baseline_noti_end_time,
            baseline_train_dep_time=baseline_train_dep_time,
            days_to_notify_tup=days_to_notify_tup,
            expires_at=expires_at,
            notification_channel=notification_channel,
            chat_id=chat_id,
        )

        if not is_input_valid:
            return

        universe = "development"

        # convert the tuple to a string
        days_to_notify_arr = []
        for idx, notify_day in enumerate(days_to_notify_tup):
            if notify_day:
                days_to_notify_arr.append(str(idx + 1))

        days_to_notify_str = ",".join(days_to_notify_arr)

        self.db.update_train_schedule_by_id(
            notification_global_id=notification_global_id,
            universe=universe,
            description=description,
            departure_station_crs=dep_stn,
            arrival_station_crs=arr_stn,
            start_noti_time=baseline_noti_start_time,
            end_noti_time=baseline_noti_end_time,
            train_dep_time=baseline_train_dep_time,
            days_to_notify=days_to_notify_str,
            number_of_trains=number_of_trains,
            notification_channel_str=notification_channel,
            chat_id=str(chat_id),
            expires_at=expires_at,
            use_fancy_greeting_message=use_fancy_greeting_message,
        )

    def render_header(self):

        st.subheader("🚄 Edit Journey Schedule")
        st.write("Update your schedule details below.")
        st.divider()

    def render_submit_button(self):
        create_journey_button = st.button(
            label="Update Journey",
            use_container_width=True,
        )

        if create_journey_button:
            try:
                self.update_journey()
                SuccessToast("Journey updated successfully!")

                # TODO: i should navigate somewhere after this tbh

            except Exception as e:
                ErrorToast(
                    "Oops... something went wrong while trying to update your journey. "
                    + "Please contact an administrator."
                    + f"Error reason: {str(e)}"
                )

    def render(self):
        self.render_back_button(
            clear_keys=[
                get_journey_form_state_key(field) for field in JourneyFormFieldKey
            ]
        )
        self.render_header()

        JourneyForm()

        self.render_submit_button()
        self.render_footer()


if __name__ == "__main__":
    EditJourneyFormPage().render()
