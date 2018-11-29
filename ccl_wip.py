import math
import time

points_sim = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 4, 4, 4, 2, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 4, 4, 4, 2, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 4, 8, 4, 2, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 3, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 3, 9, 9, 6, 4, 2],
            [0, 0, 0, 8, 0, 0, 0, 0, 0, 0, 7, 8, 5, 8, 3, 0],
            [0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 7, 9, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ]
# points_sim = [
#             [88, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5],
#             [5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5],
#             [5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5],
#         ]

def CCLBlob():
    leftPixel = 0
    topPixel = 0
    thresh = 0
    width = 16
    height = 16

    # deep copy of points
    points_labeled = []#list(points_sim)
    for i in range(len(points_sim)):
        points_labeled.append(points_sim[i][:])

    numLabels = 0
    labels = {}
    blobSizes = {}
    blobPositions = {}
    blobPressures = {}

    for y,line in enumerate(points_sim):
        for x,val in enumerate(line):
            # check if current pixel is on or off
            if(val<=thresh):
                points_labeled[y][x] = 0
                continue
            # deal with top/left border pixels
            if(y<=0):
                topPixel = 0
            else:
                topPixel = points_labeled[y-1][x]
            if(x<=0):
                leftPixel = 0
            else:
                leftPixel = points_labeled[y][x-1]
            # add new label and assign
            if(topPixel+leftPixel==0):
                numLabels = numLabels + 1
                labels[numLabels] = numLabels
                blobSizes[numLabels] = 0
                blobPositions[numLabels] = [0,0]
                blobPressures[numLabels] = 0.0
                # labels.append(numLabels)
                points_labeled[y][x] = numLabels
            else:
                if(topPixel>leftPixel):
                    if(leftPixel>0):
                        #labels[leftPixel].append(topPixel)
                        labels[topPixel] = leftPixel
                        points_labeled[y][x] = leftPixel
                    else:
                        points_labeled[y][x] = topPixel
                elif(leftPixel>topPixel):
                    if(topPixel>0):
                        # labels[topPixel].append(leftPixel)
                        labels[leftPixel] = topPixel
                        points_labeled[y][x] = topPixel
                    else:
                        points_labeled[y][x] = leftPixel
                elif(leftPixel==topPixel):
                    points_labeled[y][x] = topPixel
    
    for y,line in enumerate(points_labeled):
        for x,val in enumerate(line):
            if val!=0:
                points_labeled[y][x] = labels[val]
                blobSizes[labels[val]] += 1
                blobPositions[labels[val]][0] += float(x)#/width
                blobPositions[labels[val]][1] += float(y)#/height
                blobPressures[labels[val]] += points_sim[y][x]
            # check through labels to see if value is root (do this outside of loop? caseswitch?)
    for key in labels:
        if blobSizes[key]==0:
            blobSizes.pop(key, None)
            blobPositions.pop(key, None)
        else:
            blobPositions[key][0] /= blobSizes[key]
            blobPositions[key][0] /= width
            blobPositions[key][1] /= blobSizes[key]
            blobPositions[key][1] /= height
            blobPressures[key] /= blobSizes[key]
            blobSizes[key] /= float(width*height)

    # print("--- SIMULATED POINTS")
    # print(points_sim)
    # print("######## RESULTS ########")
    # print("--- LABELED POINTS")
    # print(points_labeled)
    # print("--- LABELS")
    # print(labels)
    # print("--- SIZES")
    # print(blobSizes)
    # print("--- POSITIONS")
    # print(blobPositions)
    # print("--- PRESSURES")
    # print(blobPressures)

while True:
    then = time.time()
    CCLBlob()
    processTimeInMs = (time.time() - then)*1000.0
    print(str(processTimeInMs) + "ms")






