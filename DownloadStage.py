import youtube_dl
import pinboard
import Notification
import re, os, os.path, csv, string, logging

log = logging.getLogger("DownloadStage")

def download(url, destinationPath, options):
  if re.search("youtu", url):
    fmt = 'bestvideo+bestaudio'
  else:
    fmt = 'best'
  ydl_opts = {
    'format': fmt,
    # 'format': 'worst',
    'simulate': not options['pinboard']['enableDownloads'],
    'logger': logging.getLogger("youtube_dl"),
    'noplaylist': True,
    'downloadarchive': 'archive.dat',
    'outtmpl': os.path.join(destinationPath, '%(title)s-%(id)s.%(ext)s'),
  }
  with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    ydl.add_default_info_extractors()
    log.debug("Downloading ''%s' to ''%s'...", url, destinationPath)
    info = ydl.extract_info(url, download=True)
    return info['title']

def downloadNewLinksFromPinboard(destinationPath, options):
  log.debug("Starting up.")
  last_update_file = options['pinboard']['lastUpdateFile']
  already_downloaded_tag = options['pinboard']['alreadyDownloadedTag']
  failed_download_tag = options['pinboard']['failedDownloadedTag']
  enable_downloads = options['pinboard']['enableDownloads']

  last_update_time = ""
  if os.path.exists(last_update_file):
    with open(last_update_file, 'r') as f:
      for line in f:
          last_update_time = line

  pinboard_conn = pinboard.open(token=options['pinboard']['apiToken'])
  pinboard_last_update_time = pinboard_conn.last_update()
  log.debug("Last updated at %s. Pinboard updated at %s", last_update_time, pinboard_last_update_time)

  if last_update_time == pinboard_last_update_time:
    log.info("No changes. Exiting.")
    exit()

  successfulDownloads = [ ]
  failedDownloads = [ ]
  log.debug("Looking for new bookmarks...")
  posts = pinboard_conn.posts(fromdt=last_update_time)
  for p in posts:
    url = p['href']
    name = p['description']
    tags = p['tags']
    update_time = p['time']
    urlMatch = False
    for pat in options['pinboard']['urlPatterns']:
        if re.search(pat, url):
            urlMatch = True
    if urlMatch and already_downloaded_tag not in tags and failed_download_tag not in tags:
      log.debug(u"Found %s (%s)", name, url)
      try:
        name = download(url, destinationPath, options)
      except Exception as e:
        tags.append(failed_download_tag)
        log.exception("Download failed. Adding failed tag.")
        failedDownloads.append(name)
      else:
        tags.append(already_downloaded_tag)
        log.debug("Download complete. Adding completed tag.")
        successfulDownloads.append(name)
      if enable_downloads:
        pinboard_conn.add(url, name, replace='yes', tags=tags)

  if enable_downloads:
    with open(last_update_file, 'w') as f:
      f.write(pinboard_last_update_time)
    if len(successfulDownloads) > 0 or len(failedDownloads) > 0:
      sucStr = string.join(['"'+name[0:20]+'"' for name in successfulDownloads], ", ")
      failStr = string.join(['"'+name[0:20]+'"' for name in failedDownloads], ", ")
      message = "%d succeeded, %d failed. OK: %s, Failed: %s" % (len(successfulDownloads), len(failedDownloads), sucStr, failStr)
      Notification.send("PinTheVideo done", message, options)
