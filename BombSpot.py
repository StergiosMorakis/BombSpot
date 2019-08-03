import os
import math
import random
import shutil

class BombSpot():

    def __init__(self):
        self.startGame()

    def startGame(self):
        os.system('cls')
        self.visited_rooms = []
        self.y = self.setHeight()
        self.x = self.setWidth()
        self.loc_x = random.randint(1, self.x)
        self.loc_y = random.randint(1, self.y)
        self.visited_rooms.append(self.x * (self.loc_y - 1) + self.loc_x - 1)
        while True:
            self.bomb_x = random.randint(1, self.x)
            self.bomb_y = random.randint(1, self.y)
            if self.loc_x != self.bomb_x or self.loc_y != self.bomb_y:
                break
        self.round = 0
        self.total_rounds = self.setTotalRounds()
        os.system('cls')
        self.introMessage()
        while(not self.foundBomb()):
            os.system('cls')
            self.round += 1
            if self.round > self.total_rounds:
                self.loseMessage()
            self.printBuilding()
            self.getCurrentLocation()
            self.indicateBombLocation()
            self.makeMove()

    def setHeight(self):
        while True:
            try:
                print('\nInsert number of Floors:')
                height = int(input())
                # The Burj Khalifa, located in Dubai, UAE, is the building with the most floors, at 163.
                if height > 0 and height < 164:
                    return height
                else:
                    print('\nValid input consists of characters 1, 2, ..., 164')
            except ValueError:
                print('\nValid input must be numerical')

    def setWidth(self):
        while True:
            try:
                print('\nInsert number of Rooms per floor:')
                width = int(input())
                if width > 1 and width <= 250:
                    return width
                else:
                    print('\nValid input consists of characters 2, 3, ..., 250')
            except ValueError:
                print('\nValid input must be numerical')

    def setTotalRounds(self):
        playable_width = 0
        playable_height = 0
        if self.loc_x < self.bomb_x:
            playable_width = self.x - self.loc_x
        if self.loc_x > self.bomb_x:
            playable_width = self.loc_x
        if self.loc_y < self.bomb_y:
            playable_height = self.x - self.loc_y
        if self.loc_y > self.bomb_y:
            playable_height = self.loc_y
        return math.ceil(math.log2(max(playable_width, playable_height)))

    def foundBomb(self):
        if self.loc_x == self.bomb_x and self.loc_y == self.bomb_y:
            return True
        else:
            return False

    def printBuilding(self):
        output = [' ', ' ', 'Round ' + str(self.round), ' ', ' '] 
        output.extend(self.getRooftop())
        for floor in range(self.y):
            output.extend(self.getRoomsPerFloor(floor))
        output += self.getGroundFloor()
        for line in output:
            print(line.center(shutil.get_terminal_size().columns), end="")

    def getRooftop(self):
        output = []
        output.append(self.x * ('   /.\\   '))
        output.append(self.x * ('_'+ 2 * '_||'+'__'))
        output.append('||' + 'x' * (self.x * 9) + '||')
        return output

    def getRoomsPerFloor(self, floor):
        
        def getRoomSymbol(floor, room):
            if self.y - floor == self.loc_y and room + 1 == self.loc_x:
                return '*'
            elif self.x * (self.y - floor - 1) + room in self.visited_rooms:
                return ' '
            else:
                return '?'

        output = []
        floor_string = ''
        output.append('||' + self.x * 'xx// \\\\xx'  + '||')
        for room in range(self.x):
            floor_string += 'xx| {} |xx'.format(getRoomSymbol(floor, room))
        output.append(len('    Floor No.' + str(self.y - floor)) * ' ' +'||' + floor_string + '||    Floor No.' + str(self.y - floor))
        output.append('||' + self.x * 'xx\\\\ //xx' + '||')
        output.append('||' + 'x' * (self.x * 9) + '||')
        return output

    def getGroundFloor(self):

        def getDoor(line):
            switch = {
                0: '///\\\\\\',
                1: '|    |',
                2: '|   o|',
                3: '|    |',
            }
            return switch.get(line)

        output = []
        for line in range(4):
            output.append('||' + getDoor(line).rjust(self.x * 7, 'x') + self.x * 2 * 'x' + '||')
        return output
    
    def getCurrentLocation(self):
        print('\n')
        print('Current Location: Room \"{0}-{1}\"'.format(self.loc_y, self.loc_x).center(shutil.get_terminal_size().columns))

    def indicateBombLocation(self):
        print('\n')
        print('Indicator reacts intensively towards{0}{1}'.format(self.getBombY(), self.getBombX()).center(shutil.get_terminal_size().columns))

    def getBombX(self):
        if self.loc_x < self.bomb_x:
            return ' Right'
        elif self.loc_x > self.bomb_x:
            return ' Left'
        else:
            return ''

    def getBombY(self):
        if self.loc_y < self.bomb_y:
            return ' Up'
        elif self.loc_y > self.bomb_y:
            return ' Down'
        else:
            return ''

    def makeMove(self):
        self.loc_y = self.setLocY()
        self.loc_x = self.setLocX()
        if not self.foundBomb():
            self.visited_rooms.append(self.x * (self.loc_y - 1) + self.loc_x - 1)
            print('\nRoom \"{0}-{1}\" seems empty..'.format(self.loc_y, self.loc_x))
        else:
            self.winMessage()

    def setLocX(self):
        while True:
            try:
                print('\nMove to Room No.')
                entry = int(input())
                if entry > 0 and entry <= self.x:
                    return entry
                else:
                    print('\nValid input consists of characters 1, 2, ..., {}'.format(self.x))
            except ValueError:
                print('\nValid input must be numerical')

    
    def setLocY(self):
        while True:
            try:
                print('\nMove to Floor No.')
                entry = int(input())
                if entry > 0 and entry <= self.y:
                    return entry
                else:
                    print('\nValid input consists of characters 1, 2, ..., {}'.format(self.y))
            except ValueError:
                print('\nValid input must be numerical')
    
    def introMessage(self):
        print('There is a bomb in this building..')
        input()
        print('We need you to find it..')
        input()
        print('You \'ve got {} rounds to locate it..'.format(str(self.total_rounds)))
        input()
        print('We depend on you, soldier!')
        input()
        print('Do you understand?')
        input()

    def winMessage(self):
        os.system('cls')
        print('The bomb has been defused!')
        input()
        print('You have saved many lives today, soldier..')
        input()
        print('Thank you!')
        input()
        self.playAgain()

    def loseMessage(self):
        os.system('cls')
        print('The bomb has exploded!')
        input()
        print('Many lives have been lost today..')
        input()
        print('All because of you, soldier!')
        input()
        self.playAgain()

        
    def playAgain(self):
        while True:
            print('\nPlay again? (Y / N)')
            answer = input().upper() 
            if answer in ['Y', 'YE', 'YES', 'YEAH']:
                self.startGame()
            elif answer in ['N', 'NO', 'NOPE']:
                print('\nAre you sure? (Y / N)')
                answer = input().upper() 
                if answer in ['Y', 'YE', 'YES', 'YEAH']:
                    os.system('cls')
                    quit()
                elif answer in ['N', 'NO', 'NOPE']:
                    print('\nYou don \'t make any sense, soldier!')
                else:
                    print('\nDidn \'t quite catch that..')
            else:
                print('\nDidn \'t catch that..')

if (__name__ =='__main__'):
    init_game = BombSpot()