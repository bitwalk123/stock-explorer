from PySide6.QtCore import QDateTime, QTimeZone, Qt

def create_qdatetime_and_get_timestamp_ms(date_str: str, time_str: str) -> int:
    """
    指定された日付文字列と時刻文字列から QDateTime インスタンスを生成し、
    そのミリ秒単位のタイムスタンプ (Unix epoch からのミリ秒数) を int で返します。
    この関数は、ローカルタイムゾーンでパースします。

    Args:
        date_str (str): 日付を表す文字列 (例: "2025-04-01")
        time_str (str): 時刻を表す文字列 (例: "09:00:01")

    Returns:
        int: 生成された QDateTime インスタンスのミリ秒単位のタイムスタンプ (Unix epoch からのミリ秒数)
    """
    # 日付と時刻の文字列を結合
    datetime_str = f"{date_str} {time_str}"

    # QDateTime.fromString() を使用して QDateTime インスタンスを生成
    # タイムゾーンを明示しない場合、システムのローカルタイムゾーンが使用されます。
    qdatetime_instance = QDateTime.fromString(datetime_str, "yyyy-MM-dd HH:mm:ss")

    # 正しくパースできたかを確認
    if not qdatetime_instance.isValid():
        print(f"エラー: 日付/時刻文字列 '{datetime_str}' のパースに失敗しました。")
        # int を返すので、エラー時は通常 -1 などとします。
        return -1

    # タイムスタンプをミリ秒で取得
    # toMSecsSinceEpoch() は Unix epoch (1970-01-01 00:00:00 UTC) からのミリ秒数を qint64 (Pythonではint) で返します。
    timestamp_ms = qdatetime_instance.toMSecsSinceEpoch()

    return timestamp_ms

if __name__ == "__main__":
    date_string = "2025-04-01"
    time_string = "09:00:01"

    print("--- ローカルタイムゾーンでの処理 (ミリ秒単位タイムスタンプ、int) ---")
    timestamp_result_ms = create_qdatetime_and_get_timestamp_ms(date_string, time_string)

    if timestamp_result_ms != -1:
        print(f"日付: {date_string}, 時刻: {time_string}")
        print(f"QDateTime のタイムスタンプ (ミリ秒、int): {timestamp_result_ms}")

        # int のタイムスタンプからQDateTimeを再構築して表示
        reconstructed_qdatetime_ms = QDateTime.fromMSecsSinceEpoch(timestamp_result_ms)
        print(f"タイムスタンプから再構築したQDateTime: {reconstructed_qdatetime_ms.toString(Qt.DateFormat.ISODateWithMs)}")
        print(f"再構築したQDateTimeのタイムゾーン: {reconstructed_qdatetime_ms.timeZone().displayName(QTimeZone.StandardTime)}")

    print("\n--- UTCでのQDateTime生成の正しい例 (参考、ミリ秒単位タイムスタンプ、int) ---")
    # 方法1: ローカルでパース後、UTCに変換
    local_qdatetime = QDateTime.fromString(f"{date_string} {time_string}", "yyyy-MM-dd HH:mm:ss")
    if local_qdatetime.isValid():
        qdatetime_utc_from_local = local_qdatetime.toTimeZone(QTimeZone.utc())
        print(f"ローカルからUTCに変換したQDateTime: {qdatetime_utc_from_local.toString(Qt.DateFormat.ISODateWithMs)}")
        print(f"そのタイムスタンプ (ミリ秒、int): {qdatetime_utc_from_local.toMSecsSinceEpoch()}")
    else:
        print("エラー: ローカルでの日付/時刻文字列のパースに失敗しました。")

    # 方法2: QDateTime のコンストラクタで明示的にUTCを指定して生成
    from PySide6.QtCore import QDate, QTime, QTimeZone
    qdate_obj = QDate.fromString(date_string, "yyyy-MM-dd")
    qtime_obj = QTime.fromString(time_string, "HH:mm:ss")

    if qdate_obj.isValid() and qtime_obj.isValid():
        # 時刻にミリ秒を追加する場合は、QTimeのコンストラクタを使用します。
        # 今回の入力文字列にはミリ秒がないため、0を設定します。
        qtime_obj_with_ms = QTime(qtime_obj.hour(), qtime_obj.minute(), qtime_obj.second(), 0)

        qdatetime_utc_constructor = QDateTime(qdate_obj, qtime_obj_with_ms, QTimeZone.utc())
        print(f"コンストラクタでUTC指定して生成したQDateTime: {qdatetime_utc_constructor.toString(Qt.DateFormat.ISODateWithMs)}")
        print(f"そのタイムスタンプ (ミリ秒、int): {qdatetime_utc_constructor.toMSecsSinceEpoch()}")
    else:
        print("エラー: 日付または時刻オブジェクトの生成に失敗しました。")