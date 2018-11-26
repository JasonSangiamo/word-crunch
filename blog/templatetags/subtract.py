from django import template
register = template.Library()
#found at https://stackoverflow.com/questions/43282008/how-to-subtract-two-fields-in-django-templates and https://stackoverflow.com/questions/4938303/how-to-properly-make-custom-filter-in-django-framework
@register.filter(name = 'subtract')
def subtract(value, argument):
    return value-argument