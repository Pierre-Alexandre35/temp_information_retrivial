import sys
sys.path.append("..")
import unittest
import Buckets as bucket
import Node as node


class BucketTest(unittest.TestCase):
    def test_insertNode(self):
        node1 = node.Node("www.google.com", 0, 0.95)
        node2 = node.Node("www.pierre.fr", 0, 0)
        node3 = node.Node("www.facebook.com", 0, 0.82)
        node4 = node.Node("www.twitter.com", 0, 0.13)
        
        outlinks_nodes = [node1, node2, node3, node4]
        
        buckets = bucket.Buckets()
        
        buckets.insert_nodes(outlinks_nodes)
        
        self.assertEqual(len(buckets.firstB), 2)
        self.assertEqual(len(buckets.secondB), 0)
        self.assertEqual(len(buckets.thirdB), 0)
        self.assertEqual(len(buckets.fourthB), 0)        
        self.assertEqual(len(buckets.fifthB), 2)
        
        
    def test_popNodes(self):

        node1 = node.Node("www.a.com", 0, 0.95)
        node2 = node.Node("www.b.fr", 0, 0)
        node3 = node.Node("www.c.com", 0, 0.82)
        node4 = node.Node("www.d.com", 0, 0.98)
        node5 = node.Node("www.f.com", 0, 0.13)
        node6 = node.Node("www.g.com", 0, 0.77)
        node7 = node.Node("www.h.com", 0, 0.65)
        
        outlinks_nodes = [node1, node2, node3, node4, node5, node6, node7]
        buckets = bucket.Buckets()
        buckets.resetBuckets()
        
        
        buckets.insert_nodes(outlinks_nodes)
        retrivied_nodes_plot1 = buckets.pop_nodes(10)
        retrivied_nodes_plot2 = buckets.pop_nodes(10)

        self.assertEqual(len(retrivied_nodes_plot1), 3)
        self.assertEqual(len(retrivied_nodes_plot2), 2)
        self.assertEqual(len(buckets.firstB), 0)

        

        