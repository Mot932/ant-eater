import os
import keyboard
import random

# Константы для размеров поля и символов
COLS = 25
ROWS = 10
EMPTY = '☐'
PLAYER = 'P'
ANT = 'a'
ANTHILL = 'A'
UP = 'up'
DOWN = 'down'
RIGHT = 'right'
LEFT = 'left'
ANTHILL_MAX = 4
ANTHILL_MIN = 1
ANTS_PER_ANTHILL_MAX = 10
ANTS_PER_ANTHILL_MIN = 1
MAX_SPAWN_COUNTER = 5

class GameObject:
    """
    Базовый класс для игровых объектов с общими функциональностями.
    """
    def _init_(self, y, x, image):
        """
        Инициализация игрового объекта с заданными координатами и изображением.
        """
        self.y = y
        self.x = x
        self.image = image


    def move(self, direction, field):
        """
        Перемещение игрового объекта в указанном направлении на поле.
        """
        new_y, new_x = self.y, self.x

        if direction == UP and self.y > 0 and not isinstance(field.cells[self.y - 1][self.x].content, Anthill):
            new_y -= 1
        elif direction == DOWN and self.y < field.rows - 1 and not isinstance(field.cells[self.y + 1][self.x].content, Anthill):
            new_y += 1
        elif direction == LEFT and self.x > 0 and not isinstance(field.cells[self.y][self.x - 1].content, Anthill):
            new_x -= 1
        elif direction == RIGHT and self.x < field.cols - 1 and not isinstance(field.cells[self.y][self.x + 1].content, Anthill):
            new_x += 1


    def place(self, field):
        """
        Размещение объекта на поле.
        """
        if field.cells[self.y][self.x].content is None:
            field.cells[self.y][self.x].content = self
        else:
            empty_cells = [
                (i, j)
                for i in range(field.rows)
                for j in range(field.cols)
                if field.cells[i][j].content is None
            ]
            if empty_cells:
                new_y, new_x = random.choice(empty_cells)
                field.cells[new_y][new_x].content = self
                self.y, self.x = new_y, new_x
            else:
                print(f'Нету клеток для размещения {self.image}!')


    def draw(self, field):
        """
        Отрисовка объекта на поле.
        """
        field.cells[self.y][self.x].content = self


class Cell:
    """
    Класс для представления ячейки на поле.
    """
    def _init_(self, Y=None, X=None):
        """
        Инициализация ячейки с заданными координатами.
        """
        self.image = EMPTY
        self.Y = Y
        self.X = X
        self.content = None

    def draw(self):
        """
        Отрисовка содержимого ячейки.
        """
        if self.content:
            print(self.content.image, end=' ')
        else:
            print(self.image, end=' ')



class Player(GameObject):
    """
    Класс для представления игрока на поле.
    """
    def _init_(self, y=None, x=None):
        """
        Инициализация игрока с заданными координатами.
        """
        super()._init_(y, x, PLAYER)

    def move(self, direction, field):
        """
        Перемещение игрока в указанном направлении на поле.
        """
        super().move(direction, field)

class Ant(GameObject):
    """
    Класс для представления муравья на поле.
    """
    def _init_(self, y, x):
        """
        Инициализация муравья с заданными координатами.
        """
        super()._init_(y, x, ANT)


class Anthill(GameObject):
    """
    Класс для представления муравейника на поле.
    """
    def _init_(self, x, y, quantity):
        """
        Инициализация муравейника с заданными координатами и количеством муравьев.
        """
        super()._init_(y, x, ANTHILL)
        self.quantity = quantity
        self.spawn_counter = 0
        self.ants_counter = random.randint(
            ANTS_PER_ANTHILL_MIN,
            ANTS_PER_ANTHILL_MAX
        )


    def place(self, field):
        """
        Размещение муравейника на поле.
        """
        super().place(field)

    def draw(self, field):
        """
        Отрисовка муравейника на поле.
        """
        super().draw(field)


