
import scrapy

class AuthorsSpider(scrapy.Spider):
    name = "authors"
    
    start_urls = [
        'http://quotes.toscrape.com/',
    ]

    def parse(self, response):
        author_pages = response.css('div.quote span a::attr(href)').getall()
        for page in author_pages:
            yield response.follow(page, self.parse_author)

        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)
    
    def parse_author(self, response):
        yield {
            'fullname': response.css('h3.author-title::text').get().strip(),
            'born_date': response.css('span.author-born-date::text').get(),
            'description': response.css('div.author-description::text').get().strip(),
        }
