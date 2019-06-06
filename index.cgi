#! /home/elcagrace/opt/python-3.7.1/bin/python3

from server import load_sidebar, load_index, serve


serve(
    origin=__file__,
    title='Grace Lutheran Church, Lincoln, Nebraska',
    skips='',
    content=load_sidebar(origin='sidebar') + load_index(origin=__file__),
    scripts=(
        'carousel.js',
    ),
)
