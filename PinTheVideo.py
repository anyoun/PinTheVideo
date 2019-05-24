#!/usr/bin/env python
import logging, datetime, sys, os
import DownloadStage, MuxBrokenFiles, Notification, PinboardAdaptor
import yaml

options_dict = {}
with open(sys.argv[1], 'r') as options_file:
    options_dict = yaml.load(options_file)

log_file = options_dict['directories']['logDir'] + "/PinTheVideo.%s.log" % (datetime.date.today())
logging.basicConfig(filename=log_file, level="DEBUG",
    format="%(asctime)-15s %(name)-8s %(module)-15s %(funcName)-15s %(message)s")
log = logging.getLogger("PinTheVideo")

destination = options_dict['directories']['destination']
if not os.path.exists(destination):
    os.mkdir(destination)

log.info("Starting with destination = '%s'", destination)

post_adaptor = PinboardAdaptor.PinboardAdaptor(options_dict['pinboard'])

try:
    DownloadStage.downloadNewLinksFromPinboard(destination, options_dict, post_adaptor)
except Exception as ex:
    log.exception("DownloadStage failed")
    Notification.send("DownloadStage failed", str(ex), options_dict)

try:
    MuxBrokenFiles.fixUnmuxedFiles(destination, options_dict)
except Exception as ex:
    log.exception("Remux failed")
    Notification.send("Remux failed", str(ex), options_dict)
