# KK - K线识别分析工具

一个基于Python的专业级K线识别分析工具，使用币安API实时获取数据，支持完整的技术指标计算和K线形态识别。

## 功能特性

### 📊 技术指标分析
- **移动平均线 (MA)**: 支持多周期SMA
- **指数移动平均 (EMA)**: 快速和慢速EMA
- **相对强弱指数 (RSI)**: 超买超卖信号
- **MACD**: 趋势和动量分析
- **布林带 (Bollinger Bands)**: 波动性分析
- **随机指标 (Stochastic)**: K值和D值
- **平均真实波幅 (ATR)**: 波动性测量
- **平均方向指数 (ADX)**: 趋势强度
- **成交量分析**: 成交量移动平均

### 🎯 K线形态识别
- **十字星 (Cross)**: 开盘价等于收盘价
- **锤子线 (Hammer)**: 小实体，下影线长
- **上吊线 (Hanging Man)**: 下降趋势中的锤子线
- **看涨吞没 (Bullish Engulfing)**: 反转信号
- **看跌吞没 (Bearish Engulfing)**: 反转信号
- **晨星 (Morning Star)**: 三根K线的看涨形态
- **黄昏星 (Evening Star)**: 三根K线的看跌形态
- **看涨孕线 (Bullish Harami)**: 反转信号
- **看跌孕线 (Bearish Harami)**: 反转信号
- **射击之星 (Shooting Star)**: 小实体，上影线长
- **倒锤线 (Inverted Hammer)**: 上升趋势中的射击之星
- **道氏线 (Doji)**: 犹豫信号

### 💾 数据导出
- CSV格式导出
- JSON格式导出
- 支持自定义文件名

## 项目结构

```
KK/
├── main.py                 # 主程序入口
├── analyzer.py            # 综合分析模块
├── indicators.py          # 技术指标计算模块
├── patterns.py            # K线形态识别模块
├── binance_api.py         # 币安API数据获取模块
├── config.py              # 配置文件
├── requirements.txt       # 依赖包列表
├── .gitignore            # Git忽略文件
└── README.md             # 本文件
```

## 安装说明

### 系统要求
- Python 3.8+
- pip (Python包管理工具)

### 步骤1: 克隆仓库

```bash
git clone https://github.com/fiystar/KK.git
cd KK
```

### 步骤2: 创建虚拟环境 (推荐)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 步骤3: 安装依赖

```bash
pip install -r requirements.txt
```

### 步骤4: 配置API密钥 (可选)

如果需要使用币安API的交易功能，编辑 `config.py`：

```python
BINANCE_API_KEY = "your_api_key_here"
BINANCE_API_SECRET = "your_api_secret_here"
```

或创建 `.env` 文件：

```
BINANCE_API_KEY=your_api_key_here
BINANCE_API_SECRET=your_api_secret_here
```

## 使用方法

### 基础使用

```bash
python main.py
```

这将：
1. 使用默认配置 (BTCUSDT, 1小时K线, 100根)
2. 获取币安数据
3. 计算所有技术指标
4. 识别K线形态
5. 显示分析结果
6. 导出到CSV和JSON

### 自定义分析

```python
from analyzer import KlineAnalyzer
import config

# 创建分析器
analyzer = KlineAnalyzer(symbol="ETHUSDT", interval="4h")

# 获取数据
analyzer.fetch_data(limit=200)

# 分析指标
analyzer.analyze_indicators()

# 识别形态
analyzer.analyze_patterns()

# 获取最新信号
latest = analyzer.get_latest_signals(rows=10)
print(latest)

# 导出数据
analyzer.export_to_csv("ethusdt_analysis.csv")
analyzer.export_to_json("ethusdt_analysis.json")

# 打印摘要
analyzer.print_summary()
```

### 高级用法

#### 获取特定时间段的数据

```python
from analyzer import KlineAnalyzer

analyzer = KlineAnalyzer(symbol="BTCUSDT", interval="1d")
analyzer.fetch_data(limit=365, start_time="2024-01-01")
analyzer.analyze_indicators()
analyzer.analyze_patterns()
```

#### 只计算特定指标

```python
from indicators import TechnicalIndicators
import binance_api
import config

fetcher = binance_api.BinanceDataFetcher()
df = fetcher.get_klines(limit=100)

indicators = TechnicalIndicators(df)
indicators.calculate_rsi()
indicators.calculate_macd()
indicators.calculate_bollinger_bands()

result = indicators.get_dataframe()
```

#### 只识别特定形态

```python
from patterns import CandlestickPatterns
import binance_api

fetcher = binance_api.BinanceDataFetcher()
df = fetcher.get_klines(limit=100)

patterns = CandlestickPatterns(df)

# 检查特定K线是否是锤子线
if patterns.is_hammer(50):
    print("发现锤子线！")

# 识别所有形态
patterns.recognize_all_patterns()
summary = patterns.get_pattern_summary()
print(summary)
```

## 配置文件说明

### config.py 主要配置项

