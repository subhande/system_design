from queue import PriorityQueue
customers = PriorityQueue() #we initialise the PQ class instead of using a function to operate upon a list. 
customers.put(2)
customers.put(3)
customers.put(1)
customers.put(4)
# print(customers.get())
# print(customers.get())
while customers.empty() == False:
     print(customers.get())