import cv2
import random
from binaryTree import BinaryTree
import numpy as np

class Collage:
    def __init__(self, alphaTarget, alpha, n):
        self.num_images = n
        self.alpha = alpha
        self.alphaTar = alphaTarget
        self.collage = None
        self.levelOrderArray = None
        self.layout = None

    def constructLayout(self):
        self.layout = BinaryTree()
        self.layout.constructTree(None, self.num_images, self.alpha, self.alphaTar)
        self.layout.calculateAlpha(self.layout.root)
        self.layout.adjustTree()
        self.layout.calculateAlpha(self.layout.root)
        self.layout.calculateDimension(2000)
        self.layout.calculateIndex()

    def makeCollage1(self, images):
        buffer = cv2.Mat(self.levelOrderArray[0].height, self.levelOrderArray[0].width, cv2.CV_8UC(3))
        for k in range(1, len(self.levelOrderArray)):
            resizedImage = cv2.Mat()
            size = cv2.Size(self.levelOrderArray[k].width, self.levelOrderArray[k].height)
            cv2.resize(images[k-1], resizedImage, size)

            a = self.levelOrderArray[k].xIndex
            b = self.levelOrderArray[k].yIndex
            h = self.levelOrderArray[k].height
            w = self.levelOrderArray[k].width
            imgROI = buffer.submat(cv2.Rect(b, a, w, h))
            resizedImage.copyTo(imgROI)

        self.collage = buffer


    def makeCollage2(self, images):

        buffer = np.zeros((abs(self.levelOrderArray[0].height), abs(self.levelOrderArray[0].width), 3), dtype = "uint8")

        for k in range(1, len(self.levelOrderArray)):

            resizedImage = cv2.resize(images[k - 1], (abs(self.levelOrderArray[k].width), abs(self.levelOrderArray[k].height)))


            a = self.levelOrderArray[k].xIndex
            b = self.levelOrderArray[k].yIndex
            for i in range(self.levelOrderArray[k].height):
                for j in range(self.levelOrderArray[k].width):
                    il = a + i
                    jl = b + j
                    data = resizedImage[i, j]
                    buffer[il, jl] = data

        return buffer

    @staticmethod
    def scalarMultiply(array, scale):
        result = [array[i] * scale for i in range(3)]
        return result

    @staticmethod
    def addArrays(array1, array2):
        result = [array1[i] + array2[i] for i in range(3)]
        return result

    @staticmethod
    def blendBoundary(image1, image2, wh, reqHeight, reqWidth):
        img1h, img1w, img1ch = image1.shape
        img2h, img2w, img2ch = image2.shape

        if wh == 'w':
            blendVal = int(1.5 * min(img1h, img2h) / 10)
            width = img1w
            height = img1h + img2h - blendVal
        else:
            blendVal = int(1.5 * min(img1w, img2w) / 10)
            width = img1w + img2w - blendVal
            height = img1h

        # buffer = cv2.Mat(height, width, cv2.CV_8UC(3))
        buffer = np.zeros((height, width, 3), dtype = "uint8")

        if wh == 'w':
            for i in range(img1h):
                for j in range(width):
                    data = image1[i, j]
                    buffer[i,j] = data

            for i in range(img2h):
                for j in range(width):
                    data1 = image2[i, j]

                    if i < blendVal:
                        data2 = buffer[img1h - blendVal + i, j]
                        scale1 = i / blendVal
                        scale2 = 1 - scale1

                        data1 = Collage.scalarMultiply(data1, scale1)
                        data2 = Collage.scalarMultiply(data2, scale2)

                        buffer[img1h - blendVal + i, j] =  Collage.addArrays(data1, data2)
                    else:
                        buffer[img1h - blendVal + i, j] =  data1
        else:
            for i in range(height):
                for j in range(img1w):
                    data = image1[i, j]
                    buffer[i, j] = data

            for i in range(height):
                for j in range(img2w):
                    data1 = image2[i, j]

                    if j < blendVal:
                        data2 = buffer[i, img1w - blendVal + j]
                        scale1 = j / blendVal
                        scale2 = 1 - scale1

                        data1 = Collage.scalarMultiply(data1, scale1)
                        data2 = Collage.scalarMultiply(data2, scale2)

                        buffer[i, img1w - blendVal + j] = Collage.addArrays(data1, data2)
                    else:
                        buffer[i, img1w - blendVal + j] = data1

        resizedImage = cv2.resize(buffer, (reqWidth, reqHeight))

        # resizedImage = cv2.Mat()
        # size = cv2.Size(reqWidth, reqHeight)
        # cv2.resize(buffer, resizedImage, size)

        return resizedImage

    def makeCollage3(self, images, treeNode, n):
        if treeNode is None:
            return cv2.Mat()
        if treeNode.left is None:
            resizedImg = cv2.resize(images[0], (abs(treeNode.width), abs(treeNode.height)))
            # resizedImg = cv2.Mat()
            # size = cv2.Size(treeNode.width, treeNode.height)
            # cv2.resize(images[0], resizedImg, size)
            return resizedImg

        a = n // 2
        slice1 = images[:a]
        slice2 = images[a:]

        collage1 = self.makeCollage3(slice1, treeNode.left, a)
        collage2 = self.makeCollage3(slice2, treeNode.right, n - a)

        wh = 'w' if treeNode.split == 'V' else 'h'

        return self.blendBoundary(collage1, collage2, wh, treeNode.height, treeNode.width)

    def makeCollage(self, frames):
        collages = [None] * 150
        for i in range(150):
            images = [frames[j][i] for j in range(self.num_images)]
            newCollage = self.makeCollage2(images)
            collages[i] = newCollage
        return collages

    def constructCollage(self):
        self.constructLayout()
        self.levelOrderArray = self.layout.levelOrder(self.num_images)

    def constructCollage(self, images, isBlendBoundary):
        self.constructLayout()
        if isBlendBoundary:
            self.collage = self.makeCollage3(images, self.layout.root, self.num_images)
        else:
            self.levelOrderArray = self.layout.levelOrder(self.num_images)
            col = self.makeCollage2(images)
            self.collage = col

    def getCollage(self):
        return self.collage
