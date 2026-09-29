from django import template

register = template.Library()


@register.simple_tag
def active_tab(current_path, path):
    """Return 'active' if current_path starts with path."""
    return "active" if current_path.startswith(path) else ""
