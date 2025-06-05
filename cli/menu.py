import inquirer
from core.run_cmd import run_shell_command, run_async_task, watch_shell_command
from core.parse_templates import parse_templates, parse_template_params

def main_menu():
    questions = [
        inquirer.List(
            "option",
            message="Select an option",
            choices=["My Infrastructure","Deploy", "Destroy", "Configure", "Exit"],
        ),
    ]
    return inquirer.prompt(questions)


def deploy_menu():
    questions = [
        inquirer.List(
            "option",
            message="Select ",
            choices=[
                "Stack",
                "Template",
            ]
        ),
    ]
    return inquirer.prompt(questions)

def deploy_menu_template():
    questions = [
        inquirer.List(
            "option",
            message="Select a template",
            choices=parse_templates(),
        ),
    ]
    
    return inquirer.prompt(questions)

def select_template(path):

    params = parse_template_params(path)
    formated_params = []
    print(params) # {'BucketName': {'Type': 'String', 'Default': 'sample-bucket'}}
    for param in params:
        param_value = input(f"Enter a value for {param}: ")
        formated_params.append(f"ParameterKey={param},ParameterValue={param_value}")
    stack_name = input("Enter a stack name: ")
    template_file = path




    cmd = f"awslocal cloudformation create-stack --stack-name {stack_name} --template-body file://{template_file} --parameters {','.join(formated_params)}"
    run_async_task(run_shell_command(cmd))
    
    # view_stack = input("Do you want to view the stack? (y/n): ")
    view_stack = inquirer.confirm("Do you want to view the stack?", default=True)
    
    if view_stack == True:
        cmd_view = f"awslocal cloudformation describe-stacks --stack-name {stack_name} --output table"
        run_async_task(watch_shell_command(cmd_view, interval=1.0))

    # destroy_stack = input("Do you want to destroy the stack? (y/n): ")
    destroy_stack = inquirer.confirm("Do you want to destroy the stack?", default=True)
    if destroy_stack == True:
        run_async_task(run_shell_command(f"awslocal cloudformation delete-stack --stack-name {stack_name}"))

def my_infrastructure():
    services = [
        "VPC",
        "S3",
        "EC2",
        "RDS",
        "ECS",
        "EKS"
    ]

    questions = [
        inquirer.List(
            "option",
            message="Select a service",
            choices=services,
        ),
    ]

    return inquirer.prompt(questions)

def view_service(service):
    if service == "VPC":
        run_async_task(run_shell_command("awslocal ec2 describe-vpcs --output table"))
    elif service == "S3":
        run_async_task(run_shell_command("awslocal s3 ls --output table"))
    elif service == "EC2":
        run_async_task(run_shell_command("awslocal ec2 describe-instances --output table"))
    elif service == "RDS":
        run_async_task(run_shell_command("awslocal rds describe-db-instances --output table"))
    elif service == "ECS":
        run_async_task(run_shell_command("awslocal ecs list-clusters --output table"))
    elif service == "EKS":
        run_async_task(run_shell_command("awslocal eks list-clusters --output table"))