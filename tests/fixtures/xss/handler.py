from html import escape

def render(value):
    if any(char in value for char in "<>"):
        return 400, "rejected"
    return 200, "<p>" + escape(value, quote=True) + "</p>"
