import threading
import tkinter as tk

def create_self_closing_popup(title, message, duration):
    root = tk.Tk()

    # Set window title
    root.title(title)

    # Center the message
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    window_width = 300
    window_height = 200
    position_top = int(screen_height / 2 - window_height / 2)
    position_right = int(screen_width / 2 - window_width / 2)
    root.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")

    # Create a frame with a slight relief and a border
    frame = tk.Frame(root, relief='raised', borderwidth=2)
    frame.pack(fill='both', expand=True)

    # Add the message label
    label = tk.Label(frame, text=message, font=('Arial', 14), padx=20, pady=20)
    label.pack(expand=True)

    # Close the window after 'duration' seconds
    root.after(duration * 1000, root.destroy)
    root.mainloop()

    
def popup(title, message, duration):
    
    threading.Thread(target=create_self_closing_popup, args=(title, message, duration)).start()


if __name__ == "__main__":
    # title, message, duration = "Popup Window", "This is a self-closing pop-up", 2
    # p = multiprocessing.Process(target=create_self_closing_popup, args=(title, message, duration))
    # p.start()
    for i in range(5):
        popup("Popup Window", "This is a self-closing pop-up", 10)
    for i in range(10):
        print(i)