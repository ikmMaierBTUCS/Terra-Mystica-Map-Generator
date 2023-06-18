#!/usr/bin/env python
# coding: utf-8

# In[9]:


import math
import random
from IPython.display import display, HTML

class HexagonalMap:
    def __init__(self, height, width, form, rivers):
        # form = 0 => sharp, form = 1 => round
        self.width = width
        self.height = height
        self.form = form
        self.rivers = rivers
        self.map = {}
        self.colors = ['red','yel','bro','bla','blu','grn','gry','~~~','???']
        
    def out_of_bounds(self,hexf):
        # is the hex outside of the map?
        if hexf[1] not in range(self.height) or hexf[0] not in range(self.width - ((hexf[1] + self.form) % 2)):
            return True
        else:
            return False
        
    def stock(self,color):
        # number of hexes of colour color that is yet on the map
        return list(self.map.values()).count(color)
        
    def work_distance(self, hexf, color):
        # measure of work required to get from hexf to the next hex of colour color
        maximal_work = 210
        if self.stock(color) == 0: # check if any hexes of same color exist yet
            print('no '+color+' yet')
            return maximal_work
        for direction in range(6): # check if color is adjacent
            if not self.out_of_bounds(self.next_hex(hexf,direction)) and self.map[self.next_hex(hexf,direction)] == color: 
                print(color+' is adjacent')
                return 0
        '''for direction in range(6): # check if color is bridgable
            if self.map[self.next_hex(hexf,direction)] == 'riv' and self.map[self.next_hex(hexf,direction + 1)] == 'riv' and  self.map[self.next_hex(next_hex(hexf,direction),direction + 1)] == color: 
                #print(color+' is bridgable')
                return 5'''
        work = maximal_work
        for path_length in range(2,5):
            if work < 42*path_length:
                break
            path = path_length * [-1]
            for initial_direction in range(6):
                path[0] = initial_direction
                for further_steers in range(3**(path_length - 1)):
                    for further_step in range(1, path_length):
                        path[further_step] = ((further_steers // (3**(further_step - 1)) % 3) - 1 + path[further_step - 1]) % 6
                    # each possible path set up
                    #print('path :'+str(path))
                    transit_colors = []
                    path_legal = True
                    hex_in_path = hexf
                    for direction in path:
                        hex_in_path = self.next_hex(hex_in_path,direction)
                        if self.out_of_bounds(hex_in_path):
                            path_legal = False
                            break
                        else:
                            transcol = self.map[hex_in_path]
                            if transcol == ' ~ ':
                                transit_colors += ['~~~']
                            else:
                                transit_colors += [transcol]
                    #print('transit colors: '+str(transit_colors))
                    if path_legal and transit_colors[-1] == color:
                        path_work = path_cost(transit_colors)
                        if path_work < work:
                            print(str(path)+' is shorter at '+str(path_work))
                            work = path_work
        return work
                            
    def share_score(self, hexf, color):
        average_stock = 0
        for colour in ['red','yel','bro','bla','blu','grn','gry']:
            average_stock += self.stock(colour)
        average_stock = average_stock / 7
        #print('average stock: '+str(average_stock))
        quantityvalue = 4 + self.stock(color) - average_stock
        #print('quantityvalue: '+str(quantityvalue))
        share_score = self.work_distance(hexf,color) // quantityvalue
        return share_score
    
    def create_map(self):
        # initialize map and set rivers
        for row in range(self.height):
            for col in range(self.width - ((row + self.form) % 2)):
                x = col
                y = row
                if (x,y) in self.rivers:
                    self.map[(x, y)] = ' ~ '
                else:
                    self.map[(x, y)] = '???'
        self.display_map()
        
        # randomize start field
        start_y = random.randint(0,self.height - 1)
        start_x = random.randint(0,self.width - ((start_y + self.form) % 2) - 1)
        current_hex = (start_x,start_y)
        if self.map[current_hex] != ' ~ ':        
            self.map[current_hex] = self.colors[random.randint(0,6)]
        else:
            self.map[current_hex] = '~~~'
        self.display_map()
        
        # randomize first step
        current_direction = random.randint(0,5)
        current_hex = self.next_hex(current_hex,current_direction)
        #print(current_direction, current_hex)
        if self.out_of_bounds(current_hex):
            pass
        elif self.map[current_hex] == ' ~ ':
            self.map[current_hex] = '~~~'
        else:
            share_scores = {}
            accumulated_scores = []
            for color in ['red','yel','bro','bla','blu','grn','gry']:
                score = self.share_score(current_hex,color)
                if len(accumulated_scores) == 0:
                    accumulated_scores += [score]
                else:
                    accumulated_scores += [accumulated_scores[-1] + score]
                share_scores[color] = score
                print(color, score)
            dice = random.randint(0,accumulated_scores[-1] - 1)
            if dice < accumulated_scores[0]:
                self.map[current_hex] = 'red'
            elif dice < accumulated_scores[1]:
                self.map[current_hex] = 'yel'
            elif dice < accumulated_scores[2]:
                self.map[current_hex] = 'bro'
            elif dice < accumulated_scores[3]:
                self.map[current_hex] = 'bla'
            elif dice < accumulated_scores[4]:
                self.map[current_hex] = 'blu'
            elif dice < accumulated_scores[5]:
                self.map[current_hex] = 'grn'
            elif dice < accumulated_scores[6]:
                self.map[current_hex] = 'gry'
        self.display_map()
        current_direction = (current_direction + 2) % 6
        #print(current_hex, current_direction)
        
        # further steps
        while '???' in self.map.values() or ' ~ ' in self.map.values():
            while not self.out_of_bounds(self.next_hex(current_hex,current_direction)) and not self.map[self.next_hex(current_hex,current_direction)] in ['???',' ~ ']:
                #print('redirection, because current direction points at neither ??? nor  ~  nor out of map')
                current_direction = (current_direction - 1) % 6
                #print(current_hex, current_direction)
            current_hex = self.next_hex(current_hex,current_direction)
            print(current_direction, current_hex)
            if self.out_of_bounds(current_hex):
                pass
            elif self.map[current_hex] == ' ~ ':
                self.map[current_hex] = '~~~'
            else:
                share_scores = {}
                accumulated_scores = []
                for color in ['red','yel','bro','bla','blu','grn','gry']:
                    score = self.share_score(current_hex,color)**2
                    if len(accumulated_scores) == 0:
                        accumulated_scores += [score]
                    else:
                        accumulated_scores += [accumulated_scores[-1] + score]
                    share_scores[color] = score
                    print(color, score)
                dice = random.randint(0,accumulated_scores[-1] - 1)
                if dice < accumulated_scores[0]:
                    self.map[current_hex] = 'red'
                elif dice < accumulated_scores[1]:
                    self.map[current_hex] = 'yel'
                elif dice < accumulated_scores[2]:
                    self.map[current_hex] = 'bro'
                elif dice < accumulated_scores[3]:
                    self.map[current_hex] = 'bla'
                elif dice < accumulated_scores[4]:
                    self.map[current_hex] = 'blu'
                elif dice < accumulated_scores[5]:
                    self.map[current_hex] = 'grn'
                elif dice < accumulated_scores[6]:
                    self.map[current_hex] = 'gry'
            self.display_map()
            current_direction = (current_direction + 1) % 6
        

    def display_map(self):
        for row in range(self.height):
            if (row + self.form) % 2 == 1:
                rowstr = '  '
            else:
                rowstr = ''
            for col in range(self.width - ((row + self.form) % 2)):
                rowstr += self.map[(col,row)] + ' '
            print(rowstr)
        print('\n')
        
    def display_final_map_colored(self):
        for row in range(self.height):
            if (row + self.form) % 2 == 1:
                rowstr = '---'
            else:
                rowstr = ''
            for col in range(self.width - ((row + self.form) % 2)):
                rowstr += transform_string_to_box(self.map[(col,row)])
            display(HTML(rowstr))
            
    def bga_format(self):
        bga_format = ''
        rows = []
        for row in range(self.height):
            rows += [','.join([bga_symbol(self.map[(col,row)]) for col in range(self.width - ((row + self.form) % 2))])]
        bga_format = '\n'.join(rows)
        return bga_format

    def next_hex(self,hexf,direction):
        if direction == 0:
            if (hexf[1] + self.form) % 2 == 0:
                return (hexf[0],hexf[1] + 1)
            else:
                return (hexf[0] + 1,hexf[1] + 1)
        if direction == 1:
            return (hexf[0] + 1,hexf[1])
        if direction == 2:
            if (hexf[1] + self.form) % 2 == 0:
                return (hexf[0],hexf[1] - 1)
            else:
                return (hexf[0] + 1,hexf[1] - 1)
        if direction == 3:
            if (hexf[1] + self.form) % 2 == 0:
                return (hexf[0] - 1,hexf[1] - 1)
            else:
                return (hexf[0],hexf[1] - 1)
        if direction == 4:
            return (hexf[0] - 1,hexf[1])
        if direction == 5:
            if (hexf[1] + self.form) % 2 == 0:
                return (hexf[0] - 1,hexf[1] + 1)
            else:
                return (hexf[0],hexf[1] + 1)
    
def path_cost(transit_colors):
    destination_color = transit_colors[-1]
    if ['~~~','~~~','~~~','~~~'] in [transit_colors[i:i + 4] for i in range(len(transit_colors) - 3)]:
        if destination_color == 'blu':
            path_work = 308
        else:
            path_work = 350
    elif ['~~~','~~~','~~~'] in [transit_colors[i:i + 3] for i in range(len(transit_colors) - 2)]:
        if destination_color == 'blu':
            path_work = 154
        else:
            path_work = 210
    elif ['~~~','~~~'] in [transit_colors[i:i + 2] for i in range(len(transit_colors) - 1)]:
        if destination_color == 'blu':
            path_work = 70
        else:
            path_work = 126
    elif ['~~~'] in [transit_colors[i:i + 1] for i in range(len(transit_colors))]:
        if destination_color == 'blu':
            path_work = 14
        else:
            path_work = 42
    else:
        path_work = 0
    for tcn in range(len(transit_colors)):
        current_color = transit_colors[tcn]
        trans_work = 42*color_distance(destination_color,transit_colors[tcn])
        if destination_color == 'red': 
            if current_color not in ['red','~~~',' ~ ']:
                trans_work = (trans_work + 70)/2
        if destination_color == 'yel': 
            if current_color not in ['yel','red','bro','~~~',' ~ '] and (tcn == 0 or transit_colors[tcn - 1] not in ['~~~',' ~ ']):
                trans_work = (trans_work + 77)/2
        if destination_color == 'bla':
            trans_work = 5*trans_work/6
        if destination_color == 'gry':
            if len(transit_colors) == 2:
                trans_work = 9*trans_work/7
            else:
                trans_work = 5*trans_work/7
        path_work += trans_work
    return path_work


def color_index(color):
    if color == 'red':
        return 0
    elif color == 'yel':
        return 1
    elif color == 'bro':
        return 2
    elif color == 'bla':
        return 3
    elif color == 'blu':
        return 4
    elif color == 'grn':
        return 5
    elif color == 'gry':
        return 6
    else:
        return 100

def color_distance(color1, color2):
    if color1 in [' ~ ','~~~'] or color2 in [' ~ ','~~~']:
        distance = 0
    elif color1 == '???' or color2 == '???':
        distance = 1.5
    else:
        distance = min([(color_index(color1) - color_index(color2)) % 7,(color_index(color2) - color_index(color1)) % 7])
    return distance
   
def transform_string_to_box(color_string):
    color_mapping = {
        'red': (' ', 'red'),
        'yel': (' ', 'yellow'),
        'bro': (' ', '#835C3B'),
        'bla': (' ', 'black'),
        'blu': (' ', 'blue'),
        'grn': (' ', 'green'),
        'gry': (' ', '#808080'),
        '~~~': (' ', '#BFEFFF')
    }

    if color_string in color_mapping:
        display_text, color = color_mapping[color_string]
        box_html = f'<div style="background-color: {color}; width: 30px; height: 25px; text-align: center; display: inline-block; margin-bottom: -20px;">{display_text[:4]}</div>'
        return box_html
    else:
        return color_string 

def bga_symbol(color):
    if color == 'red':
        return 'R'
    elif color == 'yel':
        return 'Y'
    elif color == 'bro':
        return 'U'
    elif color == 'bla':
        return 'K'
    elif color == 'blu':
        return 'B'
    elif color == 'grn':
        return 'G'
    elif color == 'gry':
        return 'S'
    elif color == '~~~':
        return 'I'
                
                              

# Run the code by executing the following commands:

#1 Create a colorless map for given river layout with parameters (height, width, form, rivers)
# height is the number of horizontal lines of hexes
# width is the number of hexes in in the LONGER lines (remember that between 2 longer lines is a line shorter by one)
# form = 0, if the uppermost line is longer, form = 1, if the uppermost line is shorter
# rivers is the list of coordinates occupied by rivers. CAUTION: the coordinates are written (column, row)
# here you can copy the layout of some well-known maps:
#archipelago: HexagonalMap(9,13,0,[(6,0),(10,0),(6,1),(7,1),(9,1),(6,2),(8,2),(9,2),(10,2),(11,2),(0,3),(4,3),(5,3),(3,3),(8,3),(11,3),(1,4),(3,4),(5,4),(6,4),(9,4),(1,5),(2,5),(5,5),(6,5),(7,5),(8,5),(11,5),(6,6),(9,6),(10,6),(11,6),(6,7),(8,7),(6,8),(9,8)])
#onion: HexagonalMap(9,13,0,[(3,1),(4,1),(5,1),(6,1),(7,1),(8,1),(2,2),(3,2),(9,2),(10,2),(2,3),(6,3),(9,3),(3,4),(5,4),(6,4),(7,4),(9,4),(10,4),(11,4),(12,4),(1,5),(2,5),(6,5),(10,5),(2,6),(3,6),(4,6),(9,6),(10,6),(3,7),(4,7),(5,7),(6,7),(7,7),(8,7)])
#loon: HexagonalMap(9,13,1,[(8,0),(9,0),(3,1),(4,1),(7,1),(10,1),(1,2),(2,2),(6,2),(10,2),(3,3),(7,3),(8,3),(10,3),(2,4),(5,4),(6,4),(8,4),(1,5),(4,5),(6,5),(8,5),(1,6),(2,6),(3,6),(9,6),(10,6),(3,7),(7,7),(8,7),(11,7),(2,8),(4,8),(5,8),(6,8)])
#FI: HexagonalMap(9,13,1,[(1,0),(5,0),(2,1),(6,1),(7,1),(8,1),(2,2),(3,2),(4,2),(8,2),(9,2),(10,2),(11,2),(12,2),(5,3),(9,3),(0,4),(1,4),(3,4),(4,4),(9,4),(2,5),(3,5),(5,5),(6,5),(7,5),(10,5),(1,6),(7,6),(10,6),(2,7),(7,7),(10,7),(2,8),(7,8),(10,8)])
#fjords: HexagonalMap(9,13,0,[(2,0),(2,1),(6,1),(7,1),(8,1),(9,1),(10,1),(3,2),(4,2),(6,2),(11,2),(0,3),(1,3),(2,3),(4,3),(5,3),(11,3),(12,3),(3,4),(6,4),(11,4),(2,5),(6,5),(10,5),(2,6),(7,6),(10,6),(1,7),(7,7),(8,7),(9,7),(1,8),(2,8),(7,8)])
#original: HexagonalMap(9,13,0,[(1,1),(2,1),(5,1),(6,1),(9,1),(10,1),(0,2),(1,2),(3,2),(5,2),(7,2),(9,2),(11,2),(12,2),(3,3),(4,3),(7,3),(9,3),(8,4),(9,4),(2,5),(3,5),(6,5),(7,5),(8,5),(0,6),(1,6),(2,6),(4,6),(6,6),(8,6),(3,7),(4,7),(5,7),(8,7),(9,8)])

hex_map = HexagonalMap(9,13,0,[(2,0),(2,1),(6,1),(7,1),(8,1),(9,1),(10,1),(3,2),(4,2),(6,2),(11,2),(0,3),(1,3),(2,3),(4,3),(5,3),(11,3),(12,3),(3,4),(6,4),(11,4),(2,5),(6,5),(10,5),(2,6),(7,6),(10,6),(1,7),(7,7),(8,7),(9,7),(1,8),(2,8),(7,8)])

#2 fill the map with colors
hex_map.create_map()

#3 print the finished map as a string suitable for BGA format map-files
print(hex_map.bga_format())

#4 print an ugly colored preview of the map
hex_map.display_final_map_colored()


# In[ ]:




