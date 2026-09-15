


def json2html(json_data):
    """Convert JSON data to a simple HTML representation."""
    if isinstance(json_data, dict):
        html = "<ul>"
        for key, value in json_data.items():
            html += f"<li><strong>{key}:</strong> {json2html(value)}</li>"
        html += "</ul>"
        return html
    elif isinstance(json_data, list):
        html = "<ul>"
        for item in json_data:
            html += f"<li>{json2html(item)}</li>"
        html += "</ul>"
        return html
    else:
        return str(json_data)