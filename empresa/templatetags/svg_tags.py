import re
from typing import Optional

from django import template
from django.utils.safestring import mark_safe

register = template.Library()


def _add_class(svg_content: str, css_class: Optional[str]) -> str:
    if not css_class:
        return svg_content

    class_attribute = f'class="{css_class}"'

    if 'class=' in svg_content:
        return re.sub(
            r'class="([^"]*)"',
            lambda match: f'class="{match.group(1)} {css_class}"',
            svg_content,
            count=1,
        )

    return svg_content.replace('<svg', f'<svg {class_attribute}', 1)


@register.simple_tag
def render_svg(file_field, css_class: str = '') -> str:
    """
    Renders the contents of an SVG FileField inline, allowing color to inherit from CSS.
    """
    if not file_field:
        return ''

    try:
        with file_field.open('rb') as svg_file:
            raw_content = svg_file.read()
        content = raw_content.decode('utf-8', errors='ignore')
    except (FileNotFoundError, ValueError, OSError):
        return ''

    return mark_safe(_add_class(content, css_class))

