## Laracasts Scraper

This is a Python web scraper that grabs your list of watched videos from Laracasts.com, counts them, and calculates the total percent of videos watched.
The results are logged to a user-defined file.

### Installation
First, you'll need to install pip (a popular Python package installer). Do ```brew install pip```.

Then, run python on the setup file: ```python setup.py```. This will run ```pip install -r requirements.txt``` to install dependencies.

### Usage
Just run python on the runner file: ```python runner.py```. On the first run, you'll be asked for your Laracasts login information and a path to your desired output location. After the first run, the data is saved locally to ```configs.yml``` so you don't need to enter it again.

```configs.yml``` is not checked into git.