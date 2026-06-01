"""币安API数据获取模块"""

import pandas as pd
from binance.client import Client
from datetime import datetime, timedelta
import config
import os
from dotenv import load_dotenv

load_dotenv()


class BinanceDataFetcher:
    """币安数据获取器"""

    def __init__(self):
        """初始化币安客户端"""
        # 从环境变量或config获取API密钥
        api_key = os.getenv("BINANCE_API_KEY") or config.BINANCE_API_KEY
        api_secret = os.getenv("BINANCE_API_SECRET") or config.BINANCE_API_SECRET

        if api_key == "your_api_key_here" or api_secret == "your_api_secret_here":
            # 如果没有设置API密钥，使用公共客户端（无交易功能）
            self.client = Client()
        else:
            self.client = Client(api_key, api_secret)

    def get_klines(
        self,
        symbol=config.DEFAULT_SYMBOL,
        interval=config.DEFAULT_INTERVAL,
        limit=config.DEFAULT_LIMIT,
        start_time=None,
    ):
        """
        获取K线数据

        Args:
            symbol: 交易对 (e.g., 'BTCUSDT')
            interval: K线时间间隔 (e.g., '1h', '1d')
            limit: 获取数据根数 (最多1000)
            start_time: 开始时间，格式：'2025-01-01' 或 datetime对象

        Returns:
            DataFrame: K线数据
        """
        try:
            if start_time:
                if isinstance(start_time, str):
                    start_time = datetime.strptime(start_time, "%Y-%m-%d")
                klines = self.client.get_historical_klines(
                    symbol, interval, start_str=start_time, limit=limit
                )
            else:
                klines = self.client.get_klines(symbol=symbol, interval=interval, limit=limit)

            # 转换为DataFrame
            df = pd.DataFrame(
                klines,
                columns=[
                    "Open Time",
                    "Open",
                    "High",
                    "Low",
                    "Close",
                    "Volume",
                    "Close Time",
                    "Quote Asset Volume",
                    "Number of Trades",
                    "Taker Buy Base Asset Volume",
                    "Taker Buy Quote Asset Volume",
                    "Ignore",
                ],
            )

            # 转换数据类型
            numeric_columns = [
                "Open",
                "High",
                "Low",
                "Close",
                "Volume",
                "Quote Asset Volume",
                "Number of Trades",
                "Taker Buy Base Asset Volume",
                "Taker Buy Quote Asset Volume",
            ]
            for col in numeric_columns:
                df[col] = pd.to_numeric(df[col])

            # 转换时间
            df["Open Time"] = pd.to_datetime(df["Open Time"], unit="ms")
            df["Close Time"] = pd.to_datetime(df["Close Time"], unit="ms")

            # 重新设置索引
            df = df.set_index("Open Time")
            df = df.drop(columns=["Close Time", "Ignore"])

            return df

        except Exception as e:
            print(f"获取数据错误: {e}")
            return None

    def get_latest_price(self, symbol=config.DEFAULT_SYMBOL):
        """
        获取最新价格

        Args:
            symbol: 交易对

        Returns:
            float: 最新价格
        """
        try:
            ticker = self.client.get_symbol_ticker(symbol=symbol)
            return float(ticker["price"])
        except Exception as e:
            print(f"获取价格错误: {e}")
            return None

    def get_symbol_info(self, symbol=config.DEFAULT_SYMBOL):
        """
        获取交易对信息

        Args:
            symbol: 交易对

        Returns:
            dict: 交易对信息
        """
        try:
            info = self.client.get_symbol_info(symbol=symbol)
            return info
        except Exception as e:
            print(f"获取交易对信息错误: {e}")
            return None
