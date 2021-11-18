# в зависимости от нажатия на стрелочки клавиатуры перемещается в определенную сторону
# уже можно написать функцию, ее вид определен
import pygame


# предполагаю что на данный момент hero_coordinates = [координата х, координата у, координата z, parameter],
# если parameter = True персонаж внутри лифта, если parameter = False - то вне лифта
# наверное целесообразно добавить еще один парметрв этот массив отвечающий за то в комнате перс. или нет
def process_event(event, hero_coordinates, massive_of_rooms, max_coordinates):
    game_end = False
    if event.type == pygame.QUIT:
        game_end = True
    # обработка событий с клавиатуры
    if event.type == pygame.KEYDOWN:
        # движение по главной плоскости xOy вдоль x
        if event.key == pygame.K_a and hero_coordinates[0] != 1:
            hero_coordinates[0] -= 1
        elif event.key == pygame.K_d and hero_coordinates[0] != max_coordinates[0]:
            hero_coordinates[0] += 1
        # лифт
        elif event.key == pygame.K_F:
            if hero_coordinates[3]:
                # механизм запускающий отрисовку выхождения из лифта (например отдельный параметр True or False)
                pass
            elif have_an_elevator(massive_of_rooms, hero_coordinates):
                # функция в условии проверяет есть ли лифт в том метсе где находится перс.
                # механизм запускающий отрисовку вхождения в лифт (например отдельный параметр True or False,
                # который передается в раздел отрисовки)
                pass
        # опускается на один этаж, меняется координата по y
        elif event.key == pygame.K_DOWN and hero_coordinates[1] != max_coordinates[1] and hero_coordinates[3]:
            hero_coordinates[2] += 1
        # поднимается на один этаж, меняется координата по y
        elif event.key == pygame.K_UP and hero_coordinates[1] != 1 and hero_coordinates[3]:
            hero_coordinates[2] -= 1
        # механизм захождения в комнату
        elif event.key == pygame.K_E and have_a_door(massive_of_rooms, hero_coordinates):
            # сделаю
            pass
    return game_end, hero_coordinates


def have_a_door(massive_of_rooms, hero_coordinates):
    """
    функция проверяет наличие дври в ячейке нахождения персонажа
    """
    for room in massive_of_rooms:
        if isinstance(room, Room):
            room_coordinates = room.get_cords()
            if room_coordinates[0] == hero_coordinates[0] and room_coordinates[1] == hero_coordinates[1] and \
                    room_coordinates[2] == hero_coordinates[2]:
                if room.get_type() == "door":
                    return True
                else:
                    return False
    return False


def have_an_elevator(massive_of_rooms, hero_coordinates):
    """
    функция проверяет наличие лифта в ячейке нахождения персонажа (вдруг клавиша будет нажата случайно)
    :param massive_of_rooms:
    :param hero_coordinates:
    :return:
    """
    for room in massive_of_rooms:
        if isinstance(room, Room):
            room_coordinates = room.get_cords()
            if room_coordinates[0] == hero_coordinates[0] and room_coordinates[1] == hero_coordinates[1] and \
                    room_coordinates[2] == hero_coordinates[2]:
                if room.get_type() == "elevator":
                    return True
                else:
                    return False
    return False


def max_coordinates_finding(massive_of_rooms):
    """
    Вариант функции возвращающей максимальные координаты влабиринте, предполагается что она будет использоваться
    единоразово, а далее возвращенный ею массив будет постпать в функцию обработки событий
    :param massive_of_rooms: массив объектов типа "Room"
    """
    max_coordinates = []
    x_cords, y_cords, z_cords = [], [], []
    for room in massive_of_rooms:
        coordinates = room.get_cords()
        x_cords.append(coordinates[0])
        y_cords.append(coordinates[1])
        z_cords.append(coordinates[2])
    max_coordinates.append(max(x_cords))
    max_coordinates.append(max(y_cords))
    max_coordinates.append(max(z_cords))
    return max_coordinates



