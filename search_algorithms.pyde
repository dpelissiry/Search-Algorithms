

scale = 20
width = 1000
height = 1000


class Button():
    def __init__(self, text,x,y):
        self.x = x
        self.y = y
        self.text = text
    
    def draw_button(self):
        rectMode(CENTER)
        fill(255,255,255)
        rect(self.x,self.y,150,50)
        fill(0,102,0)
        textSize(20)
        textAlign(CENTER)
        text(self.text, self.x,self.y+5)
        rectMode(CORNER)
    def return_x(self):
        return(self.x)
    def return_y(self):
        return(self.y)
    def mouseInButton(self,mousex,mousey):
        x_values = []
        y_values = []
        for i in range(self.x-50,self.x+50):
            x_values.append(i)
        if mousex in x_values:
            for n in range(int(self.y-25),int(self.y+25)):
                y_values.append(n)
            if mousey in y_values:
                return True
            else:
                return False
        else:
            return False
        
        
def generate_grid():
    stroke(0)
    for col in range(width/scale+1):
        line(col*scale, 0, col*scale, height)
    for row in range(height/scale+1):
        line(0, scale*row, width, scale*row)

        
def convertToArray(x, y, delete = False, origin_choice = False, finish_choice = False):
    global board
    global barriers
    global origin
    global finish
    x -= (x % scale)
    y -= (y % scale)
    x = x / scale
    y = y / scale
    array_num = y*(width/scale)+x
    if not delete:
        if board[array_num] == '0':
            board[array_num] = '1'
            barriers.append(array_num)
    elif delete and generating_barriers:
        if board[array_num] == '1':
            board[array_num] = '0'
            barriers.remove(array_num)
    if origin_choice:
        
        board[array_num] = '2'
        origin = array_num
    if finish_choice:
        board[array_num] = '3'
        finish = array_num

def draw_barriers():
    col = 0
    row = 0
    stroke(0,0,0,0)
    for char in board:
        #empty
        if char == '0': 
            fill(200)
            rect((scale*col)+1, (scale*row)+1, scale-1, scale-1)
            col += 1
            #barrier
        elif char == '1':
            fill(0)
            rect((scale*col)+1, (scale*row)+1, scale-1, scale-1)
            col +=1
        #origin
        elif char == '2':
            fill(0,200,255)
            rect((scale*col)+1, (scale*row)+1, scale-1, scale-1)
            col +=1
        #finish
        elif char == '3':
            fill(255,0,0)
            rect((scale*col)+1, (scale*row)+1, scale-1, scale-1)
            col +=1
        #opened_cell
        elif char == '4':
            fill(255,255,0)
            rect((scale*col)+1, (scale*row)+1, scale-1, scale-1)
            col +=1
        #closed_cell
        elif char == '5':
            fill(255, 0,255)
            rect((scale*col)+1, (scale*row)+1, scale-1, scale-1)
            col +=1
        elif char == '6':
            fill(128,0,128)
            rect((scale*col)+1, (scale*row)+1, scale-1, scale-1)
            col +=1
        if col == width/scale:
            row+=1
            col = 0
            
            
def finish_dist(cell):
    width_new = width/scale
    cell_dist_wall = cell % width_new
    cell_dist_roof = cell//width_new
    finish_dist_wall = finish % width_new
    finish_dist_roof = finish // width_new
    x_over = abs(cell_dist_wall - finish_dist_wall)
    y_over = abs(cell_dist_roof - finish_dist_roof)
    return x_over + y_over

def origin_dist(cell):
    width_new = width/scale
    cell_dist_wall = cell % width_new
    cell_dist_roof = cell//width_new
    finish_dist_wall = origin % width_new
    finish_dist_roof = origin // width_new
    x_over = abs(cell_dist_wall - finish_dist_wall)
    y_over = abs(cell_dist_roof - finish_dist_roof)
    return x_over + y_over

def draw_path():
    global path
    global path_draw
    path.append(finish)
    while origin not in path:    
        path.append(came_from.get(path[len(path)-1]))
    #print(path)
    
    path.remove(finish)
    path.remove(origin)
    
    for n in path:
        board[n] = '6'
        draw_barriers()
        #draw()

    
    
