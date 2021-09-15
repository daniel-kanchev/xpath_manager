import scrapy
from scrapy.http import FormRequest


class KrakenJsonSpider(scrapy.Spider):
    name = 'kraken_json'

    custom_settings = {
        "LOG_LEVEL": "DEBUG",
        "USER_AGENT": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:66.0) Gecko/20100101 Firefox/66.0"
    }

    def start_requests(self):
        url = f'http://kraken.aiidatapro.net/items/edit/{self.kraken_id}/'
        yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        return FormRequest.from_response(response,
                                         formdata={'username': 'danielk', 'password': 'Zi7dei'},
                                         callback=self.after_login)

    def after_login(self, response):
        code = response.xpath("//input[@name='feed_properties']/@value").get()
        with open('json.txt', 'w') as f:
            f.write(code)
