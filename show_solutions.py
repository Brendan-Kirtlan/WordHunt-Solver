from PIL import Image, ImageTk
import tkinter as tk
import sys
import pyautogui
import time
import math
import keyboard
size = 4
word_index = 0
pos = [
    [[66,55], [134, 55], [200,55], [266,55]],
    [[66,123], [134, 123], [200,123], [266,123]],
    [[66,191], [134, 191], [200,191], [266,191]],
    [[66,259], [134, 259], [200,259], [266,259]],
]

mouse_pos = [
    [[1097,737], [1216,737],[1336,737],[1456,737]],
    [[1097,858], [1216,858],[1336,858],[1456,858]],
    [[1097,974], [1216,974],[1336,974],[1456,974]],
    [[1097,1098], [1216,1098],[1336,1098],[1456,1098]]
]

mouse_pos5 = [
    [[1058,702], [1168, 702], [1278,702], [1388, 702],[1498, 702]],
    [[1058,812], [1168, 812], [1278,812], [1388, 812],[1498, 812]],
    [[1058,922], [1168, 922], [1278,922], [1388, 922],[1498, 922]],
    [[1058,1032], [1168, 1032], [1278,1032], [1388, 1032],[1498, 1032]],
    [[1058,1142], [1168, 1142], [1278,1142], [1388, 1142],[1498, 1142]],
]



def solve(order):
    global size
    if size == 4:
        mouse_pos_to_use = mouse_pos
    else:
        mouse_pos_to_use = mouse_pos5
    move_mouse_to(mouse_pos_to_use[order[0]][order[0+1]][0],mouse_pos_to_use[order[0]][order[0+1]][1])
    pyautogui.mouseDown(button='left')
    for i in range(2,len(order),2):
        move_mouse_to(mouse_pos_to_use[order[i]][order[i+1]][0],mouse_pos_to_use[order[i]][order[i+1]][1])
        if keyboard.is_pressed('q'):
                print("Aborting")
                exit()
    pyautogui.mouseUp(button='left')


def move_mouse_to(x, y):
    pyautogui.moveTo(x,y,0.2)

def print_mouse_position(interval=1.0):
    try:
        while True:
            x, y = pyautogui.position()
            print(f"Mouse position: ({x}, {y})")

            time.sleep(interval)
    except KeyboardInterrupt:
        print("\nScript terminated by user.")


def take_screenshot():
    screenshot = pyautogui.screenshot()

    width, height = screenshot.size
    leftp = 0.86
    topp = 0.62
    bottomp = 0.84
    rightp = 0.99
    file_path = r"C:\Users\brend\Desktop\dads vid\screenshots\board.png"

    left = int(width * leftp)     
    top = int(height * topp)     
    right = int(width * rightp)     
    bottom = int(height * bottomp)  
    
    cropped_screenshot = screenshot.crop((left, top, right, bottom))

    cropped_screenshot.save(file_path)
    return 0


def parse_output(output):
    lines = output.strip().split('\n')
    global size
    number_array = []
    word_array = []
    if not lines:
        print("No lines")
        exit()
    for line in lines:
        if line == "END":
            size = int(math.sqrt(int(lines[len(lines) - 1])))
            break
        
        if line[0].isdigit():
            numbers = line.split(',')
            
            number_array.append([int(num) for num in numbers])
        else:
            word_array.append(line)
    
    return number_array, word_array

take_screenshot()

data = sys.stdin.read()

parsed_numbers, parsed_words = parse_output(data)

image_path = r'C:\Users\brend\Desktop\dads vid\screenshots\board.png'
image = Image.open(image_path)

for i in range(len(parsed_numbers)):
    print(f"Solving for {parsed_words[i]}")
    solve(parsed_numbers[i])