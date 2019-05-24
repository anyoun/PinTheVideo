import unittest, logging
import Mocks
import DownloadStage

class TestDownloadStage(unittest.TestCase):

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)
    
    def test_download_stage(self):
        options = {
            'pinboard': {
                'enableDownloads': False
            }
        }
        adaptor = Mocks.MockPostAdaptor()
        adaptor.posts.append(Mocks.MockPost("http://example.com/foo.mp4", "Name 1"))
        downloader = Mocks.MockDownloader()
        DownloadStage.downloadNewLinksFromPinboard("~/tmp/", options, adaptor, downloader)

if __name__ == '__main__':
    logging.basicConfig()
    unittest.main()