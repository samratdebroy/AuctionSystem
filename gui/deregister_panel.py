import tkinter as tk


class DeregisterPanel(tk.Frame):

    def __init__(self, master=None, deregister_cb=None):
        super(DeregisterPanel, self).__init__(master)
        self.master = master
        self.grid()

        # Create widgets

        # Row 0
        self.deregister_label = tk.Button(self, text='Deregister', command=deregister_cb)
        self.deregister_label.grid(row=0, column=0)

        self.response_label = tk.Label(self, text='Response:')
        self.response_label.grid(row=1, column=0)

        self.response_msg_label = tk.Label(self, text='')
        self.response_msg_label.grid(row=1, column=1)
