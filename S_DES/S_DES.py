from S_DES_KEY_CREATE import *
class S_DES :

    IP8 = {4:7, 8:6, 5:5, 3:4, 6:3, 10:2, 7:1, 9:0}
    IP8Inverse = {6:7, 3:6, 5:5, 7:4, 9:3, 4:2, 10:1, 8:0}
    EPL4 = {10:3, 7:2, 8:1, 9:0}
    EPR4 = {8:3, 9:2, 10:1, 7:0}

    S0 = {
        (0,0):1, (0,1):0, (0,2):3, (0,3):2,
        (1,0):3, (1,1):2, (1,2):1, (1,3):0,
        (2,0):0, (2,1):2, (2,2):1, (2,3):3,
        (3,0):3, (3,1):1, (3,2):3, (3,3):2
        }
    S1 = {
        (0,0):0, (0,1):1, (0,2):2, (0,3):3,
        (1,0):2, (1,1):0, (1,2):1, (1,3):3,
        (2,0):3, (2,1):0, (2,2):1, (2,3):0,
        (3,0):2, (3,1):1, (3,2):0, (3,3):3
        }
    P4 = {8:3, 10:2, 9:1, 7:0}

    def Matrix(self, Left, Right) :
        LeftR = Left & 0b1001
        LeftC = Left & 0b0110
        RightR = Right & 0b1001
        RightC = Right & 0b0110

        if (LeftR) >= 0b1000 :
            LeftR = LeftR - 0b0110
        else :
            LeftR = LeftR & 0b0001

        LeftC = LeftC >> 1

        if (RightR) >= 0b1000 :
            RightR = RightR - 0b0110
        else :
            RightR = RightR & 0b0001

        RightC = RightC >> 1

        return ((LeftR, LeftC), (RightR, RightC))


key10 = int(input("10자리 2진수 키 입력 : "), 2)
mkKey = KEY()

half = mkKey.Half(mkKey.Mix(10, key10, KEY.P10), 5)

SHIFT01 = mkKey.SHIFT(1, half[0], half[1])

mergeSHIFT01 = (SHIFT01[0] << 5) + SHIFT01[1]
key01 = mkKey.Mix(8, mergeSHIFT01, KEY.P8)

SHIFT02 = mkKey.SHIFT(2, SHIFT01[0], SHIFT01[1])
mergeSHIFT02 = (SHIFT02[0] << 5) + SHIFT02[1]
key02 = mkKey.Mix(8, mergeSHIFT02, KEY.P8)


plainText = int(input("8자리 2진수 평문 입력 : "), 2)

s_des = S_DES()

halfIP = mkKey.Half(mkKey.Mix(8, plainText, S_DES.IP8), 4)
afterEPL = mkKey.Mix(4, halfIP[1], S_DES.EPL4)
afterEPR = mkKey.Mix(4, halfIP[1], S_DES.EPR4)
afterEP = (afterEPL << 4) + afterEPR

keyEP = key01 ^ afterEP
halfKeyEP = mkKey.Half(keyEP, 4)

matrixR = s_des.Matrix(halfKeyEP[0], halfKeyEP[1])

afterSbox = (S_DES.S0[matrixR[0]] << 2) + S_DES.S1[matrixR[1]]

afterP4 = mkKey.Mix(4, afterSbox, S_DES.P4)

endFK = halfIP[0] ^ afterP4

endRound = (endFK << 4) + halfIP[1]     #1라운드에선 없어도 됨
afterSW = (halfIP[1] << 4) + endFK
########################1라운드###########################

afterEPL_2 = mkKey.Mix(4, endFK, S_DES.EPL4)
afterEPR_2 = mkKey.Mix(4, endFK, S_DES.EPR4)
afterEP_2 = (afterEPL_2 << 4) + afterEPR_2

keyEP_2 = key02 ^ afterEP_2
halfKeyEP_2 = mkKey.Half(keyEP_2, 4)

matrixR_2 = s_des.Matrix(halfKeyEP_2[0], halfKeyEP_2[1])

afterSbox_2 = (S_DES.S0[matrixR_2[0]] << 2) + S_DES.S1[matrixR_2[1]]

afterP4_2 = mkKey.Mix(4, afterSbox_2, S_DES.P4)

endFK_2 = halfIP[1] ^ afterP4_2
endRound_2 = (endFK_2 << 4) + endFK

Last = mkKey.Mix(8, endRound_2, S_DES.IP8Inverse)
########################2라운드###########################

print(bin(Last))
