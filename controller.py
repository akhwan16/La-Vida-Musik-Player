from tkinter import Tk
from view import view

class Controller(view):
    def __init__(self, master):
        super().__init__(master)
    def run(self):
        self.master.mainloop()

if __name__ == "__main__":
    root = Tk()
    controller_app = Controller(root)
    controller_app.run()


