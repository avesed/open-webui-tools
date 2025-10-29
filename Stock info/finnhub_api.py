"""
title: Get stock info from Finnhub
author: Avesed
description: Get stock info from Finnhub using their API
version: 1.0.0
"""
from pydantic import BaseModel, Field
from typing import Optional, Literal
import finnhub
import pandas as pd
import json


class Tools:
    class Valves(BaseModel):
        """配置参数 - 用户可以在界面中修改"""

        FINNHUB_API_KEY: str = Field(
            default="",
            description="Finnhub API Key",
        )

    def __init__(self):
        self.valves = self.Valves()

    def _get_client(self):
        """初始化Finnhub客户端"""
        api_key = self.valves.FINNHUB_API_KEY.strip()

        if not api_key:
            return "错误: 请先在工具设置中配置 Finnhub API 密钥。请前往: 工作区 > 工具 > Finnhub Market Data Tool > 设置"

        try:
            return finnhub.Client(api_key=api_key)
        except Exception as e:
            return f"初始化客户端失败: {str(e)}\n请检查 API 密钥是否正确"

    def get_stock_quote(
        self,
        symbol: str,
        __user__: dict = {},
    ) -> str:
        """
        获取股票实时报价信息

        :param symbol: 股票代码，例如 'AAPL', 'TSLA', 'GOOGL'
        :return: 包含当前价格、开盘价、最高价、最低价等信息
        """
        client = self._get_client()
        if isinstance(client, str):
            return client

        try:
            data = client.quote(symbol)
            return f"""
            **{symbol} 股票报价**
            
            当前价格: ${data.get('c', 'N/A')}
            涨跌: ${data.get('d', 'N/A')} ({data.get('dp', 'N/A')}%)
            最高价: ${data.get('h', 'N/A')}
            最低价: ${data.get('l', 'N/A')}
            开盘价: ${data.get('o', 'N/A')}
            前收盘价: ${data.get('pc', 'N/A')}
            时间戳: {data.get('t', 'N/A')}
            """
        except Exception as e:
            return f"获取报价失败: {str(e)}"

    def get_company_profile(
        self,
        symbol: str,
        __user__: dict = {},
    ) -> str:
        """
        获取公司详细资料

        :param symbol: 股票代码，例如 'AAPL', 'MSFT'
        :return: 公司名称、行业、市值、网站等信息
        """
        client = self._get_client()
        if isinstance(client, str):
            return client

        try:
            data = client.company_profile(symbol=symbol)
            return f"""
            **{data.get('name', 'N/A')} ({symbol})**
            
            行业: {data.get('finnhubIndustry', 'N/A')}
            国家: {data.get('country', 'N/A')}
            交易所: {data.get('exchange', 'N/A')}
            市值: ${data.get('marketCapitalization', 'N/A')}M
            IPO日期: {data.get('ipo', 'N/A')}
            股票数: {data.get('shareOutstanding', 'N/A')}M
            网站: {data.get('weburl', 'N/A')}
            电话: {data.get('phone', 'N/A')}
            Logo: {data.get('logo', 'N/A')}
            """
        except Exception as e:
            return f"获取公司资料失败: {str(e)}"

    def get_company_news(
        self,
        symbol: str,
        from_date: str,
        to_date: str,
        __user__: dict = {},
    ) -> str:
        """
        获取公司相关新闻

        :param symbol: 股票代码
        :param from_date: 开始日期 (格式: YYYY-MM-DD)
        :param to_date: 结束日期 (格式: YYYY-MM-DD)
        :return: 新闻列表
        """
        client = self._get_client()
        if isinstance(client, str):
            return client

        try:
            news = client.company_news(symbol, _from=from_date, to=to_date)
            if not news:
                return f"在 {from_date} 至 {to_date} 期间没有找到 {symbol} 的新闻"

            result = f"**{symbol} 公司新闻 ({from_date} 至 {to_date})**\n\n"
            for i, item in enumerate(news[:5], 1):  # 限制显示前5条
                result += f"{i}. **{item.get('headline', 'N/A')}**\n"
                result += f"   日期: {item.get('datetime', 'N/A')}\n"
                result += f"   链接: {item.get('url', 'N/A')}\n"
                result += f"   摘要: {item.get('summary', 'N/A')[:150]}...\n\n"

            return result
        except Exception as e:
            return f"获取新闻失败: {str(e)}"

    def get_stock_candles(
        self,
        symbol: str,
        resolution: Literal["1", "5", "15", "30", "60", "D", "W", "M"],
        from_timestamp: int,
        to_timestamp: int,
        __user__: dict = {},
    ) -> str:
        """
        获取股票K线数据

        :param symbol: 股票代码
        :param resolution: 时间间隔 ('1'=1分钟, '5'=5分钟, 'D'=日, 'W'=周, 'M'=月)
        :param from_timestamp: 开始时间戳 (Unix时间戳)
        :param to_timestamp: 结束时间戳 (Unix时间戳)
        :return: K线数据
        """
        client = self._get_client()
        if isinstance(client, str):
            return client

        try:
            data = client.stock_candles(
                symbol, resolution, from_timestamp, to_timestamp
            )

            if data.get("s") == "no_data":
                return f"没有找到 {symbol} 的K线数据"

            df = pd.DataFrame(data)
            return f"""
            **{symbol} K线数据 (分辨率: {resolution})**
            
            数据点数: {len(df)}
            
            最新数据:
            {df.tail(10).to_string()}
            """
        except Exception as e:
            return f"获取K线数据失败: {str(e)}"

    def get_recommendation_trends(
        self,
        symbol: str,
        __user__: dict = {},
    ) -> str:
        """
        获取分析师推荐趋势

        :param symbol: 股票代码
        :return: 买入/持有/卖出推荐统计
        """
        client = self._get_client()
        if isinstance(client, str):
            return client

        try:
            data = client.recommendation_trends(symbol)
            if not data:
                return f"没有找到 {symbol} 的推荐数据"

            result = f"**{symbol} 分析师推荐趋势**\n\n"
            for item in data[:3]:  # 显示最近3个月
                result += f"**{item.get('period', 'N/A')}**\n"
                result += f"   强力买入: {item.get('strongBuy', 0)}\n"
                result += f"   买入: {item.get('buy', 0)}\n"
                result += f"   持有: {item.get('hold', 0)}\n"
                result += f"   卖出: {item.get('sell', 0)}\n"
                result += f"   强力卖出: {item.get('strongSell', 0)}\n\n"

            return result
        except Exception as e:
            return f"获取推荐趋势失败: {str(e)}"

    def get_company_earnings(
        self,
        symbol: str,
        limit: int = 5,
        __user__: dict = {},
    ) -> str:
        """
        获取公司财报数据

        :param symbol: 股票代码
        :param limit: 返回记录数量，默认5
        :return: 实际EPS vs 预期EPS
        """
        client = self._get_client()
        if isinstance(client, str):
            return client

        try:
            data = client.company_earnings(symbol, limit=limit)
            if not data:
                return f"没有找到 {symbol} 的财报数据"

            result = f"**{symbol} 财报数据**\n\n"
            for item in data:
                actual = item.get("actual", "N/A")
                estimate = item.get("estimate", "N/A")
                surprise = item.get("surprise", "N/A")
                result += f"**{item.get('period', 'N/A')}**\n"
                result += f"   实际EPS: ${actual}\n"
                result += f"   预期EPS: ${estimate}\n"
                result += f"   差异: ${surprise}\n"
                result += f"   惊喜%: {item.get('surprisePercent', 'N/A')}%\n\n"

            return result
        except Exception as e:
            return f"获取财报数据失败: {str(e)}"

    def get_price_target(
        self,
        symbol: str,
        __user__: dict = {},
    ) -> str:
        """
        获取分析师目标价

        :param symbol: 股票代码
        :return: 目标价、最高价、最低价等
        """
        client = self._get_client()
        if isinstance(client, str):
            return client

        try:
            data = client.price_target(symbol)
            return f"""
            **{symbol} 分析师目标价**
            
            目标价: ${data.get('targetMean', 'N/A')}
            最高目标: ${data.get('targetHigh', 'N/A')}
            最低目标: ${data.get('targetLow', 'N/A')}
            目标中位数: ${data.get('targetMedian', 'N/A')}
            分析师数量: {data.get('numberOfAnalysts', 'N/A')}
            更新时间: {data.get('lastUpdated', 'N/A')}
            """
        except Exception as e:
            return f"获取目标价失败: {str(e)}"

    def get_basic_financials(
        self,
        symbol: str,
        __user__: dict = {},
    ) -> str:
        """
        获取基本财务指标

        :param symbol: 股票代码
        :return: PE比率、市值、52周高低点等关键指标
        """
        client = self._get_client()
        if isinstance(client, str):
            return client

        try:
            data = client.company_basic_financials(symbol, "all")
            metrics = data.get("metric", {})

            return f"""
            **{symbol} 基本财务指标**
            
            **估值指标:**
            市盈率(PE): {metrics.get('peBasicExclExtraTTM', 'N/A')}
            市净率(PB): {metrics.get('pbQuarterly', 'N/A')}
            市销率(PS): {metrics.get('psAnnual', 'N/A')}
            
            **市场数据:**
            市值: ${metrics.get('marketCapitalization', 'N/A')}M
            52周最高: ${metrics.get('52WeekHigh', 'N/A')}
            52周最低: ${metrics.get('52WeekLow', 'N/A')}
            
            **盈利能力:**
            ROE: {metrics.get('roeTTM', 'N/A')}%
            ROA: {metrics.get('roaTTM', 'N/A')}%
            利润率: {metrics.get('netProfitMarginTTM', 'N/A')}%
            
            **每股数据:**
            每股收益(EPS): ${metrics.get('epsBasicExclExtraItemsTTM', 'N/A')}
            每股账面价值: ${metrics.get('bookValuePerShareQuarterly', 'N/A')}
            股息收益率: {metrics.get('dividendYieldIndicatedAnnual', 'N/A')}%
            """
        except Exception as e:
            return f"获取财务指标失败: {str(e)}"

    def search_symbol(
        self,
        query: str,
        __user__: dict = {},
    ) -> str:
        """
        搜索股票代码

        :param query: 搜索关键词（公司名称或股票代码）
        :return: 匹配的股票列表
        """
        client = self._get_client()
        if isinstance(client, str):
            return client

        try:
            data = client.symbol_lookup(query)
            results = data.get("result", [])

            if not results:
                return f"没有找到匹配 '{query}' 的股票"

            result = f"**搜索结果: '{query}'**\n\n"
            for item in results[:10]:  # 限制显示前10个
                result += f"**{item.get('description', 'N/A')}**\n"
                result += f"   代码: {item.get('symbol', 'N/A')}\n"
                result += f"   类型: {item.get('type', 'N/A')}\n"
                result += f"   交易所: {item.get('displaySymbol', 'N/A')}\n\n"

            return result
        except Exception as e:
            return f"搜索失败: {str(e)}"

    def get_market_news(
        self,
        category: Literal["general", "forex", "crypto", "merger"] = "general",
        __user__: dict = {},
    ) -> str:
        """
        获取市场新闻

        :param category: 新闻类别 (general, forex, crypto, merger)
        :return: 最新市场新闻
        """
        client = self._get_client()
        if isinstance(client, str):
            return client

        try:
            news = client.general_news(category, min_id=0)
            if not news:
                return f"没有找到 {category} 类别的新闻"

            result = f"**市场新闻 - {category.upper()}**\n\n"
            for i, item in enumerate(news[:5], 1):
                result += f"{i}. **{item.get('headline', 'N/A')}**\n"
                result += f"   日期: {item.get('datetime', 'N/A')}\n"
                result += f"   链接: {item.get('url', 'N/A')}\n"
                result += f"   摘要: {item.get('summary', 'N/A')[:150]}...\n\n"

            return result
        except Exception as e:
            return f"获取市场新闻失败: {str(e)}"

    def get_stock_peers(
        self,
        symbol: str,
        __user__: dict = {},
    ) -> str:
        """
        获取同行公司列表

        :param symbol: 股票代码
        :return: 相同行业的竞争对手
        """
        client = self._get_client()
        if isinstance(client, str):
            return client

        try:
            peers = client.company_peers(symbol)
            if not peers:
                return f"没有找到 {symbol} 的同行公司"

            result = f"**{symbol} 的同行公司**\n\n"
            result += ", ".join(peers)

            return result
        except Exception as e:
            return f"获取同行公司失败: {str(e)}"
