from pathlib import Path

import scrapy
import re

class InformacionniKartiSpider(scrapy.Spider):

    name = "informacionni_karti"
    start_urls = [
        "https://chitalishta.com/index.php?&act=community&do=list&special=1&&sql_which=0"
    ]
    
    def parse(self, response):
        for chitalishte in response.css("tr.odd"):
            chitalishte_detail_link = chitalishte.css('td.pad5 a[href*="do=detail"]::attr(href)').get()
            yield scrapy.Request(response.urljoin(chitalishte_detail_link), callback=self.parse_detail)
        yield from self.process_pagination(response)

    def parse_detail(self, response):
            information_card_links = response.css('td.bold[colspan="4"] a[href*="do=detail"]::attr(href)').getall()
            for link in information_card_links:
                yield scrapy.Request(response.urljoin(link), callback=self.parse_information_cards)
            yield from self.process_pagination(response)
    
    def parse_information_cards(self, response):
        phones = response.css('input[name="form[phone]"]::attr(value)').get().strip().replace('\n', ', ').replace('\r', ', ').replace(';', ', ')
        formatted_phones = re.sub(r'[^0-9/,]', '', phones)


        email = response.css('input[name="form[email]"]::attr(value)').get()
        emails = re.split(r'\s|[,;]', email)
        emails = filter(lambda email: re.match(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', email), emails)
        formatted_emails = ', '.join(emails)

        bulstat = response.css('input[name="form[bulstat]"]::attr(value)').get()
        bulstats = re.split(r'(?<![\/,])\D+', bulstat)
        bulstats = filter(None, bulstats)
        formatted_bulstats = ', '.join(bulstats)

        klubove_text = response.css('textarea[name="form[main][activities][clubs]"]::text').get().strip().replace('\n', ', ').replace('\r', ', ').replace(';', ', ')
        ezici_text = response.css('textarea[name="form[main][activities][lang]"]::text').get().strip().replace('\n', ', ').replace('\r', ', ').replace(';', ', ')
        kraj_text = response.css('textarea[name="form[main][activities][kraj]"]::text').get().strip().replace('\n', ', ').replace('\r', ', ').replace(';', ', ')
        muzei_text = response.css('textarea[name="form[main][activities][museum]"]::text').get().strip().replace('\n', ', ').replace('\r', ', ').replace(';', ', ')

        folk_text = response.css('textarea[name="form[main][ltvorch][folk]"]::text').get().strip().replace('\n', ', ').replace('\r', ', ').replace(';', ', ')
        teatur_text = response.css('textarea[name="form[main][ltvorch][theatre]"]::text').get().strip().replace('\n', ', ').replace('\r', ', ').replace(';', ', ')
        tancovi_grupi_text = response.css('textarea[name="form[main][ltvorch][dance]"]::text').get().strip().replace('\n', ', ').replace('\r', ', ').replace(';', ', ')
        balet_text = response.css('textarea[name="form[main][ltvorch][balley]"]::text').get().strip().replace('\n', ', ').replace('\r', ', ').replace(';', ', ')
        vocal_text = response.css('textarea[name="form[main][ltvorch][vocal]"]::text').get().strip().replace('\n', ', ').replace('\r', ', ').replace(';', ', ')
        drugi_text = response.css('textarea[name="form[main][ltvorch][other]"]::text').get().strip().replace('\n', ', ').replace('\r', ', ').replace(';', ', ')
        
        uchastiya_text = response.css('textarea[name="form[main][events]"]::text').get().strip().replace('\n', ', ').replace('\r', ', ').replace(';', ', ')
        novi_dejnosti_text = response.css('textarea[name="form[main][newactivities][txt]"]::text').get().strip().replace('\n', ', ').replace('\r', ', ').replace(';', ', ')
        rabota_s_drugi_text = response.css('textarea[name="form[main][injury]"]::text').get().strip().replace('\n', ', ').replace('\r', ', ').replace(';', ', ')
        drugi_dejnosti_text =response.css('textarea[name="form[main][other]"]::text').get().strip().replace('\n', ', ').replace('\r', ', ').replace(';', ', ')

        posledna_registraciya_text = response.css('input[name="form[org][prereg]"]::attr(value)').get().strip().replace('\n', ', ').replace('\r', ', ').replace(';', ', ')
        provedeni_subraniya_text = response.css('textarea[name="form[org][meetings]"]::text').get().strip().replace('\n', ', ').replace('\r', ', ').replace(';', ', ')
        baza_text = response.css('textarea[name="form[org][matbase]"]::text').get().strip().replace('\n', ', ').replace('\r', ', ').replace(';', ', ')
        obucheniya_text = response.css('textarea[name="form[org][obuchenie]"]::text').get().strip().replace('\n', ', ').replace('\r', ', ').replace(';', ', ')
        sankcii_text = response.css('textarea[name="form[org][sanctions]"]::text').get().strip().replace('\n', ', ').replace('\r', ', ').replace(';', ', ')
        dopulnitelno_text = response.css('textarea[name="form[remark]"]::text').get().strip().replace('\n', ', ').replace('\r', ', ').replace(';', ', ')
        yield {
            "ИНФОРМАЦИОННА КАРТА ЗА": response.css('input[name="form[year]"]::attr(value)').get().strip(),
            "Рег. номер": response.css('input[name="form[regid]"]::attr(value)').get().strip(),
            "Наименование": response.css('input[name="form[name]"]::attr(value)').get().strip(),
            "Област": response.xpath('//label[contains(text(), "Област")]/following-sibling::input[@type="hidden"]/following-sibling::text()').get().strip(),
            "Община": response.xpath('//label[contains(text(), "Община")]/following-sibling::input[@type="hidden"]/following-sibling::text()').get().strip(),
            "Град/село": response.xpath('//label[contains(text(), "Град/село")]/following-sibling::input[@type="hidden"]/following-sibling::text()').get().strip(),
            "Адрес": response.css('input[name="form[address][main]"]::attr(value)').get().split(),
            "Булстат": formatted_bulstats,
            "Телефон": formatted_phones,
            "Email": formatted_emails,
            "Web страница": response.css('input[name="form[webpage]"]::attr(value)').get(),
            "Председател": response.css('input[name="form[director]"]::attr(value)').get(),
            "Секретар": response.css('input[name="form[secretary]"]::attr(value)').get(),
            "Жители": response.css('input[name="form[teritory][person]"]::attr(value)').get(),
            "Посетители": response.css('input[name="form[teritory][users]"]::attr(value)').get(),
            "Клон 1": response.css('input[name="form[filial][1]"]::attr(value)').get(),
            "Клон 2": response.css('input[name="form[filial][2]"]::attr(value)').get(),
            "Брой членове": response.css('input[name="form[regusers]"]::attr(value)').get(),
            "Молби за членство": response.css('input[name="form[regmolba]"]::attr(value)').get(),
            "Нови членове": response.css('input[name="form[regnew]"]::attr(value)').get(),
            "Отказани молби": response.css('input[name="form[regrej]"]::attr(value)').get(),
            "Библиотечни дейности": response.css('input[name="form[main][biblioid]"]::attr(value)').get(),
            "Участие 'Живи човешки съкровища'": response.css('textarea[name="form[main][treasures]"]::text').get(),
            "Регионални листа": response.css('input[name="form[main][treasure][regnum]"]::attr(value)').get(),
            "Национални листа": response.css('input[name="form[main][treasure][nacnum]"]::attr(value)').get(),
            "Кръжоци, клубове": klubove_text,
            "Kръжоци, клубове бр.": response.css('input[name="form[main][activities][clubsnum]"]::attr(value)').get(),
            "Езикови школи, кръжоци": ezici_text,
            "Езикови, кръжоци бр.": response.css('input[name="form[main][activities][langnum]"]::attr(value)').get(),
            "Краезнание": kraj_text,
            "Краезнание бр.": response.css('input[name="form[main][activities][krajnum]"]::attr(value)').get(),
            "Музейни колекции": muzei_text,
            "Музейни колекции бр.": response.css('input[name="form[main][activities][museumnum]"]::attr(value)').get(),
            "Фолклорни състави и формации": folk_text,
            "Фолклорни състави и формации бр.": response.css('input[name="form[main][ltvorch][folknum]"]::attr(value)').get().strip(),
            "Театрални състави": teatur_text,
            "Театрални състави бр.": response.css('input[name="form[main][ltvorch][theatrenum]"]::attr(value)').get().strip(),
            "Танцови състави и групи": tancovi_grupi_text,
            "Танцови състави и групи бр.": response.css('input[name="form[main][ltvorch][dancenum]"]::attr(value)').get().strip(),
            "Групи за класически и/или модерен балет": balet_text,
            "Групи за класически и/или модерен балет бр.": response.css('input[name="form[main][ltvorch][balleynum]"]::attr(value)').get().strip(),
            "Вокални групи, хорове и индивидуални изпълнители": vocal_text,
            "Вокални групи, хорове и индивидуални изпълнители бр.": response.css('input[name="form[main][ltvorch][vocalnum]"]::attr(value)').get().strip(),
            "Други": drugi_text,
            "Други бр.": response.css('input[name="form[main][ltvorch][othernum]"]::attr(value)').get().strip(),
            "Участия празници, фестивали т.н.": uchastiya_text,
            "Участия празници, фестивали т.н. бр.": response.css('input[name="form[main][eventsnum]"]::attr(value)').get().strip(),
            "Нови дейности": novi_dejnosti_text,
            "Нови дейности самостоятелно бр.": response.css('input[name="form[main][newactivities][mainsum]"]::attr(value)').get().strip(),
            "Нови дейности несамостоятелно бр.": response.css('input[name="form[main][newactivities][partnersum]"]::attr(value)').get().strip(),
            "Работа с хора с увреждания, етнически различия и др.": rabota_s_drugi_text,
            "Работа с хора с увреждания, етнически различия и др.  бр.": response.css('input[name="form[main][othersum]"]::attr(value)').get().strip(),
            "Други дейности": drugi_dejnosti_text,
            "Други дейности бр.": response.css('input[name="form[main][ltvorch][vocalnum]"]::attr(value)').get().strip(),
            "Проведени събрания": provedeni_subraniya_text,
            "Последна регистрация": posledna_registraciya_text,
            "Материална база": baza_text,
            "Субсидирана численост": response.css('input[name="form[org][subspeople]"]::attr(value)').get(),
            "Персонал": response.css('input[name="form[org][personal][all]"]::attr(value)').get(),
            "Персонал висше": response.css('input[name="form[org][personal][hi]"]::attr(value)').get(),
            "Специализирани длъжности": response.css('input[name="form[org][personal][spec]"]::attr(value)').get(),
            "Административни длъжности": response.css('input[name="form[org][personal][adm]"]::attr(value)').get(),
            "Помощен персонал": response.css('input[name="form[org][personal][other]"]::attr(value)').get(),
            "Участие в обучения": obucheniya_text,
            "Санкции": sankcii_text,
            "Допълнително": dopulnitelno_text
        }
        yield from self.process_pagination(response)

    def process_pagination(self, response):
        pagination_links = response.css('div.pagelist a::attr(href)').getall()
        for link in pagination_links:
            if "sql_which" in link:
                yield scrapy.Request(response.urljoin(link), callback=self.parse)

