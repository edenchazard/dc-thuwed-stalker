# Dragcave Thuwed Stalker

A Python project to "track" TJ's [Thuwed](https://dragcave.net/thuwed) breedings. It doesn't grab them, but it's intended to be run whenever they've been bred and will automate a list of the eggs all in one place.

This a work in progress and really just an experiment with Python. :) To have a working copy of this project, you'll need your own [API key](https://dragcave.net/api.txt).

## Getting started

```sh
# clone repo
git clone https://github.com/edenchazard/dc-thuwed-stalker.git

cd dc-thuwed-stalker

# install pip packages
pip install -r requirements.txt

# Copy the example config file
cp config.example.json config.json

# Add your API key with your favourite text editor
nano config.json

# run
python3 main.py
```

## TODOs

- Script to automate fetching the list of Thuwed pairs.
- Implement concurrency when calling the API for each pair. Right now, the synchronous nature of the code means API calls to the /progeny endpoint are made one at a time. This is really slow!
- "Cache" the results for 7 days from the most recently bred date. They won't need to be regenerated within that period because Thuweds are bred irregularly but at minimum once a week.
- Have a web interface that displays a simple list of the eggs with the code and parent names.
- Possibly generate an image with the eggs?
