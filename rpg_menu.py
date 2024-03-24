def title() -> None:
    wall = "------------------------------------"
    name = "terminal turns"
    copyright = "copyright @sytemgames all rights reserved"
    print(wall)
    print(name)
    print(copyright)
    print(wall)

def story() -> None:
    print("you drive round the corner and see a deer you swerve around it\n")
    input("ENTER\n")
    print("you roll down the hill and wake up in a garden\n")
    input("ENTER\n")
    print("you crawl out the broken window and realize your trapped in a garden\n")
    input("ENTER\n")

def help() -> None:
    print("to move type move than enter and the dir you want to go\nto heal type heal\nto attack type attack\nto look around type look\nto pick up an item type pick than enter than the item you want\nto veiw your stats type stats\nto veiw this menu again type help\n")