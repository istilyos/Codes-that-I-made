from tkinter import *
import tkinter.messagebox as messagebox

# Add a flag to track if a calculation has been performed
calculation_done = False


def button_click(char):
    global calculation_done
    if calculation_done:
        entry.delete(0, END)
        calculation_done = False
    current = entry.get()
    entry.delete(0, END)
    entry.insert(0, current + str(char))


def clear():
    global calculation_done
    entry.delete(0, END)
    conversion_entry.delete(0, END)
    calculation_done = False


def calculate():
    global calculation_done
    current = entry.get()
    try:
        # Check if the input has leading zeros and remove them
        if current.startswith('0'):
            current = current.lstrip('0')
        # Tinatanggal natin yung leading zeros kasi hindi mainterpret ng eval function, pag may leading zero it
        # interprets it as an octal value
        result = eval(current)
        entry.delete(0, END)
        entry.insert(0, result)
        calculation_done = True  # Set the flag to True after calculation
    except Exception as e:
        entry.delete(0, END)
        entry.insert(0, "Error! Invalid input.")
        calculation_done = False  # Set the flag to False on error


# In the button_click and clear functions, reset the calculation_done flag
def button_click(char):
    global calculation_done
    if calculation_done:
        entry.delete(0, END)
        calculation_done = False
    current = entry.get()
    entry.delete(0, END)
    entry.insert(0, current + str(char))


def clear():
    global calculation_done
    entry.delete(0, END)
    conversion_entry.delete(0, END)
    calculation_done = False


def convert_number_system():
    current = entry.get()
    result = ""

    try:
        current_num = int(current)
        selected_base = base_var.get()

        if selected_base == 1:  # Binary
            result = format(current_num, 'b')
        elif selected_base == 2:  # Octal
            result = format(current_num, 'o')
        elif selected_base == 0:  # Decimal
            result = str(current_num)
        elif selected_base == 3:  # Hexadecimal
            result = format(current_num, 'X')

        # If the current base is decimal, and the user clicks "Convert to Decimal", then revert back to decimal
        if selected_base == 0 and result != "Error! Invalid input for conversion.":
            result = str(current)

        conversion_entry.delete(0, END)
        conversion_entry.insert(0, result)

    except ValueError:
        conversion_entry.delete(0, END)
        conversion_entry.insert(0, "Error! Invalid input for conversion.")


def show_conversion_frame():
    if conversion_frame.winfo_manager() == "":
        conversion_frame.grid(columnspan=4, padx=5, pady=5, ipadx=5, ipady=5, sticky='nsew')
    else:
        conversion_frame.grid_remove()


def copy_converted_value():
    converted_value = conversion_entry.get()
    root.clipboard_clear()
    root.clipboard_append(converted_value)
    root.update()
    messagebox.showinfo("Copied", "Converted value has been copied to clipboard.")


def create_button(frame, text, command):
    button = Button(frame, text=text, padx=10, pady=10, command=command, font=button_font, fg=button_fg_color)
    button.grid(row=row_value, column=column_value, padx=5, pady=5, ipadx=5, ipady=5, sticky='nsew')
    return button


# Create a function to handle the "New" menu item
def new_operation():
    # Reset the calculator for a new operation
    entry.delete(0, END)
    conversion_entry.delete(0, END)
    calculation_done = False


# Create a function to handle the "Save" menu item
def save_operation():
    # Wala pa hahaha
    pass


# Create a function to handle the "Open" menu item
def open_operation():
    # Awan pay metlang
    pass


# Create a function to handle the "Export" menu item
def export_operation():
    # None pa
    pass


# Create a function to handle the "Exit" menu item
def exit_application():
    # Close the application
    root.quit()


# Create a function to handle the "Copy" menu item
def copy_value():
    # Copy the current value to clipboard
    copied_value = entry.get()
    root.clipboard_clear()
    root.clipboard_append(copied_value)
    root.update()
    messagebox.showinfo("Copied", "Entry value has been copied to clipboard.")


# Create a function to handle the "Paste" menu item
def paste_value():
    # Paste the value from the clipboard
    clipboard_text = root.clipboard_get()
    entry.insert(INSERT, clipboard_text)


# Create a function to handle the "Basic" menu item
# Create variables to track the visibility state of the conversion frame and related widgets
conversion_frame_visible = False
conversion_label_visible = False
conversion_entry_visible = False


