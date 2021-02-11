

import pygame
from classes.plane import airplane
from classes.bullet import bullet
from classes.asteroid import asteroid
from classes.ufo import ufo

from time import perf_counter
from Mathematical_Functions import coordinates as mt
from Mathematical_Functions import Collision as ct
pygame.init()

# GLOBAL VARIABLES:
height = 600
width = 1000
screen_size = (width,height)
window = pygame.display.set_mode(screen_size, pygame.RESIZABLE)
background_color=(0,0,0)
CONTROLS=[pygame.K_LEFT,pygame.K_RIGHT,pygame.K_DOWN,pygame.K_UP]

def update_text(text_to_put,where=(140,30),anchor=False):
    global window
    font = pygame.font.Font('freesansbold.ttf', 32)
    text = font.render(text_to_put, True, (255,255,255))
    text_rect=text.get_rect()
    if anchor:
        text_rect.topleft = where
    else:
        text_rect.center=where
    window.blit(text, text_rect)


def wait_while_processing_events(seconds):
    start=perf_counter()
    global height,width
    while perf_counter()-start<seconds:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:

                pygame.quit()
                quit()
                break
            if event.type ==  pygame.VIDEORESIZE:
                height=pygame.display.get_window_size()
                width,height=height

def start_level(saucer_frequency,asteroid_num,alien_bullet_cooldown,big_side):
    global window,screen_size,width,height,score,player,bullet_color,bullet_cooldown


    bullets = []  # array of bullets to be stored
    asteroids = []  # array of asteroid objects in the game
    saucers = []  # array of ufo objects


    last_bullet_shot = perf_counter()  # when the last bullet was shot
    run = True

    death_animation_asteroids = []  # asteroids who have died, but still need to play their animation
    border_dic = {3: 0.19, 4: 0.17, 5: 0.14, 6: 0.12, 7: 0.1}  # dictionary of which side number gets how much border

    alien_bullets = []  # array of bullets shot by ufos

    # generating the initial round of asteroids:
    for i in range(asteroid_num):
        asteroids.append(
            asteroid(radius=30,player_coordinate_tuple=(player.x,player.y), side_num=big_side,
                     velocity_interval=(50, 100),
                     border=border_dic[5])
        )

    point_values = {big_side: 20, big_side - 1: 50, big_side - 2: 100}

    last_saucer = perf_counter()  # when the last saucer was generated

    while run and player.lives>0 and len(asteroids)>0:

        start=perf_counter()

        pygame.time.wait(10)

        update_text("Score: " + str(score) + " Lives: " + str(player.lives),where=(140+len(str(score))*10,30))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:

                pygame.quit()
                quit()
                break
            if event.type ==  pygame.VIDEORESIZE:
                height=pygame.display.get_window_size()
                width,height=height
                screen_size=(width,height)

        keys=pygame.key.get_pressed()
        #checking to see if spacebar is pressed, and the cooldown has passed
        if keys[pygame.K_x] and perf_counter()-last_bullet_shot>=bullet_cooldown:
            #initializing a bullet:

            #new coordinates generated so that the bullet matches the tip of the ship
            initx, inity = mt.cartesian(player.height,player.angle,(player.x,player.y))
            bullets.append(
                bullet(initx,inity,player.angle,1,color=bullet_color)
            )
            last_bullet_shot=perf_counter()

        #UPDATING AND DRAWING PLAYER:
        player.update_position(CONTROLS,#specifying controls
                               pygame.key.get_pressed(), #which keys are pressed
                               delta_time=perf_counter()-start,# timing how much time has passed
                               screen_width=width,
                               screen_height=height)
        player.fix_out_of_screen(screen_width=width,screen_height=height)
        player.draw(pygame,window)
        pygame.display.update()
        window.fill(background_color)

        #UPDATING AND DRAWING ALIEN BULLETS:
        for bul in alien_bullets:
            #The problem with the player's  coordinates, is that the bullet is initialized at the back of the
            # ship. To fix  this, we convert everything to polar coordinates, and increase the radius to match the tip of the ship.

            if ct.separating_axis_theorem(player.generate_corner_coordinates(),[(bul.x-bul.r,bul.y-bul.r),
                                                                                    (bul.x+bul.r,bul.y+bul.r),
                                                                                    (bul.x-bul.r,bul.y+bul.r),
                                                                                    (bul.x+bul.r,bul.y-bul.r)]):
                #they have collided
                player.lives-=1
                player.x,player.y=width/2,height/2
                alien_bullets.pop(alien_bullets.index(bul))

            else:
                #they have not collided, keep going
                bul.update_position(delta_time=perf_counter()-start)
                bul.draw(pygame,window,perf_counter()-start)

                #Checking to see if the bullet is out of the frame:
                if bul.x+bul.r>=width or bul.x+bul.r<=0:
                    alien_bullets.pop(alien_bullets.index(bul))
                elif bul.y+bul.r>height or bul.y+bul.r  <0:
                    alien_bullets.pop(alien_bullets.index(bul))

        #UPDATING AND DRAWING BULLETS:
        for b in bullets:
            #The problem with the player's  coordinates, is that the bullet is initialized at the back of the
            # ship. To fix  this, we convert everything to polar coordinates, and increase the radius to match the tip of the ship.
            b.update_position(delta_time=perf_counter()-start)
            b.draw(pygame,window,perf_counter()-start)

            #Checking to see if the bullet is out of the frame:
            if b.x+b.r>=width or b.x+b.r<=0:
                bullets.pop(bullets.index(b))
            elif b.y+b.r>height or b.y+b.r  <0:
                bullets.pop(bullets.index(b))



        #UPDATING THE SAUCERS:
        if perf_counter()-last_saucer>=saucer_frequency: #checking the ufo cooldown
            last_saucer=perf_counter()
            saucers.append(
                ufo(pygame,(player.x+(width/3))%width,(player.y+(height/3))%height)
            )
        for u in saucers:
            #checking to see if the ufo's bullet cooldown is down:
            if perf_counter()-u.last_bullet_shot>=alien_bullet_cooldown:
                u.last_bullet_shot=perf_counter() #reset cooldown
                alien_bullets.append(u.generate_alien_bullet((player.x,player.y)))



            hit=False
            for b in bullets:
                if ct.separating_axis_theorem(u.coordinates(),[(b.x-b.r,b.y-b.r),
                                                                                    (b.x+b.r,b.y+b.r),
                                                                                    (b.x-b.r,b.y+b.r),
                                                                                    (b.x+b.r,b.y-b.r)]):

                    hit=True
                    hit_bul = b

                    break

            if hit:
                score+=200
                if score%player.given_extra*10000==0:
                    #player.lives+=1
                    player.given_extra+=1
                saucers.pop(saucers.index(u))
                bullets.pop(bullets.index(hit_bul))
            else:
                if ct.separating_axis_theorem(player.generate_corner_coordinates(),u.coordinates()):
                    player.lives-=1
                    player.x, player.y = width / 2, height / 2

                u.update_position(perf_counter()-start)
                u.draw(pygame,window)
                if u.out_of_screen(screen_width=width,screen_height=height):
                    saucers.pop(saucers.index(u))

            # UPDATING AND DRAWING ASTEROIDS:
        for a in asteroids:
            # updated information:
            a.update_position(perf_counter() - start)
            a.draw(pygame, window)
            a.fix_out_of_screen(width, height)

            # checking to see if asteroid is hitting player:
            if ct.separating_axis_theorem(a.coordinates, player.generate_corner_coordinates()):
                player.lives -= 1
                player.x,player.y=width/2,height/2

            for b in bullets:
                # Checking to see if any bullet has hit any asteroid:
                if ct.radius_collision(a.x,a.y,a.radius,b.x,b.y,b.r):

                    # BEFORE ANYTHING, WE GET RID OF THE BULLET. EACH BULLET CAN ONLY POP 1 ASTEROID
                    bullets.pop(bullets.index(b))
                    if a.side_num > big_side - 2:

                        # the asteroid splits into 2 child asteroids with 1 less side number, and slightly smaller radius
                        child_1 = asteroid(radius=a.radius * 0.9, x=a.x, y=a.y, side_num=a.side_num - 1)
                        child_2 = asteroid(radius=a.radius * 0.9, x=a.x, y=a.y, side_num=a.side_num - 1)

                        child_2.drift_angle = 180 + child_1.drift_angle  # They need to explode in different directions

                        child_1.velocity = a.velocity + 20  # Children explode faster then their parent
                        child_2.velocity = a.velocity + 20

                        child_1.border = border_dic[
                            child_1.side_num]  # modifying their border according to their side number
                        child_2.border = border_dic[child_2.side_num]
                        asteroids.append(child_1)
                        asteroids.append(child_2)

                    else:
                        # this is the last piece, we have killed the entire asteroid:
                        pass
                    # death_animation_asteroids.append(a) #the asteroid will play it's death animation (which is a bunch of
                    # particles)
                    score += point_values[a.side_num]

                    asteroids.pop(asteroids.index(a))  # if they are colliding, we destroy the asteroid


    window.fill(background_color)



