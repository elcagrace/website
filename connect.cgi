#! /home/elcagrace/opt/python-3.7.1/bin/python3

from server import load_skips, load_content, serve


serve(
    origin=__file__,
    title='Connect – Grace Lutheran Church, Lincoln, Nebraska',
    skips=load_skips(origin=__file__),
    content=load_content(origin=__file__),
)
