from random import randint

#собственные классы исключений
#общий класс, кот.б. содержать остальные классы исключений
class BoardException(Exception):
    pass
# два класса пользовательских исключений
class BoardOutException(BoardException):
    def __str__(self):
        return 'вы пытаетесь выстрелить за доску'

class BoardUsedException(BoardException):
    def __str__(self):
        return 'вы уже стреляли в эту клетку'

#собственное исключение(не показываем пользователю), для того,
# чтобы нормально размещать корабли:
class BoardWrongShipException(BoardException):
    pass

# собственный тип данных "точка"
class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self): #отвечает за вывод точек в консоль
        return f'Dot({self.x}, {self.y})'
#нужно будет проверять, есть ли точка в списке

#класс корабля
class Ship:
    def __init__(self, bow, l, o): # bow - нос, о - ориентация корабля 0-вертикальный, 1 - горизонтальный
        self.bow = bow
        self.l = l
        self.o = o
        self.lives = l

    @property
    def dots(self):
        ship_dots = []
        for i in range(self.l): #берем нос корабля и начинаем шагать от него на i клеток
            cur_x = self.bow.x #текущие точки, нос корабля
            cur_y = self.bow.y

            if self.o == 0:
                cur_x += i

            elif self.o == 1:
                cur_y += i

            ship_dots.append(Dot(cur_x, cur_y))

        return ship_dots

    #метод, показывающий, попали ли мы в корабль
    #метод eq позваляет нам делать проверку на попадание таким вот образом:
    def shooten(self, shot):
        return shot in self.dots

# класс игровое поле, hid - нужно ли поле скрывать
class Board:
    def __init__(self, hid=False, size=6):
        self.size = size
        self.hid = hid

        #кол-во пораженный кораблей:
        self.count = 0

        #атрибут, содержащий сетку, в которой мы будем хранить состояние
        #изначально клетка ничем не занята(о) и не было выстрела
        self.field = [['o'] * size for _ in range(size)]

        #храним занятые точки/в которые выстрелили:
        self.busy = []
        self.ships = []

    # метод для размещения корабля:
    def add_ship(self, ship):
        for d in ship.dots:
         # проверяет, что каждая точка корабля не выходит за границы и что точка не занята
            if self.out(d) or d in self.busy:
        # если это не так, то мы выбрасываем исключение
                raise BoardWrongShipException
            # проходимся по точкам корабля и ставим в каждую точку квадратик
        for d in ship.dots:
            self.field[d.x][d.y] = "▪"
                # записываем точку в список занятых(в списке точки корабля и соседствующие)
            self.busy.append(d)

            # добавляем список собственных кораблей и обводим его по контуру
        self.ships.append(ship)
        self.contour(ship)

        # добавление корабля на доску
        # два метода: contour

    def contour(self, ship, verb=False):
        # все точки вокруг той, в которой мы находимсяю 0.0 - сама точкаю 0 -1 - выше исходной, 0,1 - ниже исходной
        near = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 0), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        # берем каждую точку корабля, сдвигаем исходную точку на dx dy
        # в двойном цикле пройдем все точки соседствующие с кораблем, чтобы знать, в какие клетки нельзя ставить корабли
        for d in ship.dots:
            for dx, dy in near:
                cur = Dot(d.x + dx, d.y + dy)
# если точка не выходит за границы и если не занята, то мы добавляем ее в список busy и ставим на этом месте точку, чтобы показать, что она занята
# параметр, кот. нам говорит, нужно ли ставить точки вокруг кораблей (нужно ставить во время игры, а когда мы
# расставляем, достаточно внести точки в список busy, а ставить не надо, т.к. будет виден контур корабля
                if not (self.out(cur)) and cur not in self.busy:
                    if verb:
                        self.field[cur.x][cur.y] = "."
                    self.busy.append(cur)

        #вывод корабля на доску:
        #в переменной res записываем всю доску
    def __str__(self):
        res = ""
        res += "  |  1 | 2 | 3 | 4 | 5 | 6 |"
        #в цикле рпоходим по строкам доски, с помошью enumerate берем индекс строки
        for i, row in enumerate(self.field):
            #сначала выводим номер строки, а потом через палочку клетки строки
            res += f'\n{i + 1} |  ' + ' | '.join(row) + ' |'

        if self.hid:
            res = res.replace('▪', 'o')
        return res

    #проверяем, находится ли точка за пределами доски/ отрицание условия - проверка на то, что точка выходит за пределы
    def out(self, d):
        return not ((0 <= d.x < self.size) and (0 <= d.y < self.size))

#для выстрела проверяем, выходит ли точка за границу
    def shot(self, d):
        if self.out(d):
            raise BoardOutException()
        #занята ли точка
        if d in self.busy:
            raise BoardUsedException()
        #объявляем, что точка занята, если она еще не была занята
        self.busy.append(d)

#проходимся в цикле по кораблям, проверяем, принадлежит ли точка кораблю
        for ship in self.ships:
            if ship.shooten(d):
                #уменьшаем кол-во жизней корабля и ставим в эту точку ч
                ship.lives -= 1
                self.field[d.x][d.y] = 'x'
                #если у корабля кончились жизни, то сначала прибавляем к счетчику уничтоженных кораблей 1
                #потом обводим его по контуру с verb=True, чтобы контур обозначился точками
                if ship.lives == 0:
                    self.count += 1
                    self.contour(ship, verb=True)
                    print('Корабль уничтожен!')
                    return False #дальше ход не нужно делать
                else:
                    print('Корабль ранен')
                    return True

        self.field[d.x][d.y] = '.'
        print("Мимо!")
        return False
