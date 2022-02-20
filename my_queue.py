import asyncio

class Queue:
    def __init__(self, name):
        self.queue = asyncio.Queue()
        self.id = name
        
    def isEmpty(self):
        return self.queue.empty()
    
    def enqueue(self, item):
        self.queue.put_nowait(item)
        
    def done(self):
        self.queue.task_done()

    def dequeue(self):
        if not self.queue.empty():
            return self.queue.get_nowait()
        
    def get_name(self):
        return self.id