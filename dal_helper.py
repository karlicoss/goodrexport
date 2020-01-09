import argparse
from glob import glob
from pathlib import Path
from typing import Any, Dict, Union, TypeVar

PathIsh = Union[str, Path]
Json = Dict[str, Any] # TODO Mapping?


T = TypeVar('T')
Res = Union[T, Exception]


def make_parser():
    p = argparse.ArgumentParser(
        'DAL (Data Access/Abstraction Layer)',
        formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, width=100), # type: ignore
    )
    p.add_argument(
        '--source',
        type=str,
        required=True,
        help='''
Path to exported data. Can be single file, or a glob, e.g. '/path/to/exports/*.ext'
''')
    # TODO link to exports post why multiple exports could be useful
    p.add_argument(
        '--no-glob',
        action='store_true',
        help='Treat path in --source literally'
    )
    p.add_argument('-i', '--interactive', action='store_true', help='Start Ipython session to play with data')

    p.epilog = """
You can use =dal.py= (stands for "Data Access/Abstraction Layer") to access your exported data, even offline.

- main usecase is to be imported as python module to allow for programmatic access to your data.

  You can find some inspiration in [[https://github.com/karlicoss/my][=my.=]] package that I'm using as an API to all my personal data.

- to test it against your export, simply run: ~./dal.py --source /path/to/export~

- you can also try it interactively: ~./dal.py --source /path/to/export --interactive~

"""
    # TODO add docs on motivation behind DAL?
    return p


def main(*, DAL, demo=None):
    p = make_parser()
    args = p.parse_args()
    if '*' in args.source and not args.no_glob:
        sources = glob(args.source)
    else:
        sources = [args.source]

    # logger.debug('using %s', sources)
    dal = DAL(list(sorted(sources)))
    print(dal)
    # TODO autoreload would be nice... https://github.com/ipython/ipython/issues/1144
    # TODO maybe just launch through ipython in the first place?
    if args.interactive:
        import IPython # type: ignore
        IPython.embed(header="Feel free to mess with 'dal' object in the interactive shell")
    else:
        assert demo is not None, "No 'demo' in 'dal.py'?"
        demo(dal)


def logger(logger, **kwargs):
    # TODO FIXME vendorize
    try:
        # pylint: disable=import-error
        from kython.klogging import LazyLogger # type: ignore
    except ModuleNotFoundError as ie:
        import logging
        logging.exception(ie)
        logging.warning('fallback to default logger!')
        return logging.getLogger(logger)
    else:
        return LazyLogger(logger, **kwargs)


__all__ = [
    'PathIsh',
    'Json',
    'Res',
]

