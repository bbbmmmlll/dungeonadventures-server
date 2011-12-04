"""
A thread that pulls tasks off of a queue and processes them.
"""
import time
import threading

from app.log import mylogger as log

# we need to open seperate sqlite connections per worker
class Worker(threading.Thread):
    """
    A single worker thread.
    """
    def __init__(self, task_queue):
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.setName('Worker')
        self.task_queue = task_queue
        self.start()
        
    def run(self):
        """
        Start worker.
        """
        log.info("worker started")
        while True:
            task_name, _callable, args, kwds = self.task_queue.get()
            log.debug("worker got " + task_name)
            # pylint: disable-msg=W0142
            results = _callable(*args, **kwds)
            # pylint: enable-msg=W0142
            if results is False:
                log.error("Task failed: " + task_name)
        
    def get_task(self):
        """
        Return worker's current task.
        """
        pass
        
def test_task(task):
    """
    Dummy task for basic testing.
    """
    time.sleep(task)
    log.debug("test_task[" + str(task) + "] called")            

    