def do_they_want(line1="Would you like to be featured on the high score list?", line2="Press r to quit. Press any "
                                                                                      "other key to continue."):
    global height,width
    font = pygame.font.Font(None, 50) #Setting the font
    prompt=line1
    prompt_line_2=line2
    while True:
        pygame.time.wait(10)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                break
            if event.type == pygame.VIDEORESIZE:
                height = pygame.display.get_window_size()
                width, height = height

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r :
                    return False
                else:
                    return True


        prompt_surface=font.render(prompt,True,(255,255,255)) #initializing the prompt surface
        p2_surface =font.render(prompt_line_2,True,(255,255,255)) #initializing the prompt surface

        window.blit(prompt_surface,((width/2-7.6*len(prompt),200)))
        window.blit(p2_surface,((width/2-7.6*len(prompt_line_2),250)))
        pygame.display.update()
        window.fill((0,0,0))

def get_name(prompt="Enter a nickname less than 10 characters."):
    global height,width
    font = pygame.font.Font(None, 50) #Setting the font
    prompt=prompt
    user_text=""

    while True:
        pygame.time.wait(10)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                break
            if event.type == pygame.VIDEORESIZE:
                height = pygame.display.get_window_size()
                width, height = height

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    user_text = user_text[0:-1]

                elif event.key == pygame.K_RETURN: #pressed the enter key
                    return user_text
                else:
                    user_text += event.unicode



        prompt_surface=font.render(prompt,True,(255,255,255)) #initializing the prompt surface

        window.blit(prompt_surface,((width/2-7.6*len(prompt),200)))

        user_surface=font.render(user_text,True,(255,255,255)) #initializing the username surface

        window.blit(user_surface,((width/2-7.6*len(user_text),400)))
        pygame.display.update()
        window.fill((0,0,0))
