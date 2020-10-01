from artists.items import ArtistsItem
from scrapy import Spider, Request
import re


class Artists(Spider):
    name = 'artists_spider'
    allowed_urls = ['https://www.artfinder.com/#/']
    start_urls = ['https://www.artfinder.com/artist/api/artist-search/']

    def parse(self, response):
        # here I get the max page of numbers
        # max_page = response.xpath(
        #     '//ul[@class="pagination"]/li/a/@href').extract()[-2].split("=", 1)[1]
        # list_pages = list(range(2, int(max_page)+1, 1))
        list_pages = list(range(2, 4))

        list_urls = [
            f'https://www.artfinder.com/artist/api/artist-search/?page={num}' for num in list_pages]

        # the first url is the url itself without any additional hrefs
        list_urls.append(response.url)

        # go for each page
        for url in list_urls:
            yield Request(url=url, callback=self.parse_page)

    def parse_page(self, response):
        # get the big JSON string
        big_json = (response.xpath(
            "//pre[@class='prettyprint']").extract()[1]).split("\n")
        # clean the JSON
        big_json_clean = list(map(str.strip, big_json))

        # big list with all lists
        biglist = []

        # ARTFINDER ID
        id_list = [re.findall('\d+', x[len("id")+4:])
                   for x in big_json_clean if x.startswith('"id')]
        biglist.append(id_list)

        # NAMES
        names_list = [re.findall(r'"([^"]*)"', x[len("name")+4:])
                      for x in big_json_clean if x.startswith('"name')]
        biglist.append(names_list)

        # COUNTRY
        country_list = [re.findall(r'"([^"]*)"', x[len("country")+4:])
                        for x in big_json_clean if x.startswith('"country')]
        biglist.append(country_list)

        # products_count
        products_count_list = [re.findall('\d+', x[len("product_count")+4:])
                               for x in big_json_clean if x.startswith('"product_count')]
        biglist.append(products_count_list)

        # follows
        follows_list = [re.findall('\d+', x[len("interest_count")+4:])
                        for x in big_json_clean if x.startswith('"interest_count')]
        biglist.append(follows_list)

        # profession
        profession_list = [re.findall(r'"([^"]*)"', x[len("profession")+4:])
                           for x in big_json_clean if x.startswith('"profession')]
        biglist.append(profession_list)

        # is_represented_by_gallery
        irbg_list = [re.findall("[a-zA-Z]+", x[len("is_represented_by_gallery")+4:])
                     for x in big_json_clean if x.startswith('"is_represented_by_gallery')]
        biglist.append(irbg_list)

        # is_artist
        ia_list = [re.findall("[a-zA-Z]+", x[len('"is_artist"')+2:])
                   for x in big_json_clean if x.startswith('"is_artist"')]
        biglist.append(ia_list)

        # accepts_commissions
        ac_list = [re.findall("[a-zA-Z]+", x[len("accepts_commissions")+4:])
                   for x in big_json_clean if x.startswith('"accepts_commissions')]
        biglist.append(ac_list)

        # artist_rating
        ar_list = [re.findall('\d+', x[len("artist_rating")+4:])
                   for x in big_json_clean if x.startswith('"artist_rating')]
        biglist.append(ar_list)

        # seller_rating
        sr_list = [x.split(": ")[1][:-1]
                   for x in big_json_clean if x.startswith('"seller_rating')]
        biglist.append(sr_list)

        # is_artist_of_the_day_today
        iaotdt_list = [re.findall("[a-zA-Z]+", x[len("is_artist_of_the_day_today")+4:])
                       for x in big_json_clean if x.startswith('"is_artist_of_the_day_today')]
        biglist.append(iaotdt_list)

        # slug
        slug_list = [re.findall(r'"([^"]*)"', x[len("slug")+4:])
                     for x in big_json_clean if x.startswith('"slug')]
        biglist.append(profession_list)

        for i in range(0, len(biglist[0])):
            item = ArtistsItem()
            item['artFinderId'] = biglist[0][i][0]
            item['artistName'] = biglist[1][i][0]
            item['country'] = biglist[2][i][0]
            item['products_count'] = biglist[3][i][0]
            item['follows'] = biglist[4][i][0]
            item['profession'] = biglist[5][i][0]
            item['is_represented_by_gallery'] = biglist[6][i][0]
            item['is_artist'] = biglist[7][i][0]
            item['accepts_commissions'] = biglist[8][i][0]
            item['artist_rating'] = biglist[9][i][0]
            item['seller_rating'] = biglist[10][i][0]
            item['is_artist_of_the_day_today'] = biglist[11][i][0]
            item['slug'] = biglist[12][i][0]

            yield item
