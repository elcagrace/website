import os
import sys

from datetime import date


INACTIVE_NAVIGATION_ITEM_TEMPLATE = '<li><a href="{url}">{name}</a></li>'
ACTIVE_NAVIGATION_ITEM_TEMPLATE = '<li class="active"><a>{name}</a></li>'
SCRIPT_TAG_TEMPLATE = '<script src="./theme/js/{script}"></script>'


def serve_by_template(template_path, origin, navigation, scripts=(), **kwargs):
    with open(template_path, encoding='utf-8') as template_file:
        template = template_file.read()
    page_url = os.path.basename(origin)
    navigation = ''.join(
        (ACTIVE_NAVIGATION_ITEM_TEMPLATE if url == page_url else INACTIVE_NAVIGATION_ITEM_TEMPLATE).format(
            name=name,
            url=url,
        ) for name, url in navigation
    )
    year = date.today().year
    extra_scripts = '\n    '.join(
        SCRIPT_TAG_TEMPLATE.format(script=script) for script in scripts
    )
    substitutions = {
        'navigation': navigation,
        'skips': '',
        'year': year,
        'extra_scripts': extra_scripts,
    }
    substitutions.update(kwargs)
    output = f'Content-Type: text/html\n\n{template.format(**substitutions)}'
    sys.stdout.buffer.write(output.encode('utf-8'))
