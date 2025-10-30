"""
title: Finnhub_api
author: Avesed
version: 2.0
description: use finnhub api to get stock datas
"""

import requests
import json
from typing import Callable, Any
from pydantic import BaseModel, Field


class Tools:
    class Valves(BaseModel):
        FINNHUB_API_KEY: str = Field(
            default="", description="Finnhub API Key"
        )

    def __init__(self):
        self.valves = self.Valves()

    def finnhub_stock_quote(self, symbol: str) -> str:
        """
        获取股票实时报价

        :param symbol: 股票代码，如 AAPL, TSLA, BINANCE:BTCUSDT
        :return: 股票报价信息
        """
        if not self.valves.FINNHUB_API_KEY:
            return "错误: 请先在工具设置中配置 Finnhub API Key"

        try:
            url = "https://finnhub.io/api/v1/quote"
            params = {"symbol": symbol, "token": self.valves.FINNHUB_API_KEY}
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()

            if not data or data.get("c") == 0:
                return f"未找到股票代码: {symbol}"

            result = f"""
                    {symbol} 股票报价

                    当前价格: ${data.get('c', 'N/A')}
                    最高价: ${data.get('h', 'N/A')}
                    最低价: ${data.get('l', 'N/A')}
                    开盘价: ${data.get('o', 'N/A')}
                    前收盘价: ${data.get('pc', 'N/A')}
                    涨跌: ${data.get('d', 'N/A')} ({data.get('dp', 'N/A')}%)
                    更新时间戳: {data.get('t', 'N/A')}
                    """
            return result.strip()

        except Exception as e:
            return f"获取股票报价失败: {str(e)}"

    def finnhub_company_profile(self, symbol: str) -> str:
        """
        获取公司详细信息 (Profile2)

        :param symbol: 股票代码，如 AAPL, TSLA
        :return: 公司信息
        """
        if not self.valves.FINNHUB_API_KEY:
            return "错误: 请先在工具设置中配置 Finnhub API Key"

        try:
            url = "https://finnhub.io/api/v1/stock/profile2"
            params = {"symbol": symbol, "token": self.valves.FINNHUB_API_KEY}
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()

            if not data:
                return f"未找到公司信息: {symbol}"

            result = f"""
                    {data.get('name', 'N/A')} ({symbol})

                    行业: {data.get('finnhubIndustry', 'N/A')}
                    网站: {data.get('weburl', 'N/A')}
                    国家: {data.get('country', 'N/A')}
                    交易所: {data.get('exchange', 'N/A')}
                    股票代码: {data.get('ticker', 'N/A')}
                    市值: ${data.get('marketCapitalization', 'N/A')}M
                    IPO日期: {data.get('ipo', 'N/A')}
                    电话: {data.get('phone', 'N/A')}
                    股份流通: {data.get('shareOutstanding', 'N/A')}M
                    Logo: {data.get('logo', 'N/A')}                        
                    """
            return result.strip()

        except Exception as e:
            return f"获取公司信息失败: {str(e)}"

    def finnhub_company_peers(self, symbol: str) -> str:
        """
        获取公司同行/竞争对手列表

        :param symbol: 股票代码，如 AAPL, TSLA
        :return: 同行公司列表
        """
        if not self.valves.FINNHUB_API_KEY:
            return "错误: 请先在工具设置中配置 Finnhub API Key"

        try:
            url = "https://finnhub.io/api/v1/stock/peers"
            params = {"symbol": symbol, "token": self.valves.FINNHUB_API_KEY}
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()

            if not data:
                return f"未找到 {symbol} 的同行公司"

            result = f"{symbol} 的同行公司:\n\n"
            result += ", ".join(data)

            return result.strip()

        except Exception as e:
            return f"获取同行公司失败: {str(e)}"

    def finnhub_company_basic_financials(self, symbol: str, metric: str = "all") -> str:
        """
        获取公司基本财务指标

        :param symbol: 股票代码，如 AAPL, TSLA
        :param metric: 指标类型，默认为 all
        :return: 财务指标信息
        """
        if not self.valves.FINNHUB_API_KEY:
            return "错误: 请先在工具设置中配置 Finnhub API Key"

        try:
            url = "https://finnhub.io/api/v1/stock/metric"
            params = {
                "symbol": symbol,
                "metric": metric,
                "token": self.valves.FINNHUB_API_KEY,
            }
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()

            if not data or "metric" not in data:
                return f"未找到 {symbol} 的财务指标"

            metrics = data["metric"]
            result = f"{symbol} 基本财务指标:\n\n"

            # 关键财务指标
            key_metrics = {
                "52周最高": metrics.get("52WeekHigh"),
                "52周最低": metrics.get("52WeekLow"),
                "市盈率 (P/E)": metrics.get("peBasicExclExtraTTM"),
                "每股收益 (EPS)": metrics.get("epsBasicExclExtraItemsTTM"),
                "市净率 (P/B)": metrics.get("pbQuarterly"),
                "资产回报率 (ROA)": metrics.get("roaTTM"),
                "股本回报率 (ROE)": metrics.get("roeTTM"),
                "股息收益率": metrics.get("dividendYieldIndicatedAnnual"),
                "Beta": metrics.get("beta"),
                "市值": metrics.get("marketCapitalization"),
            }

            for key, value in key_metrics.items():
                if value is not None:
                    result += f"{key}: {value}\n"

            return result.strip()

        except Exception as e:
            return f"获取财务指标失败: {str(e)}"

    def finnhub_insider_transactions(self, symbol: str) -> str:
        """
        获取公司内部交易记录

        :param symbol: 股票代码，如 TSLA, AAPL
        :return: 内部交易信息
        """
        if not self.valves.FINNHUB_API_KEY:
            return "错误: 请先在工具设置中配置 Finnhub API Key"

        try:
            url = "https://finnhub.io/api/v1/stock/insider-transactions"
            params = {"symbol": symbol, "token": self.valves.FINNHUB_API_KEY}
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()

            if not data or "data" not in data:
                return f"未找到 {symbol} 的内部交易记录"

            transactions = data["data"][:10]  # 只显示前10条
            result = f"{symbol} 内部交易记录 (最近10条):\n\n"

            for i, txn in enumerate(transactions, 1):
                result += f"{i}. {txn.get('name', 'N/A')}\n"
                result += f"   日期: {txn.get('transactionDate', 'N/A')}\n"
                result += f"   股份: {txn.get('share', 'N/A')}\n"
                result += f"   价格: ${txn.get('transactionPrice', 'N/A')}\n"
                result += f"   类型: {txn.get('transactionCode', 'N/A')}\n\n"

            return result.strip()

        except Exception as e:
            return f"获取内部交易失败: {str(e)}"

    def finnhub_insider_sentiment(
        self, symbol: str, from_date: str = "2023-01-01", to_date: str = "2024-12-31"
    ) -> str:
        """
        获取公司内部交易情绪

        :param symbol: 股票代码，如 TSLA, AAPL
        :param from_date: 开始日期，格式 YYYY-MM-DD
        :param to_date: 结束日期，格式 YYYY-MM-DD
        :return: 内部情绪信息
        """
        if not self.valves.FINNHUB_API_KEY:
            return "错误: 请先在工具设置中配置 Finnhub API Key"

        try:
            url = "https://finnhub.io/api/v1/stock/insider-sentiment"
            params = {
                "symbol": symbol,
                "from": from_date,
                "to": to_date,
                "token": self.valves.FINNHUB_API_KEY,
            }
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()

            if not data or "data" not in data:
                return f"未找到 {symbol} 的内部情绪数据"

            sentiments = data["data"][:5]  # 只显示前5条
            result = f"{symbol} 内部情绪 ({from_date} 到 {to_date}):\n\n"

            for i, sent in enumerate(sentiments, 1):
                result += (
                    f"{i}. {sent.get('year', 'N/A')}-{sent.get('month', 'N/A'):02d}\n"
                )
                result += f"   MSPR (净买入比例): {sent.get('mspr', 'N/A')}\n"
                result += f"   变化: {sent.get('change', 'N/A')}\n\n"

            return result.strip()

        except Exception as e:
            return f"获取内部情绪失败: {str(e)}"

    def finnhub_financials_reported(self, symbol: str, freq: str = "annual") -> str:
        """
        获取公司财务报告 (原始数据)

        :param symbol: 股票代码，如 AAPL, TSLA
        :param freq: 频率 annual (年度) 或 quarterly (季度)
        :return: 财务报告信息
        """
        if not self.valves.FINNHUB_API_KEY:
            return "错误: 请先在工具设置中配置 Finnhub API Key"

        try:
            url = "https://finnhub.io/api/v1/stock/financials-reported"
            params = {
                "symbol": symbol,
                "freq": freq,
                "token": self.valves.FINNHUB_API_KEY,
            }
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()

            if not data or "data" not in data:
                return f"未找到 {symbol} 的财务报告"

            reports = data["data"][:3]  # 只显示最近3条
            result = f"{symbol} 财务报告 ({freq}):\n\n"

            for i, report in enumerate(reports, 1):
                result += f"{i}. 报告期: {report.get('year', 'N/A')}-Q{report.get('quarter', '')}\n"
                result += f"   提交日期: {report.get('filedDate', 'N/A')}\n"
                result += f"   接受日期: {report.get('acceptedDate', 'N/A')}\n"
                result += f"   表格类型: {report.get('form', 'N/A')}\n\n"

            return result.strip()

        except Exception as e:
            return f"获取财务报告失败: {str(e)}"

    def finnhub_recommendation_trends(self, symbol: str) -> str:
        """
        获取分析师推荐趋势

        :param symbol: 股票代码，如 AAPL, TSLA
        :return: 推荐趋势信息
        """
        if not self.valves.FINNHUB_API_KEY:
            return "错误: 请先在工具设置中配置 Finnhub API Key"

        try:
            url = "https://finnhub.io/api/v1/stock/recommendation"
            params = {"symbol": symbol, "token": self.valves.FINNHUB_API_KEY}
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()

            if not data:
                return f"未找到 {symbol} 的推荐信息"

            result = f"{symbol} 分析师推荐趋势:\n\n"

            for i, rec in enumerate(data[:3], 1):  # 显示最近3个月
                result += f"{i}. 期间: {rec.get('period', 'N/A')}\n"
                result += f"   强烈买入: {rec.get('strongBuy', 0)}\n"
                result += f"   买入: {rec.get('buy', 0)}\n"
                result += f"   持有: {rec.get('hold', 0)}\n"
                result += f"   卖出: {rec.get('sell', 0)}\n"
                result += f"   强烈卖出: {rec.get('strongSell', 0)}\n\n"

            return result.strip()

        except Exception as e:
            return f"获取推荐趋势失败: {str(e)}"

    def finnhub_earnings_surprises(self, symbol: str) -> str:
        """
        获取公司历史季度收益惊喜

        :param symbol: 股票代码，如 AAPL, TSLA
        :return: 收益惊喜信息
        """
        if not self.valves.FINNHUB_API_KEY:
            return "错误: 请先在工具设置中配置 Finnhub API Key"

        try:
            url = "https://finnhub.io/api/v1/stock/earnings"
            params = {"symbol": symbol, "token": self.valves.FINNHUB_API_KEY}
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()

            if not data:
                return f"未找到 {symbol} 的收益数据"

            result = f"{symbol} 历史季度收益惊喜:\n\n"

            for i, earning in enumerate(data[:5], 1):  # 显示最近5个季度
                result += f"{i}. 日期: {earning.get('period', 'N/A')}\n"
                result += f"   实际EPS: ${earning.get('actual', 'N/A')}\n"
                result += f"   预期EPS: ${earning.get('estimate', 'N/A')}\n"
                result += f"   惊喜: ${earning.get('surprise', 'N/A')}\n"
                result += f"   惊喜百分比: {earning.get('surprisePercent', 'N/A')}%\n\n"

            return result.strip()

        except Exception as e:
            return f"获取收益惊喜失败: {str(e)}"

    def finnhub_earnings_calendar(
        self, from_date: str = None, to_date: str = None, days: int = 30
    ) -> str:
        """
        获取收益发布日历

        :param from_date: 开始日期，格式 YYYY-MM-DD，默认为今天
        :param to_date: 结束日期，格式 YYYY-MM-DD，默认为未来30天
        :param days: 如果未指定日期，查询未来多少天，默认30天
        :return: 收益日历信息
        """
        if not self.valves.FINNHUB_API_KEY:
            return "错误: 请先在工具设置中配置 Finnhub API Key"

        try:
            from datetime import datetime, timedelta

            # 如果没有提供日期，使用默认值
            if not from_date:
                from_date = datetime.now().strftime("%Y-%m-%d")
            if not to_date:
                to_date = (datetime.now() + timedelta(days=days)).strftime("%Y-%m-%d")

            url = "https://finnhub.io/api/v1/calendar/earnings"
            params = {
                "from": from_date,
                "to": to_date,
                "token": self.valves.FINNHUB_API_KEY,
            }
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()

            if not data or "earningsCalendar" not in data:
                return f"未找到 {from_date} 到 {to_date} 的收益日历"

            calendar = data["earningsCalendar"][:20]  # 显示前20条
            result = f"收益发布日历 ({from_date} 到 {to_date}):\n\n"

            for i, event in enumerate(calendar, 1):
                result += f"{i}. {event.get('symbol', 'N/A')}\n"
                result += f"   日期: {event.get('date', 'N/A')}\n"
                result += f"   预期EPS: ${event.get('epsEstimate', 'N/A')}\n"
                result += f"   盘前/盘后: {event.get('hour', 'N/A')}\n\n"

            return result.strip()

        except Exception as e:
            return f"获取收益日历失败: {str(e)}"

    def finnhub_market_news(self, category: str = "general", limit: int = 5) -> str:
        """
        获取市场新闻

        :param category: 新闻类别 (general, forex, crypto, merger)
        :param limit: 返回新闻数量，默认5条
        :return: 市场新闻列表
        """
        if not self.valves.FINNHUB_API_KEY:
            return "错误: 请先在工具设置中配置 Finnhub API Key"

        try:
            url = "https://finnhub.io/api/v1/news"
            params = {"category": category, "token": self.valves.FINNHUB_API_KEY}
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()

            if not data:
                return "未找到相关新闻"

            result = f"市场新闻 ({category.upper()}):\n\n"

            for i, news in enumerate(data[:limit], 1):
                result += f"{i}. {news.get('headline', 'N/A')}\n"
                result += f"   日期: {news.get('datetime', 'N/A')}\n"
                result += f"   来源: {news.get('source', 'N/A')}\n"
                result += f"   摘要: {news.get('summary', 'N/A')[:200]}...\n"
                result += f"   链接: {news.get('url', '#')}\n\n"
                result += "---\n\n"

            return result.strip()

        except Exception as e:
            return f"获取市场新闻失败: {str(e)}"

    def finnhub_company_news(self, symbol: str, days: int = 7) -> str:
        """
        获取特定公司新闻

        :param symbol: 股票代码
        :param days: 获取最近几天的新闻，默认7天
        :return: 公司新闻列表
        """
        if not self.valves.FINNHUB_API_KEY:
            return "错误: 请先在工具设置中配置 Finnhub API Key"

        try:
            from datetime import datetime, timedelta

            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)

            url = "https://finnhub.io/api/v1/company-news"
            params = {
                "symbol": symbol,
                "from": start_date.strftime("%Y-%m-%d"),
                "to": end_date.strftime("%Y-%m-%d"),
                "token": self.valves.FINNHUB_API_KEY,
            }
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()

            if not data:
                return f"未找到 {symbol} 的相关新闻"

            result = f"{symbol} 公司新闻 (最近{days}天):\n\n"

            for i, news in enumerate(data[:5], 1):
                date = datetime.fromtimestamp(news.get("datetime", 0))
                result += f"{i}. {news.get('headline', 'N/A')}\n"
                result += f"   日期: {date.strftime('%Y-%m-%d %H:%M')}\n"
                result += f"   来源: {news.get('source', 'N/A')}\n"
                result += f"   摘要: {news.get('summary', 'N/A')[:200]}...\n"
                result += f"   链接: {news.get('url', '#')}\n\n"
                result += "---\n\n"

            return result.strip()

        except Exception as e:
            return f"获取公司新闻失败: {str(e)}"

    def finnhub_search_symbol(self, query: str) -> str:
        """
        搜索股票代码

        :param query: 搜索关键词（公司名称或股票代码）
        :return: 匹配的股票列表
        """
        if not self.valves.FINNHUB_API_KEY:
            return "错误: 请先在工具设置中配置 Finnhub API Key"

        try:
            url = "https://finnhub.io/api/v1/search"
            params = {"q": query, "token": self.valves.FINNHUB_API_KEY}
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()

            if not data.get("result"):
                return f"未找到匹配的股票: {query}"

            result = f"搜索结果: {query}\n\n"

            for i, item in enumerate(data["result"][:10], 1):
                result += f"{i}. {item.get('description', 'N/A')}\n"
                result += f"   代码: {item.get('symbol', 'N/A')}\n"
                result += f"   类型: {item.get('type', 'N/A')}\n\n"

            return result.strip()

        except Exception as e:
            return f"搜索失败: {str(e)}"
