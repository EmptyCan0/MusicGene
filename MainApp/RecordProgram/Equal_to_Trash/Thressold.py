import numpy as np

def remove_below_threshold_duplicates(array, threshold):
    # 空のリストを初期化
    result = []
    # 配列をループして、閾値より低いかつ重複を消去
    for i in range(len(array)):
        #一回目だったらスキップ
        if not result:
            result.append(array[i])
            continue
        if result[-1] >= threshold:
            result.append(array[i])
        elif array[i] >= threshold:
            result.append(array[i])
    # リストをNumPy配列に変換
    return np.array(result)

# 例として元の配列を作成
original_array = np.array([1, 2, 0.5, 0.3, 4, 5,0.1,0.8, 0.2, 6, 7, 8])

# 設定する閾値
threshold = 1.0

new_array = remove_below_threshold_duplicates(original_array,threshold)

print("Original array:", original_array)
print("New array after merging values below threshold:", new_array)
