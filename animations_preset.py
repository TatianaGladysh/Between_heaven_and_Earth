import pygame.image


def make_surfs_from_files(list_of_pics_files):
    return list(map(pygame.image.load, list_of_pics_files))


WalkingAnimationsSurfs = make_surfs_from_files(
    ["assets/main_hero/step1.png", "assets/main_hero/step2.png", "assets/main_hero/step3.png",
     "assets/main_hero/step4.png", "assets/main_hero/step5.png", "assets/main_hero/step6.png",
     "assets/main_hero/step7.png", "assets/main_hero/step8.png", "assets/main_hero/step9.png"])

StayMainPersonSurf = pygame.image.load("assets/main_hero/stay.png")

ElevatorClosingSurfs = make_surfs_from_files(
    ["assets/elevator/open_elevator.png", "assets/elevator/closing_elevator_1.png",
     "assets/elevator/closing_elevator_2.png", "assets/elevator/closing_elevator_3.png",
     "assets/elevator/closing_elevator_4.png", "assets/elevator/closing_elevator_5.png",
     "assets/elevator/closing_elevator_6.png", "assets/elevator/closing_elevator_7.png",
     "assets/elevator/closing_elevator_8.png", "assets/elevator/closing_elevator_9.png",
     "assets/elevator/closing_elevator_10.png", "assets/elevator/closing_elevator_11.png",
     "assets/elevator/closing_elevator_12.png", "assets/elevator/closing_elevator_13.png",
     "assets/elevator/closing_elevator_14.png", "assets/elevator/closing_elevator_15.png",
     "assets/elevator/closing_elevator_16.png", "assets/elevator/closing_elevator_17.png",
     "assets/elevator/closing_elevator_18.png", "assets/elevator/close_elevator.png"])

ElevatorOpeningSurfs = make_surfs_from_files(
    ["assets/elevator/close_elevator.png", "assets/elevator/closing_elevator_18.png",
     "assets/elevator/closing_elevator_17.png", "assets/elevator/closing_elevator_16.png",
     "assets/elevator/closing_elevator_15.png", "assets/elevator/closing_elevator_14.png",
     "assets/elevator/closing_elevator_13.png", "assets/elevator/closing_elevator_12.png",
     "assets/elevator/closing_elevator_11.png", "assets/elevator/closing_elevator_10.png",
     "assets/elevator/closing_elevator_9.png", "assets/elevator/closing_elevator_8.png",
     "assets/elevator/closing_elevator_7.png", "assets/elevator/closing_elevator_6.png",
     "assets/elevator/closing_elevator_5.png", "assets/elevator/closing_elevator_4.png",
     "assets/elevator/closing_elevator_3.png", "assets/elevator/closing_elevator_2.png",
     "assets/elevator/closing_elevator_1.png", "assets/elevator/open_elevator.png"])
