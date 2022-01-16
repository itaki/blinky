import threading
import queue

def console(q):
    while 1:
        cmd = input('> ')
        q.put(cmd)
        if cmd == 'quit':
            break

def action_foo():
    print('--> action foo')

def action_bar():
    print('--> action bar')

def invalid_input():
    print('---> Unknown command')

def main():
    cmd_actions = {'foo': action_foo, 'bar': action_bar}
    cmd_queue = queue.Queue()

    dj = threading.Thread(target=console, args=(cmd_queue,))
    dj.start()

    while 1:
        cmd = cmd_queue.get()
        if cmd == 'quit':
            break
        action = cmd_actions.get(cmd, invalid_input)
        action()

main()