import pygame.image
import pygame

pygame.init()

pygame.display.set_mode((0, 0), pygame.FULLSCREEN)


def make_surfs_from_files(list_of_pics_files):
    """
    Возвращает список поверхностей для заданного списка изображений

    :param list_of_pics_files: список файлов с картинками
    :return: список поверхностей для этих избражений
    """
    result_surfaces = []
    for file in list_of_pics_files:
        result_surfaces.append(pygame.image.load(file).convert_alpha())
    return result_surfaces


def transform_surfs_scale_to_screen_params(list_of_surfs):
    """
    Меняет масштаб для поверхностей из заданного списка

    :param list_of_surfs: список поверхностей для обработки
    :return: обработанный список поверхностей
    """
    screen_width = pygame.display.Info().current_w
    for i in range(len(list_of_surfs)):
        surf = list_of_surfs[i]
        list_of_surfs[i] = pygame.transform.scale(surf,
                                                  (int(screen_width), int(surf.get_height() * (
                                                          screen_width / surf.get_width()))))
    return list_of_surfs


# создание списков поверхностей для различных анимаций

WalkingAnimationsSurfs = make_surfs_from_files(
    ["assets/main_hero/step1.png", "assets/main_hero/step2.png", "assets/main_hero/step3.png",
     "assets/main_hero/step4.png", "assets/main_hero/step5.png", "assets/main_hero/step6.png",
     "assets/main_hero/step7.png", "assets/main_hero/step8.png", "assets/main_hero/step9.png"])

StayMainPersonSurf = pygame.image.load("assets/main_hero/stay.png")

ElevatorClosingSurfs = make_surfs_from_files(
    ["assets/rooms/elevator/open_elevator.png", "assets/rooms/elevator/closing_elevator_1.png",
     "assets/rooms/elevator/closing_elevator_2.png", "assets/rooms/elevator/closing_elevator_3.png",
     "assets/rooms/elevator/closing_elevator_4.png", "assets/rooms/elevator/closing_elevator_5.png",
     "assets/rooms/elevator/closing_elevator_6.png", "assets/rooms/elevator/closing_elevator_7.png",
     "assets/rooms/elevator/closing_elevator_8.png", "assets/rooms/elevator/closing_elevator_9.png",
     "assets/rooms/elevator/closing_elevator_10.png", "assets/rooms/elevator/closing_elevator_11.png",
     "assets/rooms/elevator/closing_elevator_12.png", "assets/rooms/elevator/closing_elevator_13.png",
     "assets/rooms/elevator/closing_elevator_14.png", "assets/rooms/elevator/closing_elevator_15.png",
     "assets/rooms/elevator/closing_elevator_16.png", "assets/rooms/elevator/closing_elevator_17.png",
     "assets/rooms/elevator/closing_elevator_18.png", "assets/rooms/elevator/close_elevator.png"])

ElevatorOpeningSurfs = make_surfs_from_files(
    ["assets/rooms/elevator/close_elevator.png", "assets/rooms/elevator/closing_elevator_18.png",
     "assets/rooms/elevator/closing_elevator_17.png", "assets/rooms/elevator/closing_elevator_16.png",
     "assets/rooms/elevator/closing_elevator_15.png", "assets/rooms/elevator/closing_elevator_14.png",
     "assets/rooms/elevator/closing_elevator_13.png", "assets/rooms/elevator/closing_elevator_12.png",
     "assets/rooms/elevator/closing_elevator_11.png", "assets/rooms/elevator/closing_elevator_10.png",
     "assets/rooms/elevator/closing_elevator_9.png", "assets/rooms/elevator/closing_elevator_8.png",
     "assets/rooms/elevator/closing_elevator_7.png", "assets/rooms/elevator/closing_elevator_6.png",
     "assets/rooms/elevator/closing_elevator_5.png", "assets/rooms/elevator/closing_elevator_4.png",
     "assets/rooms/elevator/closing_elevator_3.png", "assets/rooms/elevator/closing_elevator_2.png",
     "assets/rooms/elevator/closing_elevator_1.png", "assets/rooms/elevator/open_elevator.png"])

