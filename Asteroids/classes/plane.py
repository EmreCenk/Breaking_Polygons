from Mathematical_Functions import coordinates as mt
from random import randint
from time import perf_counter
class airplane:
    def __init__(self,x,y,units_per_second,angle_units_per_second=150,angle=90,color=(255,255,255),height=30,
                 width=50,):
        #Initializing the class:
        self.x=x
        self.y=y
        self.height=height
        self.width=width
        self.units_per_second=units_per_second
        self.color=color
        self.lives=3 #how many lives player has
        self.angle=angle #initial angle of player
        self.angle_units_per_second=angle_units_per_second #How many degrees change when rotating the player

        self.momentum=units_per_second*0.1#initial momentum value (to give the drifting effect)
        self.momentum_angle=self.angle#we save the momentum angle so that the momentum will not change direction when
        # the player starts to look left or right

        self.hyper_space_cooldown = 0.4  # 2 seconds
        self.last_hyper_space = 0

        self.given_extra=1 #how many extra lives that have been given to the player
    def get_velocity(self,delta_time):
        #We multiply the units per second with the time passed so that the speed of the plane does not depend on the
# frame rate
        return self.units_per_second*delta_time

    def get_angle_change(self,delta_time):
        return self.angle_units_per_second*delta_time

    def fix_out_of_screen(self,screen_width,screen_height):
        #generating corner coordinates:
        c,cc,ccc=self.generate_corner_coordinates()
        if c[0]<0 and cc[0]<0 and ccc[0]<0: #only if all 3 corners are out of the screen, it is considered shifted
            #The triangle has shifted to the left side of the screen. we will teleport everything to the other side.
            self.x+=screen_width

        elif c[0]>screen_width and cc[0]>screen_width and ccc[0]>screen_width:
            # The triangle has shifted. we will teleport everything to the other side.
            self.x-=screen_width

        elif c[1]<0 and cc[1]<0 and ccc[1]<0:
            # The triangle has shifted. we will teleport everything to the other side.

            self.y+=screen_height

        elif c[1]>screen_height and cc[1]>screen_height and ccc[1]>screen_height:
            # The triangle has shifted. we will teleport everything to the other side.

            self.y-=screen_height

    def hyper_space(self,width,height):
        #teleporting to a random place on the screen
        self.x=randint(0,width)
        self.y=randint(0,height)
    def update_position(self,controls_array,pressed_keys,delta_time,screen_width,screen_height):

        """Updates the position of the plane. The controls array is an array specifying the controls"""
        velocity=self.get_velocity(delta_time=delta_time)#get the velocity in this frame
        angle_dif=self.get_angle_change(delta_time)

        #Making sure the momentum of the ship cannot get infinitely big:
        if self.momentum>velocity*1.2:
            self.momentum=velocity*1.2

        elif self.momentum>0.45: #we make sure that the momentum cannot go under 0.45 . If momentum falls under 0,
            # then the ship will start going backwards
            self.momentum-=0.001



        self.x, self.y = mt.cartesian(self.momentum*1.2, self.momentum_angle, (self.x, self.y))

        if pressed_keys[controls_array[0]]:
            self.angle-= angle_dif
            self.angle=self.angle%360 #we conver it to mod 360 so that the self.angle variable doesn't become
            # insanely big

        if pressed_keys[controls_array[1]]:
            self.angle += angle_dif
            self.angle=self.angle%360 #we conver it to mod 360 so that the self.angle variable doesn't become
            # insanely big

        if pressed_keys[controls_array[2]]and perf_counter()-self.last_hyper_space>=self.hyper_space_cooldown:
            #we go to hyperspace
            self.hyper_space(width=screen_width,height=screen_height)
            self.last_hyper_space=perf_counter() #reseting the hyperspace cooldown
        if pressed_keys[controls_array[3]] :
            self.x,self.y=mt.cartesian(velocity,self.angle,(self.x,self.y))
            self.momentum+=0.004
            self.momentum_angle=self.angle


    def generate_corner_coordinates(self):
        interval = 120  # The angles between each corner

        # Calculating the angles (since polar coordinates are used), for each corner:
        a = self.angle
        aa = self.angle - interval
        aaa = self.angle - 2 * interval

        # converting 3 polar coordinates to  cartesian:
        c=mt.cartesian(r=self.width/2,theta=a,tuple_new_origin=(self.x,self.y))
        cc=mt.cartesian(r=self.height/2,theta=aa,tuple_new_origin=(self.x,self.y))
        ccc=mt.cartesian(r=self.height/2,theta=aaa,tuple_new_origin=(self.x,self.y))

        return c,cc,ccc
    def draw(self,pygame,window):
        #We take pygame and window as an input to make sure that the pygame the plane draws on is the main
        # initialized pygame

        #generating corner coordinates:
        c,cc,ccc=self.generate_corner_coordinates()

        pygame.draw.polygon(window,self.color,[c,cc,ccc]) #Actually drawing the triangle

# if __name__ == "__main__":
#     import pygame
#     pygame.init()
#
#     a=airplane(width)