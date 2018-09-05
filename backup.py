#!/usr/bin/env python3

from urllib.request import urlopen
from xml.dom.minidom import parse # type: ignore

from goodreads_secrets import USER, KEY

def get_url(page, per_page=100):
    return 'https://www.goodreads.com/review/list/' + USER + '.xml?v=2&key=' + KEY + '&per_page=' + str(per_page) + '&page=' + str(page)

import logging


def main():
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("goodreads-backup")

    header = True

    current_page = 1
    reviews = []
    total = None

    while total is None or len(reviews) < total:
        u = get_url(current_page)
        logger.info(f"Retrieving {u}")

        xml = urlopen(u)
        dom = parse(xml)

        curr = dom.getElementsByTagName('reviews')
        total = int(curr[0].getAttribute('total'))
        reviews.extend(dom.getElementsByTagName('review'))
        current_page += 1

    for r in reviews:
        print(r.toxml())

if __name__ == '__main__':
    main()
