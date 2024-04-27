import os
import math
import sys

letter_len = 11.25
position_x = 0
position_y = 0
z_len = 4.8
speed = 5000
lift_speed = 10000
header = f'G91\nG1 F{lift_speed}\nG1 Z-10\n\n'
size = 4

def create_path(coords, word):
    global letter_len
    global position_x
    global position_y
    global z_len
    
    s = ''
    s += f'; {word}\n'
    dy = letter_len * (position_y - coords[0])
    dx = letter_len * (coords[1] - position_x)
    s += f'G1 X{dx} Y{dy}\n'
    position_y = coords[0]
    position_x = coords[1]
    
    s += f'G1 Z-{z_len} \n' #pen down
    s+= f'G1 F{speed}\n'
    
    for i in range(2, len(coords), 2):
        dy = letter_len * (position_y - coords[i])
        dx = letter_len * (coords[i+1] - position_x)
        s += f'G1 X{dx} Y{dy}\n'
        position_y = coords[i]
        position_x = coords[i+1]
        
    s+= f'G1 F{lift_speed}\n'
    s += f'G1 Z{z_len} \n\n' #pen up
    return s

def save_gcode_file(gcode_string):
    directory = r"D:\Youtube\Wordhunt vid\gcode"
    file_name = "solution.gcode"
    file_path = os.path.join(directory, file_name)
    
    try:
        with open(file_path, 'w') as file:
            file.write(gcode_string)
        print(f"G-code file saved successfully at: {file_path}")
    except Exception as e:
        print(f"Error occurred while saving the G-code file: {e}")

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

data = sys.stdin.read()
parsed_nums, parsed_words = parse_output(data)


gcode_string = ''
gcode_string += header

#parsed_nums = [[3,0,2,0,3,1,3,2,2,1,1,1,2,2], [1,0,2,0,3,1,3,2,2,1,1,1,2,2]]
#parsed_words = ['hi', 'stinky']
for i in range(len(parsed_nums)):
    gcode_string += create_path(parsed_nums[i], parsed_words[i])

dy = letter_len * (position_y - 0)
dx = letter_len * (0 - position_x)
gcode_string += f'G1 X{dx} Y{dy} Z10\n' #back to starting position

save_gcode_file(gcode_string)

#print(gcode_string)