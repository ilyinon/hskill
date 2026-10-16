"""Synthetic server rendering; only HTML text insertion is modeled."""
from html import escape

def main_page(value):
    return "<p>" + escape(value, quote=True) + "</p>"

def legacy_preview(value, encode=False):
    text = escape(value, quote=True) if encode else value
    return "<div>" + text + "</div>"