```python
# 默认交易对
DEFAULT_SYMBOL = "BTCUSDT"

# K线时间间隔
DEFAULT_INTERVAL = "1h"  # 1m, 5m, 15m, 1h, 4h, 1d, 1w

# 获取数据的默认根数
DEFAULT_LIMIT = 100

# 技术指标参数
INDICATOR_PARAMS = {
    "MA_PERIOD": [5, 10, 20, 50, 100, 200],
    "EMA_PERIOD": [12, 26],
    "RSI_PERIOD": 14,
    # ... 更多参数
}

# 是否导出数据
EXPORT_TO_CSV = True
EXPORT_TO_JSON = True
```

## API参考

### BinanceDataFetcher

```python
fetcher = BinanceDataFetcher()

# 获取K线数据
df = fetcher.get_klines(
    symbol="BTCUSDT",
    interval="1h",
    limit=100,
    start_time="2025-01-01"
)

# 获取最新价格
price = fetcher.get_latest_price(symbol="BTCUSDT")

# 获取交易对信息
info = fetcher.get_symbol_info(symbol="BTCUSDT")
```

### TechnicalIndicators

```python
indicator = TechnicalIndicators(df)

# 计算指标
indicator.calculate_ma(periods=[5, 10, 20])
indicator.calculate_rsi(period=14)
indicator.calculate_macd()
indicator.calculate_bollinger_bands()
# ... 更多指标

# 一次计算所有指标
indicator.calculate_all_indicators()

result = indicator.get_dataframe()
```

### CandlestickPatterns

```python
patterns = CandlestickPatterns(df)

# 单个检查
if patterns.is_hammer(idx):
    print("是锤子线")

# 识别所有形态
patterns.recognize_all_patterns()

# 获取摘要
summary = patterns.get_pattern_summary()

result = patterns.get_dataframe()
```

### KlineAnalyzer

```python
analyzer = KlineAnalyzer(symbol="BTCUSDT", interval="1h")

# 获取数据
analyzer.fetch_data(limit=100)

# 分析
analyzer.analyze_indicators()
analyzer.analyze_patterns()

# 获取最新信号
latest = analyzer.get_latest_signals(rows=5)

# 导出
analyzer.export_to_csv("output.csv")
analyzer.export_to_json("output.json")

# 打印摘要
analyzer.print_summary()
```

## 示例输出

### 终端输出示例

```
============================================================
              K线识别分析工具
============================================================

初始化分析器...

获取数据...
正在���取 BTCUSDT 1h 的K线数据...
成功获取 100 根K线

分析技术指标...
正在计算技术指标...
技术指标计算完成

识别K线形态...
正在识别K线形态...
K线形态识别完成

------------------------------------------------------------
最近 5 根K线数据
------------------------------------------------------------
Open        High        Low         Close       Volume  ...
45000.50    45500.00    44900.00    45250.00    1000.5  ...
...

------------------------------------------------------------
K线详细分析
------------------------------------------------------------

价格信息:
  开盘价: 45000.5000
  最高价: 45500.0000
  最低价: 44900.0000
  收盘价: 45250.0000
  幅度: 0.56%

技术指标 (最新):
  RSI: 65.45
  MACD: 250.3456 (信号线: 240.1234)
  随机指标K: 75.32
  随机指标D: 72.45
  ATR: 450.50
  ADX: 35.67

K线形态识别 (最新):
  ✓ 看涨吞没
  ✓ Hammer

============================================================
分析完成！
```

## 常见问题 (FAQ)

### Q: 如何修改默认交易对?
A: 编辑 `config.py` 中的 `DEFAULT_SYMBOL`，例如：
```python
DEFAULT_SYMBOL = "ETHUSDT"  # 改为以太坊
```

### Q: 支持哪些K线时间间隔?
A: 支持以下间隔：
- `1m` - 1分钟
- `5m` - 5分钟  
- `15m` - 15分钟
- `1h` - 1小时
- `4h` - 4小时
- `1d` - 1天
- `1w` - 1周

### Q: 如何获得更多历史数据?
A: 修改 `fetch_data()` 的 `limit` 参数：
```python
analyzer.fetch_data(limit=1000)  # 最多1000根
```

### Q: 数据在哪里导出?
A: 默认导出到程序所在目录，文件名为 `{SYMBOL}_{INTERVAL}.csv` 和 `{SYMBOL}_{INTERVAL}.json`

### Q: 如何禁用数据导出?
A: 编辑 `config.py`：
```python
EXPORT_TO_CSV = False
EXPORT_TO_JSON = False
```

## 依赖包说明

| 包名 | 版本 | 用途 |
|------|------|------|
| python-binance | 1.0.17 | 币安API |
| pandas | 2.0.3 | 数据处理 |
| numpy | 1.24.3 | 数值计算 |
| ta | 0.10.2 | 技术分析指标 |
| matplotlib | 3.7.2 | 数据可视化 |
| seaborn | 0.12.2 | 高级可视化 |
| requests | 2.31.0 | HTTP请求 |
| colorama | 0.4.6 | 终端彩色输出 |
| python-dotenv | 1.0.0 | 环境变量管理 |

## 许可证

MIT License

## 贡献

欢迎提交Issue和Pull Request！

## 联系方式

- GitHub: [fiystar](https://github.com/fiystar)
- 项目地址: [KK](https://github.com/fiystar/KK)

## 免责声明

本工具仅供学习和研究使用。使用者应自行承担使用本工具进行交易或投资决策的所有风险。作者不对因使用本工具而产生的任何直接或间接损失负责。

---

**更新时间**: 2025年
**版本**: 1.0.0
