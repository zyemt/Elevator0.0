import threading
from time import ctime,sleep
import random
maxfloor = 20
minfloor = 0
free = 2
up = 1
down = 0
single = 1
double = 2
All = 3
calls = [10,5,3,7,17]
todeal=[]
unreachable = 888


def inputafloor():
    a = []
    a = input('Type in the floor you go:---------------\n').split()
    if a != []:
        a = list(map(int, a))
        for element in a:
            calls.append(element)

def destination(floor):
    aim = random.randint(0,1)
    if aim == up:
        destinate = random.randint(floor-1,20)
    else:
        destinate = random.randint(0,floor-1)
    return destinate


class Elevator:
    def __init__(self,theid ,mode,maxnum,maxweight):

        self.direction = up
        self.maxfloor = maxfloor
        self.minfloor = minfloor
        self.mode = mode #单 双 全部
        if self.mode == single:
            self.current_layer = 1
        else:
            self.current_layer = 0

        self.maxnum = maxnum
        self.maxweight = maxweight
        self.num = 0
        self.id = theid
        self.floortogo = []  #要上电梯的楼层
        self.floortoleave = []  #要下电梯的楼层
        self.isfull = 0


    def add_destination(self,thegoal):
        if self.floortogo ==[] and self.floortoleave == []:
            if thegoal > self.current_layer:
                self.direction  = up
            else:
                self.direction = down
        self.floortogo.append(thegoal)


    def inandout(self,getin,out):
        fla = 1
        sleep(6)
        if out:
            self.num -= out
            for x in self.floortoleave[:]:
                if x == self.current_layer:
                    self.floortoleave.remove(x)
        if getin:
            if self.maxnum - self.num >= getin:
               self.num += getin
               try:
                   todeal.remove(self.current_layer)
               except ValueError:
                   print('!', self.current_layer)
            else:
                calls.append(self.current_layer)
                self.num = self.maxnum
                fla = 0

            for y in self.floortogo[:]:
                if y == self.current_layer:
                    self.floortogo.remove(y)
                    destinate = destination(y)
                    self.floortoleave.append(destinate)

        print("电梯号:{},要进入人数:{},出去人数:{},楼层:{},电梯内人数:{},该层是否全载:{}".format(self.id,getin,out,self.current_layer,self.num,fla))

    def searchit(self):
        out = 0
        getin = 0
        for a in self.floortogo:
            if self.current_layer == a:
                getin +=1
        for b in self.floortoleave:
            if self.current_layer == b:
                out += 1
        return [getin,out]


    def move(self):
        if self.floortogo == [] and self.floortoleave == []:
            sleep(5)
            self.direction = free
        if self.direction == up:
            for i in range(21):
                if self.mode == single:
                    if self.current_layer % 2 >0 and  (self.current_layer in self.floortogo  or  self.current_layer in self.floortoleave):
                        gl = self.searchit()
                        getin = gl[0]
                        out = gl[1]
                        self.inandout(getin,out)
                    sleep(1)
                if self.mode == double:
                    if self.current_layer % 2 ==0 and (self.current_layer in self.floortogo  or  self.current_layer in self.floortoleave):
                        gl = self.searchit()
                        getin = gl[0]
                        out = gl[1]
                        self.inandout(getin, out)
                    sleep(1)
                else:
                    if self.current_layer in self.floortogo  or self.current_layer in self.floortoleave:
                        gl = self.searchit()
                        getin = gl[0]
                        out = gl[1]
                        self.inandout(getin, out)
                    sleep(1)
                self.current_layer = i
                if self.current_layer == maxfloor:
                    sleep(2)
                    self.direction = down
        else:
            for i in range(21):
                if self.mode == single:
                    if self.current_layer % 2 > 0 and (self.current_layer in self.floortogo  or  self.current_layer in self.floortoleave):
                        gl = self.searchit()
                        getin = gl[0]
                        out = gl[1]
                        self.inandout(getin, out)
                    sleep(1)
                if self.mode == double:
                    if self.current_layer % 2 == 0 and(self.current_layer in self.floortogo  or  self.current_layer in self.floortoleave):
                        gl = self.searchit()
                        getin = gl[0]
                        out = gl[1]
                        self.inandout(getin, out)
                    sleep(1)
                else:
                    if self.current_layer in self.floortogo or self.current_layer in self.floortoleave:
                        gl = self.searchit()
                        getin = gl[0]
                        out = gl[1]
                        self.inandout(getin, out)
                    sleep(1)
                self.current_layer = maxfloor-i

                if self.current_layer == minfloor:
                    sleep(2)
                    self.direction = up

    def get_value(self, pos):
        if self.direction == up:
            if self.current_layer > pos:
                tm = 2*self.maxfloor - self.current_layer - pos
            else :
                tm = pos - self.current_layer
        else:
            if self.current_layer < pos:
                tm = self.current_layer + pos
            else:
                tm = self.current_layer - pos
        if self.direction == free:
            tm = abs(pos-self.current_layer)
        if self.mode == single and pos % 2 == 0:
            tm = unreachable
        if self.mode == double and pos % 2:
            tm = unreachable
        return tm

    def run(self):
        while 1:
            self.move()


l1 = Elevator(1, 0, 10, 800)
l2 = Elevator(2, 1, 10, 800)
l3 = Elevator(3, 2, 10, 800)
l4 = Elevator(4, 0, 20, 2000)
ls = [l1,l2,l3,l4]


def estimate():
    while 1:
        inputafloor()
        global calls
        global todeal
        #calls = list(set(calls))
        print(calls)
        for x in calls[:]:
            #print(len(calls))
            v1 = l1.get_value(x)
            v2 = l2.get_value(x)
            v3 = l3.get_value(x)
            v4 = l4.get_value(x)
            lk = min(v1,v2,v3,v4)
            for h in ls:
                if h.get_value(x) == lk:
                    h.add_destination(x)
                    calls.remove(x)
                    todeal.append(x)
                    todeal = list(set(todeal))
                   # h.floortogo = list(set(h.floortogo))
                    break
        print('details:',l1.floortogo,l2.floortogo,l3.floortogo,l4.floortogo)
        print('ds:',l1.current_layer,l2.current_layer,l3.current_layer,l4.current_layer)

        #n = random.randint(10,45)
        #sleep(n)
        sleep(45)


tx = threading.Thread(target = estimate)
tx.start()
for i in ls:
    t = threading.Thread(target = i.run)
    t.start()

#tx = threading.Thread(target = estimate)
#tx.start()






