import tkinter as tk


class RegisterPanel(tk.Frame):

    def __init__(self, master=None, register_cb=None):
        super(RegisterPanel, self).__init__(master)
        self.master = master
        self.grid()

        # Fields
        self.register_cb = register_cb

        # Create widgets

        # Row 0
        self.name_label = tk.Label(self, text='Name')
        self.name_label.grid(row=0, column=0)

        self.name_entry = tk.Entry(self)
        self.name_entry.grid(row=0, column=1)

        self.server_ip_label = tk.Label(self, text='Server IP Address')
        self.server_ip_label.grid(row=0, column=2)

        self.server_ip_entry = tk.Entry(self)
        self.server_ip_entry.grid(row=0, column=3)

        # Row 1
        self.register_label = tk.Button(self, text='Register', command=self.register_cmnd)
        self.register_label.grid(row=1, column=0)

        # TODO: Change to read only text, make method to fill text
        self.response_label = tk.Label(self, text='Response:')
        self.response_label.grid(row=1, column=1)

        self.response_msg_label = tk.Label(self, text='')
        self.response_msg_label.grid(row=1, column=2, columnspan=2)

    def register_cmnd(self):
        name = self.name_entry.get()
        server_ip = self.server_ip_entry.get()
        self.register_cb(name, server_ip)

    def set_response_text(self, response):
        self.response_msg_label['text'] = response



