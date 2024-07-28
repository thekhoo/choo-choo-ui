import streamlit as st

from components.common.toasts import WarningToast
from components.Journey import Journey, JourneyGroup
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
        super().__init__()

    def render_search_results(self, departure_station: str, arrival_station: str):
        if departure_station == arrival_station:
            WarningToast(
                "Stations cannot be the same. "
                + "Please choose a different departure/arrival station.",
            )
            return

        db = ChooChooDatabase(**get_db_credentials())

        train_journeys = db.get_train_reports_by_journey(
            "development", departure_station, arrival_station
        )

        train_journey_cache_key = get_search_cache_key(
            f"journey-{departure_station}-{arrival_station}"
        )

        if not get_search_cache_value(train_journey_cache_key):
            st.session_state[train_journey_cache_key] = train_journeys

        if not train_journeys:
            WarningToast(
                f"Could not find any journey from {departure_station} to {arrival_station}"
            )

            st.write(
                f"No train journeys from {departure_station} to {arrival_station} found."
            )

        else:
            st.write(f"Found {len(train_journeys)} records.")
            if (
                get_search_cache_value("prevDepartureStation") != departure_station
                or get_search_cache_value("prevArrivalStation") != arrival_station
            ):
                # re render because the search has changed
                # update the cache
                st.session_state[get_search_cache_key("prevDepartureStation")] = (
                    departure_station
                )
                st.session_state[get_search_cache_key("prevArrivalStation")] = (
                    arrival_station
                )
                for idx, journey in enumerate(
                    get_search_cache_value(
                        f"journey-{departure_station}-{arrival_station}"
                    )
                ):
                    Journey(idx, journey)
                    st.divider()

    def render_header(self):
        st.header("Search For Schedule by Stations")
        st.write("Search for all schedules between the departure and arrival station")
        st.caption(
            "NOTE: You will need to click the 'Search Journeys' button again to see your updates applied if any."
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
        )

        if search_btn:
            db = ChooChooDatabase(**get_db_credentials())

            train_journeys = db.get_train_reports_by_journey(
                "development", departure_station, arrival_station
            )

            set_search_cache_state_value("trainJourneys", train_journeys)

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
