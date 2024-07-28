import logging
from datetime import datetime
from uuid import uuid4

import pytz

from core.profiling import profileit
from core.sql import Database
from service.constants import NotificationChannel, Station
from service.types import TrainNotifyRequest

logger = logging.getLogger(__name__)

REQUIRED_SSM = ["host", "user", "port", "password", "database"]


class ChooChooDatabase(Database):

    def __init__(
        self,
        host: str,
        user: str,
        port: int,
        password: str,
        database: str,
    ) -> None:

        super().__init__(
            host,
            user,
            port,
            password,
            database,
        )

    @staticmethod
    def parse_dict_to_train_notification_schedule(
        result: dict,
    ) -> TrainNotifyRequest:
        return {  # type: ignore
            **result,
            "departure_station": Station(result["departure_station"]),
            "arrival_station": Station(result["arrival_station"]),
            "start_notification_time": result["start_notification_time"].time(),
            "end_notification_time": result["end_notification_time"].time(),
            "train_departure_time": result["train_departure_time"].time(),
            "expires_at": result["expires_at"].date(),
            "notification_channel": NotificationChannel(result["notification_channel"]),
            "days_to_notify": [
                int(day)
                for day in str(result.get("days_to_notify", "")).split(",")
                if day
            ],
        }

    @profileit(template="Queried DB for report with ID {2} in {_time}")
    def get_notification_schedule_by_id(
        self, universe: str, notification_global_id: str
    ):
        result = self.query_one(
            """
            SELECT * FROM notification_schedules
            WHERE notification_schedule_global_id = %s
            AND universe = %s
            """,
            (notification_global_id, universe),
        )

        return self.parse_dict_to_train_notification_schedule(result)

    @profileit(template="Queried DB for all active schedules in {_time}")
    def get_active_notification_schedules(self, universe: str):
        result = self.query(
            """
            SELECT * FROM notification_schedules
            WHERE NOW() < expires_at
                AND is_deleted = 0
                AND universe = %s
            ORDER BY departure_station
            """,
            [universe],
        )

        return [self.parse_dict_to_train_notification_schedule(res) for res in result]

    @profileit(template="Queried DB for train reports to notify now in {_time}")
    def get_train_reports_to_notify_now(
        self, universe: str
    ) -> list[TrainNotifyRequest]:
        results = self.query(
            """
            SELECT *
            FROM notification_schedules
            WHERE universe = %s
                AND (TIME(%s) BETWEEN
                    TIME(start_notification_time)
                    AND TIME(end_notification_time + INTERVAL 1 MINUTE))
                AND is_deleted = 0
                AND NOW() < expires_at
            """,
            [universe, datetime.now().astimezone(pytz.timezone("Europe/London"))],
        )

        return [
            self.parse_dict_to_train_notification_schedule(result) for result in results
        ]

    @profileit(template="Queried DB for all journeys from {2} to {3} in {_time}")
    def get_train_reports_by_journey(self, universe: str, dep_stn: str, arr_stn: str):
        results = self.query(
            """
            SELECT * FROM notification_schedules
            WHERE universe = %s
                AND departure_station = %s
                AND arrival_station = %s
                AND is_deleted = 0
                AND NOW() < expires_at
            """,
            [universe, dep_stn, arr_stn],
        )

        return [
            self.parse_dict_to_train_notification_schedule(result) for result in results
        ]

    @profileit(template="inserted new schedule in {_time}")
    def insert_new_train_schedule(
        self,
        universe: str,
        description: str,
        departure_station_crs: str,
        arrival_station_crs: str,
        start_noti_time: datetime,
        end_noti_time: datetime,
        train_dep_time: datetime,
        days_to_notify: str,
        number_of_trains: int,
        notification_channel_str: str,
        chat_id: str,
        expires_at: datetime,
        use_fancy_greeting_message: bool,
    ):
        return self.insert_one(
            """
            INSERT INTO notification_schedules (
                notification_schedule_global_id,
                universe,
                description,
                departure_station,
                arrival_station,
                start_notification_time,
                end_notification_time,
                train_departure_time,
                days_to_notify,
                number_of_trains,
                notification_channel,
                chat_id,
                expires_at,
                is_deleted,
                use_fancy_greeting_message
            ) VALUES (
                %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s
            )
            """,
            [
                str(uuid4()),
                universe,
                description,
                departure_station_crs,
                arrival_station_crs,
                start_noti_time,
                end_noti_time,
                train_dep_time,
                days_to_notify,
                number_of_trains,
                notification_channel_str,
                chat_id,
                expires_at,
                False,  # is_deleted
                use_fancy_greeting_message,
            ],
        )

    @profileit("updated schedule for {0} in {_time}")
    def update_train_schedule_by_id(
        self,
        notification_global_id: str,
        universe: str,
        description: str,
        departure_station_crs: str,
        arrival_station_crs: str,
        start_noti_time: datetime,
        end_noti_time: datetime,
        train_dep_time: datetime,
        days_to_notify: str,
        number_of_trains: int,
        notification_channel_str: str,
        chat_id: str,
        expires_at: datetime,
        use_fancy_greeting_message: bool,
    ):
        return self.update(
            """
            UPDATE notification_schedules
            SET
                universe = %s,
                description = %s,
                departure_station = %s,
                arrival_station = %s,
                start_notification_time = %s,
                end_notification_time = %s,
                train_departure_time = %s,
                days_to_notify = %s,
                number_of_trains = %s,
                notification_channel = %s,
                chat_id = %s,
                expires_at = %s,
                use_fancy_greeting_message = %s
            WHERE
                notification_schedule_global_id = %s
            """,
            [
                universe,
                description,
                departure_station_crs,
                arrival_station_crs,
                start_noti_time,
                end_noti_time,
                train_dep_time,
                days_to_notify,
                number_of_trains,
                notification_channel_str,
                chat_id,
                expires_at,
                use_fancy_greeting_message,
                notification_global_id,
            ],
        )

    def soft_delete_schedule_by_id(self, notification_global_id: str):
        return self.update(
            """
            UPDATE notification_schedules
            SET is_deleted = 1
            WHERE notification_schedule_global_id = %s
            """,
            [notification_global_id],
        )
