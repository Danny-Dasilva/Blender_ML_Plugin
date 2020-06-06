
lst = [1, 2, 3, 4, 5, 6, 7, 8]
# for count, x in enumerate(reversed(lst)):
#     print(count)
#     if x < 6:
#         lst.remove(x)
# print(lst)
a = ["foo", "bar", "baz"]

for i, e in reversed(list(enumerate(lst))):
    print(i, e)