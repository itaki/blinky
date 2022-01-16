import tkinter as tk

class MainWindow:
	def __init__(self, master):
		self.master = master
		self.frame = tk.Frame(self.master, width = 300, height = 300)
		self.frame.pack()
		self.bindings()
	def bindings(self):
		self.master.bind('<Key>', clicker)


def clicker(event): #
	print(event.char)

def printer(event):
	print("something happened")
	

root = tk.Tk()
window = MainWindow(root)
print("this prints before mainloop")
root.mainloop()
