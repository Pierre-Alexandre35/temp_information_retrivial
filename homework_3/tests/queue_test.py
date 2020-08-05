import sys
sys.path.append("..")

import unittest
import Buckets as bucket
import Node as node
import Queue as queue

class QueueTest(unittest.TestCase):
    def testCaseOne(self):
        node1 = node.Node("www.a.com", 0, 0.95)
        node2 = node.Node("www.b.fr", 0, 0)
        node3 = node.Node("www.c.com", 0, 0.82)
        node4 = node.Node("www.d.com", 0, 0.90)
        node5 = node.Node("www.f.com", 0, 0.13)
        node6 = node.Node("www.g.com", 0, 0.77)
        node7 = node.Node("www.h.com", 0, 0.65)
        node8 = node.Node("www.i.com", 0, 0.32)
        node9 = node.Node("www.j.com", 0, 0.99)
        node10 = node.Node("www.k.com", 0, 0.03)

        mainBucket = bucket.Buckets()
                
        mainBucket.insert_nodes([node1, node2, node3, node4, node5, node6, node7, node8, node9, node10])
        
        
        bucketOne = mainBucket.pop_nodes(10)
        
        pQueue = queue.PriorityQueue();
        
        self.assertEqual(4, len(bucketOne))

        for bucketNode in bucketOne:
            pQueue.insert(bucketNode)
             
        self.assertEqual(0, len(mainBucket.firstB))
        
        nextNodeToCrawlOne = pQueue.pop()
        
        self.assertEqual(nextNodeToCrawlOne.url, "www.j.com")
        
        
        nextNodeToCrawlTwo = pQueue.pop()

        self.assertEqual(nextNodeToCrawlTwo.url, "www.a.com")
