"""K线形态识别模块"""

import pandas as pd
import numpy as np


class CandlestickPatterns:
    """K线形态识别器"""

    def __init__(self, df):
        """
        初始化形态识别器

        Args:
            df: 包含OHLCV数据的DataFrame
        """
        self.df = df.copy()
        self.patterns = {}

    def _is_long_body(self, idx, threshold=0.5):
        """判断是否为长实体"""
        body = abs(self.df["Close"].iloc[idx] - self.df["Open"].iloc[idx])
        high_low = self.df["High"].iloc[idx] - self.df["Low"].iloc[idx]
        return body / high_low > threshold if high_low > 0 else False

    def _is_small_body(self, idx, threshold=0.3):
        """判断是否为小实体"""
        body = abs(self.df["Close"].iloc[idx] - self.df["Open"].iloc[idx])
        high_low = self.df["High"].iloc[idx] - self.df["Low"].iloc[idx]
        return body / high_low < threshold if high_low > 0 else True

    def _upper_shadow_ratio(self, idx):
        """计算上影线比例"""
        close = max(self.df["Close"].iloc[idx], self.df["Open"].iloc[idx])
        upper_shadow = self.df["High"].iloc[idx] - close
        high_low = self.df["High"].iloc[idx] - self.df["Low"].iloc[idx]
        return upper_shadow / high_low if high_low > 0 else 0

    def _lower_shadow_ratio(self, idx):
        """计算下影线比例"""
        open_close = min(self.df["Close"].iloc[idx], self.df["Open"].iloc[idx])
        lower_shadow = open_close - self.df["Low"].iloc[idx]
        high_low = self.df["High"].iloc[idx] - self.df["Low"].iloc[idx]
        return lower_shadow / high_low if high_low > 0 else 0

    def is_cross(self, idx):
        """十字星: 开盘价等于收盘价"""
        return abs(self.df["Open"].iloc[idx] - self.df["Close"].iloc[idx]) < 0.0001

    def is_hammer(self, idx):
        """锤子线: 小实体，下影线长，上影线短"""
        if idx < 1:
            return False
        return (
            self._is_small_body(idx)
            and self._lower_shadow_ratio(idx) > 0.6
            and self._upper_shadow_ratio(idx) < 0.2
        )

    def is_hanging_man(self, idx):
        """上吊线: 小实体，下影线长，上影线短（出现在上升趋势）"""
        return self.is_hammer(idx)  # 形态相同，上下文不同

    def is_engulfing_bullish(self, idx):
        """看涨吞没: 前一根为阴线，当前根为阳线且完全吞没前一根"""
        if idx < 1:
            return False
        prev_open = self.df["Open"].iloc[idx - 1]
        prev_close = self.df["Close"].iloc[idx - 1]
        curr_open = self.df["Open"].iloc[idx]
        curr_close = self.df["Close"].iloc[idx]

        # 前一根是阴线，当前根是阳线
        prev_is_bearish = prev_close < prev_open
        curr_is_bullish = curr_close > curr_open

        # 当前根完全吞没前一根
        engulfing = curr_open <= prev_close and curr_close >= prev_open

        return prev_is_bearish and curr_is_bullish and engulfing

    def is_engulfing_bearish(self, idx):
        """看跌吞没: 前一根为阳线，当前根为阴线且完全吞没前一根"""
        if idx < 1:
            return False
        prev_open = self.df["Open"].iloc[idx - 1]
        prev_close = self.df["Close"].iloc[idx - 1]
        curr_open = self.df["Open"].iloc[idx]
        curr_close = self.df["Close"].iloc[idx]

        # 前一根是阳线，当前根是阴线
        prev_is_bullish = prev_close > prev_open
        curr_is_bearish = curr_close < curr_open

        # 当前根完全吞没前一根
        engulfing = curr_open >= prev_close and curr_close <= prev_open

        return prev_is_bullish and curr_is_bearish and engulfing

    def is_morning_star(self, idx):
        """晨星: 三根K线，第一根阴线，第二根小实体低开，第三根阳线"""
        if idx < 2:
            return False
        k1_close = self.df["Close"].iloc[idx - 2]
        k1_open = self.df["Open"].iloc[idx - 2]
        k2_close = self.df["Close"].iloc[idx - 1]
        k2_open = self.df["Open"].iloc[idx - 1]
        k3_close = self.df["Close"].iloc[idx]
        k3_open = self.df["Open"].iloc[idx]

        return (
            k1_close < k1_open  # 第一根是阴线
            and self._is_small_body(idx - 1)  # 第二根是小实体
            and k2_close < k1_close and k2_open < k1_close  # 第二根低开
            and k3_close > k3_open  # 第三根是阳线
            and k3_close > k1_open  # 第三根收于第一根开盘价上方
        )

    def is_evening_star(self, idx):
        """黄昏星: 三根K线，第一根阳线，第二根小实体高开，第三根阴线"""
        if idx < 2:
            return False
        k1_close = self.df["Close"].iloc[idx - 2]
        k1_open = self.df["Open"].iloc[idx - 2]
        k2_close = self.df["Close"].iloc[idx - 1]
        k2_open = self.df["Open"].iloc[idx - 1]
        k3_close = self.df["Close"].iloc[idx]
        k3_open = self.df["Open"].iloc[idx]

        return (
            k1_close > k1_open  # 第一根是阳线
            and self._is_small_body(idx - 1)  # 第二根是小实体
            and k2_close > k1_close and k2_open > k1_close  # 第二根高开
            and k3_close < k3_open  # 第三根是阴线
            and k3_close < k1_open  # 第三根收于第一根开盘价下方
        )

    def is_bullish_harami(self, idx):
        """看涨孕线: 前一根长阴线，当前根小阳线包含在前一根内"""
        if idx < 1:
            return False
        prev_open = self.df["Open"].iloc[idx - 1]
        prev_close = self.df["Close"].iloc[idx - 1]
        curr_open = self.df["Open"].iloc[idx]
        curr_close = self.df["Close"].iloc[idx]

        return (
            self._is_long_body(idx - 1)
            and prev_close < prev_open  # 前一根是阴线
            and curr_close > curr_open  # 当前根是阳线
            and curr_open >= prev_close
            and curr_close <= prev_open  # 当前根包含在前一根内
        )

    def is_bearish_harami(self, idx):
        """看跌孕线: 前一根长阳线，当前根小阴线包含在前一根内"""
        if idx < 1:
            return False
        prev_open = self.df["Open"].iloc[idx - 1]
        prev_close = self.df["Close"].iloc[idx - 1]
        curr_open = self.df["Open"].iloc[idx]
        curr_close = self.df["Close"].iloc[idx]

        return (
            self._is_long_body(idx - 1)
            and prev_close > prev_open  # 前一根是阳线
            and curr_close < curr_open  # 当前根是阴线
            and curr_open <= prev_close
            and curr_close >= prev_open  # 当前根包含在前一根内
        )

    def is_shooting_star(self, idx):
        """射击之星: 小实体，上影线长，下影线短"""
        if idx < 1:
            return False
        return (
            self._is_small_body(idx)
            and self._upper_shadow_ratio(idx) > 0.6
            and self._lower_shadow_ratio(idx) < 0.2
        )

    def is_inverted_hammer(self, idx):
        """倒锤线: 小实体，上影线长，下影线短（出现在下降趋势）"""
        return self.is_shooting_star(idx)  # 形态相同，上下文不同

    def is_doji(self, idx, threshold=0.01):
        """道氏线: 开盘价和收盘价几乎相同"""
        body = abs(self.df["Close"].iloc[idx] - self.df["Open"].iloc[idx])
        high_low = self.df["High"].iloc[idx] - self.df["Low"].iloc[idx]
        return body / high_low < threshold if high_low > 0 else False

    def recognize_all_patterns(self):
        """
        识别所有K线形态

        Returns:
            DataFrame: 包含所有形态的识别结果
        """
        pattern_cols = [
            "Cross",
            "Hammer",
            "HangingMan",
            "EngulfingBullish",
            "EngulfingBearish",
            "MorningStar",
            "EveningStar",
            "BullishHarami",
            "BearishHarami",
            "ShootingStar",
            "InvertedHammer",
            "Doji",
        ]

        for col in pattern_cols:
            self.df[col] = 0

        for idx in range(len(self.df)):
            if self.is_cross(idx):
                self.df["Cross"].iloc[idx] = 1
            if self.is_hammer(idx):
                self.df["Hammer"].iloc[idx] = 1
            if self.is_hanging_man(idx):
                self.df["HangingMan"].iloc[idx] = 1
            if self.is_engulfing_bullish(idx):
                self.df["EngulfingBullish"].iloc[idx] = 1
            if self.is_engulfing_bearish(idx):
                self.df["EngulfingBearish"].iloc[idx] = 1
            if self.is_morning_star(idx):
                self.df["MorningStar"].iloc[idx] = 1
            if self.is_evening_star(idx):
                self.df["EveningStar"].iloc[idx] = 1
            if self.is_bullish_harami(idx):
                self.df["BullishHarami"].iloc[idx] = 1
            if self.is_bearish_harami(idx):
                self.df["BearishHarami"].iloc[idx] = 1
            if self.is_shooting_star(idx):
                self.df["ShootingStar"].iloc[idx] = 1
            if self.is_inverted_hammer(idx):
                self.df["InvertedHammer"].iloc[idx] = 1
            if self.is_doji(idx):
                self.df["Doji"].iloc[idx] = 1

        return self.df

    def get_pattern_summary(self):
        """
        获取形态识别摘要

        Returns:
            dict: 各形态出现次数
        """
        pattern_cols = [
            "Cross",
            "Hammer",
            "HangingMan",
            "EngulfingBullish",
            "EngulfingBearish",
            "MorningStar",
            "EveningStar",
            "BullishHarami",
            "BearishHarami",
            "ShootingStar",
            "InvertedHammer",
            "Doji",
        ]

        summary = {}
        for col in pattern_cols:
            if col in self.df.columns:
                summary[col] = int(self.df[col].sum())
            else:
                summary[col] = 0

        return summary

    def get_dataframe(self):
        """
        获取包含所有形态的DataFrame

        Returns:
            DataFrame: 完整数据
        """
        return self.df
