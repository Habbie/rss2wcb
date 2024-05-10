#!/usr/bin/env python3

import feedparser
import html
import socket
import sys
import time
import json

def maybe_decode(s):
    try:
        return html.unescape(s)
    except:
        return s

def load_state(seen_file):
    try:
        with open(seen_file, mode="r") as input:
            ret = json.load(input)
        return ret
    except:
        return []

def save_state(seen_file, obj):
    with open(seen_file, mode="w") as output:
        json.dump(obj, output)
    return

def main():
    feedurl = sys.argv[1]
    wcbip = sys.argv[2]
    wcbport = int(sys.argv[3])
    wcbpass = sys.argv[4]
    channel = sys.argv[5]
    prefix = sys.argv[6]
    interval = int(sys.argv[7])

    seen_file = f"rss2wcb_{prefix}.seen"
    seen = load_state(seen_file)

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
                seen.append(link)
                save_state(seen_file, seen)
        time.sleep(interval)


if __name__ == '__main__':
    main()
