import  pygame
import math
from queue import PriorityQueue

WIDTH=800
window=pygame.display.set_mode((WIDTH,WIDTH))
pygame.display.set_caption("A* visualizer")
pygame.init()

RED = (255, 0, 0) #closed i.e visited
GREEN = (0, 255, 0)  # in the open list 
BLUE = (0, 255, 0) # 
YELLOW = (255, 255, 0) 
WHITE = (255, 255, 255) # unexplored block
BLACK = (0, 0, 0)  # barrier 
PURPLE = (128, 0, 128) # path color
ORANGE = (255, 165, 0)  # Start position
GREY = (128, 128, 128)
BROWN = (162, 110, 44)  # is end

class Block:
    
    def __init__(self,row,col,width,total_rows):
        self.row=row
        self.width=width
        self.col=col
        self.x=row*width
        self.y=col*width
        self.neighbours=[] # empty list of neighbours (4 neighbours each at distance 1)
        self.color=WHITE 
        self.total_rows=total_rows

    def get_position(self):
        return self.row,self.col

    def draw(self,window):
        #draw on the grid
        pygame.draw.rect(window,self.color,(self.x,self.y,self.width,self.width))

    def __lt__(self, other):
	    return False

    def make_visited(self):
        self.color=RED

    def make_open(self):
        self.color = GREEN

    def make_src(self):
        self.color = ORANGE

    def make_dest(self):
        self.color = BROWN

    def make_barrier(self):
        self.color = BLACK

    def reset(self):
        self.color = WHITE

    def make_path(self):
        self.color = PURPLE

    def is_closed(self):
        return self.color==RED

    def is_open(self):
        return self.color == GREEN

    def is_barrier(self):
        return self.color==BLACK

    def is_start(self):
        return self.color == ORANGE

    def is_end(self):
        return self.color == BROWN

    def get_neighbours(self,grid):
        self.neighbours=[]
        #4 neighbours (left right up down)

        #up
        if(self.row-1>=0 and not grid[self.row-1][self.col].is_barrier()):
            self.neighbours.append(grid[self.row-1][self.col])
    
        #down
        if(self.row+1 < self.total_rows and not grid[self.row+1][self.col].is_barrier()):
            self.neighbours.append(grid[self.row+1][self.col])

        #left
        if(self.col-1 >= 0 and not grid[self.row][self.col-1].is_barrier()):
            self.neighbours.append(grid[self.row][self.col-1])
        
        #up
        if(self.col+1 < self.total_rows and not grid[self.row][self.col+1].is_barrier()):
            self.neighbours.append(grid[self.row][self.col+1])


def calc_heuristic(p1,p2):
    (x1,y1)=p1
    (x2,y2)=p2
    return abs(x1-x2)+abs(y1-y2)

def make_grid(rows,width):
    gap=width // rows
    grid=[]
    for i in range(rows):
        grid.append([])
        # new_list=[]
        for j in range(rows):
            block = Block(i,j,gap,rows)
            # new_list.append(block)
            grid[i].append(block)
        # grid.append(new_list)
    return grid

def draw_grid(window,rows,width):
    gap =width//rows
    for i in range(rows):
        pygame.draw.line(window,GREY,(0,i*gap),(width,i*gap))
        pygame.draw.line(window, GREY, (i*gap, 0), (i*gap,width))

def reset_grid(grid):
    for row in grid:
        for block in row:
            block.reset()


def draw(window,grid,rows,width):
    #run this at the begining of every frame 
    window.fill(WHITE)

    for row in grid:
        for block in row:
            block.draw(window)
    
    for i in range(rows):
        grid[0][i].make_barrier()
        grid[rows-1][i].make_barrier()
        grid[i][0].make_barrier()
        grid[i][rows-1].make_barrier()
        
    draw_grid(window,rows,width)
    pygame.display.update()

def get_clicked_pos(pos, rows, width):
	gap = width // rows
	y, x = pos
	row = y // gap
	col = x // gap
	return row, col

def draw_path(came_from, current,draw):
   while current in came_from:
       current.make_path()
       current=came_from[current]
       draw()

def astar(draw,grid,start,end,width):
    print("ammmit")
    # draw()
    count=0
    open_set=PriorityQueue()
    open_set.put((0,count,start)) 
    #count is for tie breaker

    parent ={}
    # for row in grid :
    #     for block in row:
    #         g_score[block]=float("inf")

    g_score={block: float("inf") for row in grid for block in row}
    g_score[start]=0

    f_score = {block: float("inf") for row in grid for block in row}
    f_score[start] = calc_heuristic(start.get_position(),end.get_position())

    open_set_hash ={start} # visited or not

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current=open_set.get()[2]
        open_set_hash.remove(current)

        if current==end:
            draw_path(parent,current,draw)
            end.make_dest()
            return True

        neigh=current.neighbours
        for neighbor in neigh:
            temp_g_score=g_score[current]+1
            if temp_g_score<g_score[neighbor]:
                parent[neighbor]=current
                g_score[neighbor]=temp_g_score
                temp_h_score = calc_heuristic(neighbor.get_position(), end.get_position())
                
                f_score[neighbor] = temp_g_score+temp_h_score

                if neighbor not in open_set_hash:
                    count+=1
                    open_set.put((f_score[neighbor],count,neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()
        
        draw()

        if current!=start:
            current.make_visited()

    # print("F")
    window.fill(WHITE)
    font = pygame.font.Font('freesansbold.ttf', 32)
    text = font.render('NOT POSSIBLE', True, RED,BLACK)
    textRect = text.get_rect()
    textRect.center = (width // 2, width // 2)
    window.blit(text, textRect)
    
    pygame.display.update()
    pygame.time.wait(2000)
    # draw()
    return False



def main(window,width):
    ROWS=50 
    grid=make_grid(ROWS,WIDTH)
    
    start=None
    end=None
    run=True
    started=False

    while run:
        draw(window, grid, ROWS, WIDTH)
        for event in pygame.event.get():
            if event.type ==pygame.QUIT:
                run =False

            if started:
                #if the algorithm is running then the user should not be allowed to 
                continue

            if pygame.mouse.get_pressed()[0]:
                #left mouse button
                pos =pygame.mouse.get_pos()
                row , col =get_clicked_pos(pos , ROWS , WIDTH)
                # print(row,col)
                block=grid[row][col]
                if not start and block !=end and not block.is_barrier():
                    start=block
                    start.make_src()
                
                if block==start:
                    continue 

                elif not end and block != start and not block.is_barrier():
                    end=block
                    end.make_dest()

                elif block !=end and block !=start:
                    block.make_barrier()
                

            elif pygame.mouse.get_pressed()[2]:
                #right mouse button
                print("right clicked")
                pos = pygame.mouse.get_pos()
                row , col =get_clicked_pos(pos , ROWS , WIDTH)
                # print(row,col)
                block=grid[row][col]
                block.reset()
                if block==start:
                    start=None
                elif block==end:
                    end=None
            # pygame.display.update()
            if event.type==pygame.KEYDOWN:
                print("amit")
                if event.key ==pygame.K_SPACE and not started:
                    for rows in grid:
                        for block in rows:
                            block.get_neighbours(grid)

                    if astar(lambda : draw( window, grid, ROWS, WIDTH),grid,start,end,WIDTH)==False:
                        reset_grid(grid)
                        start=None
                        end=None

                        # pygame.time.wait(5000)
                        

                        #used to pass a fxn inside another fxn 

                    #x=lambda:print("amit")
                    # x() will call 


    pygame.quit()

main(window,WIDTH)



    

    




