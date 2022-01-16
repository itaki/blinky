import time
import concurrent.futures
start = time.perf_counter() 

def do_something(seconds):
    print(f'sleep for {seconds} seconds')
    time.sleep(seconds)
    return f'done sleeping for {seconds} seconds'

with concurrent.futures.ThreadPoolExecutor() as executor:
    secs = [5,4,3,2,1]
    results = executor.map(do_something, secs)

    # for result in results: #
    #     print(result)



#     results = [executor.submit(do_something, sec) for sec in secs]

#     for f in concurrent.futures.as_completed(results):
#         print(f.result())
# # threads = []

# for _ in range(1000): 
#     t = threading.Thread(target=do_something, args=[1.5])
#     t.start()
#     threads.append(t)

# for thread in threads: 
#     thread.join() 

finish = time .perf_counter()

print (f'finished in {round(finish-start, 2)} seconds')