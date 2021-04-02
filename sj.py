import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem


class SjSpider(scrapy.Spider):
    name = 'sj'
    allowed_domains = ['superjob.ru']
    start_urls = [
        'https://russia.superjob.ru/vacancy/search/?keywords=Pythonn',
    ]

    def parse(self, response: HtmlResponse):
        vacancy_links = response.xpath(
            '//div[contains(@class,"_3mfro PlM3e _2JVkc _3LJqf")]/a/@href'
        ).extract()
        for link in vacancy_links:
            yield response.follow(link, callback=self.parse_vacancies)

        next_page = response.xpath('//a[@rel="next"]/@href').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        pass

    def parse_vacancies(self, response: HtmlResponse):
        title = response.xpath('//h1//text()').get()
        salary = response.xpath('//span[@class="_3mfro _2Wp8I PlM3e _2JVkc"]/text()').getall()
        link = response.url
        site = 'superjob.ru'
        yield JobparserItem(title=title, salary=salary, link=link, site=site)
