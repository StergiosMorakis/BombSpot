import os
import math
import random
import shutil

class BombSpot():

    def __init__(self, width: int, height: int):
        self.height = height
        self.width = width
        # set random player position
        self.pos_x = random.randint(1, self.width)
        self.pos_y = random.randint(1, self.height)
        # visited positions
        # bottom-left: pos 0
        # top-right: pos width*height-1
        self.tabu_list = []
        self.tabu_list.append(self.width*(self.pos_y)+self.pos_x)
        # set random bomb position
        while True:
            self.bomb_x = random.randint(1, self.width)
            self.bomb_y = random.randint(1, self.height)
            if self.pos_x!=self.bomb_x or self.pos_y!=self.bomb_y:
                break
        # set timer
        self.curr_round = 0
        self.round_limit = self.calc_worst_case_rounds()

    def start(self):
        input('Earlier this morning, we received a call about a planted bomb in this building.\nYour mission is to defuse it within {} round{}.\nWe depend on you!'.format(self.round_limit, 's' if self.round_limit>1 else ''))
        while(not self.bomb_spotted()):
            self.curr_round+=1
            if self.curr_round>self.round_limit:
                break
            self.print_all()
            self.make_move()
        self.end_game(self.bomb_spotted())

    def make_move(self):
        '''
            Gets input for new position
        '''
        make_move_dict = {
            'pos_y': {'text': '> Move to floor No.:\n', 'limit': 'height'},
            'pos_x': {'text': '> Move to room No.:\n', 'limit': 'width'},
        }
        for key, val in make_move_dict.items():
            if getattr(self, val['limit'])==1:
                continue
            while True:
                try:
                    entry = int(input(val['text']))
                    if 0<entry<=getattr(self, val['limit']):
                        setattr(self, key, entry)
                        break
                    else:
                        print('Error - Input not in range 1, {}{}'.format( \
                            '' if getattr(self, val['limit'])==2 \
                                else '2, ' if getattr(self, val['limit'])==3 \
                                else '2, 3, ' if getattr(self, val['limit'])==4 \
                                else '..., ', \
                            getattr(self, val['limit'])))
                except ValueError:
                    print('Error - Non-numerical value')
        if not self.bomb_spotted():
            # Add to tabu list
            self.tabu_list.append(self.width*(self.pos_y)+self.pos_x)

    def bomb_spotted(self):
        '''
            Returns: True if player position is equal to bomb position
        '''
        return self.pos_x==self.bomb_x and self.pos_y==self.bomb_y

    def calc_worst_case_rounds(self):
        '''
            Binary Search: O(logn)
            Returns: highest log of distance between player position and edge closest to bomb position
        '''
        availabe_w = self.width-self.pos_x+1 if self.pos_x < self.bomb_x else self.pos_x if self.pos_x > self.bomb_x else 0
        availabe_h = self.width-self.pos_y+1 if self.pos_y < self.bomb_y else self.pos_y if self.pos_y > self.bomb_y else 0
        ttl_rounds = math.ceil(math.log2(max(availabe_w, availabe_h)))
        return ttl_rounds

    def get_building(self):
        # rooftop
        output=self.get_rooftop()
        # building blocks
        for floor in range(self.height):
            output.extend(self.get_floor(floor))
        # ground floor
        output += self.get_ground_floor()
        return output

    def get_rooftop(self):
        '''
            Returns: list of 3 string lines for rooftop
        '''
        return [self.width*('   /.\\   ')
            , self.width*('_'+2*'_||'+'__')
            , '||'+'x'*(self.width*9)+'||'
        ]

    def get_floor(self, floor: int):
        '''
            Returns: list of 4 string lines representing a floor
        '''
        window_symbols = {'current': '*', 'visited': ' ', 'not_visited': '?'}
        get_window_symbol = lambda y, x: window_symbols['current'] if self.height-y==self.pos_y and x+1==self.pos_x else \
                                         window_symbols['visited'] if self.width*(self.height-y)+x+1 in self.tabu_list else \
                                         window_symbols['not_visited']
        # window line w/ chars
        window_str=''.join(['xx| {} |xx'.format(get_window_symbol(floor, room)) for room in range(self.width)])
        return ['||'+self.width*'xx// \\\\xx'+'||'
            , len('    Floor No.{}'.format(self.height-floor))*' '+'||'+window_str+'||    Floor No.{}'.format(self.height-floor)
            , '||'+self.width*'xx\\\\ //xx'+'||'
            , '||'+'x'*(self.width*9)+'||'
        ]

    def get_ground_floor(self):
        '''
            Returns: list of 4 string lines for ground floor
        '''
        door=['///\\\\\\', '|    |', '|   o|', '|    |']
        return ['||'+door[i].rjust(self.width*7,'x')+self.width*2*'x'+'||' for i in range(4)]

    def print_all(self):
        '''
            Display necessary information per round
        '''
        # print round number
        print('Round {}\n'.format(self.curr_round).center(shutil.get_terminal_size().columns))
        # print building blocks
        for line in self.get_building():
            print(line.center(shutil.get_terminal_size().columns), end="")
        # print current location Floor-Room
        print('\nCurrent location: Room \"{0}-{1}\"\nThis room looks empty...'.format(self.pos_y, self.pos_x).center(shutil.get_terminal_size().columns))
        # print indication towards bomb position
        indication_on_y, indication_on_x = self.get_bomb_indication()
        print('\nIndicator reacts intensively towards{}{}\n'.format(indication_on_y, indication_on_x).center(shutil.get_terminal_size().columns))

    def get_bomb_indication(self):
        '''
            Returns: tuple w/ indication strings towards bomb on both axes
        '''
        return (
            ' Up' if self.pos_y < self.bomb_y else ' Down' if self.pos_y > self.bomb_y else '',
            ' Right' if self.pos_x < self.bomb_x else ' Left' if self.pos_x > self.bomb_x else '',
        )

    def end_game(self, win: bool):
        '''
            Ending scene
        '''
        os.system('cls')
        input('Bomb spotted and defused!' if win else 'The bomb has exploded!')
        input('You have saved many lives today.\nGood job!' if win  else 'Many lives were lost today.\nAnd it was all your fault!')

def get_dimensions_input():
    '''
        Get input from user for board dimensions
    '''
    dimensions_dict = {
        'height': {'text': '> Insert number of floors:\n', 'range': (0,50)},
        'width': {'text': '> Insert number of rooms per floor:\n', 'range': (1,150)},
    }
    for key, val in dimensions_dict.items():
        while True:
            try:
                size = int(input(val['text']))
                if val['range'][0]<size<val['range'][1]:
                    dimensions_dict[key]['length']=size
                    break
                else:
                    print('Error - Input not in range {}, {}, ..., {}'.format(val['range'][0], val['range'][0]+1, val['range'][1]))
            except ValueError:
                print('Error - Non-numerical value')
    return (dimensions_dict['width']['length'], dimensions_dict['height']['length'])

if __name__ =='__main__':
    os.system('cls')
    width_input, height_input = get_dimensions_input()
    BombSpot(width_input, height_input).start()
    while True:
        ans = input('Play again? (Y / N)\n').lower()
        if ans=='y':
            BombSpot(width_input, height_input).start()
        elif ans=='n':
            confirm = input('Are you sure? (Y / N)\n').lower() 
            if confirm=='y':
                os.system('cls')
                quit()
            else:
                print('You don\'t make any sense!')
        else:
            print('Error - Invalid input')