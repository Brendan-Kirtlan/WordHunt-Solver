import pyautogui
from PIL import Image, ImageEnhance, ImageOps, ImageFilter
import pytesseract
import time
import keyboard
import os
import numpy as np

#position of all letters when in full screen in the screen mirroring app
letter_croppings = [0.6, 0.23, 0.66, 0.33,
                    0.68, 0.23, 0.74, 0.33,
                    0.76, 0.23, 0.81, 0.33,
                    0.84,0.23,0.89,0.33,
                    0.61,0.37,0.65,0.46,
                    0.69,0.37,0.73,0.46,
                    0.77,0.37,0.81,0.46,
                    0.84,0.37,0.89,0.46,
                    0.61,0.5,0.65,0.61,
                    0.69,0.5,0.73,0.61,
                    0.77,0.5,0.81,0.61,
                    0.84,0.5,0.89,0.61,
                    0.6,0.66,0.65,0.74,
                    0.68,0.66,0.73,0.74,
                    0.761,0.66,0.81,0.74,
                    0.84,0.66,0.892,0.74,
                    ]

letter_croppings2 = [0.40902777777777805,0.48000000000000026,0.4491512345679019,0.5444444444444441,
                    0.4564351851851856,0.48000000000000026,0.49458333333333415,0.5444444444444441,
                    0.5038425925925928,0.48000000000000026,0.5416203703703713,0.5444444444444441,
                    0.5512129629629629,0.48000000000000026,0.5890277777777784,0.5444444444444441,
                    
                    0.4110030864197534,0.5619753086419751,0.4487808641975319,0.6274074074074065,
                    0.45643518518518567,0.5619753086419751,0.49618827160493945,0.6274074074074065,
                    0.5038425925925928,0.5619753086419751,0.5416203703703713,0.6274074074074065,
                    0.5512499999999999,0.5619753086419751,0.5890277777777784,0.6274074074074065,
                    
                    0.4110030864197534,0.6479012345679015,0.4487808641975319,0.7140740740740738,
                    0.45841049382716054,0.6479012345679015,0.496188271604939,0.7140740740740738,
                    0.50483024691358,0.6479012345679015,0.5435956790123462,0.7140740740740738,
                    0.5512499999999995,0.6479012345679015,0.5890277777777774,0.7140740740740738,
                    
                    0.41050925925925896,0.7309876543209883,0.44483024691358014,0.7988234567901233,
                    0.4579166666666661,0.7309876543209883,0.4942129629629626,0.7988234567901233,
                    0.5053240740740732,0.7309876543209883,0.5416203703703697,0.7988234567901233,
                    0.5512499999999995,0.7309876543209883,0.5890277777777774,0.7988234567901233,
                    ]

letter_croppings3 = [0.398046875, 0.45625, 0.43125, 0.5145833333333333, 
                     0.441015625, 0.45694444444444443, 0.473046875, 0.5152777777777777, 
                     0.4828125, 0.45694444444444443, 0.516015625, 0.5145833333333333, 
                     0.52421875, 0.45902777777777776, 0.5578125, 0.5159722222222223, 
                     0.56796875, 0.45625, 0.6, 0.5159722222222223, 
                     0.398046875, 0.5319444444444444, 0.43046875, 0.5916666666666667, 
                     0.440234375, 0.5340277777777778, 0.473046875, 0.5909722222222222, 
                     0.483203125, 0.5333333333333333, 0.516015625, 0.5909722222222222, 
                     0.524609375, 0.5319444444444444, 0.55703125, 0.5916666666666667, 
                     0.567578125, 0.5326388888888889, 0.6, 0.5895833333333333, 
                     0.400390625, 0.6083333333333333, 0.430078125, 0.6638888888888889,
                     0.440625, 0.6083333333333333, 0.470703125, 0.6666666666666666,
                     0.4828125, 0.6083333333333333, 0.515234375, 0.6605833333333333,
                     0.52421875, 0.6083333333333333, 0.556640625, 0.6638888888888889,
                     0.568359375, 0.6069444444444444, 0.600390625, 0.6659722222222222,
                     0.398046875, 0.6826388888888889, 0.4296875, 0.7409722222222223,
                     0.440234375, 0.6833333333333333, 0.469921875, 0.7388888888888889, 
                     0.4828125, 0.6826388888888889, 0.513671875, 0.7395833333333334,
                     0.526171875, 0.6840277777777778, 0.557421875, 0.7409722222222223,
                     0.56796875, 0.6840277777777778, 0.59921875, 0.7416666666666667,
                     0.3984375, 0.7590277777777777, 0.43046875, 0.8166666666666667,
                     0.43984375, 0.7618055555555555, 0.4734375, 0.8173611111111111, 
                     0.482421875, 0.7597222222222222, 0.512890625, 0.8166666666666667,
                     0.525, 0.7583333333333333, 0.555859375, 0.8166666666666667,
                     0.5671875, 0.7597222222222222, 0.59765625, 0.8173611111111111]

