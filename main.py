import turtle
import random
import time
import math

#turtle.screensize(2000, 700)
turtle.setworldcoordinates(0, 0, 1000, 700)
turtle.speed(0)
turtle.ht()
#turtle.listen()

class Rocket:

    def __init__(self, data, data_keys, size=25, ):
        self.size = size
        self.data = data
        self.data_keys = data_keys

    def spawn(self, x=500, y=None):
        if y == None:
            y = 700-self.size
        turtle.teleport(x, y)
        for i in range(4):
            turtle.forward(self.size)
            turtle.left(90)

        return (x, y)

    def v_fall(self, x, y):
        t1 = time.monotonic() #initial setup
        yf = y

        angl = turtle.heading() #turtle info and base positioning
        hx = x + self.size*math.cos(angl)
        hy = y + self.size*math.sin(angl)

        print(f'{hx=}, {hy=}')
        
        line = binarySearch(self.data_keys, x) #vertice to the left of left corner
        start = line
##        x1 = self.data[line][0]
##        y1 = self.data[line][1]

        for i in range(line, len(self.data_keys)): #vertice to the right of right corner
            if self.data_keys[i] >= hx:
                finish = i
##                x2 = self.data[i][0]
##                y2 = self.data[i][1]
                break

# square can hit only (vertice on vertice or edge) or (edge on vertice) 
            
        x1 = self.data[start][0]
        y1 = self.data[start][1]
        x2 = self.data[start+1][0]
        y2 = self.data[start+1][1]
        impact_points = [(x, ((y2-y1)*(x-x1)/(x2-x1) + y1) if x != x1 else y1)]
        #left vertice
        for i in range(start+1, finish):
            impact_points += [self.data[i]]
        #side on vertice
        x1 = self.data[finish-1][0]
        y1 = self.data[finish-1][1]
        x2 = self.data[finish][0]
        y2 = self.data[finish][1]
        impact_points += [(hx, ((y2-y1)*(hx-x1)/(x2-x1) + y1) if hx != x1 else y1)]
        #right vertice

        #we foresee which exact impact will happen by choosing the least of
        #distances between verices and corresponding impact point
        #in order to next section of code work
        
        comparison = [y-impact_points[0][1]]
        for i in range(start+1, finish):
            comparison += [y+(impact_points[i-start][0]-x)*math.tan(angl)-impact_points[i-start][1]]
        comparison += [hy-impact_points[-1][1]]
        impact_distance = min(comparison)
        where = impact_points[comparison.index(impact_distance)]
        correction = (where[0]-x)*math.tan(angl)
        print(f'{impact_points=} \n {impact_distance=} \n {comparison=} \n {where=} \n {correction=}')
        
        #impact = ((y2-y1)*(x-x1)/(x2-x1) + y1) if x != x1 else y1
        while True: #add collision - based on surface log, full stop on
            #corresponding line segment DONE (for hitpoint)
            #do it now for the whole base
            turtle.color("white")
            self.spawn(x, yf)
            t2 = time.monotonic()
            yf = y-(100*(t2-t1)**2/2)
            if yf+correction < where[1]:
                turtle.color("black")
                self.spawn(x, where[1])
                print(where[1])
                break
            turtle.color("black")
            self.spawn(x, yf)
            print(yf)         

class Moon:

    def __init__(self, surf_dev=50, surf_det=50):
        self.surf_dev = surf_dev
        self.surf_det = surf_det

    def generate(self):

        turtle.clear()
        
        base1 = random.uniform(0, 900)
        base2 = random.uniform(base1+50, 950) #x cords of platforms, second one
        #is always generated after first one
        #print(base1, base2)

        surf_dev = 50 #surface deviation - half of an amplitude of moon landscape
        surf_det = 50 # surface detail - length limit of generated line segments

        turtle.teleport(0, surf_dev)

        xpos = 0
        ypos = surf_dev

        surf_data = [(xpos, ypos)]

        while surf_det < (1000 - xpos):
            
            xpos = random.uniform(xpos, xpos+surf_det)
            
            if xpos > base1 or xpos > base2:
                
                turtle.color("blue")
                turtle.width(3)
                #print("plant", f'{xpos=}')
                
                turtle.setpos(turtle.xcor()+50, ypos)
                surf_data += [(turtle.xcor(), ypos)]
                
                turtle.color("black")
                turtle.width(1)
                
                if xpos > base1:
                    base1 = 1001
                else:
                    base2 = 1001
                    
                if turtle.xcor() > xpos:
                    xpos = turtle.xcor()
                    continue
                
            ypos = random.uniform(0, surf_dev*2)
            turtle.setpos(xpos, ypos)
            surf_data += [(xpos, ypos)]
            #print(f'{xpos=}, {ypos=}')
            
        ypos = random.uniform(0, surf_dev*2)
        turtle.setpos(1000, ypos)
        surf_data += [(1000, ypos)]

        return surf_data

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

g1 = Moon()
g1log = g1.generate()
g1logmiles = [i[0] for i in g1log]
apollo = Rocket(g1log, g1logmiles)
x, y = apollo.spawn()
apollo.v_fall(x, y)

def test(n):
    for i in range(n):
        print('\n \n \n')
        x, y = apollo.spawn(random.uniform(0, 950), 700)
        turtle.dot(20, 1/(n-1)*i, 1/(n-1)*i, 0)
        apollo.v_fall(x, y)


#construction site
#dont look




