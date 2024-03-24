#random and time
import random
from rpg_menu import *

#global vars
global map
global psucc
psucc = 0.5
5
#movement checker
dir_list =[]

#paths
p1 = "east"
p2 = "west"
p3 = "north"
p4 = "south"
p5 = "stay"
e1_path = [p2,p3,p2,p5,p5,p5,p4,p1]

placed_enemys = []

#map
map = {"big_hall":{"available_dir":{"east":"small_hall","north":"feasting_room","west":"yard","stay":"big hall","south":"bathroom"},
        #big hall items
        "room_items":["brown_key"]},
       "small_hall":{"available_dir":{"west":"big_hall","south":"bedroom","east":"entrance","stay":"small_hall","north":"bedroom2"}
        #small hall items
        ,"room_items":["grip_gloves"]}
       ,"feasting_room":{"available_dir":{"south":"big_hall","west":"kitchen","stay":"feasting_room"}},
       "kitchen":{"available_dir":{"east":"feasting_room","stay":"kitchen","south":"storage"}},
       "bedroom":{"available_dir":{"north":"small_hall","stay":"bedroom","west":"closet"}},
       "yard":{"available_dir":{"east":"big_hall","south":"shed","stay":"yard"},
        #locked doors
        "locked_doors":{"south":"brown_key"}},
       "shed":{"available_dir":{"north":"yard","stay":"shed"},"room_items":["shotgun"]},
       "front_yard":{"available_dir":{"west":"entrance","stay":"front_yard"},"room_items":["basic_sword"]},
       "entrance":{"available_dir":{"east":"front_yard","west":"small_hall","stay":"entrance"}},
       "closet":{"available_dir":{"east":"bedroom","stay":"closet"}},
       "bedroom2":{"available_dir":{"south":"small_hall","stay":"bedroom2"}},
       "bathroom":{"available_dir":{"north":"big_hall","stay":"bathroom"}},
       "storage":{"available_dir":{"north":"kitchen","stay":"storage"}},
       "backrooms":{"avialable_dir":{"stay":"backrooms"}}}

#e types
enemy_types = {
    "goblin":{"min_health":30,"max_health":75,"min_attack_dmg":25,"max_attack_dmg":35,"hit_chance":0.5},
    "skeleton":{"min_health":20,"max_health":30,"min_attack_dmg":35,"max_attack_dmg":40,"hit_chance":0.65},
    "golem":{"min_health":50,"max_health":75,"min_attack_dmg":10,"max_attack_dmg":15,"hit_chance":0.5}
}


#inventory
class Inventory():
    
    #initilitation
    def __init__(self):
        self.items = []
        
    #add items
    def add_item(self,item):
        self.items.append(item)
        print(f"you picked up {item}")
        
    #remove item
    def remove_item(self,item):
        if item in self.items:
            self.items.remove(item)
            print(f"you have used/dropped {item}")
        else:
            print("you dont have that")
            
    #display items
    def display_items(self):
        if self.items:
            for item in self.items:
                print(f"- {item}")
        else:
            print("you have no items")
        
#player class
class Player:
    
    
    #initilitation
    def __init__(self,health,position,succ):
        self.health = health
        self.position = position
        self.attack_dmg = 25
        self.succ = succ
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
            
        #check locked doors
        if dir in map[self.position].get("locked_doors",{}):
            required_key = map[self.position]["locked_doors"][dir]
            if required_key in self.inventory.items:
                print(f"you unlocked the door with the {required_key}")
                self.use_item(required_key)
            else:
                print(f"the door is loked you need {required_key}")
                return
        
        #change position
        self.position = (map[self.position]["available_dir"][dir])
        print(f"you're in {self.position}")
        
        #check enemys
        for enemy in placed_enemys:
            if enemy.position == self.position:
                combat(self,enemy)
        
        
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
            player_attack_succ = random.random() < self.succ
            if player_attack_succ:
                enemy.health -= player.attack_dmg
                print(f"you hit {enemy.name} and done {player.attack_dmg} damage\nthe {enemy.name} has {enemy.health} health left")
            else:
                print("you missed")
        else:
            print("you can't spell atck you lose a turn\n ps go to school")
        
    #add item
    def take_item(self,item):
        self.inventory.add_item(item)
        if item == "basic_sword":
            self.attack_dmg = 50
        elif item == "grip_gloves":
            self.succ = 0.8
        elif item == "shotgun":
            self.attack_dmg = 100
        
    #remove item
    def use_item(self,item):
        self.inventory.remove_item(item)
    
    #stats
    def stats(self):
        print(f"you have {self.health} health left, {self.attack_dmg} attack dmg, {self.succ} success rate and youre at {self.position}")
        
    #help
    def call_help(self):
        help()
    
