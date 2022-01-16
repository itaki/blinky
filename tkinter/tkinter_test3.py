import json
import tkinter as tk
from os.path import dirname, join

current_dir = dirname(__file__)
print("THIS IS MY CURRENT WORKING DIRECTORY"+current_dir)
file_path = join(current_dir, "./tools.json")
with open(file_path, 'r') as tools_list:
	tools = json.load(tools_list)
dump = json.dumps(tools, indent=4)
print(dump)
for tool in tools: 

	print('\nTool Name', tool)
	print('status: ',tools[tool]['status'])

	#


class MainWindow:
	def __init__(self, master):
		self.master = master
		self.frame = tk.Frame(self.master, width = 300, height = 300)
		self.frame.pack()
		self.bindings()
	def bindings(self):
		self.master.bind('<Key>', clicker)


def clicker(event): #
	key_clicked = event.char
	try:
		tool_selected = tools[key_clicked]['name']
		print(tool_selected)
	except:
		print(key_clicked, "is not a tool")


root = tk.Tk()
window = MainWindow(root)
print("this prints before mainloop")
root.mainloop()
print("this prints AFTER mainloop")



