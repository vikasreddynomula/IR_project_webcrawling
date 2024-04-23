import scrapy
import json
import os


class WikiHowSpider(scrapy.Spider):
    name = "wikiHow_spider"

    # Seed URL (Wikipedia main page)
    start_urls = ["https://www.wikihow.com/Main-Page"]

    # Maximum pages to crawl (adjust for your assignment)
    max_pages = 300  # Adjust this limit as needed

    # Maximum depth to follow links (adjust for your assignment)
    max_depth = 2  # Adjust this limit as needed

    # Current depth (internal variable)
    current_depth = 0

    # Current page count (internal variable)
    current_page = 1

    def parse(self, response):
        # Check if page limit is reached
        if self.current_page > self.max_pages:
            return
        self.logger.info("Parse function called on %s", response.url)

        # Parse the response and extract the required data.
        page = {
            "link": response.url,  # The link to the scraped webpage
            "article": response.css('h1>a::text').get(),
            "intro": str(response.css('div.mf-section-0>p::text').get()).replace("\n", ""),
            "points": []
        }

        for section in response.css("div.section.steps"):
            point = {
                "name": str(section.css('h3>span.mw-headline::text').get()).replace("\n", ""),
                "steps": []
            }

            for points in section.css("div.section_text>ol>li"):
                step = {
                    # The step number
                    "step": str(points.css('li>div.step_num::text').get()).replace("\n", ""),
                    "title": str.join("", points.css('li>div.step>b::text').getall()).replace("\n", ""),
                    "subtitle": str.join("", points.css('li>div.step::text').getall()).replace("\n", ""),
                    "sub-points": []
                }

            for subPoint in points.css('li>div.step>ul>li'):
                step["sub-points"].append(str.join("",
                                                   subPoint.css('li::text').getall()).replace('\n', ''))
                point["steps"].append(step)

            page["points"].append(point)

        # If the 'article' field is not empty, save the parsed data to a JSON file
        if page["article"] is not None:
            filename = f"crawler/data/webpage_{self.current_page}.json"

            # Open the file in write mode and dump the parsed data to it
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(page, f, ensure_ascii=False, indent=4)

            self.logger.info("Saved to %s" % filename)
            self.current_page += 1

        # Follow links within the page (limited by depth)
        # Access depth from response.meta
        if response.meta.get('depth') < self.max_depth:
            for next_page in response.css("a::attr(href)").getall():
                # Filter internal wiki links (avoid disambiguation pages)
                if next_page.startswith("/Quizzes") or next_page.startswith("/Course"):
                    continue
                elif next_page.startswith('https://') or next_page.startswith('http://'):
                    continue
                elif next_page.startswith('/wikiHow'):
                    continue
                elif next_page.__contains__('/Category:'):
                    continue
                yield response.follow(next_page, callback=self.parse, meta={'depth': response.meta.get('depth', 0) + 1})

