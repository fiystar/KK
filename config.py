"""配置文件"""

# Binance API 配置
BINANCE_API_KEY = "your_api_key_here"
BINANCE_API_SECRET = "your_api_secret_here"

# 默认交易对
DEFAULT_SYMBOL = "BTCUSDT"

# K线时间间隔
KLINE_INTERVALS = {
    "1m": "1分钟",
    "5m": "5分钟",
    "15m": "15分钟",
    "1h": "1小时",
    "4h": "4小时",
    "1d": "1天",
    "1w": "1周",
}

# 默认时间间隔
DEFAULT_INTERVAL = "1h"

# 获取数据的默认根数
DEFAULT_LIMIT = 100

# 技术指标参数
INDICATOR_PARAMS = {
    "MA_PERIOD": [5, 10, 20, 50, 100, 200],  # 移动平均线周期
    "EMA_PERIOD": [12, 26],  # 指数移动平均线周期
    "RSI_PERIOD": 14,  # 相对强弱指数周期
    "MACD_FAST": 12,  # MACD快线
    "MACD_SLOW": 26,  # MACD慢线
    "MACD_SIGNAL": 9,  # MACD信号线
    "BB_PERIOD": 20,  # 布林带周期
    "BB_STD": 2,  # 布林带标准差
    "STOCH_PERIOD": 14,  # 随机指标周期
    "STOCH_SMOOTH": 3,  # 随机指标平滑周期
    "ATR_PERIOD": 14,  # 平均真实波幅周期
}

# 输出配置
OUTPUT_FORMAT = "table"  # "table" 或 "json"
EXPORT_TO_CSV = True
EXPORT_TO_JSON = True
