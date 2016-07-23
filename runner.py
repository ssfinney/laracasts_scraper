#!/usr/bin/env python
"""
runner.py

This is the runner for the Laracasts.com scraper.
It crawls through various pages, searching both for the videos
that I've watched (series and non-series) and the total number
of videos that exist on the site.
"""

from LaracastsScraper import Authenticator, Scraper

# Start a new HTTP session by POSTing to laracasts.com/sessions
session = Authenticator.create_session('https://laracasts.com/sessions')

# Get the regular (non-series) videos that I've watched.
# Start scraping at results page number 1.
page_number = 1

watched_videos_url = "https://laracasts.com/profiles/StephenFinney/completed?page=" + str(page_number)

page = Scraper.page_html(watched_videos_url, session)

# Until there are no more search results,
# get each page's HTML, parse them, and save the video names.
names = []
while page:
    print("Getting HTML for page number " + str(page_number) + "...")
    names += Scraper.regular_page_watched_videos(page)

    # Increment page number inside variable AND inside the watched_videos_url
    page_number += 1
    watched_videos_url = watched_videos_url[:-1] + str(page_number)

    page = Scraper.page_html(watched_videos_url, session)


# Now, scrape the videos from the Series lists and add them to our totals
pages = Scraper.series_urls(session)

print "Scraping video names from series pages...\n"
for page in pages:
    names += Scraper.series_page_watched_videos(page, session)


# Save all video names (alphebetized) to the output file
Scraper.save_data(sorted(names))

# Get the total number of videos that exist on Laracasts.com
total_videos = Scraper.total_video_count(session)

# Now, calculate the percent of videos I've watched.
Scraper.save_statistics(len(names), total_videos)

print("Program complete.")
