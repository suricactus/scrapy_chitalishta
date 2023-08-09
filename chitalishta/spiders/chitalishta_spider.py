from pathlib import Path
import scrapy

class ChitalishteSpider(scrapy.Spider):
    name = "chitalishta_spider"
    start_urls = [
        "https://chitalishta.com/index.php?&act=community&do=list&special=1&&sql_which=0"
    ]
    
    def parse(self, response):
        for chitalishte in response.css("tr.odd"):
            yield {
                "Номер": chitalishte.css('td.pad5::text').get().strip(), 
                "Линк": 'https://' + chitalishte.css('td.pad5 a[href*="do=detail"]::attr(href)').get(), 
                "Име на читалище": chitalishte.css('td.pad5 a[href*="do=detail"]::text').get().strip('"\n '),  
                "Град/село": chitalishte.css('td.pad5:nth-child(3)::text').get().strip(),  
                "Община": chitalishte.css('td.pad5:nth-child(4)::text').get().strip(),   
                "Област": chitalishte.css('td.pad5:nth-child(5)::text').get().strip(),  
            }
        
        pagination_links = response.css('div.pagelist a::attr(href)').getall()
        print(pagination_links)
        for link in pagination_links:
            if "sql_which" in link:
                yield scrapy.Request(response.urljoin(link), callback=self.parse)