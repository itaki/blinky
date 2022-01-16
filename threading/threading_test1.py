import time
import threading
start = time.perf_counter() 

def do_something(seconds):
    print(f'sleep for {seconds} seconds')
    time.sleep(seconds)
    print('done sleeping for 1 second')

threads = []

for _ in range(1000): 
    t = threading.Thread(target=do_something, args=[1.5])
    t.start()
    threads.append(t)

for thread in threads: 
    thread.join() 

finish = time .perf_counter()

print (f'finished in {round(finish-start, 2)} seconds')