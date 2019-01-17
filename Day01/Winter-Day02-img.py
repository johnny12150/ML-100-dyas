import numpy as np
from PIL import Image


def bruteforce(I, P):
    r"""
    暴力比較兩張圖
    :param I: image, 大圖
    :param P: pattern, 小圖
    :return: error最小的 h & w
    """

    # 大圖的長寬
    BH = I.shape[0]
    BW = I.shape[1]

    # 小圖的長寬
    SH = P.shape[0]
    SW = P.shape[1]
    minError = 255 * 64 * 64

    for h in range(BH-SH+1):
        print(h)
        for w in range(BW-SW+1):
            error = 0
            for y in range(SH):
                for x in range(SW):
                    d = I[h + y, w + x] - P[y, x]
                    if (d < 0):
                        d = -d
                    error += d
            if error < minError:
                minError = error
                minh = h
                minw = w

    print(error)
    return minh, minw


def Integral(I):
    H, W = I.shape
    II = np.zeros((H, W)).astype(int)
    II[:, 0] = I[:, 0]

    for h in range(H):
        for w in range(1, W):
            II[h, w] = II[h, w-1] + I[h, w]
    III = np.zeros((H, W)).astype(int)
    III[0, :] = II[0, :]

    for h in range(1, H):
        for w in range(W):
            III[h, w] = III[h-1, w] + II[h, w]

    # 最左與最上補0
    IIII = np.zeros((H+1, W+1)).astype(int)
    IIII[1:H+1, 1:W+1] = III[:, :]
    # III(h2, w2) + III(h1-1, w1-1) - III(h2, w1-1)- III(h1-1, w2)
    # print(III[164, 164] + III[99, 99] - III[164, 99] - III[99, 164])
    return IIII


def calc_error(I2, P2, I, P, h, w, L):
    if L == 6:
        tmpsum = 0
        for m in range(64):
            for n in range(64):
                tmp = I[h+m][w+n] - P[m][n]
                if tmp < 0:
                    tmp = -tmp
                tmpsum += tmp
        return tmpsum

    # 算切成幾乘幾, block size
    cut = int(64 / 2**L)
    tmpsum =0
    # 計算每格
    for k in range(0, 64, cut):
        for l in range(0, 64, cut):
            # tmp暫存err
            # tmp = cal_integral(w+k, h+l, cut, I2) - cal_integral(k, l, cut, P2)
            Ih2 = k+h+cut
            Ih1 = k+h
            Iw1 = l+w
            Iw2 = l+w+cut
            Ph2 = k + cut
            Ph1 = k
            Pw2 = l +cut
            Pw1 = l
            tmp1 = I2[Ih2, Iw2]+I2[Ih1, Iw1]-I2[Ih2, Iw1]-I2[Ih1, Iw2]
            tmp2 = P2[Ph2, Pw2]+P2[Ph1, Pw1]-P2[Ph2, Pw1]-P2[Ph1, Pw2]
            # tmp = tmp1 - tmp2
            # 同意思
            tmp = cal_integral(k+h, l+w, cut, I2) - cal_integral(k, l, cut, P2)

            if tmp < 0:
                tmp = -tmp
            tmpsum += tmp
    return tmpsum


def cal_integral(xmin, ymin, cut, integral):
    return integral[xmin, ymin] + integral[xmin+cut, ymin+cut] - integral[xmin, ymin+cut] - integral[xmin+cut, ymin]


img = Image.open('big.jpg')
grey_img = img.convert('L')  # 轉成灰階
img_arr = np.array(grey_img)  # tuple轉array
img_arr = img_arr.astype(int)  # unit8轉int32
# print(img_arr)
# print(img_arr.dtype)

img2 = Image.open('small.jpg')
grey_img2 = img2.convert('L')  # 轉成灰階
img_arr2 = np.array(grey_img2)  # tuple轉array
img_arr2 = img_arr2.astype(int)

#   RUN 硬解的比較
# bruteh, brutew = bruteforce(img_arr, img_arr2)
# print([bruteh, brutew])

I2 = Integral(img_arr)
P2 = Integral(img_arr2)
print(I2)

# 100加64
print(np.sum(img_arr[100:164, 100:164]))
print(I2[100, 100]+I2[164, 164]-I2[100, 164]-I2[164, 100])

print(calc_error(I2, P2, img_arr, img_arr2, 83, 64, 4))

IH, IW = img_arr.shape
PH, PW = img_arr2.shape
num = (IH-PH+1) * (IW-PW+1)
Table = np.ndarray((num, 4)).astype(int)
count = 0

for h in range(IH-PH+1):
    for w in range(IW-PW+1):
        Table[count][0] = h
        Table[count][1] = w
        Table[count][2] = 0
        Table[count][3] = calc_error(I2, P2, img_arr, img_arr2, h, w, 0)
        count += 1


def heapify(Tree, Table, n):
    # 數的長度
    num = len(Tree)
    # 左兒子節點
    lc = 2*n+1
    rc = 2*n+2
    # 沒兒子
    if lc >= num:
        return
    # 有右兒子
    if rc < num and Table[Tree[rc], 3] < Table[Tree[lc], 3]:
        sc = rc
    else:
        sc =lc
    # 跟小兒子互換
    if Table[Tree[sc], 3] < Table[Tree[n], 3]:
        # python特殊的swap
        Tree[sc], Tree[n] = Tree[n], Tree[sc]
        heapify(Tree, Table, sc)


# 建heap tree
Tree = np.arange(num)
for count in range(num//2, -1, -1):
    heapify(Tree, Table, count)

mini = Tree[0]
while Table[mini][2] < 6:
    h = Table[mini][0]
    w = Table[mini][1]
    L = Table[mini][2] + 1
    Table[mini][2] = L
    Table[mini][3] = calc_error(I2, P2, img_arr, img_arr2, h, w, L)
    heapify(Tree, Table, 0)
    mini = Tree[0]

print([Table[mini][0], Table[mini][1]])

# 用heap tree前找min err的方法
"""
mini = 0
# 假定最小值
minError = Table[0][1]
for i in range(1, num):
    if Table[i][3] < minError:
        minError = Table[i][3]
        mini = i

while Table[mini][2] < 6:
    h = Table[mini][0]
    w = Table[mini][1]
    L = Table[mini][2] + 1
        Table[mini][2] = L
    Table[mini][3] = calc_error(I2, P2, img_arr, img_arr2, h, w, L)
    mini = 0
    minError = Table[0][1]
    for i in range(1, num):
        if Table[i][3] < minError:
            minError = Table[i][3]
            mini = i

print([Table[mini][0], Table[mini][1]])
"""
