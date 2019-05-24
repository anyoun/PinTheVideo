import pinboard
import logging

class MockPost:
    def __init__(self, url, name, tags=[]):
        self.__url = url
        self.__name = name
        self.__tags = tags
    
    def url(self):
        return self.__url
    def name(self):
        return self.__name
    def tags(self):
        return self.__tags
        

class MockPostAdaptor:
    def __init__(self):
        self.posts = []
        self.last_update_time = "1999-09-09 21:09"

    def get_new_bookmarks(self):
        return (self.posts, self.last_update_time)
        
    def save_update_time(self, last_update_time):
        pass
    
    def mark_completed(self, post, succeeded):
        pass
    
class MockDownloader:
    def download(self, url, destinationPath, enable_downloads, options):
        pass