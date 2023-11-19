import string
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from ttkthemes import ThemedTk
from pymongo import MongoClient
import re
from PIL import Image, ImageTk
from ttkthemes.themed_style import ThemedStyle
import subprocess

# MongoDB connection
client = MongoClient(
    'mongodb+srv://steliosashbeey:matatag123@cluster0.gnoyesb.mongodb.net/')
db = client['sad']
users_collection = db['sad']


def register_user(email, username, password):
    user_data = {
        'email': email.lower(),
        'username': username.lower(),
        'password': password
    }
    users_collection.insert_one(user_data)


def is_email_valid(email):
    lower_email = email.lower()
    return re.match(r"[^@]+@[^@]+\.[^@]+", lower_email) is not None


def is_username_available(username):
    return users_collection.find_one({'username': username}) is None


def is_email_available(email):
    lower_email = email.lower()
    return users_collection.find_one({'email': lower_email}) is None


class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.iconbitmap("ico.ico")
        self.root.title("Shrek's Playground")

        self.set_background_image()

        window_width = 400
        window_height = 600
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.root.geometry(f"400x600+{x}+{y}")

        self.root.resizable(False, False)

        self.create_widgets()

    def set_background_image(self):
        background_image = Image.open("bgg.jpg")
        background_image = background_image.resize((400, 600))
        self.background_image = ImageTk.PhotoImage(background_image)
        background_label = ttk.Label(self.root, image=self.background_image)
        background_label.place(relwidth=1, relheight=1)

    def create_widgets(self):
        button_style = ttk.Style()
        button_style.configure("TButton", font=("Helvetica", 11, "bold"))

        logo_image = Image.open("icon.jpg")
        logo_image = logo_image.resize((150, 150))
        self.logo_image = ImageTk.PhotoImage(logo_image)
        logo_label = ttk.Label(self.root, image=self.logo_image)
        logo_label.place(relx=0.5, rely=0.2, anchor="center")

        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()

        ttk.Label(self.root, text="Username:", font=("Helvetica", 12)).place(relx=0.35, rely=0.35, anchor="e")
        ttk.Entry(self.root, textvariable=self.username_var, width=25, font=("Helvetica", 14)).place(relx=0.5, rely=0.4,
                                                                                                     anchor="center")

        ttk.Label(self.root, text="Password:", font=("Helvetica", 12)).place(relx=0.35, rely=0.45, anchor="e")
        ttk.Entry(self.root, textvariable=self.password_var, show='*', width=25, font=("Helvetica", 14)).place(relx=0.5,
                                                                                                               rely=0.5,
                                                                                                               anchor="center")
        ttk.Button(self.root, text="Login", command=self.login, width=15, style='TButton', padding=(10, 5)).place(
            relx=0.5, rely=0.6, anchor="center")
        label_reg = ttk.Label(self.root, text="Don't have an account?", font=("Helvetica", 12))
        label_reg.place(relx=0.3, rely=0.7, anchor="center")
        label_reg.configure(style="TLabel")

        ttk.Button(self.root, text="Register", command=self.show_registration_window, width=15, style='TButton',
                   padding=(10, 5)).place(relx=0.7, rely=0.7, anchor="center")

        ttk.Button(self.root, text="Forgot Password?", command=self.forgot_password, width=20, style='TButton',
                   padding=(10, 5)).place(relx=0.5, rely=0.8, anchor="center")

    def login(self):
        username = self.username_var.get().lower()
        password = self.password_var.get()

        if self.login_user(username, password):
            player_name = self.get_player_name(username)
            self.show_dashboard(player_name)
        else:
            messagebox.showerror("Error", "Login failed. Invalid username or password.")

    def get_player_name(self, username):
        user_data = users_collection.find_one({'username': username})
        if user_data and 'player_name' in user_data:
            return user_data['player_name']
        else:
            player_name = simpledialog.askstring("Player Name", "Enter your player name:")
            while player_name:
                if len(player_name) > 12:
                    messagebox.showerror("Error", "Player name cannot exceed 12 characters.")
                    player_name = simpledialog.askstring("Player Name", "Enter your player name:")
                elif users_collection.find_one({'player_name': player_name}):
                    messagebox.showerror("Error", "Player name already exists. Please choose a different one.")
                    player_name = simpledialog.askstring("Player Name", "Enter your player name:")
                else:
                    users_collection.update_one({'username': username}, {'$set': {'player_name': player_name}})
                    return player_name
            else:
                return "Guest"

    def show_dashboard(self, player_name):
        self.root.withdraw()

        dashboard_root = tk.Toplevel(self.root)
        dashboard_root.title("Dashboard")

        dashboard_width = 800
        dashboard_height = 600
        x = self.root.winfo_x() + (self.root.winfo_width() - dashboard_width) // 2
        y = self.root.winfo_y() + (self.root.winfo_height() - dashboard_height) // 2
        dashboard_root.geometry(f"800x600+{x}+{y}")

        dashboard_app = DashboardApp(dashboard_root, player_name)

    def login_user(self, username, password):
        username_lower = username.lower()
        user_data = users_collection.find_one({'username': username_lower, 'password': password})
        return user_data is not None

    def show_registration_window(self):
        self.root.withdraw()

        registration_root = tk.Toplevel(self.root)
        registration_root.title("Registration")

        registration_width = 400
        registration_height = 600
        x = self.root.winfo_x() + (self.root.winfo_width() - registration_width) // 2
        y = self.root.winfo_y() + (self.root.winfo_height() - registration_height) // 2
        registration_root.geometry(f"400x600+{x}+{y}")

        registration_app = RegistrationApp(registration_root, self)

    def show_login_window(self):
        # Show the login window
        self.root.deiconify()

    def forgot_password(self):
        forgot_password_dialog = tk.Toplevel(self.root)
        forgot_password_dialog.title("Forgot Password")

        dialog_width = 300
        dialog_height = 200
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - dialog_width) // 2
        y = (screen_height - dialog_height) // 2
        forgot_password_dialog.geometry(f"{dialog_width}x{dialog_height}+{x}+{y}")

        ttk.Label(forgot_password_dialog, text="Enter your email:").place(relx=0.5, rely=0.2, anchor="center")
        email_var = tk.StringVar()
        email_entry = ttk.Entry(forgot_password_dialog, textvariable=email_var)
        email_entry.place(relx=0.5, rely=0.3, anchor="center")

        def ok_button_handler():
            email = email_var.get().lower()

            if not email:
                messagebox.showerror("Error", "Email cannot be empty.")
                return

            if not is_email_valid(email):
                messagebox.showerror("Error", "Invalid email format.")
                return

            user_data = users_collection.find_one({'email': email})
            if user_data:
                new_password = simpledialog.askstring("Forgot Password", "Enter your new password:",
                                                      parent=forgot_password_dialog, show='*')

                if new_password:
                    users_collection.update_one({'email': email}, {'$set': {'password': new_password}})
                    messagebox.showinfo("Success", "Password reset successful!")
                    forgot_password_dialog.destroy()
                else:
                    messagebox.showerror("Error", "Invalid new password.")
            else:
                messagebox.showerror("Error", "Email not found.")

        ttk.Button(forgot_password_dialog, text="OK", command=ok_button_handler).place(relx=0.5, rely=0.5,
                                                                                       anchor="center")

        ttk.Button(forgot_password_dialog, text="Cancel", command=forgot_password_dialog.destroy).place(relx=0.5,
                                                                                                        rely=0.7,
                                                                                                        anchor="center")

        forgot_password_dialog.transient(self.root)
        forgot_password_dialog.grab_set()
        self.root.wait_window(forgot_password_dialog)