def switch_to_basic_calculator():
    global conversion_frame_visible, conversion_label_visible, conversion_entry_visible

    # Save the visibility state of the conversion frame and related widgets
    conversion_frame_visible = conversion_frame.winfo_manager() != ""
    conversion_label_visible = conversion_label.winfo_manager() != ""
    conversion_entry_visible = conversion_entry.winfo_manager() != ""

    # Hide the conversion frame, conversion label, and conversion entry
    conversion_frame.grid_remove()
    conversion_label.grid_remove()
    conversion_entry.grid_remove()
    toggle_conversion_button.grid_remove()


def switch_to_programmer_calculator():
    global conversion_frame_visible, conversion_label_visible, conversion_entry_visible

    # Restore the visibility state of the conversion frame and related widgets
    if conversion_frame_visible:
        conversion_frame.grid()
    if conversion_label_visible:
        conversion_label.grid()
    if conversion_entry_visible:
        conversion_entry.grid()
    toggle_conversion_button.grid()


themes = {
    "Default": {"bg": "wheat", "fg": "black"},
    "Dark Mode": {"bg": "black", "fg": "white"},
    "Blue Theme": {"bg": "blue", "fg": "white"},
    "Green Theme": {"bg": "green", "fg": "black"},
}


# Create a function to handle the "Themes" menu item
def change_theme():
    # Create a new window for theme selection
    theme_window = Toplevel(root)
    theme_window.title("Select Theme")

    # Create a StringVar to store the selected theme
    selected_theme = StringVar()
    selected_theme.set("Default")  # Set the initial theme

    # Create radio buttons for each theme
    for theme_name in themes.keys():
        Radiobutton(theme_window, text=theme_name, variable=selected_theme, value=theme_name).pack()

    # Create a button to apply the selected theme
    apply_button = Button(theme_window, text="Apply Theme", command=lambda: apply_theme(selected_theme.get()))
    apply_button.pack()


def apply_theme(theme_name):
    global button_fg_color

    # Get the selected theme colors
    theme_colors = themes.get(theme_name)

    if theme_colors:
        # Update the button foreground color based on the selected theme
        button_fg_color = theme_colors["fg"]

        # Update the background color of the main window (root)
        root.configure(background=theme_colors["bg"])

        # Apply the new button foreground color to existing buttons
        for widget in root.winfo_children():
            if isinstance(widget, Button):
                widget.config(fg=button_fg_color)


# Create a function to handle the "About" menu item
def about_application():
    # Display information about the calculator application
    messagebox.showinfo("About",
                        "Calculator ni Rizal\nVersion 1.3\nDeveloped by Stelios Longboan and Nymfha Sugando\nBSIT 2A")


# Create the main window
root = Tk()
root.title("Calculator with Conversion")
root.config(background="wheat")
root.maxsize(500, 800)
root.minsize(400, 500)

# Create a menu bar
menu_bar = Menu(root)
root.config(menu=menu_bar)

# Create File menu
file_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="New", command=new_operation)
file_menu.add_command(label="Save", command=save_operation)
file_menu.add_command(label="Open", command=open_operation)
file_menu.add_command(label="Export", command=export_operation)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=exit_application)

# Create Edit menu
edit_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Edit", menu=edit_menu)
edit_menu.add_command(label="Undo")
edit_menu.add_command(label="Redo")
edit_menu.add_separator()
edit_menu.add_command(label="Copy", command=copy_value)
edit_menu.add_command(label="Paste", command=paste_value)

# Create View menu
view_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="View", menu=view_menu)
view_menu.add_command(label="Basic", command=switch_to_basic_calculator)
view_menu.add_command(label="Scientific")
view_menu.add_command(label="Programmer", command=switch_to_programmer_calculator)
view_menu.add_checkbutton(label="History")

# Create Options menu
options_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Options", menu=options_menu)
options_menu.add_command(label="Settings")
options_menu.add_command(label="Themes", command=change_theme)

# Create Help menu
help_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Help", menu=help_menu)
help_menu.add_command(label="User Guide")
help_menu.add_command(label="About", command=about_application)
help_menu.add_command(label="Check for Updates")

# Create labels for the entry fields
entry_label = Label(root, text="Enter Number:", font="Helvetica 12", bg="wheat")
entry_label.grid(row=0, column=0, columnspan=4, padx=5, pady=(20, 5), sticky='nsew')

# Entry field for displaying numbers
entry = Entry(root, width=30, font="Helvetica 13")
entry.grid(row=1, column=0, columnspan=4, padx=5, pady=5, ipadx=5, ipady=5, sticky='nsew')

conversion_label = Label(root, text="Converted Result:", font="Helvetica 12", bg="wheat")
conversion_label.grid(row=4, column=0, columnspan=4, padx=5, pady=(10, 5), sticky='nsew')

