field = [[' ']*3 for i in range(3)]

#вывод на экран поля
def show():
    print(f'  0 1 2')
    for i in range(3):
        print(f'{i} {field[i] [0]} {field[i] [1]} {field[i] [2]}')

# ввод пользоватлеля
def ask():
    while True:
        cords = input("      введите координаты:").split()
        if len(cords) != 2:
            print("введите две координаты")
            continue
        x, y = cords

        if not(x.isdigit()) or not(y.isdigit()):
            print("введите числа")
            continue
        x, y = int(x), int(y)

        if 0 > x or x > 2 or 0 > y or y > 2:
            print("координаты вне диапазона")
            continue

        if field[x] [y] != ' ':
            print("клетка занята")
            continue

        return x, y

def check_win():
    win_cord = (((0, 0), (0, 1), (0, 2)), ((1, 0), (1, 1), (1, 2)), ((2, 0), (2, 1), (2, 2)),
                ((0, 0), (1, 0), (2, 0)), ((0, 1), (1, 1), (2, 1)), ((0, 2), (1, 2), (2, 2)),
                ((0, 0), (1, 1), (2, 2)), ((0, 2), (1, 1), (2, 0)))
    for cord in win_cord:
        symbols = []
        for c in cord:
            symbols.append(field[c[0]][c[1]])
        if symbols == ["X", "X", "X"]:
            print("Выиграл X!!!")
            return True
        if symbols == ["0", "0", "0"]:
            print("Выиграл 0!!!")
            return True
    return False

#номер хода
num = 0
while True:
    num += 1
    show()


    if num%2 ==1:
        print('ходит крестик')
    else:
        print('ходит нолик')

    x, y = ask()

    if num%2 ==1:
        field [x] [y] = "X"
    else:
        field [x] [y] = "0"

    if check_win():
        break
    if num == 9:
        print(" Ничья!")
        break











