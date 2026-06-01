"""K线综合分析模块"""

import pandas as pd
from binance_api import BinanceDataFetcher
from indicators import TechnicalIndicators
from patterns import CandlestickPatterns
import config


class KlineAnalyzer:
    """K线综合分析器"""

    def __init__(self, symbol=config.DEFAULT_SYMBOL, interval=config.DEFAULT_INTERVAL):
        """
        初始化分析器

        Args:
            symbol: 交易对
            interval: K线时间间隔
        """
        self.symbol = symbol
        self.interval = interval
        self.df = None
        self.fetcher = BinanceDataFetcher()

    def fetch_data(self, limit=config.DEFAULT_LIMIT, start_time=None):
        """
        获取K线数据

        Args:
            limit: 数据根数
            start_time: 开始时间

        Returns:
            bool: 是否成功
        """
        print(f"正在获取 {self.symbol} {self.interval} 的K线数据...")
        self.df = self.fetcher.get_klines(
            symbol=self.symbol, interval=self.interval, limit=limit, start_time=start_time
        )

        if self.df is not None and len(self.df) > 0:
            print(f"成功获取 {len(self.df)} 根K线")
            return True
        else:
            print("获取数据失败")
            return False

    def analyze_indicators(self):
        """
        分析技术指标

        Returns:
            DataFrame: 包含指标的数据
        """
        if self.df is None or len(self.df) == 0:
            print("错误: 请先获取K线数据")
            return None

        print("正在计算技术指标...")
        indicator = TechnicalIndicators(self.df)
        self.df = indicator.calculate_all_indicators()
        print("技术指标计算完成")
        return self.df

    def analyze_patterns(self):
        """
        分析K线形态

        Returns:
            DataFrame: 包含形态识别结果的数据
        """
        if self.df is None or len(self.df) == 0:
            print("错误: 请先获取K线数据")
            return None

        print("正在识别K线形态...")
        patterns = CandlestickPatterns(self.df)
        self.df = patterns.recognize_all_patterns()
        print("K线形态识别完成")
        return self.df

    def get_latest_signals(self, rows=5):
        """
        获取最新交易信号

        Args:
            rows: 返回最近几行数据

        Returns:
            DataFrame: 最新的信号数据
        """
        if self.df is None or len(self.df) == 0:
            print("错误: 没有数据")
            return None

        # 选择关键列
        key_cols = [
            "Open",
            "High",
            "Low",
            "Close",
            "Volume",
            "RSI",
            "MACD",
            "MACD_Signal",
            "BB_High",
            "BB_Mid",
            "BB_Low",
            "EngulfingBullish",
            "EngulfingBearish",
            "Hammer",
            "ShootingStar",
            "Doji",
        ]

        available_cols = [col for col in key_cols if col in self.df.columns]
        return self.df[available_cols].tail(rows)

    def export_to_csv(self, filename=None):
        """
        导出数据到CSV

        Args:
            filename: 文件名

        Returns:
            bool: 是否成功
        """
        if self.df is None or len(self.df) == 0:
            print("错误: 没有数据")
            return False

        if filename is None:
            filename = f"{self.symbol}_{self.interval}.csv"

        try:
            self.df.to_csv(filename)
            print(f"数据已导出到 {filename}")
            return True
        except Exception as e:
            print(f"导出失败: {e}")
            return False

    def export_to_json(self, filename=None):
        """
        导出数据到JSON

        Args:
            filename: 文件名

        Returns:
            bool: 是否成功
        """
        if self.df is None or len(self.df) == 0:
            print("错误: 没有数据")
            return False

        if filename is None:
            filename = f"{self.symbol}_{self.interval}.json"

        try:
            self.df.to_json(filename, orient="index", indent=2)
            print(f"数据已导出到 {filename}")
            return True
        except Exception as e:
            print(f"导出失败: {e}")
            return False

    def print_summary(self):
        """
        打印分析摘要
        """
        if self.df is None or len(self.df) == 0:
            print("错误: 没有数据")
            return

        print("\n" + "=" * 50)
        print(f"K线分析摘要 - {self.symbol} ({self.interval})")
        print("=" * 50)

        # 最新价格信息
        latest = self.df.iloc[-1]
        print(f"\n最新价格: {latest['Close']:.2f}")
        print(f"最高: {latest['High']:.2f} | 最低: {latest['Low']:.2f}")
        print(f"成交量: {latest['Volume']:.0f}")

        # 技术指标
        print(f"\n技术指标 (最新):")
        if "RSI" in latest:
            print(f"  RSI: {latest['RSI']:.2f}")
        if "MACD" in latest:
            print(f"  MACD: {latest['MACD']:.4f} (信号线: {latest['MACD_Signal']:.4f})")
        if "BB_High" in latest:
            print(f"  布林带: {latest['BB_Low']:.2f} - {latest['BB_High']:.2f}")

        # K线形态识别
        print(f"\nK线形态识别 (最新):")
        patterns_list = [
            "EngulfingBullish",
            "EngulfingBearish",
            "Hammer",
            "ShootingStar",
            "Doji",
            "MorningStar",
            "EveningStar",
        ]
        found_patterns = False
        for pattern in patterns_list:
            if pattern in latest and latest[pattern] == 1:
                print(f"  ✓ {pattern}")
                found_patterns = True
        if not found_patterns:
            print("  没有发现特殊形态")

        print("\n" + "=" * 50)
