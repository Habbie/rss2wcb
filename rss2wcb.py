#!/usr/bin/env python3

import feedparser
import html
import socket
import sys
import time

def maybe_decode(s):
    try:
        return html.unescape(s)
    except:
        return s

def main():
    feedurl = sys.argv[1]
    wcbip = sys.argv[2]
    wcbport = int(sys.argv[3])
    wcbpass = sys.argv[4]
    channel = sys.argv[5]
    prefix = sys.argv[6]

    seen = set()

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    while True:
        feed = feedparser.parse(feedurl)

        for item in feed["items"]:
            title = maybe_decode(item["title"])
            link = item["link"]
            if link not in seen:
                s = f"\x02[{prefix}]\x02 {title}: {link}"
                sock.sendto((f"{wcbpass} {channel} {s}").encode('utf-8'),
                            (wcbip, wcbport))
                seen.add(link)
        time.sleep(30)


if __name__ == '__main__':
    main()
