"""主程序入口"""

from analyzer import KlineAnalyzer
import config
from colorama import init, Fore, Style
import pandas as pd

init()  # 初始化colorama


def print_header(text):
    """打印标题"""
    print(f"\n{Fore.CYAN}{'=' * 60}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{text.center(60)}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'=' * 60}{Style.RESET_ALL}")


def print_section(text):
    """打印分段标题"""
    print(f"\n{Fore.GREEN}{text}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}{'-' * len(text)}{Style.RESET_ALL}")


def display_latest_data(analyzer, rows=5):
    """显示最新数据"""
    print_section(f"最近 {rows} 根K线数据")
    latest = analyzer.get_latest_signals(rows=rows)

    if latest is not None:
        # 格式化显示
        pd.set_option("display.max_columns", None)
        pd.set_option("display.width", None)
        pd.set_option("display.max_colwidth", None)
        print(latest.to_string())
    else:
        print("获取数据失败")


def display_candlestick_info(analyzer):
    """显示K线详细信息"""
    print_section("K线详细分析")

    if analyzer.df is None or len(analyzer.df) == 0:
        print("没有数据")
        return

    latest = analyzer.df.iloc[-1]

    print(f"\n{Fore.YELLOW}价格信息:{Style.RESET_ALL}")
    print(f"  开盘价: {latest['Open']:.4f}")
    print(f"  最高价: {latest['High']:.4f}")
    print(f"  最低价: {latest['Low']:.4f}")
    print(f"  收盘价: {latest['Close']:.4f}")
    print(f"  幅度: {((latest['Close'] - latest['Open']) / latest['Open'] * 100):.2f}%")

    print(f"\n{Fore.YELLOW}技术指标 (最新):{Style.RESET_ALL}")
    indicators = [
        ("RSI", "RSI"),
        ("MACD", "MACD"),
        ("MACD信号线", "MACD_Signal"),
        ("MACD柱状图", "MACD_Diff"),
        ("随机指标K", "Stoch_K"),
        ("随机指标D", "Stoch_D"),
        ("ATR", "ATR"),
        ("ADX", "ADX"),
        ("平均成交量(20)", "Volume_MA20"),
    ]

    for label, col in indicators:
        if col in latest and pd.notna(latest[col]):
            print(f"  {label}: {latest[col]:.4f}")

    print(f"\n{Fore.YELLOW}K线形态识别 (最新):{Style.RESET_ALL}")
    patterns = [
        ("十字星", "Cross"),
        ("锤子线", "Hammer"),
        ("上吊线", "HangingMan"),
        ("看涨吞没", "EngulfingBullish"),
        ("看跌吞没", "EngulfingBearish"),
        ("晨星", "MorningStar"),
        ("黄昏星", "EveningStar"),
        ("看涨孕线", "BullishHarami"),
        ("看跌孕线", "BearishHarami"),
        ("射击之星", "ShootingStar"),
        ("倒锤线", "InvertedHammer"),
        ("道氏线", "Doji"),
    ]

    found_patterns = False
    for label, col in patterns:
        if col in latest and latest[col] == 1:
            print(f"  {Fore.GREEN}✓ {label}{Style.RESET_ALL}")
            found_patterns = True

    if not found_patterns:
        print(f"  {Fore.YELLOW}未发现特殊形态{Style.RESET_ALL}")


def main():
    """主函数"""
    print_header("K线识别分析工具")

    # 创建分析器
    print(f"\n{Fore.YELLOW}初始化分析器...{Style.RESET_ALL}")
    analyzer = KlineAnalyzer(
        symbol=config.DEFAULT_SYMBOL, interval=config.DEFAULT_INTERVAL
    )

    # 获取数据
    print(f"\n{Fore.YELLOW}获取数据...{Style.RESET_ALL}")
    if not analyzer.fetch_data(limit=config.DEFAULT_LIMIT):
        print(f"{Fore.RED}数据获取失败{Style.RESET_ALL}")
        return

    # 分析技术指标
    print(f"\n{Fore.YELLOW}分析技术指标...{Style.RESET_ALL}")
    analyzer.analyze_indicators()

    # 分析K线形态
    print(f"\n{Fore.YELLOW}识别K线形态...{Style.RESET_ALL}")
    analyzer.analyze_patterns()

    # 显示结果
    display_latest_data(analyzer, rows=5)
    display_candlestick_info(analyzer)

    # 打印摘要
    analyzer.print_summary()

    # 导出数据
    if config.EXPORT_TO_CSV:
        analyzer.export_to_csv()
    if config.EXPORT_TO_JSON:
        analyzer.export_to_json()

    print(f"\n{Fore.GREEN}分析完成！{Style.RESET_ALL}\n")


if __name__ == "__main__":
    main()
