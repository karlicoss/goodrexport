#!/usr/bin/env python3
from pathlib import Path
from typing import List, Dict, NamedTuple, Iterator, Optional, Sequence, Union
from datetime import datetime

from lxml import etree as ET # type: ignore

class Book(NamedTuple):
    id: str
    title: str
    authors: Sequence[str]
    shelves: Sequence[str]
    date_added: datetime
    date_started: Optional[datetime]
    date_read: Optional[datetime]

class Review(NamedTuple):
    id: str
    book: Book


def the(l):
    it = iter(l)
    try:
        first = next(it)
    except StopIteration as ee:
        raise RuntimeError('Empty iterator?')
    assert all(e == first for e in it)
    return first


def _parse_date(s: Optional[str]) -> Optional[datetime]:
    if s is None:
        return None
    res = datetime.strptime(s, "%a %b %d %H:%M:%S %z %Y")
    assert res.tzinfo is not None
    return res


def _parse_review(r):
    rid   = the(r.xpath('id'))
    be    = the(r.xpath('book'))
    title = the(be.xpath('title/text()'))
    authors = be.xpath('authors/author/name/text()')

    bid     = the(r.xpath('id/text()'))
    # isbn_element   = the(book_element.getElementsByTagName('isbn'))
    # isbn13_element = the(book_element.getElementsByTagName('isbn13'))
    date_added     = the(r.xpath('date_added/text()'))
    sss = r.xpath('started_at/text()')
    rrr = r.xpath('read_at/text()')
    started_at     = None if len(sss) == 0 else the(sss)
    read_at        = None if len(rrr) == 0 else the(rrr)

    shelves = r.xpath('shelves/shelf/name/text()')

    # if isbn_element.getAttribute('nil') != 'true':
    #     book['isbn'] = isbn_element.firstChild.data
    # else:
    #     book['isbn'] = ''

    # if isbn13_element.getAttribute('nil') != 'true':
    #     book['isbn13'] = isbn13_element.firstChild.data
    # else:
    #     book['isbn13'] = ''

    da = _parse_date(date_added)
    assert da is not None
    book = Book(
        id=bid,
        title=title,
        authors=authors,
        shelves=shelves,
        date_added=da,
        date_started=_parse_date(started_at),
        date_read=_parse_date(read_at),
    )
    return Review(
        id=rid,
        book=book,
    )

class Model:
    def __init__(self, sources: Sequence[Union[Path, str]]) -> None:
        self.sources = list(map(Path, sources))

    def iter_reviews(self):
        src = max(self.sources)
        tree = ET.fromstring(src.read_text())
        rxml = tree.xpath('//review')
        for r in rxml:
            yield _parse_review(r)

    def reviews(self):
        return list(self.iter_reviews())


if __name__ == '__main__':
    reviews = Model(['export.xml']).reviews()
    print(reviews)