LevelCompleteSurfsBeginAnimation = transform_surfs_scale_to_screen_params(make_surfs_from_files(
    ["assets/level_complete_animation_images/0.png", "assets/level_complete_animation_images/0.png",
     "assets/level_complete_animation_images/0.png", "assets/level_complete_animation_images/0.png",
     "assets/level_complete_animation_images/0.png", "assets/level_complete_animation_images/0.png",
     "assets/level_complete_animation_images/0.png", "assets/level_complete_animation_images/1.png",
     "assets/level_complete_animation_images/2.png", "assets/level_complete_animation_images/3.png",
     "assets/level_complete_animation_images/4.png", "assets/level_complete_animation_images/5.png",
     "assets/level_complete_animation_images/6.png", "assets/level_complete_animation_images/7.png",
     "assets/level_complete_animation_images/8.png", "assets/level_complete_animation_images/9.png",
     "assets/level_complete_animation_images/10.png", "assets/level_complete_animation_images/11.png",
     "assets/level_complete_animation_images/12.png", "assets/level_complete_animation_images/13.png",
     "assets/level_complete_animation_images/14.png", "assets/level_complete_animation_images/15.png",
     "assets/level_complete_animation_images/16.png", "assets/level_complete_animation_images/17.png",
     "assets/level_complete_animation_images/18.png", "assets/level_complete_animation_images/19.png",
     "assets/level_complete_animation_images/20.png", "assets/level_complete_animation_images/21.png",
     "assets/level_complete_animation_images/22.png", "assets/level_complete_animation_images/23.png",
     "assets/level_complete_animation_images/24.png", "assets/level_complete_animation_images/25.png",
     "assets/level_complete_animation_images/26.png", "assets/level_complete_animation_images/27.png",
     "assets/level_complete_animation_images/28.png", "assets/level_complete_animation_images/29.png",
     "assets/level_complete_animation_images/30.png", "assets/level_complete_animation_images/30.png",
     "assets/level_complete_animation_images/30.png", "assets/level_complete_animation_images/30.png",
     "assets/level_complete_animation_images/30.png", "assets/level_complete_animation_images/30.png",
     "assets/level_complete_animation_images/30.png", "assets/level_complete_animation_images/30.png",
     "assets/level_complete_animation_images/30.png", "assets/level_complete_animation_images/30.png"]
))

LevelCompleteSurfsEndAnimation = transform_surfs_scale_to_screen_params(make_surfs_from_files(
    ["assets/level_complete_animation_images/30.png", "assets/level_complete_animation_images/29.png",
     "assets/level_complete_animation_images/28.png", "assets/level_complete_animation_images/27.png",
     "assets/level_complete_animation_images/26.png", "assets/level_complete_animation_images/25.png",
     "assets/level_complete_animation_images/24.png", "assets/level_complete_animation_images/23.png",
     "assets/level_complete_animation_images/22.png", "assets/level_complete_animation_images/21.png",
     "assets/level_complete_animation_images/20.png", "assets/level_complete_animation_images/19.png",
     "assets/level_complete_animation_images/18.png", "assets/level_complete_animation_images/17.png",
     "assets/level_complete_animation_images/16.png", "assets/level_complete_animation_images/15.png",
     "assets/level_complete_animation_images/14.png", "assets/level_complete_animation_images/13.png",
     "assets/level_complete_animation_images/12.png", "assets/level_complete_animation_images/11.png",
     "assets/level_complete_animation_images/10.png", "assets/level_complete_animation_images/9.png",
     "assets/level_complete_animation_images/8.png", "assets/level_complete_animation_images/7.png",
     "assets/level_complete_animation_images/6.png", "assets/level_complete_animation_images/5.png",
     "assets/level_complete_animation_images/4.png", "assets/level_complete_animation_images/3.png",
     "assets/level_complete_animation_images/2.png", "assets/level_complete_animation_images/1.png",
     "assets/level_complete_animation_images/0.png"]
))
