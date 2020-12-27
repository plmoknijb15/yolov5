import os
import shutil
from os.path import join

l = os.listdir("contest")

images = []
labels = []
count = 0

for x1 in l:
    ll = os.listdir(join("contest", x1))
    #print(x1)
    for x2 in ll:
        #print(x2)
        lll = os.listdir(join("contest", x1, x2))
        images = []
        labels = []

        lll.sort()

        lll_0 = os.listdir(join("contest", x1, x2, lll[0]))
        lll_1 = os.listdir(join("contest", x1, x2, lll[1]))

        lll_0.sort()
        lll_1.sort()

        # print(len(lll_0))
        # print(len(lll_1))
        # print(lll_0[0].split('.')[0])
        # a = lll_0[0].split('.')[0]
        # print(lll_1[0].split('.')[0])
        # b = lll_1[0]
        # print(b.find(a))

        for i in lll_0:
            for j in lll_1:
                #print(i.split('.')[0])
                #print(j.split('.')[0])
                if j.find(i.split('.')[0]) == 0:
                    # images.append(join("contest", x1, x2, lll[0], i))
                    # labels.append(join("contest", x1, x2, lll[1], j))
                    shutil.move(join("contest", x1, x2, lll[0], i), join("dataset","images","train2017", i))
                    shutil.move(join("contest", x1, x2, lll[1], j), join("dataset","labels","train2017", j))
                    count += 1
                    break

print(count)
