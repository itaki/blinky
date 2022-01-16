import json
import tkinter as tk
from os.path import dirname, join


tool_ids = []



current_dir = dirname(__file__)
print("THIS IS MY CURRENT WORKING DIRECTORY"+current_dir)
file_path = join(current_dir, "./tools_list.json")
#file_path = join(current_dir, "./tools.json")
with open(file_path, 'r') as tools_list:
	tools = json.load(tools_list)
dump = json.dumps(tools, indent=4)
print(dump)
for tool in tools: 
	print(tool)
	tool_ids.append(tool['id_num'])
	#print('\nTool Name', tool)
	#print('status: ',tools[tool]['status'])

	#
print (tool_ids)