def astar_alg():
    global width_new
    global open_list
    global astar
    global came_from
    global path_draw
    width_new = (width)/scale
    height_new = height/scale
    
    
        
        
    first_value_dict = int(list(open_list.values())[0])
    for value in open_list.values():
        if value < first_value_dict:
            first_value_dict = value
    ##print(first_value_dict)
    for index, cost in open_list.items():
        
        open_list = {k: v for k, v in sorted(open_list.items(), key=lambda item: item[1])}
        #test to make sure only dealing with lowest costs
        if cost == first_value_dict:
            dist_left_wall = (index % width_new)
            dist_right_wall = ((width_new)-(index % width_new))-1
            dist_top = index//width_new
            dist_bottom = (height_new-1)-(index//width_new)
            
            #add to closed list and delete from open list
            
            closed_list[index] = cost
            ##print(open_list)
            del open_list[index]
            ##print(index, cost)
            if dist_left_wall > 0 and index-1 not in barriers and index-1 not in list(closed_list.keys()) and index-1 not in list(open_list.keys()):
                open_list[index-1] = (origin_dist(index-1) + finish_dist(index-1))-1
                came_from[index-1] = index
            if dist_right_wall > 0 and index+1 not in barriers and index+1 not in list(closed_list.keys()) and index+1 not in list(open_list.keys()):
                open_list[index+1] = (origin_dist(index+1) + finish_dist(index+1))-1
                came_from[index+1] = index
            if dist_top > 0 and index-width_new not in barriers and index-width_new not in list(closed_list.keys()) and index-width_new not in list(open_list.keys()):
                open_list[index-width_new] = (origin_dist(index-width_new) + finish_dist(index-width_new))-1
                came_from[index-width_new] = index
            if dist_bottom > 0 and index+width_new not in barriers and index+width_new not in list(closed_list.keys()) and index+width_new not in list(open_list.keys()):
                open_list[index+width_new] = (origin_dist(index+width_new)+ finish_dist(index+width_new))-1
                came_from[index+width_new] = index
    ##print(open_list)  
    for index in open_list.keys():
        if index == origin:
            board[index] = '2'
        elif index == finish:
            board[index] = '3'
            astar = False
            
            #print(came_from)
        else:
            board[index] = '5' 
    for index in closed_list.keys():
        if index == origin:
            board[index] = '2'
        elif index == finish:
            board[index] = '3'
        else:
            board[index] = '4'
    if finish in open_list.keys():
        draw_path()
    
        
                

    
    
def buttons():
    global astar_button
    global save_button
    global load_button
    
    save_button = Button('Save', (1200/24)*22,(1000/15)*12)
    astar_button = Button("A* Search",(1200/24)*22,(1000/15)*2)
    load_button = Button("Load Board", (1200/24)*22,(1000/15)*13)
    astar_button.draw_button()
    save_button.draw_button()
    load_button.draw_button()
    
def setup():
    global generating_barriers
    global choosing_origin
    global choosing_finish
    global board
    global barriers
    global selecting_alg
    global origin
    global finish
    global astar
    global open_list
    global closed_list
    global came_from
    global path_draw
    global path
    path = []
    path_draw = False
    came_from = dict()
    open_list = dict()
    closed_list = dict()
    astar = False
    origin = 0
    finish = 0
    generating_barriers = True
    choosing_origin = False
    choosing_finish = False
    selecting_alg = False
    size(1200,1000)
    frameRate(5)
    board = list('0' * ((width/scale)*(height/scale)))
    barriers = []
    generate_grid()
    buttons()
    
    
    
def draw():
    global path_draw
    global astar
    if astar:
        astar_alg()
        draw_barriers()
                
    
def keyPressed():
    global choosing_origin
    global generating_barriers
    global selecting_alg
    global choosing_finish
    if key == ENTER and generating_barriers == True:
        generating_barriers = False
        choosing_origin = True
    elif key == ENTER and choosing_origin == True:
        choosing_origin = False
        choosing_finish = True
    elif key == ENTER and choosing_finish == True:
        choosing_finish = False
        selecting_alg = True
        #print(barriers, origin, finish)
    
    
def mouseDragged():
    if generating_barriers:
        if mouseY < height and mouseX < width and mouseX > 0:
            if mouseButton == LEFT:
                convertToArray(mouseX, mouseY, False, False, False)
                draw_barriers() 
            if mouseButton == RIGHT:
                #print('hi')
                convertToArray(mouseX, mouseY, True, False, False)
                draw_barriers()
                
def mouseClicked():
    global choosing_origin
    global selecting_alg
    global choosing_finish
    global astar
    global board
    global generating_barriers
    global barriers
    global finish
    global origin
    
    if choosing_origin:
        if mouseY < height and mouseX < width and mouseX > 0:
            if mouseButton == LEFT:
                convertToArray(mouseX, mouseY, True, True, False)
                draw_barriers()
        
    if choosing_finish:
        if mouseY < height and mouseX < width and mouseX > 0:
            if mouseButton == LEFT:
                convertToArray(mouseX, mouseY, True, False, True)
                draw_barriers()
    
    if selecting_alg:
        if astar_button.mouseInButton(mouseX, mouseY):
            astar = True
            open_list[origin] = 0 + finish_dist(origin)
        '''
        if save_button.mouseInButton(mouseX, mouseY):
            file = open('saves.txt', 'w')
            for i in board:
                file.write(i)
            file.close()
        '''
    
    if generating_barriers:
        if load_button.mouseInButton(mouseX, mouseY):
            board = []
            file = open('saves.txt', 'r')
            char_count = 0
            for i in file:
                for char in i:
                    board.append(char)
                    if char == '1':
                        barriers.append(char_count)
                    elif char == '2':
                        origin = char_count
                    elif char == '3':
                        finish = char_count
                    char_count +=1
                    
            file.close()
            draw_barriers()
            generating_barriers = False
            choosing_finish = False
            choosing_origin = False
            selecting_alg = True
    
    
