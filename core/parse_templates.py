import os
import yaml

def parse_templates():
    templates = []
    for root, dirs, files in os.walk("templates"):
        for file in files:
            if file.endswith(".yaml"):
                templates.append(os.path.join(root, file))
    return templates


class CFNSafeLoader(yaml.SafeLoader):
    pass

def cfn_tag_ignore(loader, tag_suffix, node):
    return loader.construct_scalar(node)

# Registrar as tags mais comuns do CloudFormation
for tag in ['!Ref', '!Sub', '!GetAtt', '!Join', '!FindInMap', '!ImportValue', '!Select', '!Split', '!If']:
    CFNSafeLoader.add_multi_constructor(tag, cfn_tag_ignore)

def parse_template_params(template_path):
    with open(template_path, "r") as f:
        documents = yaml.load_all(f, Loader=CFNSafeLoader)
        
        parameters = []
        for document in documents:
            if "Parameters" in document:
                parameters = document["Parameters"]
        
        # print(parameters)
        return parameters

if __name__ == "__main__":
    parse_template_params("templates/s3/s3-template.yaml")