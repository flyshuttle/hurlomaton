"""
Main Hurlomaton python program
- launches the slideshow
- listen to the GPIO number ###
- if the GPIO is True for two seconds...
    - launches the spots on GPIO ###
    - wait 0.5s
    - captures an image
    - shows success screens
        - screen 1: Well done!
        - screen 2: The picture
        - sreeen 3: Thank you!
"""
from datetime import datetime, timedelta
from time import sleep
from shortuuid import ShortUUID
from controllers import GUIController, GPIOController, PhotoController
from RPi import GPIO

def capture_photo():
    photo.set_filepath(
        ShortUUID(
            alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        ).random(length=9)
    )
    myGPIO.spots_on(True)
    # sleep(1)
    photo.capture()
    print("Capturing " + photo.pathname)
    GUI.show_success()
    GUI.update()
    # sleep(0.5)
    myGPIO.spots_on(False)
    # sleep(10)
    # GUI.show_slideshow()

if __name__ == '__main__':

    SOUND_INPUT_PORT = 2
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(SOUND_INPUT_PORT, GPIO.IN)

    GUI = GUIController()
    myGPIO = GPIOController()
    photo = PhotoController()

    myGPIO.spots_on(True)
    sleep(2)
    myGPIO.spots_on(False)

    test_start_time = None
    success_start_time = None

    """
    --------1---X-------2-------3--------->
            |   |       |       |
            le son est high     |
            on donne une valeur test_start_time
                |       |       |
                |       now() - test_start_time >= 2 secondes
                |       on donne une valeur à success_start_time
                |               |
                |               now() - success_start_time >= 10 secondes
                |               on reset tout
                |
                le son passe low avant d'atteindre les 2 secondes
                on reset test_start_time
    """
    while True:
        sleep(0.2)
        GUI.update()
        if GPIO.input(SOUND_INPUT_PORT) == 1 or success_start_time:
            print("[1] Sound level high")
            """
            [1] Le sound level est HIGH
                OU success_start_time est True
            """
            if not test_start_time:
                """
                c'est la première boucle
                test_start_time n'existe pas ?
                alors on l'initialise
                """
                print("[1] Init test_start_time")
                test_start_time = datetime.now()
            else:
                """
                entre [1] et [3]
                test_start_time existe,
                donc nous allons comparer le timedelta
                entre now() et test_start_time
                """
                test_time_delta = datetime.now() - test_start_time
                print("[1]*[3] test_time_delta: ", test_time_delta)
                if test_time_delta >= timedelta(microseconds=2000000):
                    """
                    [2] test_time_delta est >= 2 secondes
                    success_start_time n'existe pas ?
                    alors on l'initialise
                    """
                    print("[2] success")
                    if not success_start_time:
                        print("[2] init success_start_time")
                        success_start_time = datetime.now()
                    else:
                        """
                        entre [2] et [3]
                        success_start_time existe,
                        donc nous allons comparer le timedelta
                        entre now() et success_start_time
                        """
                        success_time_delta = datetime.now() - success_start_time
                        print("[2]*[3] success_time_delta: ", success_time_delta)
                        if success_time_delta >= timedelta(seconds=10):
                            """
                            [3] success_time_delta est >= 10 secondes
                            on reset tous les start_time
                            """
                            print("[3] success end reset all")
                            test_start_time = None
                            success_start_time = None
        else:
            """
            [x] Si GPIO == 0 on reset start
            """
            print("[x] reset test_start_time")
            test_start_time = None

# or GUI.fake_success
