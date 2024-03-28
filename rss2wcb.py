#!/usr/bin/env python3

import feedparser
import html
import socket
import sys
import time
import pickle

def maybe_decode(s):
    try:
        return html.unescape(s)
    except:
        return s

def load_pickle():
    try:
        input = open("./rss2wcb.seen", mode="rb")
        ret = pickle.load(input)
        input.close()
        return ret
    except:
        return set()

def save_pickle(obj):
    output = open("./rss2wcb.seen", mode="wb")
    pickle.dump(obj, output, -1)
    output.close()
    return

def main():
    feedurl = sys.argv[1]
    wcbip = sys.argv[2]
    wcbport = int(sys.argv[3])
    wcbpass = sys.argv[4]
    channel = sys.argv[5]
    prefix = sys.argv[6]

    seen = load_pickle()

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    while True:
        feed = feedparser.parse(feedurl)

        for item in feed["items"]:
            title = maybe_decode(item["title"])
            title = title.split('\n')[0]
            link = item["link"]
            if link not in seen:
                s = f"\x02[{prefix}]\x02 {title}: {link}"
                sock.sendto((f"{wcbpass} {channel} {s}").encode('utf-8'),
                            (wcbip, wcbport))
                seen.add(link)
                save_pickle(seen)
        time.sleep(30)


if __name__ == '__main__':
    main()
