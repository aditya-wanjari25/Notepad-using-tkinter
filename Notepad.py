import tkinter as tk
from tkinter import ttk
from tkinter import font, colorchooser, messagebox, filedialog
import os


win = tk.Tk()
win.geometry("800x600")
win.title("MyNotePad")

main_menu = tk.Menu(win)
win.config(menu = main_menu)

# -----------File Menu-----------

text_url = " "
text_change = False

def new_file(event = None):
    global text_url
    text_url = " "
    text_editor.delete(1.0,tk.END)

def open_file(event = None):
    global text_url
    text_url = filedialog.askopenfilename(initialdir = os.getcwd(), title = "Select File" , filetypes = (("Text File","*.txt"),("All Files","*.*") ))
    try :
        with open(text_url,"r") as for_read:
            text_editor.delete(1.0,tk.END)
            text_editor.insert(1.0,for_read.read())
    except FileNotFoundError:
        return
    except:
        return
    
    win.title(os.path.basename(text_url))


# def save_file(event = None):
#     global text_url
#     try:
#         if text_url:
#             content = str(text_editor.get(1.0,tk.END))
#             with open(text_url,"w", encoding="utf-8") as for_read:
#                 for_read.write(content)
#         else:
#             text_url = filedialog.asksaveasfile(mode = "w",defaultextension = "txt", filetypes = (("Text File","*.txt"),("All Files","*.*")) ) 
#             content2 = text_editor.get(1.0,tk.END)
#             text_url.write(content2)
#             text_url.close()
#     except:
#         return 


def save_as_file(event = None):
    global text_url
    try:
        content = text_editor.get(1.0,tk.END)
        text_url = filedialog.asksaveasfile(mode = "w", defaultextension = "txt", filetypes = (("Text File","*.txt"),("All Files","*.*")) ) 
        text_url.write(content)
        text_url.close()
    except:
        return


def exit_func(event = None):
    global text_change
    global text_url
    mbox = messagebox.askyesno("Warning","Did you save your work?")
    if mbox is True:
        win.destroy()
    else:
        content2 = text_editor.get(1.0,tk.END)
        text_url = filedialog.asksaveasfile(mode = "w",defaultextension = "txt", filetypes = (("Text File","*.txt"),("All Files","*.*")) ) 
        text_url.write(content2)
        text_url.close()
        win.destroy()       
                    
        

my_file = tk.Menu(main_menu, tearoff = False)
main_menu.add_cascade(label = "File", menu = my_file )

my_file.add_command(label = "New", compound = tk.LEFT, accelerator="(Ctrl+N)", command = new_file)
my_file.add_command(label = "Open", compound = tk.LEFT, accelerator="(Ctrl+O) ", command = open_file )
# my_file.add_command(label = "Save", compound = tk.LEFT, accelerator="(Ctrl+S)", command = save_file)
my_file.add_command(label = "Save ", compound = tk.LEFT, command = save_as_file)
my_file.add_command(label = "Exit", compound = tk.LEFT, command = exit_func)



#------------Edit Menu-------------

my_edit = tk.Menu(main_menu, tearoff = False)
main_menu.add_cascade(label = "Edit", menu = my_edit )
my_edit.add_command(label = "Cut", compound = tk.LEFT, accelerator="(Ctrl+X)", command = lambda: text_editor.event_generate("<Control x>") )
my_edit.add_command(label = "Copy", compound = tk.LEFT, accelerator="(Ctrl+C)", command = lambda: text_editor.event_generate("<Control c>") )
my_edit.add_command(label = "Paste", compound = tk.LEFT, accelerator="(Ctrl+V)", command = lambda: text_editor.event_generate("<Control v>") )
my_edit.add_separator()
my_edit.add_command(label = "Clear All", compound = tk.LEFT, accelerator="(Cltr+Alt+X)", command = lambda: text_editor.delete(1.0,tk.END))

