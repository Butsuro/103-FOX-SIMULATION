class captureSystem:
    def __init__(self, length, width, height, pos):
        self.length = length
        self.width = width
        self.height = height
        self.pos = np.array(pos)
        self.totalCaptures = 0
        self.correctCaptures = 0
        self.correctCapturePercent = 0
        self.capturedCanids = []
        
    def captureCanid(self, masterArray, foxList, targetCanid):
        x = round(self.pos[0])
        y = round(self.pos[1])
        if masterArray[1][y][x] != 0:
            capturedCanid = masterArray[1][y][x]
            self.totalCaptures += 1
            #counter variable from move function
            captureTime = counter
            foxList.remove(capturedCanid)
            self.capturedCanids.append([capturedCanid, captureTime])
            if capturedCanid == targetCanid:
                self.correctCaptures += 1
                self.correctCapturePercent = self.correctCaptures/self.totalCaptures
