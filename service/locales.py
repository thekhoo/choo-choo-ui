CREATE_FORM_LOCALE = {
    "inserted_at": "Inserted At",
    "start_notification_time": "Start Notifying At",
    "end_notification_time": "End Notifying At",
    "train_departure_time": "Train Departure Time",
    "notification_channel": "Notify Via",
    "expires_at": "Expires At",
    "days_to_notify": "Days to Notify",
    "number_of_trains": "Number of Trains",
    "chat_id": "Chat ID",
}

STATION_LOCALE_MAP = {
    "BAN": "Banbury [BAN]",
    "BTH": "Bath Spa [BTH]",
    "BEE": "Beeston [BEE]",
    "BCS": "Bicester North [BCS]",
    "BIT": "Bicester Village [BIT]",
    "BHI": "Birmingham International [BHI]",
    "BHM": "Birmingham New Street [BHM]",
    "BMO": "Birmingham Moor Street [BMO]",
    "BPW": "Bristol Parkway [BPW]",
    "BRI": "Bristol Temple Meads [BRI]",
    "CBG": "Cambridge [CBG]",
    "CHM": "Chelmsford [CHM]",
    "DBY": "Derby [DBY]",
    "DID": "Didcot Parkway [DID]",
    "EAL": "Ealing Broadway [EAL]",
    "EDB": "Edinburgh Waverly [EDB]",
    "FOK": "Four Oaks [FOK]",
    "GTW": "Gatwick Airport [GTW]",
    "LEI": "Leicester [LEI]",
    "EUS": "London Euston [EUS]",
    "KGX": "London Kings Cross [KGX]",
    "LST": "London Liverpool Street [LST]",
    "MYB": "London Marylebone [MYB]",
    "STP": "London St Pancras Top Level [EMR] [STP]",
    "SPL": "London St Pancras Low Level [Thameslink] [SPL]",
    "PAD": "London Paddington [PAD]",
    "WAT": "London Waterloo [WAT]",
    "MAI": "Maidenhead [MAI]",
    "NOT": "Nottingham [NOT]",
    "OXF": "Oxford [OXF]",
    "PBO": "Peterborough [PBO]",
    "RDG": "Reading [RDG]",
    "SLO": "Slough [SLO]",
    "SOL": "Solihull [SOL]",
    "STA": "Stafford [STA]",
    "SSD": "Stansted Airport [SSD]",
    "TAH": "Tamworth Top Level [TAH]",
    "TAM": "Tamworth Low Level [TAM]",
    "TAU": "Taunton [TAU]",
    "TWY": "Twyford [TWY]",
    "WRW": "Warwick [WRW]",
    "WRP": "Warwick Parkway [WRP]",
}

NOTIFICATION_CHANNEL_LOCALE_MAP = {
    "telegram": "Telegram",
    "ms_teams": "Microsoft Teams",
}

LOCALE_MAP = {
    **CREATE_FORM_LOCALE,
    **STATION_LOCALE_MAP,
    **NOTIFICATION_CHANNEL_LOCALE_MAP,
}


def t(key: str, default: str = None):
    if key in LOCALE_MAP:
        return LOCALE_MAP[key]

    if default:
        return default

    return key
