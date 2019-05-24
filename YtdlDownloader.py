import logging, os, re
import youtube_dl

log = logging.getLogger("YtdlDownloader")

class YtdlDownloader:
    def download(self, url, destinationPath, enable_downloads, options):
      log.debug("Getting ready to download %s", url)
      if re.search("youtu", url):
        fmt = 'bestvideo+bestaudio'
      else:
        fmt = 'best'
      ydl_opts = {
        'format': fmt,
        # 'format': 'worst',
        'simulate': not enable_downloads,
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