# Entry field for displaying conversions
conversion_font = ("Arial", 13)
conversion_fg_color = "red"
conversion_entry = Entry(root, width=15, font=conversion_font, fg=conversion_fg_color, )
conversion_entry.grid(row=5, column=0, columnspan=4, padx=5, pady=5, ipadx=5, ipady=5, sticky='nsew')

# We changed how we print the buttons 'cause we incorporated to a frame, and it messes with it a lot T_T
# Define button font and foreground color
button_font = ("Helvetica", 12)
button_fg_color = "black"

# Button labels
numeric_buttons = [
    '7', '8', '9',
    '4', '5', '6',
    '1', '2', '3',
    '0', '.'
]

operator_buttons = [
    '/', '*', '-', '+'
]

special_buttons = [
    '     =     ', 'Clear', 'Toggle Conversion'
]

# Create frames for the buttons
numeric_frame = Frame(root, bg="cornsilk")
numeric_frame.grid(row=2, column=0, columnspan=3, padx=5, pady=5, ipadx=1, ipady=1, sticky='nsew')

operator_frame = Frame(root, bg="burlywood")
operator_frame.grid(row=2, column=3, padx=5, pady=5, ipadx=5, ipady=5, sticky='nsew')

special_frame = Frame(root, bg="cadetblue")
special_frame.grid(row=3, column=0, columnspan=4, padx=5, pady=5, ipadx=5, ipady=5, sticky='nsew')

# Reset row_value and column_value for numeric buttons
row_value = 0
column_value = 0

# Create numeric buttons
for button in numeric_buttons:
    create_button(numeric_frame, button, lambda l=button: button_click(l)).grid(row=row_value, column=column_value,
                                                                                padx=5, pady=5, ipadx=5, ipady=5,
                                                                                sticky='nsew')
    column_value += 1
    if column_value > 2:
        column_value = 0
        row_value += 1

# Reset row_value and column_value for operator buttons
row_value = 0
column_value = 0

# Create operator buttons
for button in operator_buttons:
    create_button(operator_frame, button, lambda l=button: button_click(l)).grid(row=row_value, column=column_value,
                                                                                 padx=5, pady=5, ipadx=5, ipady=5,
                                                                                 sticky='nsew')
    row_value += 1

# Reset row_value and column_value for special buttons
row_value = 0
column_value = 0

# Create special buttons
for button in special_buttons:
    if button == 'Toggle Conversion':
        toggle_conversion_button = create_button(special_frame, button, show_conversion_frame)
        toggle_conversion_button.grid(row=row_value, column=column_value, padx=5, pady=5, ipadx=5, ipady=5,
                                      sticky='nsew')
    else:
        create_button(special_frame, button, clear if button == 'Clear' else calculate).grid(row=row_value,
                                                                                             column=column_value,
                                                                                             padx=5,
                                                                                             pady=5, ipadx=5, ipady=5,
                                                                                             sticky='nsew')
    column_value += 1

# Create a frame for number system conversion
conversion_frame = Frame(root, bg="wheat")
conversion_frame.grid_remove()  # Initially, hide the conversion frame

# Number system conversion radio buttons
base_var = IntVar()
base_var.set(0)  # Default na selected sa Radio Buttons is Decimal
conversion_labels = ['Decimal', 'Binary', 'Octal', 'Hexadecimal']

for i, label in enumerate(conversion_labels):
    radio_button = Radiobutton(conversion_frame, text=label, variable=base_var, value=i, font=("Helvetica", 10),
                               bg="wheat", command=convert_number_system)
    radio_button.grid(row=i, column=0, padx=5, pady=5, sticky='w')

# # Create a button to perform the conversion
# convert_button = create_button(conversion_frame, "Convert", convert_number_system)
# convert_button.grid(row=len(conversion_labels), column=0, padx=5, pady=5, sticky='nsew')

# Create a button to copy the converted value
copy_button = create_button(conversion_frame, "Copy Converted Results", copy_converted_value)
copy_button.grid(row=5, column=0, padx=5, pady=5, sticky='se')

# Create a Text widget to display the note
note_text = """Note: You can just select the conversion unit and the result will appear in the box."""
note_display = Text(conversion_frame, height=2, width=60, wrap=WORD, font=("Helvetica", 10))
note_display.insert(INSERT, note_text)
note_display.config(state=DISABLED)  # Disable text editing

# Grid placement for the note Text widget
note_display.grid(row=4, column=0, padx=5, pady=5, sticky='nsew')

# Configure grid weights to make elements expandable
for i in range(4):
    root.grid_rowconfigure(i, weight=1)
    root.grid_columnconfigure(i, weight=1)

# # Call switch_to_basic_calculator to set the initial state to "Basic"
# switch_to_basic_calculator()


# Run the main loop
root.mainloop()
