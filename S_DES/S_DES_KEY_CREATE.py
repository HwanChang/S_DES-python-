class KEY :

    P10 = {3:9, 5:8, 2:7, 7:6, 4:5, 10:4, 1:3, 9:2, 8:1, 6:0}
    P8 = {6:7, 3:6, 7:5, 4:4, 8:3, 5:2, 10:1, 9:0}

    def Mix(self, cnt, key, A) :
        sum = 0
        mask = 0b0000000001
        i = 0
        for i in range(cnt) :
            if (mask << i) & key == mask << i :
                sum = sum + 2**A[10-i]
            i = i + 1
        return sum


    def Half(self, key, cnt) :
        if cnt == 5 :
            firstNum = key >> 5
            secondNum = (key & 0b0000011111)
        elif cnt == 4 :
            firstNum = key >> 4
            secondNum = (key & 0b00001111)

        return (firstNum, secondNum)
    

    def SHIFT(self, cnt, firstNum, secondNum) :
        i = 0
        for i in range(cnt) :
            if firstNum >= 16 :
                firstNum = firstNum << 1
                firstNum = (firstNum & 0b0000011111) + 1
            else :
                firstNum = firstNum << 1
            if secondNum >= 16 :
                secondNum = secondNum << 1
                secondNum = (secondNum & 0b0000011111) + 1
            else :
               secondNum = secondNum << 1

        return (firstNum, secondNum)
