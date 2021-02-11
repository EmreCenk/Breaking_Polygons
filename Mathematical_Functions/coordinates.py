
from math import cos,sin,radians,degrees,sqrt,atan2
def cartesian(r,theta,tuple_new_origin=(0,0)):
    """Converts height given polar coordinate r,theta into height coordinate on the cartesian plane (x,y). We use polar
    coordinates to make the rotation mechanics easier. This function also converts theta into radians."""
    #theta=0.0174533*theta #1 degrees = 0.0174533 radians
    theta=radians(theta)

    # we need to modify our calculation for the new origin as well
    x=r*cos(theta)+tuple_new_origin[0] #finding x
    y=r*sin(theta)+tuple_new_origin[1] #finding y

    return (x,y)

def polar(x,y,tuple_new_origin=(0,0)):
    """Is the inverse function of 'cartesian'. Converts height given cartesian coordinate; x,y into height polar coordinate in
    the form (r, theta). """

    w=(x-tuple_new_origin[0]) #width of mini triangle
    h=(y-tuple_new_origin[0]) #height of mini triangle

    r=sqrt((w**2)+(h**2)) # from the pythagorean theorem
    theta=atan2(h,w)

    return r,degrees(theta)
#I was going to use the following function, but it increases the computational complexity of the game too much
# def elipse_to_polygon(centerx, centery, height, width, accuracy=5):
#     print("input",centerx, centery, height, width)
#     """This function converts an elıpse to """
#     coordinates=[]
#     coordinates2=[]
#     y_dif= 2 * height / accuracy
#     for i in range(accuracy): #loop through y values on the elipse and calculate the corresponding x coordinate.
#
#         y=y_dif*i+centery
#         #using the equation of an elipse, we can solve for x:
#
#         soloution_part_1=sqrt(
#             (1- (((y-centery)/width)**2))*(height**2)
#         )
#         #The square root can be positive or negatve. That's why we will add both coordinates.
#         coordinates.append([y, centerx + soloution_part_1])
#         coordinates2.append([y, centerx - soloution_part_1])
#
#     final=[]
#     for i in coordinates:
#         final.append(i)
#     for i in range(1,len(coordinates2)):
#         final.append(coordinates2[-i])
#     return final

if __name__ == '__main__':
    angle=123
    r=12
    new=cartesian(r,angle)
    print(new)

    neww=polar(new[0],new[1])
    print(neww)
