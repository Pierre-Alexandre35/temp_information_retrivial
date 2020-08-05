# class for Priority queue 
class PriorityQueue:

  def __init__(self):
    self.queue = list()
    # if you want you can set a maximum size for the queue

  def insert_list(self, nodes):
    for node in nodes:
      self.insert(node)

  def insert(self, node):
    # if queue is empty
    if self.size() == 0:
      # add the new node
      self.queue.append(node)
    else:
      # traverse the queue to find the right place for new node
      for x in range(0, self.size()):
        # if the priority of new node is smaller
        if node.score < self.queue[x].score:
          # if we have traversed the complete queue
          if x == (self.size()-1):
            # add new node at the end
            self.queue.insert(x+1, node)
          else:
            continue
        else:
          self.queue.insert(x, node)
          return True

  def pop(self):
    # remove the first node from the queue
    return self.queue.pop(0)
  

  def show(self):
    for x in self.queue:
      print(str(x.url)+" - "+str(x.score))

  def size(self):
    return len(self.queue)

