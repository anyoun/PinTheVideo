import pinboard
import logging, os

log = logging.getLogger("PinboardAdaptor")

class PinboardPost:
    def __init__(self, url, name, tags):
        self.__url = url
        self.__name = name
        self.__tags = tags
    
    def url(self):
        return self.__url
    def name(self):
        return self.__name
    def tags(self):
        return self.__tags
        

class PinboardAdaptor:
    def __init__(self, pinboard_options):
        self.last_update_file = pinboard_options['lastUpdateFile']
        self.already_downloaded_tag = pinboard_options['alreadyDownloadedTag']
        self.failed_download_tag = pinboard_options['failedDownloadedTag']
        self.api_token = pinboard_options['apiToken']
        self.url_patterns = pinboard_options['urlPatterns']
        
        self.pinboard_conn = pinboard.open(token=self.api_token)
    
    def get_new_bookmarks(self):
        last_update_time = ""
        if os.path.exists(self.last_update_file):
            with open(self.last_update_file, 'r') as f:
                for line in f:
                    last_update_time = line
        
        pinboard_last_update_time = self.pinboard_conn.last_update()
        log.debug("Last updated at %s. Pinboard updated at %s", last_update_time, pinboard_last_update_time)
        
        if last_update_time == pinboard_last_update_time:
            log.info("No changes. Exiting.")
            return
        
        successfulDownloads = [ ]
        failedDownloads = [ ]
        log.debug("Looking for new bookmarks...")
        posts = [ ]
        for p in pinboard_conn.posts(fromdt=last_update_time):
            post = PinboardPost(p['href'], p['description'], p['tags'])
            urlMatch = False
            for pat in self.url_patterns:
                if re.search(pat, post.url()):
                    urlMatch = True
            if urlMatch and already_downloaded_tag not in post.tags() and failed_download_tag not in post.tags():
              log.debug(u"Found %s (%s)", post.name(), post.url())
              posts.append(post)
        
        return (posts, pinboard_last_update_time)
        
    def save_update_time(self, last_update_time):
        with open(self.last_update_file, 'w') as f:
          f.write(last_update_time)
          
    def mark_completed(self, post, succeeded):
        tag = self.already_downloaded_tag if succeeded else self.failed_download_tag
        if tag not in post.tags():
            post.tags().append(tag)
        self.pinboard_conn.add(post.url(), post.name(), replace='yes', tags=post.tags())