def print_mouse_position(interval=1.0):
    try:
        while True:
            x, y = pyautogui.position()
            print(f"Mouse position: ({x}, {y})")
            left = x / 2560
            top = y / 1440
            print(f"{left},{top},")

            if keyboard.is_pressed('g'):
                letter_croppings3.append((left, top))
                print("Coordinates appended.")

            time.sleep(interval)
    except KeyboardInterrupt:
        print("\nScript terminated by user.")

def crop_screenshot_and_save(file_path, leftp, topp, rightp, bottomp):
    screenshot = pyautogui.screenshot()

    width, height = screenshot.size

    left = int(width * leftp)     
    top = int(height * topp)     
    right = int(width * rightp)     
    bottom = int(height * bottomp)  

    cropped_screenshot = screenshot.crop((left, top, right, bottom))

    cropped_screenshot.save(file_path)

def edit_screenshot(input_path, output_path):
    img = Image.open(input_path)
    
    img = img.convert('L')

    threshold = 35
    img = img.point(lambda p: p > threshold and 255)

    img.save(output_path)

def preprocess_image(image):
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(2.0)
    image = ImageOps.grayscale(image)
    image = ImageOps.invert(image)

    threshold = 170
    image = image.point(lambda p: p > threshold and 255)

    return image

def analyze_text_in_screenshot(file_path):
    try:
        image = Image.open(file_path)
        preprocessed_image = preprocess_image(image)
        preprocessed_image.save(r'C:\Users\brend\Desktop\dads vid\screenshots\processed.png')

        custom_config = r'--psm 10'

        extracted_text = pytesseract.image_to_string(preprocessed_image, config=custom_config)
        extracted_text = ''.join(extracted_text.splitlines())
        #input(" ")
        if(extracted_text == "D"):
            new_extract = pytesseract.image_to_string(preprocessed_image, config=r'--psm 8')
            if("P" in new_extract or "p" in new_extract):
                return 'P'
        if(extracted_text == "|"):
            extracted_text = 'I'
        if(extracted_text == "="):
            extracted_text = 'E'
            #for i in range(11):
            #    mode = r'--psm '
            #    mode += str(i)
            #    try:
            #        extracted_text = pytesseract.image_to_string(preprocessed_image, config=mode)
            #        extracted_text = ''.join(extracted_text.splitlines())
            #        print(str(i) + " : " + extracted_text)
            #    except:
            #        print("Error on " + str(i))
        

        # Print the extracted text
        #print("Extracted Text:")
        #print(extracted_text)
        #input()
        return extracted_text
    except Exception as e:
        print("An error occurred during text recognition:", e)

def analyze_board(board_size, save_path):
    board = ""
    if board_size == 4:
        board_croppings = letter_croppings2
    elif board_size == 5:
        board_croppings = letter_croppings3
    else:
        print("Invalid board size")
        return
    
    for i in range((board_size*board_size)):
        crop_screenshot_and_save(save_path, board_croppings[i*4], board_croppings[i*4 + 1], board_croppings[i*4 + 2], board_croppings[i*4 + 3])
        try:       
            board += (analyze_text_in_screenshot(save_path)).lower()[0]
        except:
            print('error')
    board = ''.join(board.splitlines())
    print(board)

def analyze_text_in_screenshot2(file_path):
    try:
        image = Image.open(file_path)
        

        custom_config = r'--psm 6 --oem 3 tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ'

        extracted_text = pytesseract.image_to_string(image, lang='eng', config=custom_config)
        #extracted_text = ''.join(extracted_text.splitlines())

        #for i in range(11):
        #    mode = r'--psm '
        #    mode += str(i)
        #    try:
        #        extracted_text = pytesseract.image_to_string(image, config=mode)
        #        #extracted_text = ''.join(extracted_text.splitlines())
        #        print(str(i) + " : " + extracted_text)
        #    except:
        #        print("Error on " + str(i))
        

        # Print the extracted text
        #print("Extracted Text:")
        #print(extracted_text)
        #input()
        print(extracted_text)
    except Exception as e:
        print("An error occurred during text recognition:", e)

save_path = r"C:\Users\brend\Desktop\dads vid\boards\Capture.PNG"
analyze_board(4,save_path)
