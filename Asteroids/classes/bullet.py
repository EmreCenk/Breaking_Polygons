from Mathematical_Functions import coordinates as mt


class bullet:
    def __init__(self,x,y,angle,positive_or_negative,radius=3,color=(255,255,255),units_per_second=500):
        self.color=color #color for bullet
        self.r=radius
        #coordinates for bullet:

        self.x=x
        self.y=y
        self.angle=angle

        self.units_per_second=units_per_second #bullet speed
        self.direction=positive_or_negative #Either 1 or -1 depending on the direction of the bullet
    def get_velocity(self,delta_time):
        return delta_time*self.units_per_second

    def update_position(self,delta_time):
        #convert everything to polar coordinates, with the bullet taken as the new origin. This way we can increase
        # the 'r' value without needing to do any calculations on what x and y will be.
        self.x,self.y=mt.cartesian(self.direction*self.get_velocity(delta_time),self.angle,(self.x,self.y))

    def draw(self,pygame,window,delta_time):
        pygame.draw.circle(window,self.color,(self.x,self.y),self.r) #this is the main bullet.

        #DRAWING THE BULLET TRAIL:

        trail_bullet_num=4
        velocity=self.get_velocity(delta_time)
        new_color=self.color

        newx, newy = self.x,self.y

        for i in range(trail_bullet_num):
            new_color=(new_color[0]*0.6,new_color[1]*0.6,new_color[2]*0.6,) #creating a dimmer rgb color
            newx,newy=mt.cartesian(r=1.2*velocity,theta=self.angle-180,tuple_new_origin=(newx,newy))
            pygame.draw.circle(window, new_color, (newx,newy), self.r)  # this is the main bullet.