class RegistrationApp:
    def __init__(self, root, login_app):
        self.root = root
        self.root.iconbitmap("ico.ico")
        self.root.title("Registration ng mga Shrek Babies")

        self.login_app = login_app

        self.email_var = tk.StringVar()
        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.confirm_password_var = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        ttk.Label(self.root, text="Email:", font=("Helvetica", 12)).place(relx=0.5, rely=0.2, anchor="e")
        ttk.Entry(self.root, textvariable=self.email_var).place(relx=0.5, rely=0.2, anchor="w")

        ttk.Label(self.root, text="Username:", font=("Helvetica", 12)).place(relx=0.5, rely=0.3, anchor="e")
        ttk.Entry(self.root, textvariable=self.username_var).place(relx=0.5, rely=0.3, anchor="w")

        ttk.Label(self.root, text="Password:", font=("Helvetica", 12)).place(relx=0.5, rely=0.4, anchor="e")
        ttk.Entry(self.root, textvariable=self.password_var, show='*').place(relx=0.5, rely=0.4, anchor="w")

        ttk.Label(self.root, text="Confirm Password:", font=("Helvetica", 12)).place(relx=0.5, rely=0.5, anchor="e")
        ttk.Entry(self.root, textvariable=self.confirm_password_var, show='*').place(relx=0.5, rely=0.5, anchor="w")

        ttk.Button(self.root, text="Register", command=self.register).place(relx=0.5, rely=0.6, anchor="center")

        label_login = ttk.Label(self.root, text="Already have an account?", font=("Helvetica", 12))
        label_login.place(relx=0.5, rely=0.7, anchor="center")
        label_login.configure(style="TLabel")

        ttk.Button(self.root, text="Login", command=self.go_back_to_login).place(relx=0.5, rely=0.75, anchor="center")

    def register(self):
        email = self.email_var.get()
        username = self.username_var.get()
        password = self.password_var.get()
        confirm_password = self.confirm_password_var.get()

        if not is_email_valid(email):
            messagebox.showerror("Error", "Invalid email format.")
            return

        if not is_email_available(email):
            messagebox.showerror("Error", "Email is already taken.")
            return

        if not is_username_available(username):
            messagebox.showerror("Error", "Username is already taken.")
            return

        validation_result = self.validate_password(password)
        if not validation_result["is_valid"]:
            messagebox.showerror("Error", validation_result["message"])
            self.root.withdraw()
            self.root.after(0, self.root.deiconify)
            return

        if len(password) < 8 or password != confirm_password:
            messagebox.showerror("Error", "Password must be at least 8 characters and match.")
            self.root.withdraw()
            self.root.after(0, self.root.deiconify)
            return

        register_user(email, username, password)
        messagebox.showinfo("Success", "Registration successful!")
        self.go_back()

    def validate_password(self, password):
        if not any(char.isupper() for char in password):
            return {"is_valid": False, "message": "Password must contain at least one uppercase letter."}

        if not any(char in string.punctuation for char in password):
            return {"is_valid": False, "message": "Password must contain at least one special symbol."}

        if not any(char.isdigit() for char in password):
            return {"is_valid": False, "message": "Password must contain at least one digit."}

        if not any(char.isupper() for char in password):
            return {"is_valid": False, "message": "Password must contain at least one uppercase letter."}

        if not any(char in string.punctuation for char in password):
            return {"is_valid": False, "message": "Password must contain at least one special symbol."}

        if not any(char.isdigit() for char in password):
            return {"is_valid": False, "message": "Password must contain at least one digit."}

        return {"is_valid": True, "message": "Password meets the requirements."}

    def go_back(self):
        self.root.destroy()
        self.login_app.show_login_window()
        self.login_app.root.deiconify()

    def go_back_to_login(self):
        self.root.destroy()
        self.login_app.show_login_window()


