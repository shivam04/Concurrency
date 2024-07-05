import threading
import time


class product:
   
  def buyer(self):
    print('John consumer is wait for product')   
    print('...............')
    event_object.wait()    
    print('got product')       
   
  def seller(self):   
    time.sleep(5)
    print('Tom producer producing items')  
    print('tom goes to retailer')
    event_object.wait()
     
  def retailer(self):
    time.sleep(10)
    print('retailer found that product and directly send to buyer')
    event_object.set()

# class object      
class_obj = product()

# setting event object
if __name__=='__main__':
  event_object = threading.Event()


  # creating  threads
T1 = threading.Thread(target=class_obj.buyer)
T2 = threading.Thread(target=class_obj.seller)
T3 = threading.Thread(target=class_obj.retailer)



# starting threads
T1.start()
T2.start()
T3.start()