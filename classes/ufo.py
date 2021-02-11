
from random import uniform,choice
from classes.bullet import bullet
from Mathematical_Functions import coordinates as ct

class ufo:

    def __init__(self,pygame,x,y,change_direction_time=2):
        from time import perf_counter

        self.x=x
        self.y=y
        self.initialized_time=perf_counter()
        self.change_direction_time=change_direction_time #How frequently the ufo changes direction
        self.generate_new_components()
        self.image= pygame.image.load(r'classes\images\ufo.PNG')
        self.width=66
        self.height=31
        self.last_bullet_shot=perf_counter() #when it shot the last bullet
    def generate_new_components(self,velocity_interval=(20,50)):
        #generating a random trajectory for the ufo to go in:
        self.x_component=uniform(velocity_interval[0],velocity_interval[1])*choice([-1,1])
        self.y_component=uniform(velocity_interval[0],velocity_interval[1])*choice([-1,1])

    def get_velocity(self,delta_time):
        return delta_time*self.x_component,delta_time*self.y_component

    def update_position(self,delta_time):
        from time import perf_counter

        if perf_counter()-self.change_direction_time>self.change_direction_time:
            self.generate_new_components()
            self.change_direction_time = perf_counter()

        x_speed,y_speed=self.get_velocity(delta_time)
        self.x+=x_speed
        self.y+=y_speed
    def coordinates(self):
        return [(self.x,self.y),(self.x,self.y+self.height),(self.x+self.width,self.y+self.height),(self.x+self.width,self.y)]
    def draw(self,pygame,window):
        # pygame.draw.circle(window,(255,255,255),(self.x,self.y),3)
        window.blit(self.image,(self.x,self.y))


    def generate_alien_bullet(self,player_coordinate_tuple,color=(255,0,0)):
        px=player_coordinate_tuple[0]
        py=player_coordinate_tuple[1]
        r,theta=ct.polar(px,py,(self.x+self.width/2,self.y+self.height/2))
        # relative accuracy
        return bullet(
            x=self.x+self.width/2,
            y=self.y+self.height/2,
            angle=theta,
            positive_or_negative=1,
            color=color
        )

    def out_of_screen(self,screen_height,screen_width):
        #checking if the coordinates are out of the screen:
        if self.x+self.width<screen_width or self.x-self.width>screen_width:
            return False

        if self.y-self.height>screen_height or self.y+self.height<screen_height:
            return False

        return True
if __name__ == "__main__":
    import pygame
    from time import perf_counter
    buls=[]
    pygame.init()
    height = 600
    width = 600
    screen_size = (height, width)
    window = pygame.display.set_mode(screen_size, pygame.RESIZABLE)

    b = ufo(x=200, y=300)


    while True:
        start=perf_counter()

        pygame.time.wait(10)
        buls.append(b.generate_alien_bullet((0,0)))

        b.update_position(perf_counter()-start)
        b.draw(pygame,window)

        for k in buls:
            k.update_position(10)
            k.draw(pygame,window)
        pygame.display.update()
        window.fill((0,0,0))
