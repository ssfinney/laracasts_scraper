"""
Scraper.py

This script does the data scraping for all web pages.
It grabs results and parses them accordingly.
"""

from BeautifulSoup import BeautifulSoup
from LaracastsScraper import ConfigLoader


"""
Tests this page's HTML to see if there are any more results to return.
The website displays a special message if there aren't any more results to get.

Returns True if we're done, False if not.

Arguments:
    - page The HTML of the page to search
"""
def page_has_results(page):

    # This is the "box" that the watched videos should be in
    collection = page.find('div', {'id': 'completed'})

    msg = 'Unfortunately, nothing was returned'

    # If the text above is found, we're done.
    return not msg in collection.find('p').text


"""
Get the HTML for the result page specified. Returns the page's HTML or False if no results were found.

Arguments:
    - page_number The page number to get the results from.
    - session The authenticated Requests session with Laracasts.com
"""
def page_html(page_url, session):

    page = session.get(page_url).content
    page = BeautifulSoup(page)

    if not page_has_results(page):
        print "We're done."
        return False

    return page


"""
Get the names of the laracast videos that I've watched on this page of regular results.
Returns a list of video names

Arguments:
    - page The HTML of the page to search on
"""
def regular_page_watched_videos(page):
    print("Scraping video names from page...\n")
    videos = page.findAll('h3', {'class': 'lesson-block-title  not-wached'})

    return [video.text for video in videos]


"""
Get the count of all regular (non-series) videos on Laracasts.com
Returns the number as an integer.

Arguments:
    - session The authenticated Requests session with Laracasts.com.
"""
def regular_video_count(session):

    page = session.get('https://laracasts.com/all').content
    page = BeautifulSoup(page)

    all_videos = page.findAll('li', {'class': 'list-group-item'})

    return len(all_videos)


"""
Save these names to the output file.

Arguments:
    - names A list of names to save.
"""
def save_data(names):

    print("Saving data to the file...")

    """
    Open the output file. Join the names together, separated by newlines.
    Then, replace the HTML code for apostraphes with an actual apostraphe.
    """
    output_file = ConfigLoader.get_output_filename()

    with open(output_file, 'w') as file_stream:
        names = '\n'.join(names)
        file_stream.write("Watched Laracasts videos:\n\n")
        file_stream.write(names.replace('&#039;', "'"))


"""
Save some other statistics about the videos to the output file.

Arguments:
    - watched The number of vidoes watched.
    - total The total number of videos.
"""
def save_statistics(watched, total):

    print("Saving statistics to the file...\n")

    # Calculate the percent watched and round to 1 decimal place
    percent_watched = (float(watched) / float(total)) * 100
    percent_watched = round(percent_watched, 1)

    # Write the data to the output file
    output_file = ConfigLoader.get_output_filename()

    with open(output_file, 'a') as f:
        f.write("\n\n")
        f.write("Videos watched: " + str(watched) +
                " out of " + str(total) + ".\n")
        f.write("Percent watched: " + str(percent_watched) + "%.\n")


"""
Get the names of the laracast videos that I've watched on this page of series results.
Returns a list of video names

Arguments:
    - page the HTML of the page to search on
    - session The authenticated Requests session with Laracasts.com.
"""
def series_page_watched_videos(page, session):

    page = session.get(page).content
    page = BeautifulSoup(page)

    # Watched videos on series pages have strikethrough applied to their names
    videos = page.findAll('a', {'class': 'strike '})

    print(videos)

    return [video.text for video in videos]


"""
Get the URLs for all series on Laracasts.com

Arguments:
    - session The authenticated Requests session with Laracasts.com.
"""
def series_urls(session):

    # Get the page to scrape. The links we want are in a div with class 'lesson-set'
    page = session.get('https://laracasts.com/series').content
    page = BeautifulSoup(page)

    # First, get all of the video title "blocks" on the page
    all_series = page.findAll('h3', {'class': 'lesson-block-title'})

    # Then, get the links inside each of them and return the URLs
    return [series.find('a')['href'] for series in all_series]


"""
Get the count of all series videos on Laracasts.com
Returns the number as an integer.

Arguments:
    - session The authenticated Requests session with Laracasts.com.
"""
def series_video_count(session):

    pages = series_urls(session)
    video_count = 0

    for page in pages:

        # Get the page's HTML, then parse it with BeautifulSoup
        page = session.get(page).content
        page = BeautifulSoup(page)

        # Return the number of videos on this page
        return len(page.findAll('td', {'class': 'episode-title'}))


"""
Returns the number of regular and series videos on Laracasts.com

Arguments:
    - session The authenticated Requests session with Laracasts.com.
"""
def total_video_count(session):

    print("Finding total number of videos...")

    url = 'https://laracasts.com/all?page=1'
    page = session.get(url).content
    page = BeautifulSoup(page)

    # Start with page number 1 of the videos on the page
    video_count = 0
    page_number = 1
    page_videos = page.findAll('li', {'class': 'list-group-item clearfix'})

    while page_videos:
        video_count += len(page_videos)

        # Increment the page number AND change the number on the url
        page_number += 1
        url = url[:-1] + str(page_number)

        # Advance to the next page and count the videos there, too
        page = session.get(url).content
        page = BeautifulSoup(page)
        page_videos = page.findAll('li', {'class': 'list-group-item clearfix'})

    return video_count
