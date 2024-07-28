from datetime import date, datetime, time
from typing import Optional, TypedDict

from service.constants import NotificationChannel, Station


class TrainNotifyRequest(TypedDict):
    notification_scehdule_global_id: str
    universe: str
    description: str
    departure_station: Station
    arrival_station: Station
    inserted_at: Optional[datetime]
    last_updated_at: Optional[datetime]
    start_notification_time: time
    end_notification_time: time
    train_departure_time: time
    expires_at: date
    days_to_notify: list[int]
    number_of_trains: int
    notification_channel: NotificationChannel
    chat_id: str
    is_deleted: bool
    use_fancy_greeting_message: bool
