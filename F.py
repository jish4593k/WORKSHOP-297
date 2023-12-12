import cv2
import tkinter as tk
from tkinter import ttk

from config import CASCADES

class WebcamApp:
    def __init__(self, master, cascades):
        self.master = master
        master.title("Webcam Face Detection")

        self.video_capture = cv2.VideoCapture(0)

        self.canvas = tk.Canvas(master)
        self.canvas.pack()

        self.quit_button = ttk.Button(master, text="Quit", command=self.quit_app)
        self.quit_button.pack()

        self.cascades = cascades

        self.update()

    def update(self):
        _, webcam_frame = self.video_capture.read()
        gray_frame = cv2.cvtColor(webcam_frame, cv2.COLOR_BGR2GRAY)

        for cascade, color in self.cascades:
            captures = cascade.detectMultiScale(
                gray_frame,
                scaleFactor=1.1,
                minNeighbors=10,
                minSize=(30, 30)
            )
            for (x, y, w, h) in captures:
                self.draw_square(webcam_frame, x, y, w, h, color)

        self.show_frame(webcam_frame)
        self.master.after(10, self.update)

    def draw_square(self, frame, x, y, w, h, color):
        cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)

    def show_frame(self, frame):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame)
        imgtk = ImageTk.PhotoImage(image=img)
        self.canvas.imgtk = imgtk
        self.canvas.config(image=imgtk)

    def quit_app(self):
        self.video_capture.release()
        self.master.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    cascades = get_cascades()
    app = WebcamApp(root, cascades)
    root.mainloop()
