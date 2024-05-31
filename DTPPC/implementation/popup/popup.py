import sys
import platform
import threading
import time
import tkinter as tk
from plyer import notification
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget
from PyQt5.QtCore import QThread, pyqtSignal
from multiprocessing import Process, Queue
def create_self_closing_popup(title, message, image=None, duration=5, window_width=300, window_height=200, position_right=-1, position_top=-1):
    root = tk.Tk()
    # Set window title
    root.title(title)
    # Center the message
    if position_right == -1:
        screen_width = root.winfo_screenwidth()
        position_right = int(screen_width / 2 - window_width / 2)
    if position_top == -1:
        screen_height = root.winfo_screenheight()
        position_top = int(screen_height / 2 - window_height / 2)
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
    return root 
    
def popup(title, message="", image=None, timeout=5):
    threading.Thread(target=create_self_closing_popup, args=(title, message, image, timeout)).start()

def notify(title, message=" ", timeout=2):
    notification.notify(title=title, message=message, app_name='DTPPC', timeout=5)

'''
if platform.system() == 'Windows' and platform.release() == '7':
    import json
    from filelock import FileLock
    import csv
    class FileQueue:
        def __init__(self, filename):
            self.filename = filename
            self.lock = FileLock(self.filename + ".lock")
            try:
                self.get()
            except FileNotFoundError:
                with open(self.filename, 'w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow({})

        def put(self, item):
            with self.lock:
                with open(self.filename, 'a', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow([item])

        def get(self):
            with self.lock:
                with open(self.filename, 'r+', newline='') as f:
                    reader = csv.reader(f)
                    lines = list(reader)
                    if lines:
                        item = lines[0]
                        # Remove the first line
                        with open(self.filename, 'w', newline='') as f:
                            writer = csv.writer(f)
                            writer.writerows(lines[1:])
                        return item
                    else:
                        return None
    class MessageThread(QThread):
        message_signal = pyqtSignal(str)
        def __init__(self, queue):
            super().__init__()
            self.queue = queue
        def run(self):
            while True:
                message = self.queue.get()
                if message:
                    self.message_signal.emit(message)
                time.sleep(0.1)
    class AppDemo(QWidget):
        def __init__(self, queue):
            super().__init__()
            self.messages = []
            self.layout = QVBoxLayout()
            self.message_thread = MessageThread(queue)
            self.message_thread.message_signal.connect(self.add_message)
            self.message_thread.start()
            self.setLayout(self.layout)
        def add_message(self, message):
            self.messages.insert(0, QLabel(message))
            if len(self.messages) > 20:
                self.messages.pop().deleteLater()
            for i in range(len(self.messages)):
                self.layout.insertWidget(i, self.messages[i])
    class Logger:
        def __init__(self, queue):
            self.queue = queue
            self.run_app(self.queue)
            
        def run_app(self, queue):
            app = QApplication(sys.argv)
            demo = AppDemo(queue)
            demo.show()
            sys.exit(app.exec_())

        def notify(self,title="", message="", timeout=None):
            if not title:
                msg = message
            elif not message:
                msg = title
            else:
                msg = "%s: %s"%(title, message)
            self.queue.put(msg)

    # logger = Logger()
    # notify = logger.notify

if __name__ == '__main__':
    input = "ewrwe 34534 fsd \nerewr ere er"
    name = "r3r34werwwe"
    # root = notify(title="Digital Twin request",message="DT instance: %s\nis executing request:\n%s"%(name,input),timeout=5)
    # notify(title="Digital Twin request",message="DT instance: %s\nis executing request:\n%s"%(name,input),timeout=5)
    window_height, window_width, position_right, position_top = 200, 300, 0, 0
    queue = FileQueue("a.csv")
    logger = Logger(queue)
    queue.put(1)
'''