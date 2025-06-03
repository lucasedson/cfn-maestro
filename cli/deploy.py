import inquirer
from core.parse_templates import parse_templates

def deploy_menu():
    inquirer.prompt([inquirer.List("option", message="Select a template", choices=parse_templates())])