import subprocess
import tkinter as tk
from tkinter import ttk
import math

all_words = ''
output_string = ""
solution_gcode_path = r"D:\Youtube\Wordhunt vid\gcode\solution.gcode"

speed = 5000
up_speed = 10000

#All directories removed along with IPs for printer stuff

def call_read_board_script():
    try:
        #directory for read_board.py
        output = subprocess.check_output(["python", r""], shell=True, universal_newlines=True)
        return output.strip()  
    except subprocess.CalledProcessError as e:
        return str(e)

def display_output():
    global output_string
    output_text = call_read_board_script()
    if len(output_text) != 16:
        output_text = "Error: Output length is not 16"
    for i in range(16):
        output_labels[i].config(text=output_text[i].upper())
    output_string = output_text

def call_second_program():
    global all_words
    try:
        #directory for c++ program
        output = subprocess.check_output([r"", output_string], universal_newlines=True)
        all_words = output
        number_array, word_array = parse_output(output)
        second_tab_list.delete(0, tk.END) 
        for word in word_array:
            second_tab_list.insert(tk.END, word)
    except Exception as e:
        print("Error:", e)

def call_generate_gcode():
    global all_words
    try:
        output = all_words
        if output:
            #directory for generate_gcode.py
            process = subprocess.Popen(["python", r""], stdin=subprocess.PIPE)
            process.communicate(output.encode())
    except Exception as e:
        print("Error:", e)

def call_all():
    display_output()
    call_second_program()
    call_generate_gcode()
    upload_solution_gcode()

def upload_solution_gcode():
    try:
        #removed ips and passwords
        subprocess.run(["curl", "-u", "bblp:", "-T", solution_gcode_path, "-k", "--ftp-ssl", "ftps:// /customs/solution.gcode"])
    except Exception as e:
        print("Error:", e)

def parse_output(output):
    lines = output.strip().split('\n')
    size = int(math.sqrt(int(lines[-1]))) if lines else 0
    number_array = []
    word_array = []
    if not lines:
        print("No lines")
        exit()
    for line in lines:
        if line == "END":
            break
        if line[0].isdigit():
            numbers = line.split(',')
            number_array.append([int(num) for num in numbers])
        else:
            word_array.append(line)
    return number_array, word_array

#I don't actually use the preferences in the program I still need to change the generate_gcode.py to accept command line arguments
def open_preferences():
    global speed, up_speed 
    preferences_window = tk.Toplevel(app)
    preferences_window.title("Preferences")
    
    preferences_window.configure(bg='#1e1e1e')
    ttk.Style().configure('TLabel', foreground='white', background='#1e1e1e')
    ttk.Style().configure('TEntry', foreground='black', background='white')
    #ttk.Style().configure('TButton', foreground='black', background='#c5c5c5')
    
    ttk.Label(preferences_window, text="Speed:").grid(row=0, column=0, padx=5, pady=5)
    ttk.Label(preferences_window, text="Up Speed:").grid(row=1, column=0, padx=5, pady=5)
    
    speed_entry = ttk.Entry(preferences_window, style='TEntry')
    speed_entry.grid(row=0, column=1, padx=5, pady=5)
    speed_entry.insert(0, str(speed))
    
    up_speed_entry = ttk.Entry(preferences_window, style='TEntry')
    up_speed_entry.grid(row=1, column=1, padx=5, pady=5)
    up_speed_entry.insert(0, str(up_speed))
    
    def save_preferences():
        global speed, up_speed 
        speed = int(speed_entry.get())
        up_speed = int(up_speed_entry.get())
        preferences_window.destroy()
    
    save_button = ttk.Button(preferences_window, text="Save", command=save_preferences, style='TButton')
    save_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

app = tk.Tk()
app.title("Word Hunt Solver")

app.geometry("450x645")

style = ttk.Style()
style.theme_use('clam')
style.configure('.', background='#1e1e1e', foreground='white')
style.configure('TNotebook.Tab', foreground='black')

tab_control = ttk.Notebook(app)
tab1 = ttk.Frame(tab_control)
tab2 = ttk.Frame(tab_control)
tab_control.add(tab1, text='Word Hunt Output')
tab_control.add(tab2, text='Words')

tab_control.pack(expand=1, fill='both')

output_frame = ttk.Frame(tab1, padding=10, style='TFrame')
output_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

output_labels = []
for i in range(16):
    padx_value = 5 if i < 12 else 3  
    label = ttk.Label(output_frame, text="", style='TLabel', font=('Liberation Mono', 60), anchor='center', relief='solid', width=2)
    label.grid(row=i // 4, column=i % 4, padx=padx_value, pady=5) 
    output_labels.append(label)


button_get_output = ttk.Button(tab1, text="Get Board", command=display_output, style='TButton')
button_get_output.pack(pady=5)

button_call_second_program = ttk.Button(tab1, text="Find Words", command=call_second_program, style='TButton')
button_call_second_program.pack(pady=5)

second_tab_list = tk.Listbox(tab2, background='#1e1e1e', foreground='white')
second_tab_list.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

button_call_generate_gcode = ttk.Button(tab1, text="Generate G-Code", command=call_generate_gcode, style='TButton')
button_call_generate_gcode.pack(pady=5)

button_call_all = ttk.Button(tab1, text="Call All", command=call_all, style='TButton')
button_call_all.pack(pady=5)

menu = tk.Menu(app)
app.config(menu=menu)
preferences_menu = tk.Menu(menu, tearoff=False)
menu.add_cascade(label="Preferences", menu=preferences_menu)
preferences_menu.add_command(label="Open Preferences", command=open_preferences)

app.mainloop()
