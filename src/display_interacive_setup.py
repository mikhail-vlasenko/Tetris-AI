import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
from tkinter import ttk
import threading

from config import CONFIG


class InteractiveSetup:
    def __init__(self):
        import matplotlib
        matplotlib.use('TkAgg')
        plt.ion()
        self.fig, self.axes = plt.subplots(1, 3, figsize=(7, 5))
        self.axes[0].set_title("Raw Field View")
        self.axes[1].set_title("Processed Field View")
        self.axes[2].set_title("Next Piece View")
        self.buffers = [self.axes[0].imshow(np.zeros((20, 10))),
                        self.axes[1].imshow(np.zeros((20, 10))),
                        self.axes[2].imshow(np.zeros((5, 5)))]

    def render_frame(self, field, simplified, next_img, next_piece):
        self.buffers[0].set_array(field.copy())
        img_simplified = simplified.copy()
        # displays better when converted to 3 channels
        img_simplified = np.expand_dims(img_simplified, axis=2)
        img_simplified = np.broadcast_to(img_simplified, (img_simplified.shape[0], img_simplified.shape[1], 3))
        self.buffers[1].set_array(img_simplified*255)
        self.buffers[2].set_array(next_img.copy())
        self.axes[2].set_title(f"Next Piece (detected {next_piece})")

        self.fig.canvas.draw()
        self.fig.canvas.flush_events()


class ConstantsGUI:
    def __init__(self, display_consts):
        self.display_consts = display_consts
        self.root = None
        self.vars = None
        self.font = ('Arial', 14)
        self.thread = threading.Thread(target=self.create_gui, daemon=True)
        self.thread.start()

    def create_gui(self):
        self.root = tk.Tk()
        self.root.title("Display Constants Setup")
        self.root.geometry(CONFIG['helper window size'])

        style = ttk.Style()
        style.configure('Large.TLabel', font=self.font)
        style.configure('Large.TEntry', font=self.font)
        style.configure('Large.TButton', font=self.font)

        self.vars = {
            'top': tk.IntVar(value=self.display_consts.top),
            'bottom': tk.IntVar(value=self.display_consts.bottom),
            'left': tk.IntVar(value=self.display_consts.left),
            'right': tk.IntVar(value=self.display_consts.right),
            'next_top': tk.IntVar(value=self.display_consts.next_top),
            'next_bottom': tk.IntVar(value=self.display_consts.next_bottom),
            'next_left': tk.IntVar(value=self.display_consts.next_left),
            'next_right': tk.IntVar(value=self.display_consts.next_right),
            'num_extra_rows': tk.IntVar(value=self.display_consts.num_extra_rows)
        }

        for name, var in self.vars.items():
            frame = ttk.Frame(self.root)
            frame.pack(fill='x', padx=10, pady=5)

            ttk.Label(frame, text=f"{name}:", style='Large.TLabel').pack(side='left')

            # Create buttons frame
            btn_frame = ttk.Frame(frame)
            btn_frame.pack(side='right')

            # Up and down buttons
            up_btn = ttk.Button(btn_frame, text="▲", width=3,
                                command=lambda v=var: self.adjust_value(v, 5))
            up_btn.pack(side='top')

            down_btn = ttk.Button(btn_frame, text="▼", width=3,
                                  command=lambda v=var: self.adjust_value(v, -5))
            down_btn.pack(side='bottom')

            # Entry field
            entry = ttk.Entry(frame, textvariable=var, font=self.font, width=10)
            entry.pack(side='right', padx=5)

        ttk.Button(self.root, text="Update All", command=self.update_all,
                  style='Large.TButton').pack(pady=20)

        ttk.Label(self.root, text="Every time you update,\n"
                                  "the DisplayConsts with new values is printed in console.\n"
                                  "Don't forget to copy it to config.py",
                  style='Large.TLabel').pack(pady=20)

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

    def update_value(self, name):
        value = self.vars[name].get()
        setattr(self.display_consts, name, value)

    def adjust_value(self, var, delta):
        current = var.get()
        var.set(current + delta)
        self.update_all()

    def update_all(self):
        for name in self.vars:
            self.update_value(name)
        self.display_consts.update()
        print("Display Constants updated to:", self.display_consts)

    def on_closing(self):
        if self.root:
            self.root.quit()
            self.root.destroy()
            self.root = None

    def is_alive(self):
        return self.thread.is_alive()

