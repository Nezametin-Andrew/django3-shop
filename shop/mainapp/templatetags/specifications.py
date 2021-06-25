from django import template
from django.utils.safestring import mark_safe

register = template.Library()

pass_field = [
    "ID",
    "Наименование",
    "Стоимость",
    "Описание",
    "Производитель",
    "Категория",
    "Изображение",
    "Просмотры",
    "Этот товар понравился",
    "Скидка",
    "Новинка"
]

TABLE_ELEMENT = """
            <tr>
            <td></td>
            <td>{name}</td>
            <td></td>
            <td>{value}</td>
            </tr>
"""


@register.filter
def product_spec(product):
    table_body = ""
    for field in product._meta.fields:
        if field.verbose_name in pass_field: continue
        table_body += TABLE_ELEMENT.format(name=field.verbose_name, value=field.value_to_string(product))
    return mark_safe(table_body)




