import numpy as np

# 例として元の配列を作成
original_array = np.arange(100)  # 例えば、0から99までの配列

# 配列を5つの要素ごとに平均値を計算
def average_block(arr, block_size):
    return arr.reshape(-1, block_size).mean(axis=1)

# 5つの要素ごとの平均値を計算
block_size = 5
reduced_array = average_block(original_array, block_size)

print("Original array length:", len(original_array))
print("Reduced array length:", len(reduced_array))
print("Reduced array:", reduced_array)
