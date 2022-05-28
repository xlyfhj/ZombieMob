import itertools, sys, time, random, math, pygame
from pygame.locals import *
from MyLibrary import *
last_time = 0
many = 0
mode = 0
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
pygame.mixer.init()
mot = input("You want the game hard or normal(h/n)?")
if mot == 'h': mode = 1
pygame.init()
channel = pygame.mixer.find_channel(True)
audio_clip = pygame.mixer.Sound("zombie-eat.wav")
audio_clip2 = pygame.mixer.Sound("score.mp3")
pygame.mixer.music.load('Look up at the Sky.mp3')
pygame.mixer.music.play(-1)

#move zombies
def calc_velocity(direction, vel=1.0):
    velocity = Point(0,0)
    if direction == 0: #north
        velocity.y = -vel
    elif direction == 1: #north east
        velocity.x = vel
        velocity.y = -vel
    elif direction == 2: #east
        velocity.x = vel
    elif direction == 3: #east south
        velocity.x = vel
        velocity.y = vel
    elif direction == 4: #south
        velocity.y = vel
    elif direction == 5: #south west
        velocity.x = -vel
        velocity.y = vel
    elif direction == 6: #west
        velocity.x = -vel
    elif direction == 7: #west north
        velocity.x = -vel
        velocity.y = -vel
    return velocity

#reverse the zombies direction
def reverse_direction(sprite):
    if random.randint(1,5) == 1:
        if sprite.direction == 0:
            sprite.direction = 4
        elif sprite.direction == 1:
            sprite.direction = 5
        elif sprite.direction == 2:
            sprite.direction = 6
        elif sprite.direction == 3:
            sprite.direction = 7
        elif sprite.direction == 4:
            sprite.direction = 0
        elif sprite.direction == 5:
            sprite.direction = 1
        elif sprite.direction == 6:
            sprite.direction = 2
        elif sprite.direction == 7:
            sprite.direction = 3
    else:
        sprite.direction = random.randint(0, 7)

def z_reverse_direction(sprite):
    if sprite.direction == 0:
        sprite.direction = 4
    elif sprite.direction == 1:
        sprite.direction = 5
    elif sprite.direction == 2:
        sprite.direction = 6
    elif sprite.direction == 3:
        sprite.direction = 7
    elif sprite.direction == 4:
        sprite.direction = 0
    elif sprite.direction == 5:
        sprite.direction = 1
    elif sprite.direction == 6:
        sprite.direction = 2
    elif sprite.direction == 7:
        sprite.direction = 3

#keep the zombies turn in the direction of player
def forward_player(sprite):
    if player.X < sprite.X and player.Y > sprite.Y:
        if sprite.X - player.X == player.Y - sprite.Y: sprite.direction = 5
    elif player.X > sprite.X and player.Y > sprite.Y:
        if player.X - sprite.X == player.Y - sprite.Y: sprite.direction = 3
    elif player.X > sprite.X and player.Y < sprite.Y:
        if player.X - sprite.X == sprite.Y - player.Y: sprite.direction = 1
    elif player.X < sprite.X and player.Y < sprite.Y:
        if sprite.X - player.X == sprite.Y - player.Y: sprite.direction = 7
    elif player.X < sprite.X: sprite.direction = 6
    elif player.X > sprite.X: sprite.direction = 2
    elif player.Y > sprite.Y: sprite.direction = 4
    elif player.Y < sprite.Y: sprite.direction = 0

#main program begins
screen = pygame.display.set_mode((800,600))
pygame.display.set_icon(pygame.image.load('brain.png'))
pygame.display.set_caption("Zombie Mob Game")
font = pygame.font.Font(None, 36)
timer = pygame.time.Clock()
pygame.mouse.set_visible(False)

#load bitmaps
bg = pygame.image.load("background.jpg").convert_alpha()

#create sprite groups
player_group = pygame.sprite.Group()
zombie_group = pygame.sprite.Group()
health_group = pygame.sprite.Group()

#create the player sprite
player = MySprite()
player.load("farmer walk.png", 96, 96, 8)
player.position = 80, 80
player.direction = 4
player_group.add(player)

#create the zombie sprites
zombie_image = pygame.image.load("zombie walk.png").convert_alpha()
for n in range(0, 15):
    zombie = MySprite()
    zombie.load("zombie walk.png", 96, 96, 8)
    zombie.position = random.randint(0,700), random.randint(0,500)
    text = random.randint(0,3)
    if random.randint(1,3) == 1: text += 0.5
    zombie.direction = text * 2
    zombie_group.add(zombie)
    many += 1

#create heath sprite
health = MySprite()
health.load("health.png", 41, 50, 1)
health.position = 400,300
health_group.add(health)

