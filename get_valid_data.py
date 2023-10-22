import datetime as dt


def main():
    day1 = 24 * 60 * 60
    tz_delta = 9 * 60 * 60  # Asia/Tokyo timezone
    now_dt = dt.datetime.now()
    now = int(dt.datetime.timestamp(now_dt)) + tz_delta
    end = (now // day1 - 1) * day1
    start = end - 365 * day1
    print(
        'date scope :',
        dt.datetime.fromtimestamp(start),
        '-',
        dt.datetime.fromtimestamp(end)
    )


if __name__ == "__main__":
    main()
