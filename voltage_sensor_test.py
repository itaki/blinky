from tool_manager import Tool_Manager
import voltage_sensor as vs

tools_file = 'tools.json'
backup_dir = 'BU/'

tm = Tool_Manager(tools_file, backup_dir)
while True:
    