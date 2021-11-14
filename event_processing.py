# в зависимости от нажатия на стрелочки клавиатуры перемещается в определенную сторону
# уже можно написать функцию, ее вид определен
import pygame


def process_event(event):
    game_end = False
    if event.type == pygame.QUIT:
        game_end = True
    if event.type == pygame.KEYDOWN:
        if event.mod != pygame.KMOD_LSHIFT and event.key == pygame.K_a:
            print(1)
        elif event.mod != pygame.KMOD_LSHIFT and event.key == pygame.K_d:
            print(2)
        else:
            print(3)
    return game_end
