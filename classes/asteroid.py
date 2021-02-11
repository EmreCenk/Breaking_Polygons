from Mathematical_Functions import coordinates as mt
from random import randint,uniform

class asteroid:
    def __init__(self,radius,x=None,y=None,color=(255,255,255),background_color=(0,0,0),
                 velocity_interval=(30,40),angle_change_per_second_interval=(20,50),border=0.1,
                 player_coordinate_tuple=(),side_num=8):
        self.radius=radius

        #Generating random points if no specific location is given:0

        if x==None and y==None:
            #if not specified, then randomly generate:
            self.x,self.y=mt.cartesian(randint(self.radius*6,self.radius*20),uniform(0,360))
        else:
            #if specified, then generate at the specified coordinate
            self.x=x
            self.y=y

        self.color=color
        self.background_color=background_color
        self.drift_angle=uniform(0,360) #the angle must be a decimal. When we generate mass amounts of
        # asteroids with integer angles, then it gives an articifial impression
        self.velocity=uniform(velocity_interval[0],velocity_interval[1])

        self.angle_change_per_second=uniform(
            angle_change_per_second_interval[0],
            angle_change_per_second_interval[1]
        )
        self.side_num=side_num
        self.border=border
        #Initializing side_num amount of corners:
        self.inner_angle=0
        self.coordinates=self.generate_coordinates(self.radius,self.side_num)

    def get_relative_change(self,delta_time):
        return self.velocity*delta_time, self.angle_change_per_second*delta_time

    def generate_coordinates(self,given_radius,side_number):
        coordinates=[]
        internal_angles=360/side_number

        for i in range(side_number): #Generating a corner for each internal angle
            coordinates.append(
                mt.cartesian(given_radius,internal_angles*i+self.inner_angle,(self.x,self.y))
            )

        return coordinates

    def draw(self,pygame,window,):
        #We loop through all the edges, and draw them as lines:
        for i in range(len(self.coordinates)):
            i=i%len(self.coordinates)-1

            #line starting position:
            x1=self.coordinates[i][0]
            y1=self.coordinates[i][1]

            #line ending position:
            x2=self.coordinates[i+1][0]
            y2=self.coordinates[i+1][1]

            pygame.draw.line(window,self.color,(x1,y1),(x2,y2))

        # pygame.draw.polygon(window,self.color,self.coordinates)
        # pygame.draw.polygon(window,self.background_color,self.inner_coordinates)

    def fix_out_of_screen(self,screen_width,screen_height):
        """This funtion makes sure asteroids don't go out of bounds."""
        out_left=True
        for point in self.coordinates:
            if point[0]>0: #Is it not passed the left side of the screen?
                out_left=False
                break


        if out_left:
            self.x+=screen_width

        else:
            out_right=True
            for point in self.coordinates:
                if point[0]<screen_width: #his it in the screen?
                    out_right=False
                    break

            if out_right:
                self.x-=screen_width+self.radius

        out_up=True
        for point in self.coordinates:
            if point[1]>0:#is it under the top limit?
                out_up=False
                break
        if out_up:
            self.y+=screen_height+self.radius

        else:
            out_down=True
            for point in self.coordinates:
                if point[1]<screen_height:
                    out_down=False
                    break
            if out_down:
                self.y-=screen_height+self.radius
    def update_position(self,delta_time):
        """Updating the poisition of the asteroid"""
        vel,angle_change=self.get_relative_change(delta_time)

        self.inner_angle+=angle_change
        self.inner_angle=self.inner_angle%360

        self.x,self.y=mt.cartesian(vel,self.drift_angle,(self.x,self.y))
        self.coordinates=self.generate_coordinates(self.radius,self.side_num)
        self.inner_coordinates=self.generate_coordinates(self.radius*(1-self.border),self.side_num)


if __name__ == '__main__':
    import pygame
    from time import perf_counter
    pygame.init()
    height = 600
    width = 600
    screen_size = (height, width)
    window = pygame.display.set_mode(screen_size, pygame.RESIZABLE)

    b = asteroid(radius=30, x=200, y=300, side_num=7)
    a = asteroid(radius=20, x=300, y=300,side_num=6)
    c = asteroid(radius=10, x=100, y=300,side_num=5,border=0.15)


    while True:
        start=perf_counter()

        pygame.time.wait(10)
        a.update_position(perf_counter()-start)

        a.draw(pygame, window)

        b.update_position(perf_counter()-start)
        b.draw(pygame,window)

        c.update_position(perf_counter()-start)
        c.draw(pygame,window)
        pygame.display.update()
        window.fill((0,0,0))