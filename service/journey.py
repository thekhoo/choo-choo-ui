from datetime import date, datetime, time, timedelta

from components.common.toasts import ErrorToast
from service.constants import NotificationChannel, Station


def validate_journey(
    description: str,
    dep_stn: Station,
    arr_stn: Station,
    baseline_noti_start_time: time,
    baseline_noti_end_time: time,
    baseline_train_dep_time: time,
    expires_at: date,
    days_to_notify_tup: tuple[bool],
    notification_channel: NotificationChannel,
    chat_id: str | None,
):
    if not description:
        ErrorToast("You're not gonna describe your journey???!?!")
        return False

    if not dep_stn:
        ErrorToast("I think you missed your departure station...")
        return False

    if not arr_stn:
        ErrorToast("I think you missed your departure station...")
        return False

    if dep_stn == arr_stn:
        ErrorToast(
            "Bruh... departure station cannot be the same as the arrival station",
        )
        return False

    if baseline_noti_start_time > baseline_noti_end_time:
        ErrorToast("End time must be after start time.")
        return False

    if baseline_train_dep_time - baseline_noti_start_time > timedelta(
        hours=2
    ) or baseline_noti_end_time - baseline_train_dep_time > timedelta(hours=2):
        ErrorToast(
            "Train departure time must be within 2 hours of the start and end notification time."
        )
        return False

    if expires_at <= datetime.now().date():
        ErrorToast("Date to stop notifying must be some date in the future.")
        return False

    if not any(days_to_notify_tup):
        ErrorToast("I think you missed which days you want to be notified for")
        return False

    if notification_channel and not chat_id:
        ErrorToast("Please insert a valid Chat ID")
        return False

    return True
