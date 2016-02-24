# PinTheVideo

This script downloads your bookmarks from Pinboard and makes any supported videos available offline.

### Options file

This file is required and contains all of the various settings required by PinTheVideo. The included `example.yaml` file is a good place to start.

### Getting Started

1. Edit `example.yaml` and add your Pinboard API token and (optionally) your pushover API token.
1. From the command line, run `python PinTheVideo.py example.yaml`
1. Set up a scheduled task to run the script regularly.

### Requires

* python-pinboard
* youtube_dl
* PyYAML
* python-pushover
