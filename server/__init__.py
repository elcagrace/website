import os
import sys
import markdown

from subprocess import run, PIPE

from .flavors import SkipFlavor, ContentFlavor, SidebarFlavor, IndexFlavor, FormFlavor
from .template import serve_by_template


def _load(origin, flavor):
    name, _ = os.path.splitext(os.path.basename(origin))
    with open(f'content/pages/{name}.md', encoding='utf-8') as source_file:
        source = source_file.read()
    return markdown.markdown(source, extensions=(flavor,), output_format='html5')


SKIP_FLAVOR = SkipFlavor()
CONTENT_FLAVOR = ContentFlavor()
SIDEBAR_FLAVOR = SidebarFlavor()
INDEX_FLAVOR = IndexFlavor()


def load_skips(origin):
    return _load(origin, SKIP_FLAVOR)


def load_content(origin):
    return _load(origin, CONTENT_FLAVOR)


def load_sidebar(origin):
    return _load(origin, SIDEBAR_FLAVOR)


def load_index(origin):
    return _load(origin, INDEX_FLAVOR)


def load_form(origin, substitutions):
    return _load(origin, FormFlavor(substitutions))


TEMPLATE_PATH = './theme/templates/page.html'
NAVIATION = (
    ('Home', 'index.cgi'),
    ('About', 'about.cgi'),
    ('Visit', 'visit.cgi'),
    ('Connect', 'connect.cgi'),
    ('Community', 'community.cgi'),
    ('Resources', 'resources.cgi'),
    ('Sermons', 'sermons.cgi'),
)


def git_pull():
    run(('git', 'pull'), stdin=PIPE, stdout=PIPE)


def serve(origin, scripts=(), **kwargs):
    serve_by_template(TEMPLATE_PATH, origin, NAVIATION, scripts, **kwargs)
    os.close(sys.stdout.fileno())
    sys.stdout.close()
    git_pull()
