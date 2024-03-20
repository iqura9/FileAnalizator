import threading
import time
import random

num_philosophers = 5
num_forks = num_philosophers

fork_locks = [threading.Lock() for _ in range(num_forks)]
mutex = threading.Lock()

def philosopher(index):
    while True:
        print(f"Philosopher {index} is thinking...")
        time.sleep(random.randint(1, 5))
		
        mutex.acquire()
	
        left_fork_index = index
        right_fork_index = (index + 1) % num_forks
        
        fork_locks[left_fork_index].acquire()
        fork_locks[right_fork_index].acquire() 
	
        mutex.release() 
    
        print(f"\033[91mPhilosopher {index} is eating...\033[0m") 
        time.sleep(random.randint(1, 5))  
        
        fork_locks[left_fork_index].release()  
        fork_locks[right_fork_index].release()  

philosopher_threads = [threading.Thread(target=philosopher, args=(i,)) for i in range(num_philosophers)]

for thread in philosopher_threads:
    thread.start()

for thread in philosopher_threads:
    thread.join()

