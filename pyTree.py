import random as rd

class Node:
    def __init__(self,key,value):
        self.key = key
        self.value = value
        self.left = 0
        self.right = 0

class BinarySearchTree:
    def __init__(self):
        self.root = 0
        self.current = 0
    def empty(self):
        return self.root == 0
    def addNode(self,key,value):
        self.current = self.root
        if(self.empty()):
            self.root = Node(key,value)
        else:
            newNode = Node(key,value)
            while self.current != 0:
                temp = self.current
                if key > self.current.key:
                    self.current = self.current.right
                elif key == self.current.key:
                    key += 1
                    self.current = self.current.right
                else:
                    self.current = self.current.left
            if key > temp.key:
                temp.right = newNode
            else:
                temp.left = newNode 
    def inorder(self,current,outList):
        if current != 0:
            self.inorder(current.left,outList)
            # print(str(current.key) , current.value)
            outList += [[str(current.key)] + [current.value]]
            self.inorder(current.right,outList)
# temp = []
# a = BinarySearchTree()
# for i in range (1,5):
#     a.addNode(rd.randint(1,10000),input())
# a.inorder(a.root,temp)
# outStr = ""
# for i in range(0,len(temp)):
#     outStr += temp[i][0] + temp[i][1]
# print(outStr)