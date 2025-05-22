# --- ロギング設定の初期化関数 ---
import logging
import logging.handlers
import os


def setup_logging():
    # ログディレクトリの作成
    log_dir = 'logs'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # ルートロガーの取得（またはアプリケーション専用ロガー）
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)  # 全てのレベルを出力するためDEBUGに設定

    # 既存のハンドラがあれば削除（二重出力防止のため、再設定時などに）
    if not logger.handlers:
        # コンソールハンドラ
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)  # コンソールにはINFO以上だけ出す
        console_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        ch.setFormatter(console_formatter)
        logger.addHandler(ch)

        # ファイルハンドラ（ローテーションあり）
        log_file_path = os.path.join(log_dir, 'daytrader.log')
        fh = logging.handlers.RotatingFileHandler(
            log_file_path,
            maxBytes=10 * 1024 * 1024,  # 10MB
            backupCount=5,
            encoding='utf-8'
        )
        fh.setLevel(logging.DEBUG)  # ファイルにはDEBUGレベルも出力
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s - %(lineno)d - %(message)s')
        fh.setFormatter(file_formatter)
        logger.addHandler(fh)

        # xlwingsのログもファイルに書き出す
        xlwings_logger = logging.getLogger('xlwings')
        xlwings_logger.setLevel(logging.INFO)  # xlwingsのログレベルをINFOに設定
        if not xlwings_logger.handlers:  # xlwingsロガーにハンドラがなければ追加
            xlwings_logger.addHandler(fh)  # 同じファイルハンドラを使う

    return logger
