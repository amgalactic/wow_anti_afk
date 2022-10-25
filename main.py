import cv2
import numpy as np 
import pytesseract
import pyautogui
from time import sleep, time
import datetime
import random

global START_TIME


START_TIME = time()


def get_scene_text():
    image = np.array(pyautogui.screenshot())
    image = image[:, :, ::-1].copy()
    width, height = image.shape[:2]
    cntY, cntX = width//2, height//2
    minX, minY, maxY = int(cntX - 0.5*cntX), int(cntY - 0.75*cntY), int(cntY + 0.9*cntY)
    roi = image[minY:maxY, minX:]
    # Get only yellow text
    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, (15, 190, 190), (36, 255,255))
    imask = mask>0
    res = np.zeros_like(roi, np.uint8)
    res[imask] = roi[imask]
    # Convert image to grayscale and enhance
    img = cv2.cvtColor(np.array(res), cv2.COLOR_BGR2GRAY)
    kernel = np.ones((2, 2), np.uint8)
    roi = cv2.dilate(img, kernel, iterations=1)
    roi = cv2.erode(roi, kernel, iterations=1)
    # Get text from image 
    scene_text = (pytesseract.image_to_string(roi, lang='rus'))
    # print(f'Got this text from screen:\n{scene_text}')
    return scene_text


def reconnect(array, image):
    if array[0][0] and array[0][1] and array[0][2] and array[0][3] in image:
        pyautogui.press('enter')
        print('Reconnect pressed!')
        sleep(5)
    else:
        re_login()


def re_login():
    pyautogui.press('enter')
    print('Re-login pressed!')


def afk(array, image):
    keys = ['w', 'a', 's', 'd', 'space', 'q', 'e']
    if array[0][0] and array[0][1] and array[0][2] and array[0][3] not in image:
        keys_select = random.randint(0, 6)
        pressed_time = random.uniform(0, 2)
        rand_wait = random.uniform(1, 225)
        pyautogui.keyDown(keys[keys_select])
        sleep(pressed_time)
        pyautogui.keyUp(keys[keys_select])
        print(f'Script working for {(time() - START_TIME) / 60:.1f} minutes.\nPressed key {keys[keys_select]} for {pressed_time:.1f} seconds.\nWaiting {rand_wait:.1f} seconds.\n')
        sleep(rand_wait)


def main(words):
    while True:
        wow_title = "World of Warcraft"
        current_window = pyautogui.getActiveWindowTitle()
        if current_window == wow_title:
            screen_text = get_scene_text()

            if words[2][0] and words[2][1] in screen_text:
                print(f'{datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")} Still in queue.\nWill wait 60 seconds.')
                sleep(60)

            elif words[1][0] in screen_text:
                re_login()
                sleep(30)

            elif words[0][0] or words[0][1] or words[0][2] or words[0][3] in screen_text:
                reconnect(words, screen_text)
                sleep(5)

            afk(words, screen_text)
        else:
            print('Wrong window')
            sleep(5)


if __name__ == '__main__':
    russian_words = [['Переподключение', 'Настройки', 'Создатели', 'Выйти'], ['Войти в игровой мир'],
                     ['Место в очереди:', 'Время ожидания:']]
    main(russian_words)