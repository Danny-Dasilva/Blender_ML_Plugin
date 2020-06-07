
lst = [1, 2, 3, 4, 5, 6, 7, 8]
# for count, x in enumerate(reversed(lst)):
#     print(count)
#     if x < 6:
#         lst.remove(x)
# print(lst)

col = [
            [255, 128, 0, 1],
            [255, 255, 0, 1],
            [0, 255, 0, 1],
            [0, 255, 128, 1],
            [0, 255, 255, 1],
            [0, 128, 255, 1],
            [0, 0, 255, 1],
            [127, 0, 255, 1],
            [255, 0, 127, 1],
   
        ]
def normalize(a):
        amin, amax = 0, 255
        for count, v in enumerate(a):
            for i, val in enumerate(v):
                print(a[count])
                a[count][i] = (val-amin) / (amax-amin)

        return a
print(normalize(col))