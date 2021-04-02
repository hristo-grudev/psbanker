import scrapy

from scrapy.loader import ItemLoader

from ..items import PsbankerItem
from itemloaders.processors import TakeFirst


class PsbankerSpider(scrapy.Spider):
	name = 'psbanker'
	start_urls = ['https://www.psbanker.com/blog/']

	def parse(self, response):
		post_links = response.xpath('//a[@class="read-more read-more-border"]/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

		next_page = response.xpath('//a[@class="next page-numbers"]/@href').getall()
		yield from response.follow_all(next_page, self.parse)

	def parse_post(self, response):
		title = response.xpath('//div[@class="entry-header"]/h1/text()').get()
		description = response.xpath('//div[@class="entry-content"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description if '{' not in p]
		description = ' '.join(description).strip()
		date = response.xpath('//span[@class="item-metadata-time"]//text()').getall()
		date = [p.strip() for p in date]
		date = ' '.join(date).strip()

		item = ItemLoader(item=PsbankerItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
