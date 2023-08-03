from pathlib import Path

import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        urls = [
            "https://quotes.toscrape.com/page/1/",
            "https://quotes.toscrape.com/page/2/",
        ]

        # return [url for url in urls] # wnt work
        # return [scrapy.Request(url=url, callback=self.parse) for url in urls] # work as well

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # scrapping data
        for quote in response.css("div.quote"):
            author_links = quote.css(".author + a")
            yield from response.follow_all(author_links, self.parse_author)
            yield {
                "author": quote.css("small.author::text").get(),
                "text": quote.css("span.text::text").get(),
                "tags": quote.css("div.tags a.tag::text").getall(),
            }

        # follow next url(s)
        next_page = response.css("li.next a::attr(href)").get()

        # if next_page is not None:
        #     next_page = response.urljoin(next_page)
        #     yield scrapy.Request(next_page, callback=self.parse)

        # shorthand notation with no url join required
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

    def parse_author(self, response):
        # scrape author info from author url
        def extract_with_css(query):
            return response.css(query).get(default="").strip()

        author_info = {
            "name": extract_with_css("h3.author-title::text"),
            "birthdate": extract_with_css(".author-born-date::text"),
            "bio": extract_with_css(".author-description::text"),
        }
        print(f"author_info: {author_info}")
        yield author_info
