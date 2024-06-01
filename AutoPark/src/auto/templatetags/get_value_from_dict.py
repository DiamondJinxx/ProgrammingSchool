from django import template


register = template.Library()


@register.filter()
def get_value_from_dict(mapper, key) -> str:
    if key:
        return mapper[key]
