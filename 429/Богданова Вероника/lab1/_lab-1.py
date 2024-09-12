from asyncio.windows_events import NULL
from inspect import trace


file = "maze-for-u.txt"

maze = tuple(open(file).read().split('\n'))
maze = maze[:-1]
maze_list= list(maze)
max_x, max_y = len(maze[0]), len(maze)
print("Max y: ", max_y)
print("Max x: ", max_x)

POSSIBLE_WAYS = ('N', 'S', 'W', 'E')

def set_point(coord, sign):
    global maze_list

    maze_row = list(maze_list[coord[1]])
    maze_row[coord[0]] = sign
    maze_list[coord[1]] = ''.join(maze_row)


def get_point(maze, row):
    return [maze[row].find(" "), row]


def is_coord_in_maze(maze, coord):
    if coord[0]<0 or coord[0]>len(maze[0])-1:
        return False
    if coord[1]<0 or coord[1]>len(maze)-1:
        return False
    return True


def is_coord_exit(coord):
    if coord[1]>len(maze)-2:
        return True
    return False


def is_coord_treasure(coord):
    global treasure_is_here
    if coord[1] == treasure_is_here[1] and\
        coord[0] == treasure_is_here[0]:
        return True
    return False


def is_path_clean(maze, coord):
    if maze[coord[1]][coord[0]] == '#':
        return False
    return True


def step(coord, direction):
    if direction == 'N':
         return step_N(coord)
    elif direction == 'S':
         return step_S(coord)
    elif direction == 'E':
         return step_E(coord)
    elif direction == 'W':
         return step_W(coord)


def step_N(coord):
    return [coord[0], coord[1]-1]


def step_E(coord):
    return [coord[0]+1, coord[1]]


def step_S(coord):
    return [coord[0], coord[1]+1]


def step_W(coord):
    return [coord[0]-1, coord[1]]


def cut_way_back(direction):
    """
    Cut the opposite direction in possible ways to prevent stepping back
    """
    if direction == 'N':
        return ('N', 'E', 'W')

    if direction == 'S':
        return ('S', 'E', 'W')

    if direction == 'E':
        return ('N', 'E', 'S')

    if direction == 'W':
        return ('N', 'S', 'W')


def restore_path(coord):
    global maze_list, path_to_exit
    
    for node in path_to_exit:
        set_point(coord, '.')
        coord = step(coord, node)


def find_a_way(maze, coord, possible_ways):
    global path_to_exit, current_path
    
    if not is_coord_in_maze(maze, coord):
        print('Не пройдёшь')
        return

    if is_coord_exit(coord):
        print('Выход')
        return

    if is_coord_treasure(coord):
        print('Новый путь найдёшь')
        path_to_exit = current_path.copy()
        return

    if len(current_path) > len(path_to_exit):
        print('Долгий путь, путник')
        print(f'{len(current_path)} > {len(path_to_exit)}')
        return

    for direction in possible_ways:
        if is_path_clean(maze, step(coord, direction)):
               current_path.append(direction)
               find_a_way(maze, step(coord, direction), cut_way_back(direction))
               current_path.pop()
        
    return 


d = [[-1 for j in range(max_x)] for i in range(max_y)]


def find_the_exit(treasure, end):
    #treasure[0] - column, treasure[1] - row
    #y - row, x - column

    
    queue = []
    queue.append(treasure)

    d[treasure[1]][treasure[0]] = 0

    while queue:
        node = queue.pop(0)

        for i in [[-1, 0],[1, 0],[0, -1],[0, 1]]:
            x = node[0] + i[0]
            y = node[1] + i[1]
            if (x < 0 or x >= max_x or y < 0 or y >= max_y):
                continue
            if (maze[y][x] == " " and d[y][x] == -1):
                d[y][x] = [node[0],node[1]]
                queue.append([x, y]) 

    x = end[0]
    y = end[1]  

    while d[y][x] != 0:
        set_point([x,y], ',')
        temp_x = d[y][x][0]
        temp_y = d[y][x][1]
        x, y = temp_x, temp_y


path_to_exit = []
for i in range(len(maze)*len(maze[0])):
    path_to_exit.append(' ')
current_path = []

start_point = get_point(maze, 0)
end_point = get_point(maze, max_y-1)
print("Начало:", start_point)
print("Конец:",end_point)

treasure_is_here = ()

while(not (treasure_is_here and is_path_clean(maze, treasure_is_here))):
    x = int(input(f'Где же сокровище? (x is between 0 and {max_x-1}) '))
    y = int(input(f'Где же сокровище? (y is between 0 and {max_y-1}) '))
    treasure_is_here = (abs(x) if abs(x) < max_x-1 else max_x-1, abs(y) if abs(y) < max_y-1 else max_y-1)

set_point(treasure_is_here, '*')
print("Сокровище здесь:",treasure_is_here)

find_a_way(maze, start_point, POSSIBLE_WAYS)

restore_path(start_point)

find_the_exit(treasure_is_here, end_point)

f = open('maze-for-me-done.txt', 'w')
for i in range(len(maze_list)):
    f.write(maze_list[i])
    f.write("\n")
f.close()

print("Поздравляю!")