#!/usr/bin/env python3
import sys
import getopt
import os
import urllib.parse
from feedgen.feed import FeedGenerator


def usage(code=0):
    print('$0 -r <uri_root> -t <title>')
    sys.exit(code)


def main(argv):
    uri_root = ''
    title = ''
    try:
        opts, args = getopt.getopt(argv, "ht:r:", ["root", "title"])
    except getopt.GetoptError:
        usage(1)
    for opt, arg in opts:
        if opt == "-h":
            usage()
        elif opt in ("-r", "--root"):
            uri_root = arg
        elif opt in ("-t", "--title"):
            title = arg

    if len(uri_root) == 0 or len(title) == 0:
        usage(2)

    if not uri_root.endswith("/"):
        uri_root += "/"

    feed = FeedGenerator()
    feed.load_extension('podcast')
    feed.podcast.itunes_category('Arts', 'Books')
    feed.title(title)
    feed.description(title)
    feed.link(href=f"{uri_root}rss.xml", rel="self")
    for root, directories, files in os.walk("."):
        for name in files:
            if name.lower() == "cover.jpg" or name.lower() == "cover.jpeg" or name.lower() == "cover.png":
                feed.podcast.itunes_image("{uri_root}{name}")
            if name.endswith(".mp3"):
                entry = feed.add_entry()
                entry.id(uri_root + name)
                entry.title(name)
                entry.description(name)
                entry.enclosure(f"{uri_root}{urllib.parse.quote(name)}", 0, "audio/mpeg")
                print(name)
    feed.rss_str(pretty=True)
    feed.rss_file('rss.xml')

if __name__ == "__main__":
    main(sys.argv[1:])
