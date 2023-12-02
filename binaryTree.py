import random


class Node:
    def __init__(self, arg1, arg2, u):
        if (u == 1):
            self.init1(arg1, arg2)
        else:
            self.init2(arg1, arg2)

    def init1 (self, alphaV, parentV):
        self.split = 'N'
        self.alpha = alphaV
        self.left = None
        self.right = None
        self.alphaTar = -1
        self.parent = parentV
        self.width = -1
        self.height = -1
        self.xIndex = -1
        self.yIndex = -1

    def init2(self, splitV, parentV):
        self.split = splitV
        self.alpha = -1
        self.left = None
        self.right = None
        self.alphaTar = -1
        self.parent = parentV
        self.width = -1
        self.height = -1
        self.xIndex = -1
        self.yIndex = -1

class BinaryTree:
    def __init__(self):
        self.root = None
        self.index = 0

    def levelOrder(self, n):
        result = [None] * (n + 1)
        i = 1
        if self.root is None:
            return result
        result[0] = self.root
        q = [self.root]

        while q:
            temp = q.pop(0)
            if temp.left is None and temp.right is None:
                result[i] = temp
                i += 1
            if temp.left:
                q.append(temp.left)
            if temp.right:
                q.append(temp.right)
        
        return result

    def calculateAlpha(self, temp):
        if temp.left and temp.right:
            self.calculateAlpha(temp.left)
            self.calculateAlpha(temp.right)
            a = temp.left.alpha
            b = temp.right.alpha
            if temp.split == 'V':
                temp.alpha = a + b
            else:
                temp.alpha = (a * b) / (a + b)

                
    def calculateDimension(self, width):
        q = [self.root]
        while q:
            temp = q.pop(0)
            if temp == self.root:
                temp.width = width
                temp.height = int(width / temp.alpha)
            else:
                if temp.parent.split == 'V':
                    temp.height = temp.parent.height
                    temp.width = int(temp.alpha * temp.height)
                else:
                    temp.width = temp.parent.width
                    temp.height = int(temp.width / temp.alpha)
            if temp.left:
                q.append(temp.left)
            if temp.right:
                q.append(temp.right)
            
    def calculateIndex(self):
        q = [self.root]
        while q:
            temp = q.pop(0)
            if temp == self.root:
                temp.xIndex = 0
                temp.yIndex = 0
            if temp.left and temp.split == 'H':
                temp.left.xIndex = temp.xIndex
                temp.left.yIndex = temp.yIndex
                temp.right.xIndex = temp.xIndex + temp.left.height
                temp.right.yIndex = temp.yIndex
            elif temp.left and temp.split == 'V':
                temp.left.xIndex = temp.xIndex
                temp.left.yIndex = temp.yIndex
                temp.right.xIndex = temp.xIndex
                temp.right.yIndex = temp.yIndex + temp.left.width
            if temp.left:
                q.append(temp.left)
            if temp.right:
                q.append(temp.right)

    def constructTree(self, temp, n, alpha, alphaTar):
        if n <= 0:
            return
        if temp is None and n == 1:
            node = Node(alpha, None, 1)
            node.alphaTar = alphaTar
            self.root = node
        elif temp is None:
            rndNum = random.random()
            if rndNum < 0.5:
                newNode = Node('V', None, 0)
            else:
                newNode = Node('H', None, 0)
            newNode.alphaTar = alphaTar
            self.root = newNode
            self.constructTree(self.root, n, alpha, alphaTar)
        elif n == 2:
            temp.left = Node(alpha, temp, 1)
            temp.right = Node(alpha, temp, 1)
            if temp.split == 'V':
                temp.left.alphaTar = alphaTar / 2
                temp.right.alphaTar = alphaTar / 2
            else:
                temp.left.alphaTar = alphaTar * 2
                temp.right.alphaTar = alphaTar * 2
        elif n > 2:
            a = n // 2
            b = n - a
            rndNum = random.random()
            split = 'H'
            if a == 1:
                temp.left = Node(alpha, temp, 1)
            else:
                if rndNum < 0.5:
                    split = 'V'
                temp.left = Node(split, temp, 0)
            rndNum = random.random()
            split = 'H'
            if rndNum < 0.5:
                split = 'V'
            temp.right = Node(split, temp, 0)
            if temp.split == 'V':
                temp.left.alphaTar = alphaTar / 2
                temp.right.alphaTar = alphaTar / 2
            else:
                temp.left.alphaTar = alphaTar * 2
                temp.right.alphaTar = alphaTar * 2
            self.constructTree(temp.left, a, alpha, temp.left.alphaTar)
            self.constructTree(temp.right, b, alpha, temp.right.alphaTar)

    def adjustTree(self):
        if self.root is None:
            return
        q = [self.root]
        while q:
            temp = q.pop(0)
            if temp.left:
                if temp.alpha > temp.alphaTar:
                    temp.split = 'H'
                    temp.left.alphaTar = temp.alphaTar * 2
                    temp.right.alphaTar = temp.alphaTar * 2
                elif temp.alpha < temp.alphaTar:
                    temp.split = 'V'
                    temp.left.alphaTar = temp.alphaTar / 2
                    temp.right.alphaTar = temp.alphaTar / 2
                q.append(temp.left)
            if temp.right:
                q.append(temp.right)
