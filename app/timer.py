import time
import threading
import Queue
import random #for testing

#import app.config
import app.worker
from app.log import mylogger as log

class Timer(threading.Thread):
    """
    Run tasks.
    """
    def __init__(self):
        threading.Thread.__init__(self)
        random.seed() # for testing
        self.setDaemon(True)
        self.setName('Timer')
        self.pending_queue = Queue.Queue()
        self.active_queue = Queue.Queue()
        self.done_queue = Queue.Queue()
        self.total_workers = app.config.TIMER_MAX_WORKERS
        self.current_workers = 0
        self.start()
       
    def run(self):
        """
        Check the tasks queue and run anything that is due.
        """
        while True:
            while self.current_workers < self.total_workers:
                log.debug("worker added")
                app.worker.Worker(self.active_queue)
                self.current_workers += 1
                
            self.process_pending_list()
            self.process_active_list()
            self.process_done_list()
            
            log.info('active_queue = ' + str(self.active_queue.qsize())) 
            time.sleep(app.config.TIMER_SLEEP_INTERVAL)
            log.debug("waking")            

    def process_pending_list(self):
        """
        Process all pending tasks.
        """
        log.info('pending_queue = ' + str(self.pending_queue.qsize())) 

    
    def process_active_list(self):
        """
        Process all currently running tasks.
        """
        log.info('active_queue = ' + str(self.active_queue.qsize())) 
        i = random.randint(0, 5)
        while i > 0:
            self.add_work('TEST_TASK', 
                         app.worker.test_task, 
                         random.randint(0, 30))
            i -= 1
         
    def process_done_list(self):
        """
        Finish any tasks that have completed.
        """
        log.info('done_queue = ' + str(self.done_queue.qsize())) 
        
    def add_work(self, task_name, callname, *args, **kwds):
        """
        Add task to queue.
        """
        self.active_queue.put((task_name, callname, args, kwds))
    
