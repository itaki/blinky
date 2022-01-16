from cursesmenu import SelectionMenu

a_list=["red", "blue", "green"]
b_list=["go","back","home"]
menu = SelectionMenu(a_list,"Select an option")
menu2 = SelectionMenu(b_list,"not an option")

menu.show()
menu2.show()

menu.join()

menu2.join()

selection = menu.selected_option
