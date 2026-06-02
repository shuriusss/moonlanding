import math
import random
import time
import turtle

turtle.setworldcoordinates(0, 0, 1000, 700)
turtle.speed(0)
#turtle.ht()

class Moon:

    def __init__(self, surf_dev=50, surf_det=50):
        self.surf_dev = surf_dev #surface deviation - half of an amplitude of moon landscape
        self.surf_det = surf_det # surface detail - length limit of generated line segments

    def generate(self):

        turtle.clear()
        
        base1 = random.uniform(0, 900)
        base2 = random.uniform(base1+50, 950) #x cords of platforms, second one
        #is always generated after first one
        #print(base1, base2)

        

        turtle.teleport(0, self.surf_dev)

        xpos = 0
        ypos = self.surf_dev

        surf_data = [(xpos, ypos)]

        while self.surf_det < (1000 - xpos):
            
            xpos = random.uniform(xpos, xpos+self.surf_det)
            
            if xpos > base1 or xpos > base2:
                
                turtle.color("blue")
                turtle.width(3)
                #print("plant", f'{xpos=}')
                
                turtle.setpos(turtle.xcor()+50, ypos)
                surf_data += [(turtle.xcor(), ypos)]
                
                turtle.color("black")
                turtle.width(1)
                
                if xpos > base1:
                    global land1
                    land1 = (surf_data[-1][0]-50, surf_data[-1][1])
                    base1 = 1001
                else:
                    global land2
                    land2 = (surf_data[-1][0]-50, surf_data[-1][1])
                    base2 = 1001
                    
                if turtle.xcor() > xpos:
                    xpos = turtle.xcor()
                    continue
                
            ypos = random.uniform(0, self.surf_dev*2)
            turtle.setpos(xpos, ypos)
            surf_data += [(xpos, ypos)]
            #print(f'{xpos=}, {ypos=}')
            
        ypos = random.uniform(0, self.surf_dev*2)
        turtle.setpos(1000, ypos)
        surf_data += [(1000, ypos)]

        return surf_data

class Rocket:
    def __init__(self, data, data_keys, x=500, y=687.5, size=25, angle=0, act=True):
        self.size = size
        self.data = data
        self.data_keys = data_keys
        self.angle = angle
        self.x = x
        self.y = y
        self.act = act
        
    def spawn(self, orient=0, visible=True):
        if visible:
            turtle.color("black")
        else:
            turtle.color("white")
        turtle.setheading(orient-90) 
        turtle.teleport(self.x, self.y)
        turtle.penup()
        turtle.right(45)
        turtle.forward(self.size*2**(1/2)/2)
        turtle.left(135)
        turtle.pendown()
        for i in range(4):
            turtle.forward(self.size)
            turtle.left(90)
        turtle.setheading(orient-90) 
        turtle.teleport(self.x, self.y)
        print(f'{self.x=} {self.y=} {self.angle=}')


    def rotate(self, direction, rot_v=20):
        # direction: 1 (Right), -1 (Left)
        self.spawn(self.angle, False)
        self.angle += direction*rot_v
        self.angle %= 360
        turtle.setheading(self.angle)
        self.spawn(self.angle)

    def move(self, v=100):
        self.spawn(self.angle, False)
        turtle.forward(v)
        self.x, self.y = turtle.pos()
        self.check()
        self.spawn(self.angle)

    def check(self):
        new_an = self.angle*math.pi/180+math.pi/4
        vector = (math.cos(new_an)*self.size*2**(1/2)/2, math.sin(new_an)*self.size*2**(1/2)/2)
        corners = []
        for i in range(4):
            corners += [(self.x + vector[0], self.y + vector[1])]
            vector = (-vector[1], vector[0])
        print(f'{self.x=} {self.y=} {self.angle=} {corners=}')
        for i in corners:
            here = binarySearch(self.data_keys, i[0])
            x1 = self.data_keys[here]
            x2 = self.data_keys[here+1]
            y1 = self.data[here][1]
            y2 = self.data[here+1][1]
            contact_height = (y2-y1)*(i[0]-x1)/(x2-x1) + y1
            print(f'{contact_height=}')
            if i[1] < contact_height:
                self.move(-5)
                self.check()
                break
        self.win_check()
            
    def win_check(self):
        if self.angle == 0 or self.angle == 180:
            if self.x >= land1[0]+self.size/2 and self.x <= land1[0]+self.size/2*3:
                if self.y >= land1[1] and self.y <= land1[1]+20:
                    self.act = False
            elif self.x >= land2[0]+self.size/2 and self.x <= land2[0]+self.size/2*3:
                if self.y >= land2[1] and self.y <= land2[1]+20:
                    self.act = False
        if not self.act:
            turtle.color("blue")
            turtle.teleport(100, 350)
            turtle.write("YOU WIN!", False, 'left', ('Arial', 50, 'normal'))
        
def binarySearch(log, x): #for indentifying line segment above which  directly is rocket
  left = 0
  right = len(log) - 1

  while left <= right:
    mid = (left + right) // 2

    if log[mid] <= x and x <= log[mid+1]:
      return mid

    elif log[mid] < x:
      left = mid + 1
      
    else:
      right = mid - 1

  return -1

def main():
    global LANDED, CRASHED
    
    # Setup
    screen = turtle.Screen()
    
    # Generate World
    g1 = Moon()
    g1log = g1.generate()
    g1logmiles = [i[0] for i in g1log]
    apollo = Rocket(g1log, g1logmiles)
    apollo.spawn()
    
    
    # Controls
    screen.listen()
    screen.onkey(lambda: apollo.rotate(-1) if apollo.act else None, "Right")
    screen.onkey(lambda: apollo.rotate(1) if apollo.act else None, "Left")
    screen.onkey(lambda: apollo.move() if apollo.act else None, "Up")
    screen.onkey(screen.bye, "Escape")
    screen.onkey(lambda: main(), "r") # Restart


main()