game_over = False
player_moving = False
player_health = 100
ticktime = 30
#repeating loop
while True:
    timer.tick(ticktime)
    ticks = pygame.time.get_ticks()
    ticks2 = pygame.time.get_ticks()
    for event in pygame.event.get():
        if event.type == QUIT: sys.exit()
    keys = pygame.key.get_pressed()
    if keys[K_ESCAPE] or keys[K_RETURN]: sys.exit()
    elif keys[K_UP] and keys[K_LEFT] or keys[K_w] and keys[K_a]:
        player.direction = 7
        player_moving = True
    elif keys[K_UP] and keys[K_RIGHT] or keys[K_w] and keys[K_d]:
        player.direction = 1
        player_moving = True
    elif keys[K_LEFT] and keys[K_DOWN] or keys[K_a] and keys[K_s]:
        player.direction = 5
        player_moving = True
    elif keys[K_RIGHT] and keys[K_DOWN] or keys[K_d] and keys[K_s]:
        player.direction = 3
        player_moving = True
    elif keys[K_UP] or keys[K_w]:
        player.direction = 0
        player_moving = True
    elif keys[K_RIGHT] or keys[K_d]:
        player.direction = 2
        player_moving = True
    elif keys[K_DOWN] or keys[K_s]:
        player.direction = 4
        player_moving = True
    elif keys[K_LEFT] or keys[K_a]:
        player.direction = 6
        player_moving = True
    else:
        player_moving = False
    if ticks2 > last_time + 5000:#create a zombie every five second
        zombie = MySprite()
        zombie.load("zombie walk.png", 96, 96, 8)
        zombie.position = random.randint(0,700), random.randint(0,500)
        text = random.randint(0,3)
        if random.randint(1,3) == 1:text += 0.5
        zombie.direction = text * 2
        zombie_group.add(zombie)
        last_time = ticks2
        many += 1
        ticktime += 1

    if not game_over:
        #set animation frames based on player's direction
        player.first_frame = player.direction * player.columns
        player.last_frame = player.first_frame + player.columns-1
        if player.frame < player.first_frame:
            player.frame = player.first_frame

        if not player_moving:
            #stop animating when player is not pressing a key
            player.frame = player.first_frame = player.last_frame
        else:
            #move player in direction 
            player.velocity = calc_velocity(player.direction, 1.5)
            player.velocity.x *= 1.5
            player.velocity.y *= 1.5

        #update player sprite
        player_group.update(ticks, 50)

        #manually move the player
        if player_moving:
            player.X += player.velocity.x
            player.Y += player.velocity.y
            if player.X < 0: player.X = 0
            elif player.X > 700: player.X = 700
            if player.Y < 0: player.Y = 0
            elif player.Y > 500: player.Y = 500

        #update zombie sprites
        zombie_group.update(ticks, 50)

        #manually iterate through all the zombies
        for z in zombie_group:
            #set the zombie's animation range
            z.first_frame = z.direction * z.columns
            z.last_frame = z.first_frame + z.columns-1
            if z.frame < z.first_frame:
                z.frame = z.first_frame
            #keep the zombie on the screen
            if mode == 1: forward_player(z)#the zombies turn to player
            z.velocity = calc_velocity(z.direction)
            z.X += z.velocity.x
            z.Y += z.velocity.y
            if z.X < 0:
                z.X = 0
                reverse_direction(z)
            elif z.X > 700:
                z.X = 700
                reverse_direction(z)
            elif z.Y < 0:
                z.Y = 0
                reverse_direction(z)
            elif z.Y > 500:
                z.Y = 500
                reverse_direction(z)
        
        #check for collision with zombies
        attacker = None
        attacker = pygame.sprite.spritecollideany(player, zombie_group)
        if attacker != None:
            #we got a hit, now do a more precise check
            if pygame.sprite.collide_rect_ratio(0.5)(player,attacker):
                player_health -= 10
                channel.play(audio_clip)
                if attacker.X < player.X:
                    attacker.X -= 10
                elif attacker.X > player.X:
                    attacker.X += 10
                elif attacker.Y > player.Y:
                    attacker.Y += 10
                elif attacker.Y < player.Y:
                    attacker.Y -= 10
            else:
                attacker = None

        #check for collision with zombies
        for z in zombie_group:
            check = None
            check = pygame.sprite.spritecollideany(z, zombie_group)
            if check != None and check != z:
                #we got a hit, now do a more precise check
                if pygame.sprite.collide_rect_ratio(0.5)(z,check) and mode == 0:
                    if check.X < z.X:
                        check.X -= 10
                        z.X += 10
                    if check.X > z.X:
                        check.X += 10
                        z.X -= 10
                    if check.Y > z.Y:
                        check.Y += 10
                        z.Y -= 10
                    if check.Y < z.Y:
                        check.Y -= 10
                        z.Y += 10
                    z_reverse_direction(z)
                    z_reverse_direction(check)
                else:
                    check = None

        #check for collision with health
        if pygame.sprite.collide_rect_ratio(0.5)(player,health):
            player_health += 10
            channel.play(audio_clip2)
            if player_health > 100: player_health = 100
            health.X = random.randint(0,600)
            health.Y = random.randint(0,400)

    #update the health drop
    health_group.update(ticks, 50)

    #is player dead?
    if player_health <= 0:
        game_over = True
    
    #clear the screen
    screen.fill((50,50,100))

    # draw the background
    screen.blit(bg, (0, 0))

    #draw sprites
    health_group.draw(screen)
    zombie_group.draw(screen)
    player_group.draw(screen)

    #draw energy bar
    if player_health > 50:
        pygame.draw.rect(screen, GREEN, Rect(300, 570, player_health * 2, 25))
        pygame.draw.rect(screen, GREEN, Rect(300, 570, 200, 25), 2)
        print_text(font, 500, 570, str(player_health), GREEN)
    else:
        pygame.draw.rect(screen, RED, Rect(300, 570, player_health * 2, 25))
        pygame.draw.rect(screen, RED, Rect(300, 570, 200, 25), 2)
        print_text(font, 500, 570, str(player_health), RED)
    print_text(font, 550, 570, "zombies: ", GREEN)
    print_text(font, 660, 570, str(many), GREEN)

    if game_over:
            print_text(font, 300, 100, "G A M E  O V E R")
            print_text(font, 180, 150, "THE ZOMBIES ARE EATING YOUR BRAIN!")
            print_text(font, 320, 200, "TRY AGAIN!")

    pygame.display.update()
