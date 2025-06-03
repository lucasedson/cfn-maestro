import os

def parse_templates():
    templates = []
    for root, dirs, files in os.walk("templates"):
        for file in files:
            if file.endswith(".yaml"):
                templates.append(os.path.join(root, file))
    return templates