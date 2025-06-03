import inquirer

from core.parse_templates import parse_templates
def main_menu():
    questions = [
        inquirer.List(
            "option",
            message="Select an option",
            choices=["Deploy", "Destroy", "Exit"],
        ),
    ]
    return inquirer.prompt(questions)


def deploy_menu():
    inquirer.prompt([inquirer.List("option", message="Select a template", choices=parse_templates())])