#когда будем начинать игру, нужно чтобы список busy обнулился,потому что
#до игры этот список нужен, чтобы хранить соседние с короблями точки, а теперь нужен, чтобы хранить точки, в которые игрок стрелял

    def begin(self):
        self.busy = []

#метод, который будет возвращать (добавили в конце)
    def defeat(self):
        return self.count == len(self.ships)

#описываем класс игрока
#в кач-ве аргумента передаются 2 доски
class Player:
    def __init__(self, board, enemy):
        self.board = board
        self.enemy = enemy

#метод аск не определяем,мы просто говорим, что он должен быть, но при поытке
#его вызвать будет выводить ошибка - сказать, что метод д.б., но д.б. у потомков этого класса
    def ask(self):
        raise NotImplementedError()

#в бесконечном цикле пытаемся сделать выстрел, просим компьюер или пользователя дать координаты выстрела,
#выполняем выстрел, если выстрел попал, то возвращаем, нужно ли повторить ход
#если выстрел выбросил исключение, то мы его печатаем и цикл продолжается
    def move(self):
        while True:
            try:
                target = self.ask()
                repeat = self.enemy.shot(target)
                return repeat
            except BoardOutException as e:
                print(e)

#опишем класс игрока-компьютера

class AI(Player):
    def ask(self):
        #случайно генерируем две точки от 0 до 5 (в начале файла импортируем функцию кandint)
        d = Dot(randint(0,5), randint(0, 5))
        print(f"Ход компьютера: {d.x+1} {d.y+1}")
        return d

class User (Player):
    def ask(self):
        while True:
            cords = input("Ваш ход: ").split()

            if len(cords) != 2:
                print("Введите две координаты")
                continue

            x, y = cords

            if not(x.isdigit()) or not(y.isdigit()):
                print("Введите числа")
                continue

            x, y = int(x), int(y)

            return Dot(x-1, y-1)

#генерируем доски, заполненные кораблями

class Game:

#в конструкторе мы не только задаем размер доски, но и генерируем две случайные доски для компьюера и игрока

    def __init__(self, size=6):
        self.size = size
        pl = self.random_board()
        co = self.random_board()
        # для компьютера скрываем корабли с помощью параметра hid
        co.hid = True

#создаем двух игроков
        self.ai = AI(co, pl)
        self.us = User(pl, co)

    #метод, пытающийся создать доску
    def try_board(self):
        #список длин кораблей
        lens = [3, 2, 2, 1, 1, 1, 1]
        #создаем доску
        board = Board(size=self.size)
        attempts = 0
        #для каждой длины корабля пытаемся в бесконечном цикле его поставить
        for l in lens:
            while True:
  #считаем кол-во попыток поставить корабли,
                attempts += 1
                if attempts > 2000:
                    return None

                ship = Ship(Dot(randint(0, self.size), randint(0, self.size)), l, randint(0, 1))
                try:
                    board.add_ship(ship)
                   #если все хорошо прошло, делаем break и заканчиваем бесконечный цикл
                    break
                except BoardWrongShipException:
                    #если выбросит исключение, то продолжаем итерацию заново(это нужно, чтобы делать попытки поставить корабль)
                    pass
           #как только разместили корабли, возвращаем нашу доску
            board.begin()
            return board

#метод, кот. гарантированно генерирует доску
    def random_board(self):
        #в методе доска изначально пустая и пока она пустая, мы в бесконечном цикле пытаемся ее создать
        board = None
        while board is None:
            board = self.try_board()
        return board
#как только цикл закончился, доска уже не пустая, и мы ее возвращаем

    def greet(self):
        print("-------------------")
        print("  Приветсвуем вас  ")
        print("      в игре       ")
        print("    морской бой    ")
        print("-------------------")
        print(" формат ввода: x y ")
        print(" x - номер строки  ")
        print(" y - номер столбца ")

#создаем игровой цикл
#бесконечный цикл
    def loop(self):
        num = 0 #номер хода
        while True: #сначала выводим доск пользователя и компьютера

            print("-"*20)
            print("Доска пользователя:")
            print(self.us.board)
            print("-"*20)
            print("Доска компьютера:")
            print(self.ai.board)
            print("-" * 20)
            if num % 2 == 0: #действуем в зависимости от номера хода
                print("ходит пользователь")
                repeat = self.us.move() #вызываем соответствующий метод move,отвечающий за ход
            else:
                print("ходит компьютер")
                repeat = self.ai.move()
 #записывваем результат в repeat(то, что возвращает метод move -это то, нужно ли повторить ход

            if repeat:
                num -= 1 #уменьшаем, чтобы переменная осталась такой же (в конце номер хода увеличивается каждый раз, а тут мы его
            # уменьшаем, чтобы ход остался того же игрока

# делаем проверку, что кол-во пораженных кораблей = 7 (или кол-ву кораблей на доске == len(self.ai.board.ships).
            #вместо if self.ai.board.count == 7 вызываем новый метод(выше)
            if self.ai.board.defeat():
                print("-"*20)
                print("пользователь выиграл")
                break
##вместо if self.us.board.count == 7 вызываем новый метод(выше)
            if self.us.board.defeat():
                print("-"*20)
                print("компьютер выиграл")
                break
            num += 1
    #метод, который совмещает все вместе
    def start(self):
        self.greet()
        self.loop()

g = Game()
g.start()
