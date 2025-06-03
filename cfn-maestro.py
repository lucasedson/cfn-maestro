import inquirer
from cli.menu import main_menu, deploy_menu, deploy_menu_template, select_template, my_infrastructure, view_service

if __name__ == "__main__":
    
    choose = main_menu()
    if choose["option"] == "Deploy":
        choose_deploy = deploy_menu()
        if choose_deploy["option"] == "Template":
            choose_deploy_template = deploy_menu_template()
            print(choose_deploy_template)
            if choose_deploy_template["option"]:
                select_template(choose_deploy_template["option"])

        elif choose["option"] == "Exit":
            exit()
    elif choose["option"] == "My Infrastructure":
        print("My Infrastructure")
        choose_infrastructure = my_infrastructure()

        print("Viewing " + choose_infrastructure["option"])
        view_service_name = choose_infrastructure["option"]
        view_service(view_service_name)