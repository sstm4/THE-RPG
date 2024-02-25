#random and time
import random
import time

#global var map
global map

#movement checker
dir_list =[]

#paths
p1 = "east"
p2 = "west"
p3 = "north"
p4 = "south"
p5 = "stay"
e1_path = [p2,p3,p2,p5,p5,p5,p4,p1]

#map
map = {"big_hall":{"available_dir":{"east":"small_hall","north":"feasting_room","west":"yard","stay":"big hall","south":"bathroom"}},
       "small_hall":{"available_dir":{"west":"big_hall","south":"bedroom","east":"entrance","stay":"small_hall","north":"bedroom2"}}
       ,"feasting_room":{"available_dir":{"south":"big_hall","west":"kitchen","stay":"feasting_room"}},
       "kitchen":{"available_dir":{"east":"feasting_room","stay":"kitchen","south":"storage"}},
       "bedroom":{"available_dir":{"north":"small_hall","stay":"bedroom","west":"closet"}},
       "yard":{"available_dir":{"east":"big_hall","south":"shed","stay":"yard"}},
       "shed":{"available_dir":{"north":"yard","stay":"shed"}},
       "front_yard":{"available_dir":{"west":"entrance","stay":"front_yard"},"room_items":["basic_sword"]},
       "entrance":{"available_dir":{"east":"front_yard","west":"small_hall","stay":"entrance"}},
       "closet":{"available_dir":{"east":"bedroom","stay":"closet"}},
       "bedroom2":{"available_dir":{"south":"small_hall","stay":"bedroom2"}},
       "bathroom":{"available_dir":{"north":"big_hall","stay":"bathroom"}},
       "storage":{"available_dir":{"north":"kitchen","stay":"storage"}}}

class Inventory():
    def __init__(self):
        self.items = []
        
    def add_item(self,item):
        self.items.append(item)
        print(f"you picked up {item}")
        
    def remove_item(self,item):
        if item in self.items:
            self.items.remove(item)
            print(f"you have used/dropped {item}")
        else:
            print("you dont have that")
            
    def display_items(self):
        if self.items:
            for item in self.items:
                print(f"- {item}")
        else:
            print("you have no items")
        
#player class
class Player:
    
    
    #initilitation
    def __init__(self,health,position):
        self.health = health
        self.position = position
        self.attack_dmg = 25
        self.inventory = Inventory()
        
    #movement
    def move(self):
        print("\nYour available directions are:\n")
    
        #displays the dir
        for dir in (map[self.position]["available_dir"].keys()):
            print(dir.title())
            dir_list.append(dir)
            
        #input
        dir = input("what dir do you want to move:\n> ").lower()
        
        #movement check
        if dir not in dir_list:
            print("invalid dir ")
            dir = "stay"
        
        #change position
        self.position = (map[self.position]["available_dir"][dir])
        print(f"you're in {self.position}")
        
        
        
    #heal 
    def heal(self):
        self.health += 10 
        if self.health > 100:
            self.health = 100
        print(f"you healed you are now at {self.health} health")
        
    #player attack
    def attack(self,enemy):
        print("player turn")
        action = input(str("choose an action\n")).lower()
        if action == "attack":
            player_attack_succ = random.random() < 0.8
            if player_attack_succ:
                enemy.health -= player.attack_dmg
                print(f"you hit {enemy.name} and done {player.attack_dmg} damage\nthe {enemy.name} has {enemy.health} health left")
            else:
                print("you missed")
        else:
            print("you can't spell atck you lose a turn\n ps go to school")
        
    def take_item(self,item):
        self.inventory.add_item(item)
        
    def use_item(self,item):
        self.inventory.remove_item(item)
    
#enemy class
class Enemy:
    
    #total enemys
    total_enemys = 0
    
    #initilitation
    def __init__(self,health,position,name,attack_dmg):
        self.health = health
        self.position = position
        self.name = name
        self.attack_dmg = attack_dmg
        Enemy.total_enemys += 1
        print(Enemy.total_enemys)
    
    #enemy attack
    def attack(self,player):
        print("enemy turn")
        enemy_attack_succ = random.random() < 0.5
        if enemy_attack_succ:
            player.health -= self.attack_dmg
            print(f"{self.name} hit you for {self.attack_dmg} damage\n\nyou have {player.health} health left")
        else:
            print(f"{self.name} missed")
    

#menu     
def menu():
        
    #menu options
    menu_options = ["move","heal","quit","items","look","pick"]
    
    #loop
    while True:
        
        #input
        input_choice = input("what do you want to do:\n> ").lower()
        
        #return
        if input_choice in menu_options:
            return input_choice
        
        #input check
        else:
            print("invalid input")

#combat loop
def combat(player,enemy):
    print(f"you're in the same room as {enemy.name}")
    while player.health > 0 or enemy.health > 0:
        input("press ENTER to continue\n")
        player.attack(enemy)
        if enemy.health <= 0:
            print(f"the {enemy.name} has been defeated")
            break
        input("press ENTER to continue\n")
        enemy.attack(player)
        if player.health <= 0:
            print(f"you have been defeated by the {enemy.name}")
            break
        

#player initilitation
player = Player(100,"front_yard")

#enemy initilitation
e1 = Enemy(50,"small_hall","test",25)


#main loop
while True:
    
    #health check
    if player.health <= 0:
        print("you died")
        quit()
    
    #gets choice
    menu_choice = menu()
    
    #movement
    if menu_choice == "move":
        player.move()
        if player.position == e1.position:
            combat(player,e1)
        
    #healing
    elif menu_choice == "heal":
        player.heal()
        
            
    elif menu_choice == "items":
        player.inventory.display_items()
        
    elif menu_choice == "look":
        if "room_items" in map[player.position].keys():
            for x in map[player.position]["room_items"]:
                print(x.title())
            
        else:
            print("there is no items in this room :(")
            
    elif menu_choice == "pick":
        if "room_items" in map[player.position].keys():
            item_wanted = str(input("ask for an item:\n> ")).lower()
            if item_wanted in map[player.position]["room_items"]:
                player.take_item(item_wanted)
                
            else:
                print("that item dosen't exist :(")
                
        else:
            print("there is no items in this room :(")
        
    #quit
    elif menu_choice == "quit":
        quit()