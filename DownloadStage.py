import pinboard
import Notification
import re, os, os.path, csv, string, logging

log = logging.getLogger("DownloadStage")

def downloadNewLinksFromPinboard(destinationPath, options, post_adaptor, dl_adaptor):
  log.debug("Starting up.")
  
  enable_downloads = options['pinboard']['enableDownloads']

  successfulDownloads = [ ]
  failedDownloads = [ ]
  log.debug("Looking for new bookmarks...")
  posts, last_update_time = post_adaptor.get_new_bookmarks()
  for post in posts:
    try:
      download_name = dl_adaptor.download(post.url(), destinationPath, enable_downloads, options)
    except Exception as e:
      log.exception("Download failed. Adding failed tag.")
      if enable_downloads:
        post.mark_failed()
      failedDownloads.append(post.name)
    else:
      log.debug("Download complete. Adding completed tag.")
      if enable_downloads:
        post.mark_successful()
      successfulDownloads.append(download_name)
      
  if enable_downloads:
    post_adaptor.save_update_time(last_update_time)
    if len(successfulDownloads) > 0 or len(failedDownloads) > 0:
      sucStr = string.join(['"'+name[0:20]+'"' for name in successfulDownloads], ", ")
      failStr = string.join(['"'+name[0:20]+'"' for name in failedDownloads], ", ")
      message = "%d succeeded, %d failed. OK: %s, Failed: %s" % (len(successfulDownloads), len(failedDownloads), sucStr, failStr)
      Notification.send("PinTheVideo done", message, options)
