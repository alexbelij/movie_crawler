import scrapy


class MovieSpidet(scrapy.Spider):
    name = "movies"
    start_urls = [
        'https://www.imdb.com/movies-coming-soon/',
    ]

    def parse(self, response):
        for film in response.css('div.list_item'):
            
            try:
                trailer = film.css('td.overview-bottom a.title-trailer').attrib['href']
                trailer = response.urljoin(trailer)
            except KeyError:
                self.log("Key error.")
                trailer = None            
            
            genre = film.css('p.cert-runtime-genre span::text').getall()
            genre = [g for g in genre if g != '|']
            
            yield {
                'title': film.css('h4 a::text').get(),
                'image': film.css('div.image img').attrib['src'],
                'time' : film.css('p.cert-runtime-genre time::text').get(),
                'trailer' : trailer,
                'genre' : genre,
            }
            
        next_page = response.css('div.see-more a')[1].attrib['href']
        year, month = next_page.split('/')[-2].split('-')
        
        if next_page is not None and year != '2020' and month != '05':
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)