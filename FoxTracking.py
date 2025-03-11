largestValues = []

def sortArray(largestValues, trackingArr):
    while(True):
        swapsMade = 0
        for i in range(len(largestValues)-1):
            if trackingArr[largestValues[i][1]][largestValues[i][0]] > trackingArr[largestValues[i+1][1]][largestValues[i+1][0]]:
                temp = largestValues[i]
                largestValues[i] = largestValues[i+1]
                largestValues[i+1] = temp
                swapsMade += 1
        if swapsMade == 0:
            break
            
#largestValues in x,y coordinates of the pen            
def findFiveLargest(trackingArr, largestValues, numLocations, arrSizeX, arrSizeY):
    for y in range(arrSizeY):
        for x in range(arrSizeX):
            if len(largestValues) < numLocations:
                largestValues.append([x,y])
            else:
                sortArray(largestValues, trackingArr)
                if trackingArr[y][x] > trackingArr[largestValues[0][1]][largestValues[0][0]]:
                    largestValues[0][0] = x
                    largestValues[0][1] = y

def highCanidTraffic(arr1, arr2, trafficArr, arrSizeX, arrSizeY):
    for y in range(arrSizeY):
        for x in range(arrSizeX):
            if arr2[y][x] > 0 and arr2[y][x] != arr1[y][x]:
                trafficArr[y][x] += 1   

highCanidTraffic(array1, array2, trafArr, 3, 3)
print(trafArr)
#arr1 = 2D array, uniqueFoxArray = 3D array
def uniqueCanidTraffic(arr1, uniqueFoxArray, arrSizeX, arrSizeY):
    for y in range(arrSizeY):
        for x in range(arrSizeX):
            if arr1[y][x] > 0 and arr1[y][x] not in uniqueFoxArray[y][x][1:]:
                uniqueFoxArray[y][x][0] += 1
                uniqueFoxArray[y][x].append(arr1[y][x])

