from __future__ import annotations

from collections.abc import Iterator, Sequence
from datetime import datetime, timezone
from typing import NamedTuple, Optional

from lxml import etree as ET

from .exporthelpers import dal_helper
from .exporthelpers.dal_helper import PathIsh, datetime_aware, pathify, the


class Book(NamedTuple):
    id: str
    title: str
    authors: Sequence[str]
    shelves: Sequence[str]
    date_added: datetime_aware
    date_started: Optional[datetime_aware]
    date_read: Optional[datetime_aware]


class Review(NamedTuple):
    id: str
    book: Book


def _parse_date(s: Optional[str]) -> Optional[datetime_aware]:
    if s is None:
        return None
    res = datetime.strptime(s, "%a %b %d %H:%M:%S %z %Y")
    assert res.tzinfo is not None
    return res


def _parse_review(r) -> Review:
    rid = the(r.xpath('id'))
    be = the(r.xpath('book'))
    title = the(be.xpath('title/text()'))
    authors = be.xpath('authors/author/name/text()')

    bid = the(r.xpath('id/text()'))
    # isbn_element   = the(book_element.getElementsByTagName('isbn'))
    # isbn13_element = the(book_element.getElementsByTagName('isbn13'))
    date_added = the(r.xpath('date_added/text()'))
    sss = r.xpath('started_at/text()')
    rrr = r.xpath('read_at/text()')
    started_at = None if len(sss) == 0 else the(sss)
    read_at = None if len(rrr) == 0 else the(rrr)

    shelves = [s.attrib['name'] for s in r.xpath('shelves/shelf')]

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


class DAL:
    def __init__(self, sources: Sequence[PathIsh]) -> None:
        self.sources = list(map(pathify, sources))
        # TODO take all sources into the account?
        self._source = max(self.sources)

    def reviews(self) -> Iterator[Review]:
        tree = ET.fromstring(self._source.read_text())
        rxml = tree.xpath('//review')
        for r in rxml:  # type: ignore[union-attr]
            yield _parse_review(r)


def demo(dal: DAL) -> None:
    print("Your books:")

    mindt = datetime.min.replace(tzinfo=timezone.utc)
    reviews = sorted(dal.reviews(), key=lambda r: r.book.date_read or mindt)
    for r in reviews:
        print(r.book.date_read, r.book.title)


def main() -> None:
    dal_helper.main(DAL=DAL, demo=demo)


if __name__ == '__main__':
    main()
