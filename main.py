import math
import random
import time
import turtle


#canvas prep
turtle.setworldcoordinates(0, 0, 1000, 700)
turtle.speed(0)
turtle.ht()


class Rocket:

    def __init__(self, data, data_keys, size=25, mass=1, bounce=0.5):
        self.size = size
        self.data = data
        self.data_keys = data_keys
        self.mass = mass
        self.bounce = bounce

    def spawn(self, x=500, y=None, orient=0):
        turtle.setheading(orient)
        if y == None:
            y = 700-self.size
        turtle.teleport(x, y)
        print(f'{x=}, {y=}, {orient=}')
        for i in range(4):
            turtle.forward(self.size)
            turtle.left(90)

        return (x, y)

    def check_down(self, x, y, hx, hy, angl):
        third = False
        if angl == math.pi/2:
            x = x - self.size
            hy = hy - self.size
        elif angl == math.pi*3/2:
            hx = x + self.size
            y = y - self.size
        elif angl == math.pi:
            x, hx = hx, x
            y, hy = hy-self.size, y-self.size
        elif angl < math.pi/2:
            third = True
            xmid, ymid = x, y
            x = x+math.cos(angl+math.pi/2)*self.size
            y = y+math.sin(angl+math.pi/2)*self.size
        elif angl > math.pi/2 and angl < math.pi:
            third = True
            xmid, ymid = hx, hy
            hx, hy = x, y
            x = x+math.cos(angl+math.pi/4)*self.size*2**(1/2)
            y = y+math.sin(angl+math.pi/4)*self.size*2**(1/2)
        elif angl > math.pi and angl < math.pi*3/2:
            third = True
            xmid = x+math.cos(angl+math.pi/4)*self.size*2**(1/2)
            ymid = y+math.sin(angl+math.pi/4)*self.size*2**(1/2)
            x, y = hx, hy
            hx = hx+math.cos(angl+math.pi*3/4)*self.size*2**(1/2)
            hy = hy+math.sin(angl+math.pi*3/4)*self.size*2**(1/2)
        elif angl > math.pi*3/2:
            third = True
            xmid, ymid = hx, hy
            hx = x+math.cos(angl+math.pi/4)*self.size*2**(1/2)
            hy = y+math.sin(angl+math.pi/4)*self.size*2**(1/2)

        print(x, y, '\n', xmid if third else None, ymid if third else None, '\n', hx, hy)
            
            
        line = binarySearch(self.data_keys, x) #vertice to the left of left corner
        start = line

        yet = True
        for i in range(line, len(self.data_keys)): #vertice to the right of right corner
            if yet and self.data_keys[i] >= hx and self.data_keys[i-1] <= hx:
                middle = i
                yet = False
            if self.data_keys[i] >= hx:
                finish = i
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
        if third:
            x1 = self.data[start][0]
            y1 = self.data[start][1]
            x2 = self.data[start+1][0]
            y2 = self.data[start+1][1]
            impact_points += [(x, ((y2-y1)*(x-x1)/(x2-x1) + y1) if x != x1 else y1)]

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


        #NOTE: tan function involved - consider cases for angl = 90+180n, n ~ Z
        #NOTE: probably last and this section can be merged but i dont feel like
        #doing that, as well as concerned if getting data wouldnt be harder
        comparison = [y-impact_points[0][1]]
        for i in range(start+1, finish):
            comparison += [y+(impact_points[i-start][0]-x)*math.tan(angl)-impact_points[i-start][1]]
        if third:
            comparison += [ymid-impact_points[-2][1]]
        comparison += [hy-impact_points[-1][1]]
        if comparison[0] == comparison[-1]:
            stabilize = True
        else:
            stabilize = False
        impact_distance = min(comparison)
        where = comparison.index(impact_distance)
        col_pos = impact_points[where]
        print(f'\n CHECK {impact_points=} \n {impact_distance=} \n {comparison=} \n')

        return col_pos, impact_distance, stabilize

    def hit_slope(self, xpos, ypos, vel, v_rot, xcol, angl):
        slide = binarySearch(self.data_keys, xcol)
        print(f'PRE {xpos=}, {ypos=}, {vel=}, {xcol=},  {angl=} \n')
        inertia = self.mass*self.size**2/6
        slope = ((self.data[slide][1]-self.data[slide+1][1])/(self.data[slide][0]-self.data[slide+1][0]), -1) #as vector -> radius vector (hence - one) -> as normal vector (perpendicular (a, b) -> (-b, a))
        if slope[0] > 1 or slope[0] < -1:
            slope = (1, -1/slope[0])
        if slope[1] < 0:
            slope = (-slope[0], -slope[1])
        mass_c = ((xcol-xpos)*math.cos(angl)-math.cos(angl+math.pi/4)*self.size*2**(1/2)/2, (xcol-xpos)*math.sin(angl)-math.sin(angl+math.pi/4)*self.size*2**(1/2)/2)
        v_rel = (vel[0]+v_rot*mass_c[0])*slope[0]+(vel[1]+v_rot*mass_c[1])*slope[1]
        impulse = (-(1 + self.bounce)*v_rel) / (1/self.mass + (mass_c[0]*slope[0]+mass_c[1]*slope[1])**2 / inertia)
        new_v = (vel[0] + (impulse*slope[0])/self.mass, vel[1] + (impulse*slope[1])/self.mass)
        v_rot_new = v_rot + impulse*(mass_c[0]*slope[0]+mass_c[1]*slope[1])/inertia
        print(f'POST {inertia=}, {slope=}, {mass_c=}, {v_rel=}, {impulse=}, {new_v=} \n')
        return new_v, v_rot_new

    def hit_vertice(self):
        pass

    def stabilize(self):
        pass

    def sliding(self):
        pass

    def v_fall(self, x, y):
        t1 = time.monotonic() #initial setup
        ypos = y
        xpos = x

        angl_d = turtle.heading() #turtle info and base positioning
        angl_r = angl_d/180*math.pi
         
        vel = (0, 0)
        v_rot = 0

        counter = 0

        while True: #add collision - based on surface log, full stop on
            #corresponding line segment DONE (for hitpoint)
            #do it now for the whole base DONE

            hx = xpos + self.size*math.cos(angl_r)
            hy = ypos + self.size*math.sin(angl_r)
            
            

            turtle.color("white")
            self.spawn(xpos, ypos)
            t2 = time.monotonic()
            dt = t2 - t1
            ypos = y+vel[1]*dt-(100*dt**2/2) #in rockets spawn point
            xpos = x+vel[0]*dt-5*dt**2/2*(abs(vel[0])/vel[0]) if vel[0] else x

            col_pos, imp_dis, st = self.check_down(xpos, ypos, hx, hy, angl_r)
            xcol, ycol = col_pos
            angl_r = (angl_r + v_rot*dt) % (math.pi*2)
            angl_d = angl_r*180/math.pi
            if imp_dis <= 0:
                ypos -= imp_dis
                turtle.color("red")
                self.spawn(xpos, ypos, angl_d)
                print(ycol, "hit! \n")
                print(f'{vel=} {v_rot=} {angl_r=} {angl_d=}')
                time.sleep(20)
                vel = (vel[0], vel[1]-(100*dt/2))

                counter += 1
                vel, v_rot = self.hit_slope(xpos, ypos, vel, v_rot, xcol, angl_r)
                time.sleep(20)
                x, y = xpos, ypos
                t1 = time.monotonic()
                if vel[0] == 0 or counter > 25 or st:
                    if vel[0] == 0:
                        print("FALLEN FLAT")
                    if st:
                        print("STUCK")
                    if counter > 25:
                        print("TOO MUCH")
                    break
                continue
            if xpos < 0 or xpos > 1000:
                break
            turtle.color("black")
            print(f'{xpos=}, {ypos=}, {vel=}')
            self.spawn(xpos, ypos, angl_d)
            print(ypos)         
#2+"3"

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
                    base1 = 1001
                else:
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

#test(5)

#tasks
#break code in more functions, as well as moving some to other files
#code rotation on impact 




