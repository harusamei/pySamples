# 创建一个整数数组
def double(pair):
    return [pair[0], pair[1] * 2]
my_array = [1, 2, 3, 4, 5]
new_array = list(map(lambda pair: [pair[0],pair[1]], enumerate(my_array)))
# 打印数组
print(sum(new_array, []))

