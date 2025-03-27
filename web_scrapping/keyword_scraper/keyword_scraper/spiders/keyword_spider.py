import scrapy


class KeywordSpiderSpider(scrapy.Spider):
    name = "keyword_spider"
    allowed_domains = ["www.scrapmonster.com"]
    start_urls = ["https://www.scrapmonster.com/companies"]

keywords = ["python", "scrapy", "web scraping"]  # Define your keywords

def parse(self, response):
    for keyword in self.keywords:
        if keyword.lower() in response.text.lower():
            yield {
                "url": response.url,
                "keyword": keyword,
                "content": response.text[:500],  # Get snippet of the content
            }

# run the spider in terminal
# scrapy crawl keyword_spider -o web_scrapping_results.json
