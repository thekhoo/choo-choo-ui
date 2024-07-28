import streamlit as st

from components.common.forms import DropdownInputField, TextInputField
from components.Journey import Journey
from components.JourneyForm import StationDropdownInputField
from components.Page import Page
from service.environment import (
    get_db_credentials,
    get_search_cache_key,
    get_search_cache_value,
    set_search_cache_state_value,
)
from service.sql import ChooChooDatabase


class SearchByJourney(Page):

    def __init__(self) -> None:
        self.db = ChooChooDatabase(**get_db_credentials())
        super().__init__()

    def searching_for_journey_spinner(self):
        return st.spinner("Getting your schedules 🚂...")

    def search_by_departure_and_arrival_station(self):
        st.caption(
            "Gets all journeys that specifically depart and arrive at the specified stations."
        )

        left_col, right_col = st.columns(2)
        with left_col:
            departure_station = StationDropdownInputField(
                label="Select Departing Station",
                key=get_search_cache_key("departureStation"),
            )

        with right_col:
            arrival_station = StationDropdownInputField(
                "Select Arrival Station", key=get_search_cache_key("arrivalStation")
            )

        search_btn = st.button(
            label="Search For Journeys",
            use_container_width=True,
            key=get_search_cache_key("btnSearchDepArrStation"),
        )

        if search_btn:
            with self.searching_for_journey_spinner():

                train_journeys = self.db.get_train_reports_by_journey(
                    "development", departure_station, arrival_station
                )

                set_search_cache_state_value("trainJourneys", train_journeys)

    def search_by_single_station(self):
        st.caption(
            "Returns all journeys that include the specified station (Departure or Arrival)"
        )

        station = StationDropdownInputField(
            label="Select Station",
            key=get_search_cache_key("singleStation"),
        )

        search_btn = st.button(
            label="Search For Journeys",
            use_container_width=True,
            key=get_search_cache_key("btnSearchSingleStation"),
        )

        if search_btn:
            with self.searching_for_journey_spinner():
                train_journeys = self.db.get_train_reports_by_station(
                    "development", station
                )

                set_search_cache_state_value("trainJourneys", train_journeys)

    def search_by_both_stations(self):
        st.caption(
            "Returns all journeys between both stations regardless of departure and arrival"
        )

        left_col, right_col = st.columns(2)
        with left_col:
            first_station = StationDropdownInputField(
                label="Select First Station",
                key=get_search_cache_key("firstStation"),
            )

        with right_col:
            second_station = StationDropdownInputField(
                "Select Second Station", key=get_search_cache_key("secondStation")
            )

        search_btn = st.button(
            label="Search For Journeys",
            use_container_width=True,
            key=get_search_cache_key("btnSearchBothStations"),
        )

        if search_btn:
            with self.searching_for_journey_spinner():
                train_journeys = self.db.get_train_reports_for_both_stations(
                    "development", first_station, second_station
                )

                set_search_cache_state_value("trainJourneys", train_journeys)

    def search_by_description(self):
        st.caption("Returns all journeys that match the given description")
        description = TextInputField(
            label="Description",
            placeholder="Enter the journey description",
            key=get_search_cache_key("searchDescription"),
        )

        search_btn = st.button(
            label="Search For Journeys",
            use_container_width=True,
            key=get_search_cache_key("btnSearchDescription"),
        )

        if search_btn:
            with self.searching_for_journey_spinner():
                train_journeys = self.db.get_train_reports_by_description(
                    "development", description
                )

                set_search_cache_state_value("trainJourneys", train_journeys)

    def search_specific_journey(self):
        st.caption("Returns information for a specific journey")

        universe = "development"
        global_id_to_description_map = self.db.get_train_reports_id_to_description_map(
            universe
        )

        notification_global_id = DropdownInputField(
            label="Select Journey",
            dropdown_options=global_id_to_description_map.keys(),
            format_func=lambda s: f"{s} | {global_id_to_description_map[s]}",
            key=get_search_cache_key("searchNotificationGlobalId"),
        )

        search_btn = st.button(
            label="Search For Journeys",
            use_container_width=True,
            key=get_search_cache_key("btnSearchSpecifcJourney"),
        )

        if search_btn:
            with self.searching_for_journey_spinner():
                train_journey = self.db.get_train_report_by_id(
                    "development", notification_global_id
                )

                set_search_cache_state_value("trainJourneys", [train_journey])

    def render_header(self):
        st.header("Find Your Journey")
        st.write("Search for the journey schedule that you're looking for")
        st.caption(
            "NOTE: You will need to click the 'Search Journeys' button again to see your updates applied if any."
        )
        (
            dep_arr_stn_search_tab,
            single_stn_search_tab,
            double_stn_search_tab,
            description_search_tab,
            global_id_search_tab,
        ) = st.tabs(
            [
                "Dep. & Arr. Station",
                "Single Station",
                "Both Stations",
                "Description",
                "Specific Journey",
            ]
        )

        with dep_arr_stn_search_tab:
            self.search_by_departure_and_arrival_station()

        with single_stn_search_tab:
            self.search_by_single_station()

        with double_stn_search_tab:
            self.search_by_both_stations()

        with description_search_tab:
            self.search_by_description()

        with global_id_search_tab:
            self.search_specific_journey()

    def render(self):

        self.render_back_button(clear_keys=[get_search_cache_key("trainJourneys")])
        self.render_header()

        train_journeys = get_search_cache_value("trainJourneys", [])
        st.write(f"Found {len(train_journeys)} records.")
        for idx, journey in enumerate(train_journeys):
            Journey(idx, journey)
            st.divider()

        self.render_footer()


if __name__ == "__main__":
    SearchByJourney().render()