def find_func(event = None):

    def find():
        word = find_input.get()
        text_editor.tag_remove("march","1.0",tk.END)
        matches = 0
        if word:
            start_pos = "1.0"
            while True:
                start_pos = text_editor.search(word,start_pos,stopindex=tk.END)
                if not start_pos:
                    break
                end_pos = f"{start_pos}+{len(word)}c"
                text_editor.tag_add("match", start_pos, end_pos)
                matches += 1
                start_pos = end_pos
                text_editor.tag_config("match",foreground = "white", background = "black")
    
    def replace():
        word = find_input.get()
        replace_text = replace_input.get()
        content = text_editor.get(1.0,tk.END)
        new_content = content.replace(word , replace_text)
        text_editor.delete(1.0,tk.END)
        text_editor.insert(1.0,new_content)


    find_popup = tk.Toplevel()
    find_popup.geometry("450x200")
    find_popup.title("Find Word")
    find_popup.resizable(0,0)

    # Frame for find
    find_frame = ttk.LabelFrame(find_popup, text = "Find and Replace Word")
    find_frame.pack(pady = 20)

    text_find = ttk.Label(find_frame, text = "Find")
    text_replace = ttk.Label(find_frame, text = "Replace")

    find_input = ttk.Entry(find_frame, width = 30)
    replace_input = ttk.Entry(find_frame, width = 30)

    find_bttn = ttk.Button(find_frame, text = "Find", command = find)
    replace_bttn = ttk.Button(find_frame, text = "Replace", command = replace)
 
    text_find.grid(row = 0, column = 0, padx= 4, pady= 4)
    text_replace.grid(row = 1, column = 0, padx= 4, pady= 4)
    
    find_input.grid(row = 0, column = 1, padx= 4, pady= 4)
    replace_input.grid(row = 1, column = 1, padx= 4, pady= 4)

    find_bttn.grid(row =2 , column = 0, padx = 8, pady = 4)
    replace_bttn.grid(row =2 , column = 1, padx = 8, pady = 4)


my_edit.add_command(label = "Find", compound = tk.LEFT, accelerator="(Cltr+F)", command = find_func)




#----------- View Menu---------------

status_bar_label = ttk.Label(win)
my_view = tk.Menu(main_menu, tearoff = False)
main_menu.add_cascade(label = "View", menu = my_view )
show_status_bar = tk.BooleanVar()
show_status_bar.set(True)

def hide_stat():
    global show_status_bar
    if show_status_bar:
        status_bar.pack_forget()
        show_status_bar = False
    else:
        status_bar.pack(side = tk.BOTTOM)
        show_status_bar = True

                                
my_view.add_checkbutton(label ="Status Bar",  onvalue = True , offvalue = 0,variable = show_status_bar, compound = tk.LEFT ,command = hide_stat)



# Colour Theme

my_color = tk.Menu(main_menu , tearoff = False)
main_menu.add_cascade(label ="Color Theme", menu = my_color)

color_dict = {
    "Light (Default)" : ("#000000","#ffffff"),
    "Light Plus" : ("#474747","#e0e0e0"),
    "Dark" : ("#c4c4c4","#2d2d2d"),
    
    "Monokai" : ("#d3b774","#474747"),
    "Fade Pink" : ("#2d2d2d","#ffe8e8"),
    "Night Blue" : ("#ededed","#6b9dc2") 
}
theme_select = tk.StringVar()
def change_theme(): 
    get_theme = theme_select.get()
    color_tuple = color_dict.get(get_theme)
    fg_color, bg_color = color_tuple[0] , color_tuple[1]
    text_editor.config(background = bg_color, fg = fg_color)


for i in color_dict:
    my_color.add_radiobutton(label = i , compound = tk.LEFT,variable = theme_select, command = change_theme)
 

# Creating toolbar

# func
font_now = "Arial"
font_size_now = 16

def change_font(win):
    global font_now
    font_now = font_family.get()
    text_editor.configure(font = (font_now,font_size_now))

def change_size(win):
    global font_size_now
    font_size_now = size_var.get()
    text_editor.configure(font=(font_now, font_size_now))

def bold_func():
    text_get = tk.font.Font(font=text_editor["font"])
    if text_get.actual()["weight"] == "normal" :
        text_editor.configure(font = (font_now,font_size_now, "bold"))
    if text_get.actual()["weight"] == "bold" :
        text_editor.configure(font = (font_now,font_size_now, "normal"))
        
def italics_func():
    text_get = tk.font.Font(font=text_editor["font"])
    if text_get.actual()["slant"] == "roman" :
        text_editor.configure(font = (font_now,font_size_now, "italic"))
    if text_get.actual()["slant"] == "italic" :
        text_editor.configure(font = (font_now,font_size_now, "roman"))

