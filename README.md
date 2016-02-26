# PinTheVideo

This script searches your bookmarks on Pinboard and makes any supported videos available offline.

It uses the Pinboard API to download all of your bookmarks that have been updated since it last ran (saving the time in `last_update_time.txt`) and looks for any URLs that match `urlPatterns` in your settings file. For any matching URLs, the script calls youtube_dl to download the video. It will then mark the video with either `alreadyDownloadedTag` or `failedDownloadedTag` to prevent redownloading.

### Getting Started

1. Clone this git repo.
1. Restore packages: `pip install -r requirements.txt`
1. Edit `example.yaml` and add your Pinboard API token and (optionally) your pushover API token.
1. From the command line, run `python PinTheVideo.py example.yaml`
1. Set up a scheduled task to run the script regularly.

### Options file

This file is required and contains all of the various settings required by PinTheVideo. The included `example.yaml` file is a good place to start.

### Plex

You can add the destination directory to Plex as a library to make the videos watchable in Plex.

### Requires

* python-pinboard
* youtube_dl
* PyYAML
* python-pushover

## TODO

- [ ] Add support for YouTube playlist.
- [ ] Refactor bookmark code to allow supporting other bookmark providers, include plain text files.
- [ ] Add unit tests.
- [ ] Add support for expiring watched videos by accessing metadata from Plex.
