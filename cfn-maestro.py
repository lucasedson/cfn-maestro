from cli.menu import main_menu, deploy_menu
if __name__ == "__main__":
    choose = main_menu()
    if choose["option"] == "Deploy":
        deploy_menu()
