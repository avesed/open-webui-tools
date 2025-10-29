from pydantic import BaseModel, Field
from newsapi import NewsApiClient


class Tools:
    class Valves(BaseModel):
        NEWS_API_KEY: str = Field(
            default="", description="Your News API Key from https://newsapi.org/"
        )

    def __init__(self):
        self.valves = self.Valves()

    def get_top_headlines(
        self,
        q: str = "",
        category: str = "",
        country: str = "",
        sources: str = "",
    ) -> str:
        """
        Get the top headlines for a given category and country.

        :param q: Keywords or a phrase to search for (optional, must be in English)
        :param category: Category of the news - business, entertainment, health, science, sports, technology (optional, do not use to search in general)
        :param country: 2-letter ISO 3166-1 country code, e.g., us, gb, cn (optional, cannot be used with sources)
        :param sources: Comma-separated news sources, e.g., bbc-news,the-verge (optional, cannot be used with country)
        :return: Top headlines articles
        """
        if not self.valves.NEWS_API_KEY:
            return "Error: NEWS_API_KEY is not set. Please configure it in the tool settings."

        if country and sources:
            return "Error: 'country' and 'sources' parameters cannot be used together."

        try:
            api = NewsApiClient(api_key=self.valves.NEWS_API_KEY)

            # Build parameters
            params = {}
            if q:
                params["q"] = q
            if category:
                params["category"] = category
            if country:
                params["country"] = country
            if sources:
                params["sources"] = sources

            # Get top headlines
            result = api.get_top_headlines(**params)

            # Format the response
            if result.get("status") == "ok":
                articles = result.get("articles", [])
                if not articles:
                    return "No articles found."

                formatted_result = f"Found {result.get('totalResults', len(articles))} top headlines:\n\n"
                for idx, article in enumerate(articles[:10], 1):  # Limit to 10 articles
                    formatted_result += (
                        f"**{idx}. {article.get('title', 'No title')}**\n"
                    )
                    formatted_result += f"   Source: {article.get('source', {}).get('name', 'Unknown')}\n"
                    formatted_result += (
                        f"   Published: {article.get('publishedAt', 'Unknown')}\n"
                    )
                    if article.get("description"):
                        formatted_result += f"   {article.get('description')}\n"
                    formatted_result += f"   {article.get('url', 'No URL')}\n\n"

                if len(articles) > 10:
                    formatted_result += f"_Showing 10 of {len(articles)} articles_\n"

                return formatted_result
            else:
                return f"Error: {result.get('message', 'Unknown error')}"

        except Exception as e:
            return f"Error fetching top headlines: {str(e)}"

    def get_everything(
        self,
        q: str = "",
        sources: str = "",
        domains: str = "",
        from_param: str = "",
        to: str = "",
    ) -> str:
        """
        Search through all news articles matching the query.

        :param q: Keywords or a phrase to search for (optional, must be in English)
        :param sources: Comma-separated news sources, e.g., bbc-news,the-verge (optional)
        :param domains: Comma-separated domains, e.g., bbc.co.uk,techcrunch.com (optional)
        :param from_param: Start date in YYYY-MM-DD format, must be within 30 days (optional)
        :param to: End date in YYYY-MM-DD format (optional)
        :return: News articles matching the query
        """
        if not self.valves.NEWS_API_KEY:
            return "Error: NEWS_API_KEY is not set. Please configure it in the tool settings."

        try:
            api = NewsApiClient(api_key=self.valves.NEWS_API_KEY)

            # Build parameters
            params = {}
            if q:
                params["q"] = q
            if sources:
                params["sources"] = sources
            if domains:
                params["domains"] = domains
            if from_param:
                params["from_param"] = from_param
            if to:
                params["to"] = to

            # Get everything
            result = api.get_everything(**params)

            # Format the response
            if result.get("status") == "ok":
                articles = result.get("articles", [])
                if not articles:
                    return "No articles found."

                formatted_result = f"📰 Found {result.get('totalResults', len(articles))} articles:\n\n"
                for idx, article in enumerate(articles[:10], 1):  # Limit to 10 articles
                    formatted_result += (
                        f"**{idx}. {article.get('title', 'No title')}**\n"
                    )
                    formatted_result += f"   Source: {article.get('source', {}).get('name', 'Unknown')}\n"
                    formatted_result += (
                        f"   Published: {article.get('publishedAt', 'Unknown')}\n"
                    )
                    if article.get("description"):
                        formatted_result += f"   {article.get('description')}\n"
                    formatted_result += f"   {article.get('url', 'No URL')}\n\n"

                if len(articles) > 10:
                    formatted_result += f"_Showing 10 of {len(articles)} articles_\n"

                return formatted_result
            else:
                return f"Error: {result.get('message', 'Unknown error')}"

        except Exception as e:
            return f"Error fetching news: {str(e)}"
