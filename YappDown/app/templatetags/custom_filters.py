from django import template

register = template.Library()

@register.filter
def is_pdf(file_url):
    return file_url.lower().endswith('.pdf')

@register.filter
def is_docx(file_url):
    return file_url.lower().endswith('.docx')