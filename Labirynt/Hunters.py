import heapq
import random
class Hunter:
    def __init__(self,id,env,pos_x=None,pos_y=None):
        self.id=id
        self.environment=env
        self.pos_x = pos_x
        self.pos_y = pos_y

    def set_position(self,pos_x,pos_y):
        self.pos_x=pos_x
        self.pos_y=pos_y

    def get_state(self):
        return (self.pos_x,self.pos_y)


    def move(self,decision,map):
        if decision==0: #do góry
            if self.pos_y>0 and map[self.pos_y-1][self.pos_x]not in[1,3]:
                self.pos_y-=1
        elif decision==1: #w dół
            if self.pos_y<len(map)-1 and map[self.pos_y+1][self.pos_x]not in[1,3]:
                self.pos_y += 1
        elif decision==2: #w lewo
            if self.pos_x>0 and map[self.pos_y][self.pos_x-1]not in[1,3]:
                self.pos_x -= 1
        elif decision==3: #w prawo
            if self.pos_x<len(map[0])-1 and map[self.pos_y][self.pos_x+1]not in[1,3]:
                self.pos_x += 1

    def where_to_go(self,start,goal,map):#a*star
        def heuristic(a,b):
            return abs(a[0] - b[0])+abs(a[1]-b[1])

        set=[]
        heapq.heappush(set,(0,start))
        went_from={}
        g_score={start:0}
        f_score={start:heuristic(start,goal)}

        while set:
            _,current_state=heapq.heappop(set)
            if current_state==goal:
                path=[]
                while current_state in went_from:
                    path.append(current_state)
                    current_state=went_from[current_state]
                path.reverse()
                return path
            x,y=current_state
            neighbours=[
                (x-1,y),(x+1,y),(x,y-1),(x,y+1)
            ]
            for fx,fy in neighbours:
                if 0<=fx<len(map[0]) and 0<=fy<len(map) and (map[fy][fx]!=1):
                    tentative_g_score=g_score[current_state]+1
                    if (fx,fy) not in g_score or tentative_g_score<g_score[(fx,fy)]:
                        went_from[(fx,fy)]=current_state
                        g_score[(fx,fy)]=tentative_g_score
                        f_score[(fx,fy)]=tentative_g_score+heuristic((fx,fy),goal)
                        heapq.heappush(set,(f_score[(fx,fy)],(fx,fy)))

        return []

    def make_decision(self,escp_pos):
        my_position=self.get_state()

        path=self.where_to_go(my_position,escp_pos,self.environment.map)
        if path:
            next_pos=path[0]
            hx,hy=my_position
            nx,ny=next_pos
            if nx<hx:
                return 2
            elif nx>hx:
                return 3
            elif ny<hy:
                return 0
            elif ny>hy:
                return 1