def display_table():
    global width,height,window,pygame
    from Storing_High_Scores import handling_csv

    information=handling_csv.parse_csv(pre_path="Storing_High_Scores")
    lines_to_display=[]
    if len(information)==0:
        lines_to_display.append("There are no high scores to show")

    else:
        base = 150
        top_display=len(information)
        if len(information)>5:
            top_display=5

        for i in range(top_display):
            username=information[i][0]
            score=str(information[i][1])
            update_text(str(i+1)+". "+username, (width * 0.3, base + i * 50),True)
            update_text(str(score),(width*0.7,base+i*50),True)

    update_text("Press r to quit. Press any other key to play again..",where=(width/2,height*0.9))
    pygame.display.update()
    #Wait until user presses a key:
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                break
            if event.type == pygame.VIDEORESIZE:
                height = pygame.display.get_window_size()
                width, height = height

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r :
                    return False
                else:
                    return True

def play():
    global player,score,bullet_cooldown,bullet_color,width,height

    saucer_frequency = 3  # saucers are generated at this second frequency
    asteroid_num = 2
    alien_bullet_cooldown = 0.5  # The frequency of their shots
    score = 0  #
    bullet_color = (0, 255, 255)

    #Defining the player:
    player = airplane(x=width / 2, y=height / 2, units_per_second=100)
    player.lives = 3  # how many lives the player has

    level=1
    bullet_cooldown = 0.3 # you can only send bullets once this cooldown has finished
    update_text("Press any key to start game",(width/2,height/2))
    pygame.display.update()
    run=True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:

                pygame.quit()
                quit()
                break
            if event.type ==  pygame.VIDEORESIZE:
                height=pygame.display.get_window_size()
                width,height=height
                update_text("Press any key to start game",(width/2,height/2))
                pygame.display.update()

            if event.type == pygame.KEYDOWN:
                run=False
    window.fill((0,0,0))

    while player.lives>0:
        update_text("Wave " +str(level),where=(width/2,height/2))
        pygame.display.update()
        wait_while_processing_events(2)
        if level % 3==0 and saucer_frequency>5:
            saucer_frequency*=0.9


        if level%2==0:
            if asteroid_num<15:
                asteroid_num+=2

            if alien_bullet_cooldown > 0.7:
                alien_bullet_cooldown *= 0.9

        level+=1

        start_level(saucer_frequency=saucer_frequency,asteroid_num=asteroid_num,alien_bullet_cooldown=alien_bullet_cooldown,    big_side = 5)

    # #THE PLAYER HAS FINISHED THE GAME. WE WILL ASK FOR THE HIGH SCORE
    update_text("Game over.",where=(width/2,height/2))
    pygame.display.update()
    wait_while_processing_events(2)
    doeshe=do_they_want()
    if doeshe:
        from Storing_High_Scores.handling_csv import automate_insertion
        username = get_name()
        while len(username)>10:
            username=get_name("Nickname needs to be less than 10 characters.")
        display_high_score=do_they_want(line1="Your high score has been saved.",line2="Do you want to display high score "
                                                                                     "list? Press r to quit.")

        automate_insertion([username,score],pre_path="Storing_High_Scores")

        if display_high_score:
            again=display_table()
            pygame.display.update()
            if again:
                window.fill((0,0,0))
                play()

play()