class Field:
    """
    Класс для представления игрового поля.
    """
    def _init_(self, cell=Cell, player=Player, anthill=Anthill):
        """
        Инициализация игрового поля с заданными классами объектов.
        """
        self.game_over = False
        self.rows = ROWS
        self.cols = COLS
        self.eaten_ants = 0
        self.escaped_ants = 0
        self.total_ants = 0
        self.anthills = []
        self.ants = []
        self.cells = [
            [cell(Y=y, X=x) for x in range(COLS)] 
            for y in range(ROWS)
        ]
        self.player = player(
            y=random.randint(0, ROWS - 1),
            x=random.randint(0, COLS - 1)
        )
        self.player.place_object(self)
        self.player.draw(self)


    def drawrows(self):
        """
        Отрисовка строк поля.
        """
        for row in self.cells:
            for cell in row:
                cell.draw()
            print()

    def add_anthill(self, anthill):
        """
        Добавление муравейника на поле.
        """
        self.anthills.append(anthill)
        anthill.place(self)

    def get_neighbours(self, y, x):
        """
        Получение координат соседних ячеек.
        """
        neighbours_coords = []
        for row in (-1, 0, 1):
            for col in (-1, 0, 1):
                if row == 0 and col == 0:
                    continue
                neighbours_coords.append((y + row, x + col))
        return neighbours_coords

    def add_anthills(self):
        """
        Добавление случайного количества муравейников на поле.
        """
        available_cells = [
            (x, y)
            for x in range(self.cols)
            for y in range(self.rows)
            if (x, y) != (self.player.x, self.player.y)
        ]

        quantity = random.randint(ANTHILL_MIN, ANTHILL_MAX)

        for i in range(quantity):
            if not available_cells:
                break
            anthill_x, anthill_y = random.choice(available_cells)
            available_cells.remove((anthill_x, anthill_y))
            anthill = Anthill(
                x=anthill_x,
                y=anthill_y,
                quantity=random.randint(ANTHILL_MIN, ANTHILL_MAX)
            )
            self.add_anthill(anthill)

        anthill.place(self)

    def spawn_ants(self):
        """
        Создание новых муравьев в муравейниках.
        """
        for anthill in self.anthills:
            if anthill.ants_counter > 0 and anthill.spawn_counter == 0:
                anthill_x, anthill_y = anthill.x, anthill.y
                neighbors = [
                    (anthill_y - 1, anthill_x - 1),
                    (anthill_y - 1, anthill_x),
                    (anthill_y - 1, anthill_x + 1),
                    (anthill_y, anthill_x - 1),
                    (anthill_y, anthill_x + 1),
                    (anthill_y + 1, anthill_x - 1),
                    (anthill_y + 1, anthill_x),
                    (anthill_y + 1, anthill_x + 1),
                ]
                empty_neighbors = [
                    (y, x)
                    for y, x in neighbors
                    if 0 <= y < self.rows and 0 <= x < self.cols
                    and not self.cells[y][x].content
                ]
                if empty_neighbors:
                    ant_y, ant_x = random.choice(empty_neighbors)
                    ant = Ant(y=ant_y, x=ant_x)
                    self.cells[ant_y][ant_x].content = ant
                    anthill.ants_counter -= 1
                    anthill.spawn_counter = 1
                    self.ants.append(ant)

            if anthill.spawn_counter > 0:
                anthill.spawn_counter += 1
                if anthill.spawn_counter > 4:
                    anthill.spawn_counter = 0

        self.move_ants()

    def move_ants(self):
        """
        Перемещение муравьев по полю.
        """
        for ant in self.ants:
            neighbours_coords = self.get_neighbours(ant.y, ant.x)
            random.shuffle(neighbours_coords)
            for y, x in neighbours_coords:
                if y < 0 or y > self.rows - 1 or x < 0 or x > self.cols - 1:
                    if ant in self.ants:
                        self.ants.remove(ant)
                        self.cells[ant.y][ant.x].content = None
                        self.escaped_ants += 1
                    break

                new_cell = self.cells[y][x]
                if new_cell.content:
                    if isinstance(new_cell.content, Player):
                        self.eaten_ants += 1
                        self.ants.remove(ant)
                        self.cells[ant.y][ant.x].content = None
                    continue
                self.cells[ant.y][ant.x].content = None
                new_cell.content = ant
                ant.y = y
                ant.x = x
                break

        ants_in_anthill = sum(anthill.ants_counter for anthill in self.anthills)

        ants_on_field = any(
            cell.content and isinstance(cell.content, Ant)
            for row in self.cells for cell in row
        )

        if ants_in_anthill == 0 and not ants_on_field:
            self.game_over = True

    def update_statistics(self):
        """
        Обновление статистики и вывод результатов игры.
        """
        self.total_ants = self.eaten_ants + self.escaped_ants
        print('Статистика:')
        print(f'Все муравьи: {self.total_ants}')
        print(f"Съеденно муравьёв: {self.eaten_ants}")
        print(f'Сбежало муравьёв: {self.escaped_ants}')
        input('Нажмите ENTER, чтобы закончить игру')


def clear_screen():
    """
    Очистка экрана консоли.
    """
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


class Game:
    """
    Класс для управления игровым процессом.
    """
    def _init_(self):
        """
        Инициализация игры.
        """
        self.field = Field()
        self.field.add_anthills()

    def handle_keyboard_event(self, event):
        """
        Обработка событий клавиатуры.
        """
        if event.event_type == keyboard.KEY_DOWN:
            if event.name == UP:
                self.field.player.move(UP, self.field)
            elif event.name == DOWN:
                self.field.player.move(DOWN, self.field)
            elif event.name == LEFT:
                self.field.player.move(LEFT, self.field)
            elif event.name == RIGHT:
                self.field.player.move(RIGHT, self.field)
            elif event.name == 'esc':
                print("Выход из игры.")
                return True
        return False

    def update_game_state(self):
        """
        Обновление состояния игры.
        """
        clear_screen()
        self.field.drawrows()
        self.field.spawn_ants()        

        if self.field.game_over:
            print('Все муравьи были съедены или сбежали. Игра окончена!')

    def run(self):
        """
        Запуск игрового цикла.
        """
        self.field.drawrows()

        while not self.field.game_over:
            event = keyboard.read_event(suppress=True)
            if self.handle_keyboard_event(event):
                break

            self.update_game_state()

        self.field.update_statistics()

        
game_instance = Game()
game_instance.run()
