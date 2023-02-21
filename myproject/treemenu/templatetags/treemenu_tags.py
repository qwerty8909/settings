from django import template
from treemenu.models import MenuItem

register = template.Library()

@register.simple_tag(takes_context=True)
def draw_menu(context, menu_name):
    menu_items = MenuItem.objects.select_related('parent').filter(menu=menu_name).order_by('order')
    menu_dict = {}

    # Build menu dictionary
    for item in menu_items:
        if not item.parent:
            menu_dict[item] = {'item': item, 'children': []}
        else:
            if item.parent not in menu_dict:
                menu_dict[item.parent] = {'item': item.parent, 'children': []}
            menu_dict[item.parent]['children'].append(item)

    # Build menu HTML
    def build_menu_html(menu_dict, parent_id=None):
        html = ''
        if parent_id is None:
            for menu_item in menu_dict.values():
                html += '<li class="{}">'.format('active' if menu_item['item'].get_absolute_url() == context['request'].path else '')
                html += '<a href="{}">{}</a>'.format(menu_item['item'].get_absolute_url(), menu_item['item'].name)
                html += build_menu_html(menu_item['children'], menu_item['item'].id)
                html += '</li>'
        else:
            children = menu_dict.get(parent_id, {}).get('children', [])
            if children:
                html += '<ul>'
                for menu_item in children:
                    html += '<li class="{}">'.format('active' if menu_item.get_absolute_url() == context['request'].path else '')
                    html += '<a href="{}">{}</a>'.format(menu_item.get_absolute_url(), menu_item.name)
                    html += build_menu_html(menu_dict, menu_item.id)
                    html += '</li>'
                html += '</ul>'
        return html

    return build_menu_html(menu_dict)
