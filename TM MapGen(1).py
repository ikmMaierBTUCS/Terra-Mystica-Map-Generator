import math
import random
from IPython.display import display, HTML
import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon
import numpy as np

class HexagonalMap:
    def __init__(self, height, width, form, rivers, start = 0):
        # form = 0 => sharp, form = 1 => round
        self.width = width
        self.height = height
        self.form = form
        self.rivers = rivers
        self.map = {}
        # initialize map and set rivers
        for row in range(self.height):
            for col in range(self.width - ((row + self.form) % 2)):
                x = col
                y = row
                if (x,y) in self.rivers:
                    self.map[(x, y)] = ' ~ '
                else:
                    self.map[(x, y)] = '???'
        self.colors = ['red','yel','bro','bla','blu','grn','gry','~~~','???']
        self.luck = np.array([0]*7, dtype=np.float64)
        if start == 0:
            self.start = (random.randint(2,width - 3),random.randint(2,height - 3))
        else:
            self.start = start
            
    def reset(self):
        return HexagonalMap(self.height, self.width, self.form, self.rivers, self.start)
        
    def out_of_bounds(self,hexf):
        # is the hex outside of the map?
        if hexf[1] not in range(self.height) or hexf[0] not in range(self.width - ((hexf[1] + self.form) % 2)):
            return True
        else:
            return False
    
    def center_hex(self):
        middle_height = (self.height - 1) / 2
        if self.height % 2 == 0:
            middle_width = (self.width - 0.5) / 2
        elif self.height % 4 == 1:
            middle_width = (self.width - 1 - self.form) / 2
        elif self.height % 4 == 3:
            middle_width = (self.width - 2 + self.form) / 2
        return (middle_width,middle_height)
    
    def fly_distance(self,hex1,hex2):
        dist = abs(hex1[1] - hex2[1]) + max([0, abs(hex1[0] - hex2[0]) - abs(hex1[1] - hex2[1])/2])
        return dist
    
    def absolute_stock(self,color):
        # number of hexes of colour color that is yet on the map
        return list(self.map.values()).count(color)
    
    def value_of_hex(self,hexf):
        if self.out_of_bounds(hexf):
            return 0
        else:
            distance = self.fly_distance(hexf,self.center_hex())
            max_dist = self.width / 3 + self.height / 2
            return 1.5 - (distance / max_dist)**2
            
    def stock(self,color):
        # sum of weights of hexes of colour color that are yet on the map
        stock = 0
        for hexf in self.map.keys():
            if self.map[hexf] == color:
                stock += self.value_of_hex(hexf)
        return stock
        #return list(self.map.values()).count(color)
        
    def work_distance(self, hexf, color):
        # measure of work required to get from hexf to the next hex of colour color
        maximal_work = 168
        if self.stock(color) == 0: # check if any hexes of same color exist yet
            #print('no '+color+' yet')
            return maximal_work
        for direction in range(6): # check if color is adjacent
            if not self.out_of_bounds(self.next_hex(hexf,direction)) and self.map[self.next_hex(hexf,direction)] == color: 
                #print(color+' is adjacent')
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
                            #print(str([dir_str(dire) for dire in path]) + ' is shorter at '+str(path_work))
                            work = path_work
        return work
    
    def number_of_landhexes(self):
        actual_rivers = [riv for riv in self.rivers if not self.out_of_bounds(riv)]
        all_hexes = self.height * (self.width) - abs((self.height + self.form) // 2)
        return all_hexes - len(actual_rivers)
    
    def contingent(self, color):
        start_contingent = self.number_of_landhexes() / 7 + 0.02
        contingent = max([0, start_contingent - self.absolute_stock(color)])
        return contingent
    
    def mapfunction(self, hexf):
        # function for the dictionary map. returns '' if hexf out_of_bounds
        if self.out_of_bounds(hexf):
            return ''
        else:
            return self.map[hexf]
    
    def river_access(self, hexf):
        if self.map[hexf] in ['~~~', ' ~ '] or self.out_of_bounds(hexf):
            return '~'
        adj_river = False
        for direction in range(6):
            if self.mapfunction(self.next_hex(hexf,direction)) in ['~~~', ' ~ ']:
                if self.mapfunction(self.next_hex(hexf,(direction + 3) % 6)) in ['~~~', ' ~ ']:
                    return 2
                if self.mapfunction(self.next_hex(hexf,(direction + 2) % 6)) in ['~~~', ' ~ '] and not self.mapfunction(self.next_hex(hexf,(direction + 1) % 6)) in ['~~~', ' ~ ']:
                    return 2
                if self.mapfunction(self.next_hex(hexf,(direction - 2) % 6)) in ['~~~', ' ~ '] and not self.mapfunction(self.next_hex(hexf,(direction - 1) % 6)) in ['~~~', ' ~ ']:
                    return 2
                adj_river = True
        if adj_river:
            return 1
        else:
            return 0
        
    def river_access_score(self, color):
        score = 0
        for hexf in self.map.keys():
            if self.map[hexf] == color:
                score += self.river_access(hexf)
        return score
    
    def river_access_saldo(self,color):
        average_score = 0
        for col in self.colors[:7]:
            average_score += self.river_access_score(col)
        average_score = average_score / 7
        saldo = self.river_access_score(color) - average_score
        return saldo
                            
    def share_score(self, distance, color):
        #print(color,distance,self.contingent(color))
        share_score = round(distance**1.5 * self.contingent(color)**0.5 * max([1,6 - self.river_access_saldo(color)])**0.5 * max([0.4,4 - self.luck[color_index(color)]]) * 10)
        return share_score
    
    def create_map(self):
        #self.display_map()
        
        # randomize start field
        #start_y = random.randint(2,self.height - 3)
        #start_x = random.randint(2,self.width - ((start_y + self.form) % 2) - 3)
        #current_hex = (start_x,start_y)
        current_hex = self.start
        if self.map[current_hex] != ' ~ ':        
            dice = random.randint(0,6)
            self.map[current_hex] = self.colors[dice]
            luck = [-self.value_of_hex(current_hex) / 7]*7
            for color in range(len(luck)):
                if color == dice:
                    luck[color] += self.value_of_hex(current_hex)
                    break
            self.luck = np.array(luck, dtype=np.float64)
            #for col in range(len(luck)):
                #print(self.colors[col] + ': ' + str(luck[col]))
            #print()
            
        else:
            self.map[current_hex] = '~~~'
            #luck = np.array([0]*7, dtype=np.float64)
        #print(luck)
        #self.display_map()
        
        # randomize first step
        current_direction = random.randint(0,5)
        current_hex = self.next_hex(current_hex,current_direction)
        #print(current_direction, current_hex)
        #print(self.value_of_hex(current_hex))
        if self.out_of_bounds(current_hex):
            pass
        elif self.map[current_hex] == ' ~ ':
            self.map[current_hex] = '~~~'
        else:
            distances = {} 
            share_scores = []
            accumulated_scores = []
            for color in ['red','yel','bro','bla','blu','grn','gry']:
                distances[color] = self.work_distance(current_hex,color)
                score = round(abs(self.share_score(distances[color],color))**1)
                if len(accumulated_scores) == 0:
                    accumulated_scores += [score]
                else:
                    accumulated_scores += [accumulated_scores[-1] + score]
                share_scores += [score]
                #print(color, score)
            randint = random.randint(0,accumulated_scores[-1] - 1)
            for acsc in range(len(accumulated_scores)):
                if randint < accumulated_scores[acsc]:
                    dice = acsc
                    break
            self.map[current_hex] = self.colors[dice]
            luck_change = [-(distances[color]**1.5) * self.value_of_hex(current_hex) / sum([dis**1.5 for dis in distances.values()]) for color in ['red','yel','bro','bla','blu','grn','gry']]
            for color in range(len(luck_change)):
                if luck_change[color] == dice:
                    luck_change[color] += self.value_of_hex(current_hex)
                    #print(sum(luck_change))
                    break
            self.luck += np.array(luck_change, dtype=np.float64)
            #for col in range(len(luck)):
                #print(self.colors[col] + ': ' + str(luck[col]))
            #print()
        #self.display_map()
        current_direction = (current_direction + 2) % 6
        #print(current_hex, current_direction)
        
        # further steps
        while '???' in self.map.values() or ' ~ ' in self.map.values():
            #plot_map()
            while not self.out_of_bounds(self.next_hex(current_hex,current_direction)) and not self.map[self.next_hex(current_hex,current_direction)] in ['???',' ~ ']:
                #print('redirection, because current direction points at neither ??? nor  ~  nor out of map')
                current_direction = (current_direction - 1) % 6
                #print(current_hex, current_direction)
            current_hex = self.next_hex(current_hex,current_direction)
            #print(dir_str(current_direction) + ' to ' +str(current_hex))
            #print(self.value_of_hex(current_hex))
            if self.out_of_bounds(current_hex):
                pass
            elif self.map[current_hex] == ' ~ ':
                self.map[current_hex] = '~~~'
            else:
                distances = {} 
                share_scores = []
                accumulated_scores = []
                for color in ['red','yel','bro','bla','blu','grn','gry']:
                    distances[color] = self.work_distance(current_hex,color)
                    score = round(abs(self.share_score(distances[color],color))**1)
                    if len(accumulated_scores) == 0:
                        accumulated_scores += [score]
                    else:
                        accumulated_scores += [accumulated_scores[-1] + score]
                    share_scores += [score]
                    #print(color, score)
                randint = random.randint(0,accumulated_scores[-1] - 1)
                for acsc in range(len(accumulated_scores)):
                    if randint < accumulated_scores[acsc]:
                        dice = acsc
                        break
                self.map[current_hex] = self.colors[dice]
                luck_change = [-(distances[color]**1.5) * self.value_of_hex(current_hex) / sum([dis**1.5 for dis in distances.values()]) for color in ['red','yel','bro','bla','blu','grn','gry']]
                #print(dice)
                for color in range(len(luck_change)):
                    if color == dice:
                        #print(self.colors[color] + ' won')
                        luck_change[color] += self.value_of_hex(current_hex)
                        #print(sum(luck_change))
                        break
                self.luck += np.array(luck_change, dtype=np.float64)
                #for col in range(len(luck)):
                    #print(self.colors[col] + ': ' + str(luck[col]))
                #print()
                #print(sum(luck))
                #self.display_map()
            #for color in self.colors[:7]:
                #print(color + ': ' + str(self.contingent(color)))
            current_direction = (current_direction + 1) % 6
        
        #print('Contingents:')
        #for color in self.colors[:7]:
        #    print(color + ': ' + str(round(self.contingent(color),2)))
        #print('River access:')
        #for color in self.colors[:7]:
        #    print(color + ': ' + str(self.river_access_score(color)))
        #print('Luck:')
        luckstr = 'Luck: '
        for col in range(len(self.luck)):
            luckstr += self.colors[col] + ': ' + str(round(self.luck[col],2)) + '; '
        luckstr = luckstr + '\n' + 'River access: '
        for color in self.colors[:7]:
            luckstr = luckstr + color + ': ' + str(self.river_access_score(color)) + '; '
        luckstr = luckstr + '\n'
        nolh = self.number_of_landhexes()
        for color in self.colors[:7]:
            delta = self.absolute_stock(color) - (nolh / 7)
            if delta >= 1:
                luckstr = luckstr + color + ' has +' + str(round(delta,1)) + ' hex;'
            if delta <= -1:
                luckstr = luckstr + color + ' has ' + str(round(delta,1)) + ' hex; '
        return luckstr
        
    def number_test(self):
        nolh = self.number_of_landhexes()
        if nolh % 7 == 0:
            av = nolh // 7
            totaldelta = 0
            for color in self.colors[:7]:
                delta = abs(self.absolute_stock(color) - (nolh / 7))
                #print(color,delta)
                totaldelta += delta
            if totaldelta > 3:
                #print(totaldelta)
                return False
            else:
                return True
        else:
            for color in self.colors[:7]:
                delta = abs(self.absolute_stock(color) - (nolh / 7))
                if delta > 1:
                    #print(color,delta)
                    return False
            return True
        
    def river_access_test(self):
        for color in self.colors[:7]:
            saldo = self.river_access_saldo(color)
            if saldo > 2:
                #print(color,saldo)
                return False
        return True
    
    def luck_test(self):
        for color in range(7):
            luck = self.luck[color]
            if luck > 1.5:
                #print(self.colors[color],luck)
                return False
        return True
        
        
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
        for row in rows:
            print(row)
        bga_format = '\n'.join(rows)
        return bga_format
    
    def river_access_map(self):
        bga_format = ''
        rows = []
        for row in range(self.height):
            if (row + self.form) % 2 == 0:
                rowstr = ''
            else:
                rowstr = ' '
            rowstr = rowstr + ','.join([str(self.river_access((col,row))) for col in range(self.width - ((row + self.form) % 2))])
            rows += [rowstr]
        for row in rows:
            print(row)
        bga_format = '\n'.join(rows)
        #return bga_format

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
    def painter(self,ax):
        plot_colors ={
                    'red': 'red',
                    'yel': 'yellow',
                    'bro': '#835C3B',
                    'bla': 'black',
                    'blu': 'blue',
                    'grn': 'green',
                    'gry': '#808080',
                    '~~~': '#BFEFFF',
                    ' ~ ': '#BFEFFF',
                    '???': 'orange'
                    }
        hexes = self.map
        for key in hexes:
            hex_x = key[1]
            hex_y = key[0]
            align_hex = 0.5 if (hex_x + self.form) % 2 ==1 else 1
            alphaval = 0.2 if hexes[key] == '~~~' else 0.7
            hex_col = plot_colors[hexes[key]]
            hexagon = RegularPolygon((hex_y - align_hex, -hex_x), numVertices=6, radius=np.sqrt(1 / 3),
                                    alpha=alphaval, fill=True, color=hex_col)
            ax.add_patch(hexagon)
    
def path_cost(transit_colors):
    destination_color = transit_colors[-1]
    if ['~~~','~~~','~~~','~~~'] in [transit_colors[i:i + 4] for i in range(len(transit_colors) - 3)]:
        if destination_color == 'blu':
            path_work = 42 * 6
        #elif destination_color == 'yel':
        #    path_work = 378 - 4 * 21
        elif destination_color == 'gry':
            path_work = 378 - 4 * 42
        else:
            path_work = 42 * 7
    elif ['~~~','~~~','~~~'] in [transit_colors[i:i + 3] for i in range(len(transit_colors) - 2)]:
        if destination_color == 'blu':
            path_work = 42 * 4
        #elif destination_color == 'yel':
        #    path_work = 42 * 35/6 - 3 * 21
        elif destination_color == 'gry':
            path_work = 42 * 35/6 - 3 * 42
        else:
            path_work = 42 * 5
    elif ['~~~','~~~'] in [transit_colors[i:i + 2] for i in range(len(transit_colors) - 1)]:
        if destination_color == 'blu':
            path_work = 42 * 10/6
        #elif destination_color == 'yel':
        #    path_work = 42 * 22/6 - 2 * 21
        elif destination_color == 'gry':
            path_work = 42 * 22/6 - 2 * 42
        else:
            path_work = 42 * 3
    elif ['~~~'] in [transit_colors[i:i + 1] for i in range(len(transit_colors))]:
        if destination_color == 'blu':
            path_work = 42 * 2/6
        #elif destination_color == 'yel':
        #    path_work = 42 * 7/6 - 1 * 21
        elif destination_color == 'gry':
            path_work = 42 * 9/6 - 1 * 42
        else:
            path_work = 42
    else:
        path_work = 0
    for tcn in range(len(transit_colors)):
        current_color = transit_colors[tcn]
        trans_work = 42*color_distance(destination_color,transit_colors[tcn])
        if destination_color == 'red': 
            if current_color not in ['red','~~~',' ~ ']:
                trans_work = (trans_work + 42 * 8/6)/2
        if destination_color == 'yel': 
            if current_color not in ['yel','red','bro','~~~',' ~ '] and (tcn == 0 or transit_colors[tcn - 1] not in ['~~~',' ~ '] or transit_colors[tcn + 1] not in ['~~~',' ~ ']):
                trans_work = min([trans_work, 42 * 8/6])
        if destination_color == 'bla':
            trans_work = trans_work * 5/6
        if destination_color == 'gry':
            if len(transit_colors) == 2:
                if transit_colors[0] in ['~~~',' ~ ']:
                    trans_work = trans_work * 10/6
                else:
                    trans_work = trans_work * 9/6
            else:
                trans_work = trans_work * 4/6
        if destination_color == 'grn':
            trans_work = trans_work * 8/6
        path_work += trans_work
    return path_work

def dir_str(number):
    if number == 0:
        return 'down-right'
    elif number == 1:
        return 'right'
    elif number == 2:
        return 'up-right'
    elif number == 3:
        return 'up-left'
    elif number == 4:
        return 'left'
    elif number == 5:
        return 'down-left'

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
    if 'gry' in [color1,color2] and '~~~' in [color1,color2]:
        distance = 1
    elif 'yel' in [color1,color2] and '~~~' in [color1,color2]:
        distance = 0.5
    elif color1 in [' ~ ','~~~'] or color2 in [' ~ ','~~~']:
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
                


def plot_map():
    fig, ax = plt.subplots(1)
    ax.set_aspect('equal')
    # painter(map_tm['lines'],ax=ax, filling=True)
    hex_map.painter(ax)
    plt.autoscale(enable=True)
    plt.show()
                      


# Example usage
# Run the code by executing the following commands:

#1 Create a colorless map for given river layout with parameters (height, width, form, rivers)
# height is the number of horizontal lines of hexes
# width is the number of hexes in in the LONGER lines (remember that between 2 longer lines is a line shorter by one)
# form = 0, if the uppermost line is longer, form = 1, if the uppermost line is shorter
# rivers is the list of coordinates occupied by rivers. CAUTION: the coordinates are written (column, row)
# here you can copy the layout of some well-known maps:
#archipelago: HexagonalMap(9,13,0,[(6,0),(10,0),(6,1),(7,1),(9,1),(6,2),(8,2),(9,2),(10,2),(11,2),(0,3),(4,3),(5,3),(3,3),(8,3),(11,3),(1,4),(3,4),(5,4),(6,4),(9,4),(1,5),(2,5),(5,5),(6,5),(7,5),(8,5),(11,5),(6,6),(9,6),(10,6),(11,6),(6,7),(8,7),(6,8),(9,8)],(4,5))
#onion: HexagonalMap(9,13,0,[(3,1),(4,1),(5,1),(6,1),(7,1),(8,1),(2,2),(3,2),(9,2),(10,2),(2,3),(6,3),(9,3),(3,4),(5,4),(6,4),(7,4),(9,4),(10,4),(11,4),(12,4),(1,5),(2,5),(6,5),(10,5),(2,6),(3,6),(4,6),(9,6),(10,6),(3,7),(4,7),(5,7),(6,7),(7,7),(8,7)])
#loon: HexagonalMap(9,13,1,[(8,0),(9,0),(3,1),(4,1),(7,1),(10,1),(1,2),(2,2),(6,2),(10,2),(3,3),(7,3),(8,3),(10,3),(2,4),(5,4),(6,4),(8,4),(1,5),(4,5),(6,5),(8,5),(1,6),(2,6),(3,6),(9,6),(10,6),(3,7),(7,7),(8,7),(11,7),(2,8),(4,8),(5,8),(6,8)],(5,3))
#FI: HexagonalMap(9,13,1,[(1,0),(5,0),(2,1),(6,1),(7,1),(8,1),(2,2),(3,2),(4,2),(8,2),(9,2),(10,2),(11,2),(12,2),(5,3),(9,3),(0,4),(1,4),(3,4),(4,4),(9,4),(2,5),(3,5),(5,5),(6,5),(7,5),(10,5),(1,6),(7,6),(10,6),(2,7),(7,7),(10,7),(2,8),(7,8),(10,8)],(7,5))
#fjords: HexagonalMap(9,13,0,[(2,0),(2,1),(6,1),(7,1),(8,1),(9,1),(10,1),(3,2),(4,2),(6,2),(11,2),(0,3),(1,3),(2,3),(4,3),(5,3),(11,3),(12,3),(3,4),(6,4),(11,4),(2,5),(6,5),(10,5),(2,6),(7,6),(10,6),(1,7),(7,7),(8,7),(9,7),(1,8),(2,8),(7,8)],(4,3))
#original: HexagonalMap(9,13,0,[(1,1),(2,1),(5,1),(6,1),(9,1),(10,1),(0,2),(1,2),(3,2),(5,2),(7,2),(9,2),(11,2),(12,2),(3,3),(4,3),(7,3),(9,3),(8,4),(9,4),(2,5),(3,5),(6,5),(7,5),(8,5),(0,6),(1,6),(2,6),(4,6),(6,6),(8,6),(3,7),(4,7),(5,7),(8,7),(9,8)],(5,4))
#ludicrous = HexagonalMap(16,21,1,[(8,0),(9,0),(13,0),(3,1),(4,1),(7,1),(10,1),(14,1),(15,1),(16,1),(1,2),(2,2),(6,2),(10,2),(11,2),(12,1),(13,2),(17,2),(18,2),(19,2),(20,2),(3,3),(7,3),(8,3),(10,3),(13,3),(17,3),(2,4),(5,4),(6,4),(8,4),(11,4),(12,4),(17,4),(1,5),(4,5),(6,5),(8,5),(13,5),(14,5),(15,5),(18,5),(1,6),(2,6),(3,6),(9,6),(10,6),(15,6),(18,6),(3,7),(7,7),(8,7),(11,7),(15,7),(18,7),(2,8),(6,8),(7,8),(8,8),(9,8),(10,8),(13,8),(14,8),(17,8),(18,8),(3,9),(4,9),(6,9),(11,9),(13,9),(15,9),(17,9),(19,9),(20,9),(0,10,),(1,10),(2,10),(4,10),(5,10),(11,10),(12,10),(15,10),(17,10),(3,11),(6,11),(16,11),(17,11),(2,12),(6,12),(10,12),(11,12),(14,12),(15,12),(16,12),(2,13),(7,13),(10,13),(12,13),(14,13),(16,13),(1,14),(7,14),(8,14),(9,14),(11,14),(12,14),(13,14),(16,14),(1,15),(2,15),(7,15),(17,15)])
#ludicrous_quebecois = HexagonalMap(17,22,0,[(1,0),(5,0),(1,1),(5,1),(6,1),(7,1),(14,1),(15,1),(18,1),(19,1),(2,2),(3,2),(4,2),(8,2),(9,2),(10,2),(11,2),(12,2),(14,2),(16,2),(18,2),(20,2),(21,2),(4,3),(8,3),(12,3),(13,3),(16,3),(18,3),(0,4),(1,4),(3,4),(4,4),(9,4),(17,4),(18,4),(1,5),(2,5),(4,5),(5,5),(6,5),(9,5),(12,5),(15,5),(16,5),(17,5),(1,6),(7,6),(10,6),(13,6),(15,6),(17,6),(1,7),(6,7),(9,7),(14,7),(13,7),(17,7),(2,8),(7,8),(10,8),(18,8),(2,9),(3,9),(6,9),(9,9),(15,9),(16,9),(17,9),(18,9),(19,9),(1,10),(2,10),(6,10),(10,10,),(12,10),(13,10),(15,10),(20,10),(2,11),(6,11),(7,11),(9,11),(11,11),(13,11),(14,11),(20,11),(2,12),(5,12),(6,12),(8,12),(12,12),(15,12),(20,12),(0,13),(3,13),(5,13),(7,13),(11,13),(15,13),(19,13),(1,14),(2,14),(3,14),(9,14),(10,14),(16,14),(19,14),(2,15),(6,15),(7,15),(10,15),(11,15),(16,15),(17,15),(18,15),(2,16),(4,16),(5,16),(6,16),(16,16)])
#the_bend: HexagonalMap(7,10,1[(4,0),(3,1),(4,1),(2,2),(5,2),(2,3),(7,3),(8,3),(9,3),(1,4),(5,4),(6,4),(2,5),(5,5),(2,6),(3,6),(4,6)],(6,3))
#big_river: HexagonalMap(9,13,0,[(0,1),(9,1),(10,1),(1,2),(5,2),(6,2),(9,2),(11,2),(1,3),(4,3),(7,3),(8,3),(11,3),(2,4),(4,4),(7,4),(9,4),(11,4),(1,5),(3,5),(4,5),(6,5),(10,5),(2,6),(3,6),(5,6),(7,6),(5,7),(6,7)])
#7isles: 7 isles hex_map = HexagonalMap(9,13,0,[(2,0),(10,0),(2,1),(3,1),(8,1),(9,1),(4,2),(5,2),(6,2),(7,2),(8,2),(3,3),(8,3),(0,4),(1,4),(2,4),(3,4),(4,4),(8,4),(9,4),(10,4),(11,4),(12,4),(3,5),(8,5),(4,6),(5,6),(6,6),(7,6),(8,6),(2,7),(3,7),(8,7),(9,7),(2,8),(8,8)])


upload_number = 300
for i in range(42,48):
    if i < 6:
        #base
        hex_map = HexagonalMap(9,13,0,[(1,1),(2,1),(5,1),(6,1),(9,1),(10,1),(0,2),(1,2),(3,2),(5,2),(7,2),(9,2),(11,2),(12,2),(3,3),(4,3),(7,3),(9,3),(8,4),(9,4),(2,5),(3,5),(6,5),(7,5),(8,5),(0,6),(1,6),(2,6),(4,6),(6,6),(8,6),(3,7),(4,7),(5,7),(8,7),(9,8)],(5,4))
    elif i < 12:
        #fjords
        hex_map = HexagonalMap(9,13,0,[(2,0),(2,1),(6,1),(7,1),(8,1),(9,1),(10,1),(3,2),(4,2),(6,2),(11,2),(0,3),(1,3),(2,3),(4,3),(5,3),(11,3),(12,3),(3,4),(6,4),(11,4),(2,5),(6,5),(10,5),(2,6),(7,6),(10,6),(1,7),(7,7),(8,7),(9,7),(1,8),(2,8),(7,8)],(4,3))
    elif i < 18:
        #fi
        hex_map = HexagonalMap(9,13,1,[(1,0),(5,0),(2,1),(6,1),(7,1),(8,1),(2,2),(3,2),(4,2),(8,2),(9,2),(10,2),(11,2),(12,2),(5,3),(9,3),(0,4),(1,4),(3,4),(4,4),(9,4),(2,5),(3,5),(5,5),(6,5),(7,5),(10,5),(1,6),(7,6),(10,6),(2,7),(7,7),(10,7),(2,8),(7,8),(10,8)],(7,5))
    elif i < 24:
        #lakes
        hex_map = HexagonalMap(9,13,1,[(8,0),(9,0),(3,1),(4,1),(7,1),(10,1),(1,2),(2,2),(6,2),(10,2),(3,3),(7,3),(8,3),(10,3),(2,4),(5,4),(6,4),(8,4),(1,5),(4,5),(6,5),(8,5),(1,6),(2,6),(3,6),(9,6),(10,6),(3,7),(7,7),(8,7),(11,7),(2,8),(4,8),(5,8),(6,8)],(5,3))
    elif i < 30:
        #arrow
        hex_map = HexagonalMap(9,13,0,[(3,1),(4,1),(5,1),(6,1),(7,1),(8,1),(2,2),(3,2),(9,2),(10,2),(2,3),(6,3),(9,3),(3,4),(5,4),(6,4),(7,4),(9,4),(10,4),(11,4),(12,4),(1,5),(2,5),(6,5),(10,5),(2,6),(3,6),(4,6),(9,6),(10,6),(3,7),(4,7),(5,7),(6,7),(7,7),(8,7)],(5,4))
    elif i < 36:
        #archipelago
        hex_map = HexagonalMap(9,13,0,[(6,0),(10,0),(6,1),(7,1),(9,1),(6,2),(8,2),(9,2),(10,2),(11,2),(0,3),(4,3),(5,3),(3,3),(8,3),(11,3),(1,4),(3,4),(5,4),(6,4),(9,4),(1,5),(2,5),(5,5),(6,5),(7,5),(8,5),(11,5),(6,6),(9,6),(10,6),(11,6),(6,7),(8,7),(6,8),(9,8)],(4,5))
    elif i < 42:
        #onion
        hex_map = HexagonalMap(9,13,1,[(0,0),(3,0),(11,0),(0,1),(3,1),(6,1),(7,1),(8,1),(9,1),(12,1),(2,2),(5,2),(9,2),(2,3),(5,3),(10,3),(1,4),(4,4),(7,4),(10,4),(2,5),(5,5),(10,5),(2,6),(5,6),(9,6),(0,7),(3,7),(6,7),(7,7),(8,7),(9,7),(12,7),(0,8),(3,8),(11,8)],(6,4))
    elif i < 48:
        #7isles
        hex_map = HexagonalMap(9,13,0,[(6,0),(10,0),(5,1),(10,1),(0,2),(1,2),(2,2),(3,2),(4,2),(5,2),(10,2),(5,3),(6,3),(7,3),(8,3),(9,3),(5,4),(8,4),(0,5),(1,5),(2,5),(4,5),(8,5),(9,5),(10,5),(11,5),(3,6),(4,6),(8,6),(3,7),(4,7),(8,7),(5,8),(6,8),(7,8),(8,8)])
    elif i < 54:
        #heart
        hex_map = HexagonalMap(9,13,0,[(3,0),(4,0),(5,0),(7,0),(8,0),(9,0),(2,1),(5,1),(6,1),(9,1),(2,2),(6,2),(10,2),(1,3),(10,3),(2,4),(10,4),(2,5),(3,5),(8,5),(9,5),(1,6),(4,6),(5,6),(7,6),(8,6),(11,6),(2,7),(5,7),(6,7),(0,8),(2,8),(3,8),(6,8),(10,8),(12,8)],(6,4))
    elif i < 60:
        #peninsulas
        hex_map = HexagonalMap(9,13,0,[(3,0),(7,0),(10,0),(3,1),(4,1),(5,1),(6,1),(7,1),(9,1),(2,2),(3,2),(6,2),(8,2),(9,2),(10,2),(1,3),(4,3),(5,3),(10,3),(3,4),(4,4),(6,4),(11,4),(2,5),(7,5),(8,5),(11,5),(6,6),(7,6),(9,6),(11,6),(5,7),(4,7),(9,7),(10,7),(8,7)],(4,5))
    elif i < 66:
        #twisty-land
        hex_map = HexagonalMap(9,13,0,[(5,0),(5,1),(6,1),(7,1),(8,1),(9,1),(1,2),(2,2),(3,2),(6,2),(10,2),(0,3),(3,3),(6,3),(9,3),(0,4),(4,4),(5,4),(6,4),(9,4),(3,5),(5,5),(9,5),(8,5),(3,6),(6,6),(8,6),(10,6),(2,7),(4,7),(6,7),(7,7),(10,7),(11,7),(2,8)])
    elif i < 72:
        #ai1
        hex_map = HexagonalMap(9,13,0,[(3,0),(8,0),(3,1),(7,1),(10,1),(1,2),(2,2),(3,2),(7,2),(8,2),(9,2),(11,2),(0,3),(4,3),(6,3),(9,3),(10,3),(1,4),(4,4),(5,4),(11,4),(1,5),(4,5),(8,5),(9,5),(10,5),(2,6),(3,6),(4,6),(8,6),(4,7),(5,7),(6,7),(7,7),(11,7),(12,8)],(7,4))
    elif i < 78:
        #ai2
        hex_map = HexagonalMap(9,13,0,[(2,0),(9,0),(10,0),(1,1),(2,1),(3,1),(4,1),(1,2),(5,2),(6,2),(9,2),(10,2),(0,3),(1,3),(3,3),(4,3),(6,3),(7,3),(9,3),(10,3),(2,4),(5,4),(7,4),(8,4),(9,4),(0,5),(3,5),(4,5),(6,5),(11,5),(1,6),(4,6),(7,6),(10,7),(9,8),(10,8)],(8,5))
    elif i < 83:
        #bend
        hex_map = HexagonalMap(7,10,1,[(4,0),(3,1),(4,1),(2,2),(5,2),(2,3),(7,3),(8,3),(9,3),(1,4),(5,4),(6,4),(2,5),(5,5),(2,6),(3,6),(4,6)],(6,3))
    elif i < 88:
        #big-river
        hex_map = HexagonalMap(9,13,0,[(0,1),(9,1),(10,1),(1,2),(5,2),(6,2),(9,2),(11,2),(1,3),(4,3),(7,3),(8,3),(11,3),(2,4),(4,4),(7,4),(9,4),(11,4),(1,5),(3,5),(4,5),(6,5),(10,5),(2,6),(3,6),(5,6),(7,6),(5,7),(6,7)])
    elif i < 92:
        #pirates-bay
        hex_map = HexagonalMap(9,13,0,[(i,0) for i in range(1,12)]+[(2,1),(3,1),(4,1),(8,1),(1,2),(3,2),(9,2),(10,2),(11,2),(1,3),(2,3),(0,3),(6,3),(11,3),(0,4),(1,4),(2,4),(3,4),(8,4),(11,4),(12,4),(1,5),(2,5),(0,5),(6,5),(11,5),(1,6),(3,6),(9,6),(10,6),(11,6),(2,7),(3,7),(4,7),(8,7)]+[(i,8) for i in range(1,12)],(4,7))
    elif i < 96:
        #swamp
        hex_map = HexagonalMap(9,11,0,[(0,0),(1,0),(10,0),(0,1),(0,2),(1,3),(8,3),(5,4),(10,4),(1,5),(8,5),(0,6),(0,7),(0,8),(1,8)]+[(i,2) for i in range(2,10)]+[(i,6) for i in range(2,10)],(5,4))
    elif i < 100:
        #central-island
        hex_map = HexagonalMap(9,12,1,[(10,0),(11,1),(1,2),(9,2),(1,3),(10,3),(1,4),(4,4),(6,4),(9,4),(1,5),(10,5),(1,6),(9,6)]+[(i,1) for i in range(1,10)]+[(i,7) for i in range(1,11)],(5,4))
    #hex_map = HexagonalMap(17,22,0,[(1,0),(5,0),(1,1),(5,1),(6,1),(7,1),(14,1),(15,1),(18,1),(19,1),(2,2),(3,2),(4,2),(8,2),(9,2),(10,2),(11,2),(12,2),(14,2),(16,2),(18,2),(20,2),(21,2),(4,3),(8,3),(12,3),(13,3),(16,3),(18,3),(0,4),(1,4),(3,4),(4,4),(9,4),(17,4),(18,4),(1,5),(2,5),(4,5),(5,5),(6,5),(9,5),(12,5),(15,5),(16,5),(17,5),(1,6),(7,6),(10,6),(13,6),(15,6),(17,6),(1,7),(6,7),(9,7),(14,7),(13,7),(17,7),(2,8),(7,8),(10,8),(18,8),(2,9),(3,9),(6,9),(9,9),(15,9),(16,9),(17,9),(18,9),(19,9),(1,10),(2,10),(6,10),(10,10,),(12,10),(13,10),(15,10),(20,10),(2,11),(6,11),(7,11),(9,11),(11,11),(13,11),(14,11),(20,11),(2,12),(5,12),(6,12),(8,12),(12,12),(15,12),(20,12),(0,13),(3,13),(5,13),(7,13),(11,13),(15,13),(19,13),(1,14),(2,14),(3,14),(9,14),(10,14),(16,14),(19,14),(2,15),(6,15),(7,15),(10,15),(11,15),(16,15),(17,15),(18,15),(2,16),(4,16),(5,16),(6,16),(16,16)])
    
    #hex_map.river_access_map()
    
    #2 fill the map with colors
    filename = "lucktracker"+str(i+upload_number)+".txt"
    while True:
        try:
            content = hex_map.create_map()
            #hex_map.display_map()
            if not hex_map.number_test():
                print('number test failed')
                hex_map = hex_map.reset()
            elif not hex_map.river_access_test():
                print('number test passed')
                print('river access test failed')
                hex_map = hex_map.reset()
            elif not hex_map.luck_test():
                print('number test passed')
                print('river access test passed')
                print('luck test failed')
                hex_map = hex_map.reset()
            else:
                print('number test passed')
                print('river access test passed')
                print('luck test passed')
                break
        except Exception as e:
            print(e)
            print('retry')
            hex_map = hex_map.reset()
            pass
    
        
    print(content)
    
    with open(filename,'w') as file:
        file.write(content)
    
    #hex_map.display_map()

    #3 print the finished map as a string suitable for BGA format map-files
    filename = "map"+str(i+upload_number)+".txt"
    content = hex_map.bga_format()
    
    with open(filename,'w') as file:
        file.write(content)
    #print('\n')
    
    #4 print a colored preview of the map
    plot_map()
