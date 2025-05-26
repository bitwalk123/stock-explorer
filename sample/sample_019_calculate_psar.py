import pandas as pd
import numpy as np


def calculate_psar(ohlc: pd.DataFrame, iaf: float = 0.02, maxaf: float = 0.2, af_step: float = 0.02) -> dict:
    """
    一般的なワイルダーのParabolic SAR (PSAR) を計算します。

    Args:
        ohlc (pd.DataFrame): OHLCV データを含むDataFrame。
                             'High', 'Low', 'Close' カラムが必要です。
        iaf (float): 初期加速因子 (Initial Acceleration Factor)。デフォルトは0.02。
        maxaf (float): 最大加速因子 (Maximum Acceleration Factor)。デフォルトは0.2。
        af_step (float): 加速因子の増加ステップ。デフォルトは0.02。

    Returns:
        dict: 'bear' (下降トレンドのSAR) と 'bull' (上昇トレンドのSAR) をキーとする
              numpy 配列を含む辞書。SAR値がない場合はNaNが含まれます。
              各配列のインデックスは入力DataFrameのインデックスに対応します。
    """
    length = len(ohlc)
    if length < 2:
        # 計算に必要な期間が不足している場合は、NaNで埋められた配列を返す
        nan_array = np.full(length, np.nan, dtype=np.float64)
        return {'bear': nan_array, 'bull': nan_array}

    high = ohlc['High'].to_numpy()
    low = ohlc['Low'].to_numpy()
    close = ohlc['Close'].to_numpy()

    # SAR値、EP（Extreme Point）、AF（Acceleration Factor）、トレンド方向を保持する配列
    sar_values = np.full(length, np.nan, dtype=np.float64)
    ep_values = np.full(length, np.nan, dtype=np.float64)  # デバッグ用/理解を深めるため
    af_values = np.full(length, np.nan, dtype=np.float64)  # デバッグ用/理解を深めるため

    # 出力用のブル・ベアSAR
    psarbull = np.full(length, np.nan, dtype=np.float64)
    psarbear = np.full(length, np.nan, dtype=np.float64)

    # --- 初期設定 (最初の有効なSARはインデックス1から) ---
    # トレンドの初期決定: 最初の2日間の終値で判断
    if close[1] > close[0]:
        bull = True  # 上昇トレンド
        current_ep = high[1]  # EPは最高値
        current_sar = low[0]  # SARの初期値は前日の最安値
    else:
        bull = False  # 下降トレンド
        current_ep = low[1]  # EPは最安値
        current_sar = high[0]  # SARの初期値は前日の最高値

    current_af = iaf  # 加速因子

    # インデックス1のSAR値を格納
    sar_values[1] = current_sar
    ep_values[1] = current_ep
    af_values[1] = current_af

    if bull:
        psarbull[1] = current_sar
    else:
        psarbear[1] = current_sar

    # --- ループ開始 (インデックス 2 から) ---
    for i in range(2, length):
        prev_sar = sar_values[i - 1]
        prev_ep = ep_values[i - 1]
        prev_af = af_values[i - 1]

        # 暫定的な今日のSARを計算
        if bull:  # 上昇トレンドの場合
            calculated_sar_today = prev_sar + prev_af * (prev_ep - prev_sar)

            # キャッピングルール: SARは現在の安値または前日の安値より高くなってはならない
            # これが一般的なワイルダーのSARのキャッピングルールです。
            calculated_sar_today = min(calculated_sar_today, low[i], low[i - 1])

        else:  # 下降トレンドの場合
            calculated_sar_today = prev_sar - prev_af * (prev_sar - prev_ep)

            # キャッピングルール: SARは現在の高値または前日の高値より低くなってはならない
            calculated_sar_today = max(calculated_sar_today, high[i], high[i - 1])

        # トレンド反転のチェック (終値がSARをクロスした場合)
        reversed_this_period = False
        if bull:  # 現在上昇トレンド
            if close[i] < calculated_sar_today:  # 終値がSARを下抜けた場合、トレンド反転
                reversed_this_period = True
                bull = False  # 新しいトレンドは下降トレンド
                current_sar = prev_ep  # 新しいSARは、前のトレンドのEP
                current_ep = low[i]  # 新しいEPは、現在の安値
                current_af = iaf  # 加速因子をリセット
        else:  # 現在下降トレンド
            if close[i] > calculated_sar_today:  # 終値がSARを上抜けた場合、トレンド反転
                reversed_this_period = True
                bull = True  # 新しいトレンドは上昇トレンド
                current_sar = prev_ep  # 新しいSARは、前のトレンドのEP
                current_ep = high[i]  # 新しいEPは、現在の高値
                current_af = iaf  # 加速因子をリセット

        # トレンドが継続する場合のSAR、EP、AFの更新
        if not reversed_this_period:
            current_sar = calculated_sar_today  # 反転しなかった場合は、計算したSARを使用
            if bull:  # 上昇トレンド継続
                if high[i] > prev_ep:  # 新しい高値の場合、EPとAFを更新
                    current_ep = high[i]
                    current_af = min(prev_af + af_step, maxaf)  # AFを加速
                else:  # 新しい高値でなければEPはそのまま
                    current_ep = prev_ep
                    current_af = prev_af  # AFもそのまま
            else:  # 下降トレンド継続
                if low[i] < prev_ep:  # 新しい安値の場合、EPとAFを更新
                    current_ep = low[i]
                    current_af = min(prev_af + af_step, maxaf)  # AFを加速
                else:  # 新しい安値でなければEPはそのまま
                    current_ep = prev_ep
                    current_af = prev_af  # AFもそのまま

        # 最終的な今日のSAR、EP、AFを配列に格納
        sar_values[i] = current_sar
        ep_values[i] = current_ep
        af_values[i] = current_af

        # SARを対応するbull/bear配列に格納
        if bull:
            psarbull[i] = current_sar
        else:
            psarbear[i] = current_sar

    return {
        'bear': psarbear,
        'bull': psarbull,
    }