class DashboardApp:
    def __init__(self, root, player_name):
        self.root = root
        self.root.iconbitmap("ico.ico")
        self.root.title("Shrek Games")

        self.set_background()
        self.player_name = player_name
        self.following_list = self.get_following_list_from_db()

        window_width = 800
        window_height = 600
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.root.geometry(f"800x600+{x}+{y}")

        self.apply_custom_theme()

        self.root.resizable(False, False)

        self.icon1 = self.load_and_resize_icon("dont.png", (150, 200))
        self.icon2 = self.load_and_resize_icon("brawl.jpg", (150, 200))
        self.icon3 = self.load_and_resize_icon("snow.png", (70, 90))
        self.icon4 = self.load_and_resize_icon("snake.jpg", (70, 90))
        self.icon5 = self.load_and_resize_icon("pacman.png", (70, 90))

        icon_button1 = ttk.Button(self.root, image=self.icon1, command=self.run_python_file3)
        icon_button1.place(relx=0.45, rely=0.2, anchor="center")

        icon_button2 = ttk.Button(self.root, image=self.icon2, command=self.run_python_file5)
        icon_button2.place(relx=0.75, rely=0.2, anchor="center")

        icon_button3 = ttk.Button(self.root, image=self.icon3, command=self.run_python_file4)
        icon_button3.place(relx=0.4, rely=0.7, anchor="center")

        icon_button4 = ttk.Button(self.root, image=self.icon4, command=self.run_python_file1)
        icon_button4.place(relx=0.6, rely=0.7, anchor="center")

        icon_button5 = ttk.Button(self.root, image=self.icon5, command=self.run_python_file2)
        icon_button5.place(relx=0.8, rely=0.7, anchor="center")

        self.create_icon_label(self.root, "Don't Touch My Presents", "By Goodgis\n\nWASD/Arrow Keys - Move",
                               0.33, 0.4)
        self.create_icon_label(self.root, "Brawler",
                               "By Coding With Russ\n\nWASD/Arrow Keys - Move\nR and T - P1 Attack | Num1 and Num2 - P2 Attack",
                               0.63, 0.4)
        self.create_icon_label(self.root, "Sno Snow", "By Barji\n\nCatch the white snow!\nWASD - Move\nESC - Exit",
                               0.34, 0.8)
        self.create_icon_label(self.root, "Snake Game", "By BroCode\n\nArrow Keys - Move\nESC - Exit", 0.54, 0.8)
        self.create_icon_label(self.root, "PacMan", "From Python FreeGame\n\nArrow Keys - Move\nESC - Exit", 0.74, 0.8)

        self.sidebar_frame = ttk.Frame(self.root, width=200, style="Sidebar.TFrame")
        self.sidebar_frame.pack(side="left", fill="y")

        welcome_label = ttk.Label(self.sidebar_frame, text=f"Hello, {player_name}!", font=("Helvetica", 14, "bold"),
                                  foreground="black", style="Sidebar.TLabel")
        welcome_label.pack(pady=10, padx=10, anchor="w")

        change_name_button = ttk.Button(self.sidebar_frame, text="Change Player Name",
                                        command=self.open_change_name_window)
        change_name_button.pack(pady=10, padx=10, anchor="w")

        search_button = ttk.Button(self.sidebar_frame, text="Search Users", command=self.open_search_window)
        search_button.pack(pady=20, padx=10, anchor="w")

        following_list_button = ttk.Button(self.sidebar_frame, text="Following List", command=self.show_following_list)
        following_list_button.pack(pady=10, padx=10, anchor="w")

        logout_button = ttk.Button(self.sidebar_frame, text="Logout", command=self.log_out_function)
        logout_button.pack(side="bottom", pady=10, padx=10, anchor="w")

        change_password_button = ttk.Button(self.sidebar_frame, text="Change Password",
                                            command=self.open_change_password_window)
        change_password_button.pack(side="bottom", pady=10, padx=10, anchor="w")

        self.following_list = self.get_following_list_from_db() or set()

        self.set_background()

    def create_icon_label(self, parent_frame, label_text, description_text, relx, rely):
        label = ttk.Label(parent_frame, text=label_text, font=("Helvetica", 12, "bold"))
        label.place(relx=relx, rely=rely)

        description_label = ttk.Label(parent_frame, text=description_text, font=("Helvetica", 9))
        description_label.place(relx=relx, rely=rely + 0.05)

    def load_and_resize_icon(self, filename, size):
        original_icon = Image.open(filename)
        resized_icon = original_icon.resize(size)
        return ImageTk.PhotoImage(resized_icon)

    def run_python_file1(self):
        subprocess.run(["python", "snake2.py"])

    def run_python_file2(self):
        subprocess.run(["python", "pacman.py"])

    def run_python_file3(self):
        script_path = "dont/main.py"
        subprocess.run(["python", script_path])

    def run_python_file4(self):
        script_path = "snow/SnoSnow.py"
        subprocess.run(["python", script_path])

    def run_python_file5(self):
        script_path = "brawler/main.py"
        subprocess.run(["python", script_path])

    def set_background(self):
        background_color = "#F0F0F0"
        self.root.configure(bg=background_color)

        self.root.style = ttk.Style(self.root)
        self.root.style.configure("IconButton.TButton", background=background_color, font=("Helvetica", 11, "bold"))
        self.root.style.configure("Sidebar.TFrame", background="#333333")


    def apply_custom_theme(self):
        style = ThemedStyle(self.root)
        style.set_theme("arc")

        style.configure("TLabel", font=("Helvetica", 14, "bold"), background=style.lookup("TFrame", "background"))
        style.configure("TButton", font=("Helvetica", 11, "bold"))

        style.configure("Sidebar.TFrame", background=style.lookup("TFrame", "background"))
        style.configure("Sidebar.TLabel", foreground="white")

        style.configure("SearchWindow.TFrame", background=style.lookup("TFrame", "background"))

        style.configure("FollowingListWindow.TFrame", background=style.lookup("TFrame", "background"))
        style.configure("FollowingListWindow.TLabel", font=("Helvetica", 12),
                        background=style.lookup("TFrame", "background"))

    def open_change_name_window(self):
        change_name_window = tk.Toplevel(self.root)
        change_name_window.title("Change Player Name")

        change_name_window_width = 300
        change_name_window_height = 200
        x = self.root.winfo_x() + (self.root.winfo_width() - change_name_window_width) // 2
        y = self.root.winfo_y() + (self.root.winfo_height() - change_name_window_height) // 2
        change_name_window.geometry(f"{change_name_window_width}x{change_name_window_height}+{x}+{y}")

        change_name_window.resizable(False, False)

        new_name_var = tk.StringVar()
        ttk.Label(change_name_window, text="Enter your new player name:").pack(pady=10)
        ttk.Entry(change_name_window, textvariable=new_name_var, font=("Helvetica", 12)).pack(pady=10)

        confirm_button = ttk.Button(change_name_window, text="Confirm",
                                    command=lambda: self.change_player_name(new_name_var.get(), change_name_window))
        confirm_button.pack(pady=10)

    def change_player_name(self, new_player_name, change_name_window):
        if not new_player_name:
            messagebox.showerror("Error", "Player name cannot be empty.")
            return

        if len(new_player_name) > 12:
            messagebox.showerror("Error", "Player name cannot exceed 12 characters.")
            return

        if users_collection.find_one({'player_name': new_player_name}):
            messagebox.showerror("Error", "Player name already exists. Please choose a different one.")
            return

        users_collection.update_one({'player_name': self.player_name}, {'$set': {'player_name': new_player_name}})

        old_player_name = self.player_name
        self.player_name = new_player_name

        self.update_welcome_label()

        if old_player_name in self.following_list:
            self.following_list.remove(old_player_name)
            self.following_list.add(new_player_name)

        self.save_following_list_to_db()

        for follower_data in users_collection.find({'following_list': {'$in': [old_player_name]}}):
            follower_following_list = follower_data.get('following_list', [])
            follower_following_list.remove(old_player_name)
            follower_following_list.append(new_player_name)
            users_collection.update_one({'player_name': follower_data['player_name']},
                                        {'$set': {'following_list': follower_following_list}})

        messagebox.showinfo("Success", f"Player name changed to {new_player_name}.")

        change_name_window.destroy()

    def update_welcome_label(self):
        for widget in self.sidebar_frame.winfo_children():
            if isinstance(widget, ttk.Label) and widget.cget("text").startswith("Hello"):
                widget.configure(text=f"Hello, {self.player_name}!")

    def get_following_list_from_db(self):
        user_data = users_collection.find_one({'player_name': self.player_name})
        return set(user_data.get('following_list', [])) if user_data else set()

    def save_following_list_to_db(self):
        users_collection.update_one({'player_name': self.player_name},
                                    {'$set': {'following_list': list(self.following_list)}})

    def open_search_window(self):
        search_window = tk.Toplevel(self.root)
        search_window.title("Search User")

        search_window_width = 300
        search_window_height = 200
        x = self.root.winfo_x() + (self.root.winfo_width() - search_window_width) // 2
        y = self.root.winfo_y() + (self.root.winfo_height() - search_window_height) // 2
        search_window.geometry(f"{search_window_width}x{search_window_height}+{x}+{y}")

        search_window.resizable(False, False)

        search_entry = ttk.Entry(search_window, font=("Helvetica", 12))
        search_entry.pack(pady=10, padx=10)

        search_button = ttk.Button(search_window, text="Follow",
                                   command=lambda: self.search_and_follow(search_entry.get(), search_window))
        search_button.pack(pady=10, padx=10)

    def search_and_follow(self, player_name, search_window):
        user_data = users_collection.find_one({'player_name': player_name})

        if user_data and 'player_name' in user_data:
            if player_name not in self.following_list:
                self.following_list.add(player_name)

                self.save_following_list_to_db()

                messagebox.showinfo("Follow", f"You are now following {player_name}.")
            else:
                messagebox.showinfo("Follow", f"You are already following {player_name}.")
        else:
            messagebox.showinfo("Follow", f"User {player_name} not found.")

        search_window.destroy()

        self.show_following_list()

    def follow_user(self, player_name):
        user_data = users_collection.find_one({'player_name': player_name})

        if user_data and 'player_name' in user_data:
            if player_name not in self.following_list:
                self.following_list.add(player_name)

                self.save_following_list_to_db()

                messagebox.showinfo("Follow", f"You are now following {player_name}.")
            else:
                messagebox.showinfo("Follow", f"You are already following {player_name}.")
        else:
            messagebox.showinfo("Follow", f"User {player_name} not found.")

        self.show_following_list()

    def show_following_list(self):
        following_list_window = tk.Toplevel(self.root)
        following_list_window.title("Following List")

        following_list_window_width = 300
        following_list_window_height = 200
        x = self.root.winfo_x() + (self.root.winfo_width() - following_list_window_width) // 2
        y = self.root.winfo_y() + (self.root.winfo_height() - following_list_window_height) // 2
        following_list_window.geometry(f"{following_list_window_width}x{following_list_window_height}+{x}+{y}")

        if self.following_list:
            ttk.Label(following_list_window, text="Following List:", font=("Helvetica", 12)).pack(pady=10)

            for player_name in self.following_list:
                player_frame = ttk.Frame(following_list_window)
                player_frame.pack(pady=5)

                ttk.Label(player_frame, text=f"Name: {player_name}", font=("Helvetica", 13)).pack(side="left")

                ttk.Label(player_frame, text=" ", font=("Helvetica", 10)).pack(side="left")

                ttk.Button(player_frame, text="Unfollow",
                           command=lambda name=player_name, window=following_list_window: self.unfollow_user(name,
                                                                                                             window)).pack(
                    side="left")

        else:
            ttk.Label(following_list_window, text="You are not following anyone yet.", font=("Helvetica", 12)).pack(
                pady=20)

        following_list_window.protocol("WM_DELETE_WINDOW",
                                       lambda: self.on_following_list_window_close(following_list_window))

    def on_following_list_window_close(self, following_list_window):
        self.save_following_list_to_db()

        following_list_window.destroy()

    def unfollow_user(self, player_name, following_list_window):
        self.following_list.discard(player_name)

        self.save_following_list_to_db()

        messagebox.showinfo("Unfollow", f"You have unfollowed {player_name}.")

        following_list_window.destroy()

        self.show_following_list()

    def validate_password(self, password):
        # Check if password has at least one uppercase letter
        if not any(char.isupper() for char in password):
            return {"is_valid": False, "message": "Password must contain at least one uppercase letter."}

        # Check if password has at least one special symbol
        if not any(char in string.punctuation for char in password):
            return {"is_valid": False, "message": "Password must contain at least one special symbol."}

        # Check if password has at least one digit
        if not any(char.isdigit() for char in password):
            return {"is_valid": False, "message": "Password must contain at least one digit."}

        return {"is_valid": True, "message": "Password meets the requirements."}

    def change_password(self, old_password, new_password, confirm_password, change_password_window):
        user_data = users_collection.find_one({'player_name': self.player_name})
        stored_password = user_data.get('password', '') if user_data else ''

        if old_password != stored_password:
            messagebox.showerror("Error", "Incorrect old password.")
            return

        password_validation_result = self.validate_password(new_password)
        if not password_validation_result["is_valid"]:
            messagebox.showerror("Error", password_validation_result["message"])
            return

        if new_password != confirm_password:
            messagebox.showerror("Error", "New password and confirmation do not match.")
            return

        users_collection.update_one({'player_name': self.player_name}, {'$set': {'password': new_password}})

        messagebox.showinfo("Success", "Password changed successfully.")

        change_password_window.destroy()

    def open_change_password_window(self):
        change_password_window = tk.Toplevel(self.root)
        change_password_window.title("Change Password")

        change_password_window_width = 400
        change_password_window_height = 350
        x = self.root.winfo_x() + (self.root.winfo_width() - change_password_window_width) // 2
        y = self.root.winfo_y() + (self.root.winfo_height() - change_password_window_height) // 2
        change_password_window.geometry(f"{change_password_window_width}x{change_password_window_height}+{x}+{y}")

        old_password_var = tk.StringVar()
        new_password_var = tk.StringVar()
        confirm_password_var = tk.StringVar()

        change_password_window.resizable(False, False)

        ttk.Label(change_password_window, text="Old Password:").pack(pady=10)
        ttk.Entry(change_password_window, textvariable=old_password_var, show="*", font=("Helvetica", 12)).pack(pady=10)

        ttk.Label(change_password_window, text="New Password:").pack(pady=10)
        ttk.Entry(change_password_window, textvariable=new_password_var, show="*", font=("Helvetica", 12)).pack(pady=10)

        ttk.Label(change_password_window, text="Confirm Password:").pack(pady=10)
        ttk.Entry(change_password_window, textvariable=confirm_password_var, show="*", font=("Helvetica", 12)).pack(
            pady=10)

        confirm_button = ttk.Button(change_password_window, text="Confirm",
                                    command=lambda: self.change_password(old_password_var.get(), new_password_var.get(),
                                                                         confirm_password_var.get(),
                                                                         change_password_window))
        confirm_button.pack(pady=10)

    def log_out_function(self):
        self.save_following_list_to_db()
        self.root.destroy()
        app.show_login_window()


if __name__ == "__main__":
    root = ThemedTk(theme="arc")
    app = LoginApp(root)
    root.mainloop()
