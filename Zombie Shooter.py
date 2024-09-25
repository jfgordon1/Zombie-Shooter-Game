'''

Heavy inspiration taken from Zombies Ate My Neighbor on SNES

Designer Documentation
https://designer-edu.github.io/designer/students/docs.html#

Phase 1:
## Galaga Features
# Milestone 1
[X] Spaceship exists 🔫 - water gun
[X] Spaceship moves
[X] Holding keys
[X] Screen limits
# Milestone 2
[X] Aliens exist 🧟 - zombie
[X] Aliens move
[X] Aliens wrap
[X] Aliens reset
[X] Aliens hurt (P.S. if time allows, flash water gun after collision)
# Milestone 3
[X] Shoot lasers 💧 - water
[X] Lasers move
[X] Offscreen lasers
[X] Lasers hurt
[X] Game over
[X] Show stats
# Extra Credit
[ ] Explosions
[ ] Menus
[ ] Items
[ ] Tractor Beams
'''
from designer import *
from dataclasses import dataclass
from random import randint

GUN_SPEED = 5
WATER_SPEED = 4

@dataclass
class World:
    water_gun: DesignerObject
    water_gun_speed: int
    left_key: bool
    right_key: bool
    zombies: []
    zombie_speed: int
    spawn_cap: int
    waters: []
    score: int
    lives: int
    round_num: int
    round_update: int
    score_text: DesignerObject
    lives_text: DesignerObject
    round_text: DesignerObject
 





#creation functions
    
def create_gun() -> DesignerObject:
    """ Create the water gun """
    water_gun = emoji("🔫")
    water_gun.y = get_height() - 75
    water_gun.x = get_width() / 2
    water_gun.angle = -90
    return water_gun

def create_zombie() -> DesignerObject:
    """ Create a zombie on the screen """
    zombie = emoji('🧟')
    zombie.x = randint(50, get_width()-50)
    zombie.y = 0
    return zombie

def create_water() -> DesignerObject:
    """
        creates the water drop that will be used to shoot the zombies
    """
    water = emoji('💧')
    water.angle = 180
    return water

def create_world() -> World:
    """ Create the world """
    return World(
                 create_gun(),
                 GUN_SPEED,
                 False,
                 False,
                 [],
                 3,
                 40,
                 [],
                 0,
                 3,
                 1,
                 20,
                 text("black", "", 20, get_width()*0.5, get_height()/2 + 25),
                 text("black", "", 20, get_width()*0.5, get_height()/2),
                 text("black", "", 20, get_width()*0.5, get_height()/2 + 50)
                 )

#Water Gun Functions

def move_gun(world: World):
    """ Move the ship horizontally based on which key field of the world is true"""
    if world.left_key:
        move_left(world)
    elif world.right_key:
        move_right(world)
    else:
        world.left_key = False
        world.right_key = False

def start_key(world: World, key: str):
    ''' activates one of the key fields from the World Dataclass. '''
    if key == "left":
        world.left_key = True
    elif key == "right":
        world.right_key = True
        
def stop_key(world: World, key: str):
    ''' detects the key to show which one should stop '''
    if key == "left":
        world.left_key = False
    elif key == "right":
        world.right_key = False

def move_left(world: World):
    """ Make the gun start moving left """
    world.water_gun_speed = -GUN_SPEED
    world.water_gun.x += world.water_gun_speed
    
def move_right(world: World):
    """ Make the gun start moving left """
    world.water_gun_speed = GUN_SPEED
    world.water_gun.x += world.water_gun_speed
    
def screen_limits(world: World):
    """ uses the gun's position on the screen to create a boundary """
    if world.water_gun.x > get_width():
        world.water_gun.x = get_width()
    elif world.water_gun.x < 0:
        world.water_gun.x = 0

#Zombie Functions
        
def make_zombies(world: World):
    """ Creates a new zombie to replace the old ones at a random rate """
    good_amount_of_zombies = len(world.zombies) < world.spawn_cap
    spawn_chance = randint(1, 5) == 1
    if good_amount_of_zombies and spawn_chance:
        world.zombies.append(create_zombie())
        
def move_zombies(world: World):
    """ moves the zombies down the screen"""
    for zombie in world.zombies:
        zombie.y += world.zombie_speed

def wrap_zombies(world: World):
    """ moves the zombies back up to the top of the screen if they are
        not destroyed before hitting the bottom of the screen"""
    for zombie in world.zombies:
        if zombie.y >= get_height():
            zombie.y = 0

def zombie_ship_collision(world: World):
    for index, zombie in enumerate(world.zombies):
        if colliding(world.water_gun, zombie):
            destroy(zombie)
            del world.zombies[index]
            world.lives -= 1

#gun functions:

def water_pos(water: DesignerObject, ship: DesignerObject):
    """ Move the bottom object to be below the top object """
    water.y = ship.y - 1
    water.x = ship.x
    
def move_water(world: World):
    """ Move all the water drops down """
    for water in world.waters:
        water.y -= WATER_SPEED
        
def destroy_waters_on_landing(world: World):
    """ Destroy any water drops that have landed on the ground """
    kept = []
    for index, water in enumerate(world.waters):
        if water.y > 0:
            kept.append(water)
        else:
            destroy(water)
            del world.waters[index]
    world.waters = kept

def shoot_water(world: World, key: str):
    if key == "space" and len(world.waters) < 3:
        water_drop = create_water()
        water_pos(water_drop, world.water_gun)
        world.waters.append(water_drop)

def zombie_water_collision(world: World):
    """
        function that detects the collision between each drop of water and each zombie created
    """
    for index_zombie, zombie in enumerate(world.zombies):
        for index_water, water in enumerate(world.waters):
            if colliding(water, zombie):
                destroy(water)
                del world.waters[index_water]
                destroy(zombie)
                del world.zombies[index_zombie]
                world.score += 1
#General Cleanup Functions

def update_score(world : World):
    """
        Update the score
    """
    world.score_text.text = "Score: " + str(world.score)

def update_lives(world : World):
    """
        Update the score
    """
    world.lives_text.text = "Lives: " + str(world.lives)
    
def update_round_text(world : World):
    """
        Updates the round text
    """
    world.round_text.text = "Round: " + str(world.round_num)
    
def flash_game_over(world: World):
    """
        Show the game over message
    """
    world.lives_text.text = "GAME OVER!"

def check_lives(world: World) -> bool:
    """
        checks the amount of lives that the player has left
    """
    has_died = False
    if world.lives == 0:
        has_died = True
    return has_died
    
def update_round(world: World):
    """
        updates the speed and number of zombies allowed on screen
    """
    world.zombie_speed += 3
    world.spawn_cap +=20
    
    
def check_score(world: World) -> bool:
    """
        checks the score to see if the score matches the score
        needed to update the round
    """
    TrueorFalse = False
    
    if world.score == world.round_update:
        TrueorFalse = True
        world.round_update+=20
    return TrueorFalse
    
when('starting', create_world)
when("updating", screen_limits)
when('typing', start_key)
when('typing', shoot_water)
when('done typing', stop_key)
when("updating", move_gun)
when("updating", make_zombies)
when("updating", move_zombies)
when("updating", wrap_zombies)
when("updating", update_lives)
when("updating", update_score)
when('updating', update_round_text)
when("updating", zombie_ship_collision)
when('updating', zombie_water_collision)
when('updating', move_water)
when('updating', destroy_waters_on_landing)
when(check_score, update_round)
when(check_lives, flash_game_over, pause)
start()

