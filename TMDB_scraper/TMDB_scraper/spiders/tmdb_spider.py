



import scrapy


class TMDBSpider(scrapy.Spider):
    # spider name
    name = 'tmdb_spider'
    # start url list
    start_urls = ['https://www.themoviedb.org/movie/2493-the-princess-bride']
    
    def parse(self, response):
        """Navigate to full cast & crew page."""
        # append '/cast' to url and make request
        yield scrapy.Request(url=response.url + 'cast/', callback=self.parse_full_credits)

    def parse_full_credits(self, response):
        """Extract and follow actor page links."""
        # loop over actor links
        for actor_link in response.xpath("//a[contains(@href, '/person/')]/@href").getall():
            # follow link
            yield response.follow(actor_link, callback=self.parse_actor_page)

    def parse_actor_page(self, response):
        """Extract actor name and movies/TV shows."""
        # get actor name
        actor_name = response.xpath("//h2[@class='title']/a/text()").get().strip()
        # loop over movie/tv show titles
        for movie_or_tv in response.xpath('//bdi/text()'):
            # get title text
            movie_or_tv_name = movie_or_tv.get().strip()
            # yield result
            yield {
                'actor': actor_name,
                'movie_or_TV_name': movie_or_tv_name
            }
