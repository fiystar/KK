"""技术指标计算模块"""

import pandas as pd
import numpy as np
import ta
from ta.momentum import RSIIndicator, MACDIndicator, StochasticOscillator
from ta.volatility import BollingerBands, AverageTrueRange
from ta.trend import SMAIndicator, EMAIndicator, ADXIndicator
import config


class TechnicalIndicators:
    """技术指标计算器"""

    def __init__(self, df):
        """
        初始化指标计算器

        Args:
            df: 包含OHLCV数据的DataFrame
        """
        self.df = df.copy()
        self.df = self.df.astype(
            {"Open": float, "High": float, "Low": float, "Close": float, "Volume": float}
        )

    def calculate_ma(self, periods=None):
        """
        计算移动平均线 (SMA)

        Args:
            periods: 周期列表，默认为config中定义的

        Returns:
            DataFrame: 包含MA的数据
        """
        if periods is None:
            periods = config.INDICATOR_PARAMS["MA_PERIOD"]

        for period in periods:
            self.df[f"MA{period}"] = SMAIndicator(
                close=self.df["Close"], window=period
            ).sma_indicator()

        return self.df

    def calculate_ema(self, periods=None):
        """
        计算指数移动平均线 (EMA)

        Args:
            periods: 周期列表，默认为config中定义的

        Returns:
            DataFrame: 包含EMA的数据
        """
        if periods is None:
            periods = config.INDICATOR_PARAMS["EMA_PERIOD"]

        for period in periods:
            self.df[f"EMA{period}"] = EMAIndicator(
                close=self.df["Close"], window=period
            ).ema_indicator()

        return self.df

    def calculate_rsi(self, period=None):
        """
        计算相对强弱指数 (RSI)

        Args:
            period: RSI周期，默认为config中定义的

        Returns:
            DataFrame: 包含RSI的数据
        """
        if period is None:
            period = config.INDICATOR_PARAMS["RSI_PERIOD"]

        self.df["RSI"] = RSIIndicator(close=self.df["Close"], window=period).rsi()
        return self.df

    def calculate_macd(self, fast=None, slow=None, signal=None):
        """
        计算MACD

        Args:
            fast: 快线周期
            slow: 慢线周期
            signal: 信号线周期

        Returns:
            DataFrame: 包含MACD的数据
        """
        if fast is None:
            fast = config.INDICATOR_PARAMS["MACD_FAST"]
        if slow is None:
            slow = config.INDICATOR_PARAMS["MACD_SLOW"]
        if signal is None:
            signal = config.INDICATOR_PARAMS["MACD_SIGNAL"]

        macd = MACDIndicator(close=self.df["Close"], window_fast=fast, window_slow=slow, window_sign=signal)
        self.df["MACD"] = macd.macd()
        self.df["MACD_Signal"] = macd.macd_signal()
        self.df["MACD_Diff"] = macd.macd_diff()

        return self.df

    def calculate_bollinger_bands(self, period=None, std=None):
        """
        计算布林带 (Bollinger Bands)

        Args:
            period: 布林带周期
            std: 标准差倍数

        Returns:
            DataFrame: 包含布林带的数据
        """
        if period is None:
            period = config.INDICATOR_PARAMS["BB_PERIOD"]
        if std is None:
            std = config.INDICATOR_PARAMS["BB_STD"]

        bb = BollingerBands(close=self.df["Close"], window=period, window_dev=std)
        self.df["BB_High"] = bb.bollinger_hband()
        self.df["BB_Mid"] = bb.bollinger_mavg()
        self.df["BB_Low"] = bb.bollinger_lband()
        self.df["BB_Width"] = bb.bollinger_wband()
        self.df["BB_Pct"] = bb.bollinger_pband()

        return self.df

    def calculate_stochastic(self, period=None, smooth=None):
        """
        计算随机指标 (Stochastic Oscillator)

        Args:
            period: 周期
            smooth: 平滑周期

        Returns:
            DataFrame: 包含Stochastic的数据
        """
        if period is None:
            period = config.INDICATOR_PARAMS["STOCH_PERIOD"]
        if smooth is None:
            smooth = config.INDICATOR_PARAMS["STOCH_SMOOTH"]

        stoch = StochasticOscillator(
            high=self.df["High"],
            low=self.df["Low"],
            close=self.df["Close"],
            window=period,
            smooth_window=smooth,
        )
        self.df["Stoch_K"] = stoch.stoch()
        self.df["Stoch_D"] = stoch.stoch_signal()

        return self.df

    def calculate_atr(self, period=None):
        """
        计算平均真实波幅 (Average True Range)

        Args:
            period: ATR周期

        Returns:
            DataFrame: 包含ATR的数据
        """
        if period is None:
            period = config.INDICATOR_PARAMS["ATR_PERIOD"]

        atr = AverageTrueRange(
            high=self.df["High"], low=self.df["Low"], close=self.df["Close"], window=period
        )
        self.df["ATR"] = atr.average_true_range()

        return self.df

    def calculate_adx(self, period=None):
        """
        计算平均方向指数 (ADX)

        Args:
            period: ADX周期

        Returns:
            DataFrame: 包含ADX的数据
        """
        if period is None:
            period = 14

        adx = ADXIndicator(
            high=self.df["High"], low=self.df["Low"], close=self.df["Close"], window=period
        )
        self.df["ADX"] = adx.adx()
        self.df["DI+"] = adx.adx_pos()
        self.df["DI-"] = adx.adx_neg()

        return self.df

    def calculate_volume_ma(self, periods=[5, 10, 20]):
        """
        计算成交量移动平均

        Args:
            periods: 周期列表

        Returns:
            DataFrame: 包含成交量MA的数据
        """
        for period in periods:
            self.df[f"Volume_MA{period}"] = (
                self.df["Volume"].rolling(window=period).mean()
            )

        return self.df

    def calculate_all_indicators(self):
        """
        计算所有技术指标

        Returns:
            DataFrame: 包含所有指标的数据
        """
        self.calculate_ma()
        self.calculate_ema()
        self.calculate_rsi()
        self.calculate_macd()
        self.calculate_bollinger_bands()
        self.calculate_stochastic()
        self.calculate_atr()
        self.calculate_adx()
        self.calculate_volume_ma()

        return self.df

    def get_dataframe(self):
        """
        获取包含所有指标的DataFrame

        Returns:
            DataFrame: 完整数据
        """
        return self.df
