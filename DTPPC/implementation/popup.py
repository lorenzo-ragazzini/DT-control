import threading
import time
import tkinter as tk
import easygui
from plyer import notification

def create_self_closing_popup(title, message, image=None, duration=5):
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
    frame = tk.Frame(root, relief='raised', borderwidth=2, bg='white')
    frame.pack(fill='both', expand=True)
    # Add the message label
    label = tk.Label(frame, text=message, font=('Arial', 14), padx=20, pady=20, bg='white', anchor='w', justify='left')
    label.pack(expand=True)
    # Add the image if provided
    if image:
        img = tk.PhotoImage(file=image)
        image_label = tk.Label(frame, image=img, bg='white')
        image_label.image = img
        image_label.pack(pady=10)
    # Add the OK button
    ok_button = tk.Button(frame, text="      OK      ", command=root.destroy, bg='white')
    ok_button.pack(pady=10, anchor='e', padx=10)  # Align the button to the right and add padding
    # Close the window after 'duration' seconds
    root.after(duration * 1000, root.destroy)
    root.mainloop()
    
def popup(title, message="", image=None, timeout=5):
    threading.Thread(target=create_self_closing_popup, args=(title, message, image, timeout)).start()

def notify(title, message=" ", timeout=2):
    notification.notify(title=title, message=message, app_name='DTPPC', timeout=5)

if __name__ == '__main__':
    input = "ewrwe 34534 fsd \nerewr ere er"
    name = "r3r34werwwe"
    popup(title="Digital Twin request",message="DT instance: %s\nis executing request:\n%s"%(name,input),timeout=5)
    notify(title="Digital Twin request",message="DT instance: %s\nis executing request:\n%s"%(name,input),timeout=5)