#enemy class
class Enemy:
    
    #total enemys
    total_enemys = 0
    
    #initilitation
    def __init__(self,health,position,name,attack_dmg,succ):
        self.health = health
        self.position = position
        self.name = name
        self.attack_dmg = attack_dmg
        self.succ = succ
        Enemy.total_enemys += 1
        print(Enemy.total_enemys)
    
    #enemy attack
    def attack(self,player):
        print("enemy turn")
        enemy_attack_succ = random.random() < self.succ
        if enemy_attack_succ:
            player.health -= self.attack_dmg
            print(f"{self.name} hit you for {self.attack_dmg} damage\n\nyou have {player.health} health left")
        else:
            print(f"{self.name} missed")
    

#menu     
def menu():
        
    #menu options
    menu_options = ["move","heal","quit","items","look","pick","mario","stats","help"]
    
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
            enemy.position = "backrooms"
            break
        input("press ENTER to continue\n")
        enemy.attack(player)
        if player.health <= 0:
            print(f"you have been defeated by the {enemy.name}")
            break
        
#random enemy
def ran_enemy(pos):
    enemy_type = random.choice(list(enemy_types.keys()))
    min_health = enemy_types[enemy_type]["min_health"]
    max_health = enemy_types[enemy_type]["max_health"]
    health = random.randint(min_health,max_health)
    
    min_attack_dmg = enemy_types[enemy_type]["min_attack_dmg"]
    max_attack_dmg = enemy_types[enemy_type]["max_attack_dmg"]
    attack_dmg = random.randint(min_attack_dmg,max_attack_dmg)
    
    print(health,pos,enemy_type,attack_dmg,enemy_types[enemy_type]["hit_chance"])
    
    return Enemy(health,pos,enemy_type,attack_dmg,enemy_types[enemy_type]["hit_chance"])

def place_enemys(amount_enemys):
    occ_rooms = ["front_yard","backrooms"]
    while Enemy.total_enemys < amount_enemys:
        room = random.choice(list(map.keys()))
        if room not in occ_rooms:
            placed_enemys.append(ran_enemy(room))
            occ_rooms.append(room)
    print(placed_enemys)

#player initilitations
player = Player(100,"front_yard",psucc)

#diffuculty
def ask_diff() ->None:
     diffuculty = str.lower(input(("input diffuculty:\n> baby , easy , medium , hard , hellish , gamer\n")))
     global selected_enemys
     if diffuculty == "baby":
          selected_enemys = 0
         
     elif diffuculty == "easy":
         selected_enemys = 3
         
     elif diffuculty == "medium":
         selected_enemys = 5
         
     elif diffuculty == "hard":
         selected_enemys = 8
         
     elif diffuculty == "hellish":
         selected_enemys = 10
         
     elif diffuculty == "gamer":
         selected_enemys = 12
ask_diff()

#enemy initilitation
place_enemys(selected_enemys)

def start() -> None:
    #story
    player.call_help()
    story()
    title()
    
start()

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
        

    #healing
    elif menu_choice == "heal":
        player.heal()
        
    #display items
    elif menu_choice == "items":
        player.inventory.display_items()
        
    #look around
    elif menu_choice == "look":
        if "room_items" in map[player.position].keys():
            for x in map[player.position]["room_items"]:
                print(x.title())
        
        #no item
        else:
            print("there is no items in this room :(")
            
    #pick up item
    elif menu_choice == "pick":
        if "room_items" in map[player.position].keys():
            item_wanted = str(input("ask for an item:\n> ")).lower()
            if item_wanted in map[player.position]["room_items"]:
                player.take_item(item_wanted)
            
            #item dosent exist
            else:
                print("that item dosen't exist :(")
        
        #no item
        else:
            print("there is no items in this room :(")
            
        #super
    elif menu_choice == "mario":
        player.health = 9999999
        player.attack_dmg = 9999999
        player.succ = 1
        print("DONT HEAL")
        
    #stats
    elif menu_choice == "stats":
        player.stats()
        
    #help
    elif menu_choice == "help":
        player.call_help()
        
    #quit
    elif menu_choice == "quit":
        quit()