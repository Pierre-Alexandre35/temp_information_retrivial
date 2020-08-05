## class to reprent a set a buckets to organize and manage nodes based on their relevance (score). 
class Buckets:      
    firstB = [] 
    secondB = [] 
    thirdB = []  
    fourthB = [] 
    fifthB = [] 
      
    def isEmpty(self):
        if(len(self.firstB) > 0 or len(self.secondB) > 0 or len(self.thirdB) > 0 or len(self.fourthB) > 0 or len(self.fifthB) > 0):
            return False
            
           
        
    def insert_nodes(self, nodes):
        for newNode in nodes: 
            if(newNode.score) > 0.90:
                self.firstB.insert(0, newNode)
            elif(newNode.score) > 0.80:
                self.secondB.insert(0, newNode)
            elif(newNode.score) > 0.65:
                self.thirdB.insert(0, newNode)          
            elif(newNode.score) > 0.50:
                self.fourthB.insert(0, newNode)   
            elif(newNode.score) > 0.30:
                self.fifthB.insert(0, newNode) 

    
    def pop_nodes(self, size):
        
        if(len(self.firstB) > 0):
            count = 0
            result = []
            
            while(len(self.firstB) > 0 and (count < size)):
                result.append(self.firstB.pop())
                count = count + 1
            return result

        elif(len(self.secondB) > 0):
            count = 0
            result = []
            while(len(self.secondB) > 0 and (count < size)):
                result.append(self.secondB.pop())
                count = count + 1
            return result
        
        elif(len(self.thirdB) > 0):
            count = 0
            result = []
            while(len(self.thirdB) > 0 and (count < size)):
                result.append(self.thirdB.pop())
                count = count + 1

            return result
        
        elif(len(self.fourthB) > 0):
            count = 0
            result = []
            while(len(self.fourthB) > 0 and (count < size)):
                result.append(self.fourthB.pop())
                count = count + 1

            return result
        
        elif(len(self.fifthB) > 0):
            count = 0
            result = []
            while(len(self.fifthB) > 0 and (count < size)):
                result.append(self.fifthB.pop())
                count = count + 1
            return result
        else:
            print("buckets are empty")
        
    def resetBuckets(self):
        self.firstB.clear()
        self.secondB.clear()
        self.thirdB.clear()
        self.fourthB.clear()
        self.fifthB.clear()