def underline_func():
    text_get = tk.font.Font(font=text_editor["font"])
    if text_get.actual()["underline"] == 0 :
        text_editor.configure(font = (font_now,font_size_now, "underline"))
    if text_get.actual()["underline"] ==  1:
        text_editor.configure(font = (font_now,font_size_now, "normal"))

def color_choose():
    color_var = tk.colorchooser.askcolor()
    text_editor.configure(fg = color_var[1])



tool_bar_label = ttk.Label(win)
tool_bar_label.pack(side = tk.TOP , fill = tk.X)

font_tuple = tk.font.families()
font_family = tk.StringVar()
font_box = ttk.Combobox(tool_bar_label, width = 30, textvariable = font_family, state ="readonly")
font_box.bind("<<ComboboxSelected>>", change_font)
font_box['values'] = font_tuple
font_box.current(font_tuple.index("Arial"))

font_box.grid(row= 0 , column= 0, padx = 5, pady = 5)

# font size
size_var = tk.IntVar()
font_size = ttk.Combobox(tool_bar_label, width = 20, state = "readonly", textvariable= size_var)
font_size.bind("<<ComboboxSelected>>",change_size)
font_size['values'] = tuple(range(8,100,2))
font_size.current(4)
font_size.grid(row=0,column = 1, padx = 5 , pady = 5)

# Bold Button
bold_btn = ttk.Button(tool_bar_label, text = "Bold")
bold_btn.configure(command = bold_func)
bold_btn.grid(row = 0, column = 2, padx =5,pady =5)
# italics Button
italics_btn = ttk.Button(tool_bar_label, text = "Italics")
italics_btn.configure(command = italics_func)
italics_btn.grid(row = 0, column = 3, padx =5,pady =5)
# underline Button
underline_btn = ttk.Button(tool_bar_label, text = "Underline")
underline_btn.configure(command = underline_func)
underline_btn.grid(row = 0, column = 4, padx =5,pady =5)

# Color pallete

color_btn = ttk.Button(tool_bar_label,text = "Color Pallete")
color_btn.configure(command = color_choose)
color_btn.grid(row = 0, column = 5, padx =5,pady =5)


# Trying to add word wrap in the following code but this doesnt work
# text_editor = tk.Text(win)

# # Word Wrap
# def wordWrapper():
#     if check:
#         text_editor.config(wrap = "word" , relief = tk.FLAT)
#     else:
#         text_editor.config(wrap = "NONE" , relief = tk.FLAT)


# check = tk.IntVar()
# word_wrapper = ttk.Checkbutton(tool_bar_label, text = "Word Wrap", variable = check, onvalue = 1, offvalue = 0 , command = wordWrapper)
# check.set(0)
# word_wrapper.grid(row = 0, column = 6 , padx = 5, pady = 5)





# Text Editor
text_editor = tk.Text(win)
text_editor.config(wrap = "word" , relief = tk.FLAT)

scroll_bar1 = tk.Scrollbar(win)
scroll_bar2 = tk.Scrollbar(win, orient =tk.HORIZONTAL)
text_editor.focus_set()
scroll_bar1.pack(side = tk.RIGHT , fill = tk.Y)
scroll_bar2.pack(side = tk.BOTTOM , fill = tk.X)
text_editor.pack(fill = tk.BOTH , expand = True)
scroll_bar1.config(command = text_editor.yview)
scroll_bar2.config(command = text_editor.xview)
text_editor.config(yscrollcommand = scroll_bar1.set)
text_editor.config(xscrollcommand = scroll_bar2.set)





# Status Bar
status_bar = ttk.Label(win , text = "Status Bar")
status_bar.pack(side = tk.BOTTOM)



def change_word(event = None):
    global text_change
    if text_editor.edit_modified():
        text_change = True
        word = len(text_editor.get(1.0,"end-1c").split())
        char = len(text_editor.get(1.0,"end-1c").replace(" ",""))
        status_bar.config(text = f"Character: {char} Words: {word}")
    text_editor.edit_modified(False)
    
text_editor.bind("<<Modified>>", change_word)




win.mainloop()
