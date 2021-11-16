# в зависимости от нажатия на стрелочки клавиатуры перемещается в определенную сторону
# уже можно написать функцию, ее вид определен
import pygame


# предполагаю что на данный момент hero_coordinates = [координата х, координата у, координата z, parameter],
# если parameter = True персонаж внутри лифта, если parameter = False - то вне лифта
# наверное целесообразно добавить еще один парметрв этот массив отвечающий за то в комнате перс. или нет


def process_event(event, hero_coordinates):
    game_end = False
    if event.type == pygame.QUIT:
        game_end = True
    # обработка событий с клавиатуры
    if event.type == pygame.KEYDOWN:
        # движение по главной плоскости xOz вдоль x
        if event.key == pygame.K_a and hero_coordinates[0] != 0:
            hero_coordinates[0] -= 1
        elif event.key == pygame.K_d and hero_coordinates[0] != 20:
            hero_coordinates[0] += 1
        # лифт (необходимо добавить условие нахождения лифта в ячеке нахождения перс.
        elif event.key == pygame.K_F:
            if hero_coordinates[3]:
                # механизм запускающий отрисовку выхождения из лифта (например отдельный параметр True or False)
                pass
            else:
                # механизм запускающий отрисовку вхождения в лифт (например отдельный параметр True or False,
                # который передается в раздел отрисовки)
                pass
        # опускается на один этаж, меняется координата по z
        elif event.key == pygame.K_DOWN and hero_coordinates[2] != 1 and hero_coordinates[3]:
            hero_coordinates[2] -= 1
        # поднимается на один этаж, меняется координата по z
        elif event.key == pygame.K_UP and hero_coordinates[2] != 5 and hero_coordinates[3]:
            hero_coordinates[2] += 1
    return game_end, hero_coordinates
