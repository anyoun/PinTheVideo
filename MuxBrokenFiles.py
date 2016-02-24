import re, os, os.path, csv, logging

ENABLE_DOWNLOADS = True
SINGLE_STREAM_FILE_PATTERN = '\.f\d+$'

log = logging.getLogger("MuxBrokenFiles")

class FileToFix:
    def __init__(self, path, size):
        self.path = path
        self.size = size

def getfilesInPath(path):
    files = []
    if False:
        with open('filenames.csv', 'rb') as csvfile:
            for row in csv.DictReader(csvfile, delimiter=',', quotechar='"'):
                files.append(FileToFix(row['FullName'], int(row['Length'])))
    else:
        for name in os.listdir(path):
            fullName = os.path.join(path, name)
            statinfo = os.stat(fullName)
            files.append(FileToFix(fullName, statinfo.st_size))
    return files


def fixUnmuxedFiles(path, options):
    log.debug("Running on path %s", path)
    groups = {}
    for file in getfilesInPath(path):
        (dir, name) = os.path.split(file.path)
        (root, ext) = os.path.splitext(name)
        root = re.sub(SINGLE_STREAM_FILE_PATTERN, '', root)
        if root not in groups:
            groups[root] = []
        groups[root].append(file)
    for (k,grp) in groups.iteritems():
        if len(grp) > 1:
            log.debug("Found group: "+k)
            audioFile = None
            videoFile = None
            for f in grp:
                (root, ext) = os.path.splitext(f.path)
                msg = ""
                if f.size < 1024:
                    msg = "DELETE SMALL "
                    if ENABLE_DOWNLOADS:
                        os.remove(f.path)
                elif re.search(SINGLE_STREAM_FILE_PATTERN, root) == None:
                    msg = "DELETE TEMP "
                    if ENABLE_DOWNLOADS:
                        os.remove(f.path)
                elif ext in [ ".m4a", ".mp4" ]:
                    msg = "AUDIO "
                    audioFile = f
                elif ext in [ ".m4v", ".webm" ]:
                    msg = "VIDEO "
                    videoFile = f
                log.debug("%s  %s%s %i", msg, root, ext, f.size)
            if audioFile and videoFile:
                outputPath = os.path.join(path, k+".mkv")
                cmd = 'ffmpeg -i "%s" -i "%s" -codec copy "%s"'%(audioFile.path, videoFile.path, outputPath)
                print cmd
                if ENABLE_DOWNLOADS:
                    if 0 != os.system(cmd):
                        log.error("Remux failed")
                    else:
                        os.remove(audioFile.path)
                        os.remove(videoFile.path)
            else:
                log.error("  Couldn't find audio and video.")
        else:
            log.warn("Singleton file %s", grp[0].path)
