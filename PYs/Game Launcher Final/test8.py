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



class DashboardApp:
    def __init__(self, root, player_name):
        self.root = root
        self.root.iconbitmap("ico.ico")
        self.root.title("Dashboard")

        # Set background image or color
        self.set_background()

        # Store the player_name as an instance variable
        self.player_name = player_name

        # Initialize the following list by retrieving it from the database
        self.following_list = self.get_following_list_from_db()

        # Center the window on the screen
        window_width = 800
        window_height = 600
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.root.geometry(f"800x600+{x}+{y}")

        self.apply_custom_theme()

        self.root.resizable(True, True)

        # Load and resize icons
        self.icon1 = self.load_and_resize_icon("dont.png", (150, 200))
        self.icon2 = self.load_and_resize_icon("brawl.jpg", (150, 200))
        self.icon3 = self.load_and_resize_icon("snow.png", (70, 90))
        self.icon4 = self.load_and_resize_icon("snake.jpg", (70, 90))
        self.icon5 = self.load_and_resize_icon("pacman.png", (70, 90))


        # Create buttons with icons and place them directly on the root window
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


        # Create labels and descriptions for each icon below the icons
        self.create_icon_label(self.root, "Don't Touch My Presents", "By Goodgis\n\nWASD/Arrow Keys - Move\nESC - Exit", 0.33, 0.4)
        self.create_icon_label(self.root, "Brawler", "By Coding With Russ\n\nWASD/Arrow Keys - Move\nR and T - P1 Attack | Num1 and Num2 - P2 Attack\nESC - Exit", 0.63, 0.4)
        self.create_icon_label(self.root, "Sno Snow", "By Barji\n\nCatch the white snow!\nWASD - Move\nESC - Exit", 0.34, 0.8)
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
        # Replace "your_script1.py" with the actual filename you want to run
        subprocess.run(["python", "snake2.py"])

    def run_python_file2(self):
        # Replace "your_script2.py" with the actual filename you want to run
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
        # Add code to set the background image or color for the dashboard
        # Example:
        background_color = "#F0F0F0"  # Light gray background color
        self.root.configure(bg=background_color)

        # Set the style for the icon buttons
        self.root.style = ttk.Style(self.root)
        self.root.style.configure("IconButton.TButton", background=background_color, font=("Helvetica", 11, "bold"))
        self.root.style.configure("Sidebar.TFrame", background="#333333")

    def open_change_password_window(self):
        # Create a new window for changing the password
        change_password_window = tk.Toplevel(self.root)
        change_password_window.title("Change Password")

        # Set the size of the change password window
        change_password_window_width = 400
        change_password_window_height = 350
        x = self.root.winfo_x() + (self.root.winfo_width() - change_password_window_width) // 2
        y = self.root.winfo_y() + (self.root.winfo_height() - change_password_window_height) // 2
        change_password_window.geometry(f"{change_password_window_width}x{change_password_window_height}+{x}+{y}")

        # Entry fields for old, new, and confirm passwords
        old_password_var = tk.StringVar()
        new_password_var = tk.StringVar()
        confirm_password_var = tk.StringVar()

        # Make the window not resizable
        change_password_window.resizable(False, False)

        ttk.Label(change_password_window, text="Old Password:").pack(pady=10)
        ttk.Entry(change_password_window, textvariable=old_password_var, show="*", font=("Helvetica", 12)).pack(pady=10)

        ttk.Label(change_password_window, text="New Password:").pack(pady=10)
        ttk.Entry(change_password_window, textvariable=new_password_var, show="*", font=("Helvetica", 12)).pack(pady=10)

        ttk.Label(change_password_window, text="Confirm Password:").pack(pady=10)
        ttk.Entry(change_password_window, textvariable=confirm_password_var, show="*", font=("Helvetica", 12)).pack(
            pady=10)

        # Confirm button
        confirm_button = ttk.Button(change_password_window, text="Confirm",
                                    command=lambda: self.change_password(old_password_var.get(), new_password_var.get(),
                                                                         confirm_password_var.get(),
                                                                         change_password_window))
        confirm_button.pack(pady=10)

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
        # Validate the old password
        # For simplicity, let's assume the old password is stored in the database as plain text
        user_data = users_collection.find_one({'player_name': self.player_name})
        stored_password = user_data.get('password', '') if user_data else ''

        if old_password != stored_password:
            messagebox.showerror("Error", "Incorrect old password.")
            return

        # Validate the new password and confirmation
        password_validation_result = self.validate_password(new_password)
        if not password_validation_result["is_valid"]:
            messagebox.showerror("Error", password_validation_result["message"])
            return

        if new_password != confirm_password:
            messagebox.showerror("Error", "New password and confirmation do not match.")
            return

        # Update the password in the database
        users_collection.update_one({'player_name': self.player_name}, {'$set': {'password': new_password}})

        messagebox.showinfo("Success", "Password changed successfully.")

        # Close the change password window
        change_password_window.destroy()

    def apply_custom_theme(self):
        # Use the ThemedStyle to apply a custom theme
        style = ThemedStyle(self.root)
        style.set_theme("arc")  # Choose your preferred theme from the available options

        # Configure styles for specific elements
        style.configure("TLabel", font=("Helvetica", 14, "bold"), background=style.lookup("TFrame", "background"))
        style.configure("TButton", font=("Helvetica", 11, "bold"))

        # Customize the sidebar frame
        style.configure("Sidebar.TFrame", background=style.lookup("TFrame", "background"))
        style.configure("Sidebar.TLabel", foreground="white")

        # Customize the search window
        style.configure("SearchWindow.TFrame", background=style.lookup("TFrame", "background"))

        # Customize the following list window
        style.configure("FollowingListWindow.TFrame", background=style.lookup("TFrame", "background"))
        style.configure("FollowingListWindow.TLabel", font=("Helvetica", 12),
                        background=style.lookup("TFrame", "background"))

    def open_change_name_window(self):
        # Create a new window for changing the player name
        change_name_window = tk.Toplevel(self.root)
        change_name_window.title("Change Player Name")

        # Set the size of the change name window
        change_name_window_width = 300
        change_name_window_height = 200
        x = self.root.winfo_x() + (self.root.winfo_width() - change_name_window_width) // 2
        y = self.root.winfo_y() + (self.root.winfo_height() - change_name_window_height) // 2
        change_name_window.geometry(f"{change_name_window_width}x{change_name_window_height}+{x}+{y}")

        # Make the window not resizable
        change_name_window.resizable(False, False)

        # Entry field for the new player name
        new_name_var = tk.StringVar()
        ttk.Label(change_name_window, text="Enter your new player name:").pack(pady=10)
        ttk.Entry(change_name_window, textvariable=new_name_var, font=("Helvetica", 12)).pack(pady=10)

        # Confirm button
        confirm_button = ttk.Button(change_name_window, text="Confirm",
                                    command=lambda: self.change_player_name(new_name_var.get(), change_name_window))
        confirm_button.pack(pady=10)

    def change_player_name(self, new_player_name, change_name_window):
        # Check if the new player name is valid
        if not new_player_name:
            messagebox.showerror("Error", "Player name cannot be empty.")
            return

        # Check if the new player name already exists in the database
        if users_collection.find_one({'player_name': new_player_name}):
            messagebox.showerror("Error", "Player name already exists. Please choose a different one.")
            return

        # Update the player name in the database for your account
        users_collection.update_one({'player_name': self.player_name}, {'$set': {'player_name': new_player_name}})

        # Update the player name in the following list for your account
        old_player_name = self.player_name
        self.player_name = new_player_name

        # Update the welcome label in the sidebar
        self.update_welcome_label()

        # Update the player name in the following list for your account
        if old_player_name in self.following_list:
            self.following_list.remove(old_player_name)
            self.following_list.add(new_player_name)

        # Update the following list in the database for your account
        self.save_following_list_to_db()

        # Update the player name in the following lists of other users who are following you
        for follower_data in users_collection.find({'following_list': {'$in': [old_player_name]}}):
            # Update the player name in the following list for the follower
            follower_following_list = follower_data.get('following_list', [])
            follower_following_list.remove(old_player_name)
            follower_following_list.append(new_player_name)
            users_collection.update_one({'player_name': follower_data['player_name']},
                                        {'$set': {'following_list': follower_following_list}})

        messagebox.showinfo("Success", f"Player name changed to {new_player_name}.")

        # Close the change name window
        change_name_window.destroy()

    def update_welcome_label(self):
        # Find the welcome label in the sidebar and update its text
        for widget in self.sidebar_frame.winfo_children():
            if isinstance(widget, ttk.Label) and widget.cget("text").startswith("Hello"):
                widget.configure(text=f"Hello, {self.player_name}!")

    def get_following_list_from_db(self):
        # Retrieve the following list from the database
        user_data = users_collection.find_one({'player_name': self.player_name})
        return set(user_data.get('following_list', [])) if user_data else set()

    def save_following_list_to_db(self):
        # Save the following list to the database
        users_collection.update_one({'player_name': self.player_name},
                                    {'$set': {'following_list': list(self.following_list)}})

    def log_out_function(self):
        # Implement the functionality to log out
        # Save the following list to the database before destroying the window
        self.save_following_list_to_db()
        self.root.destroy()
        app.show_login_window()

    def open_search_window(self):
        # Create a new window for searching other player names
        search_window = tk.Toplevel(self.root)
        search_window.title("Search User")

        # Set the size of the search window
        search_window_width = 300
        search_window_height = 200
        x = self.root.winfo_x() + (self.root.winfo_width() - search_window_width) // 2
        y = self.root.winfo_y() + (self.root.winfo_height() - search_window_height) // 2
        search_window.geometry(f"{search_window_width}x{search_window_height}+{x}+{y}")

        # Make the window not resizable
        search_window.resizable(False, False)

        # Entry field for searching
        search_entry = ttk.Entry(search_window, font=("Helvetica", 12))
        search_entry.pack(pady=10, padx=10)

        # Search button
        search_button = ttk.Button(search_window, text="Follow",
                                   command=lambda: self.search_and_follow(search_entry.get(), search_window))
        search_button.pack(pady=10, padx=10)

    def search_and_follow(self, player_name, search_window):
        # Check if the player_name exists in the database
        user_data = users_collection.find_one({'player_name': player_name})

        if user_data and 'player_name' in user_data:
            # Check if the player is already being followed
            if player_name not in self.following_list:
                # If the player is not already being followed, add them to the following list
                self.following_list.add(player_name)

                # Save the updated following list to the database
                self.save_following_list_to_db()

                messagebox.showinfo("Follow", f"You are now following {player_name}.")
            else:
                messagebox.showinfo("Follow", f"You are already following {player_name}.")
        else:
            messagebox.showinfo("Follow", f"User {player_name} not found.")

        # Close the search window
        search_window.destroy()

        # Refresh the Following List window to reflect the changes
        self.show_following_list()

    # Modify the follow_user method
    def follow_user(self, player_name):
        # Check if the player_name exists in the database
        user_data = users_collection.find_one({'player_name': player_name})

        if user_data and 'player_name' in user_data:
            # Check if the player is already being followed
            if player_name not in self.following_list:
                # If the player is not already being followed, add them to the following list
                self.following_list.add(player_name)

                # Save the updated following list to the database
                self.save_following_list_to_db()

                messagebox.showinfo("Follow", f"You are now following {player_name}.")
            else:
                messagebox.showinfo("Follow", f"You are already following {player_name}.")
        else:
            messagebox.showinfo("Follow", f"User {player_name} not found.")

        # Refresh the Following List window to reflect the changes
        self.show_following_list()

    def show_following_list(self):
        # Show a window with the list of followed players
        following_list_window = tk.Toplevel(self.root)
        following_list_window.title("Following List")

        # Set the size of the following list window
        following_list_window_width = 300
        following_list_window_height = 200
        x = self.root.winfo_x() + (self.root.winfo_width() - following_list_window_width) // 2
        y = self.root.winfo_y() + (self.root.winfo_height() - following_list_window_height) // 2
        following_list_window.geometry(f"{following_list_window_width}x{following_list_window_height}+{x}+{y}")

        # Display the list of followed players with Unfollow button
        if self.following_list:
            ttk.Label(following_list_window, text="Following List:", font=("Helvetica", 12)).pack(pady=10)

            for player_name in self.following_list:
                # Create a frame for each player entry
                player_frame = ttk.Frame(following_list_window)
                player_frame.pack(pady=5)

                # Display the player name
                ttk.Label(player_frame, text=f"Name: {player_name}", font=("Helvetica", 13)).pack(side="left")

                # Add a space between the player name and the Unfollow button
                ttk.Label(player_frame, text=" ", font=("Helvetica", 10)).pack(side="left")

                # Create an Unfollow button with a callback to remove the player from the following list
                ttk.Button(player_frame, text="Unfollow",
                           command=lambda name=player_name, window=following_list_window: self.unfollow_user(name,
                                                                                                             window)).pack(
                    side="left")

        else:
            ttk.Label(following_list_window, text="You are not following anyone yet.", font=("Helvetica", 12)).pack(
                pady=20)

        # Refresh the Following List window to reflect the changes
        following_list_window.protocol("WM_DELETE_WINDOW",
                                       lambda: self.on_following_list_window_close(following_list_window))

    def on_following_list_window_close(self, following_list_window):
        # Save the updated following list to the database
        self.save_following_list_to_db()

        # Destroy the Following List window
        following_list_window.destroy()

    def unfollow_user(self, player_name, following_list_window):
        # Remove the player from the following list
        self.following_list.discard(player_name)

        # Save the updated following list to the database
        self.save_following_list_to_db()

        messagebox.showinfo("Unfollow", f"You have unfollowed {player_name}.")

        # Destroy the old Following List window
        following_list_window.destroy()

        # Refresh the Following List window to reflect the changes
        self.show_following_list()


if __name__ == "__main__":
    root = tk.Tk()
    player_name = "saaaaa"  # Replace with the actual player name
    app = DashboardApp(root, player_name)
    root.mainloop()
