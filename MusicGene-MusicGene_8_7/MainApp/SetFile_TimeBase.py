import numpy as np


file_name = "MusicalScaleList3.txt"

write_file = "MusicalScaleList4.txt"
fw = open(write_file, 'w', encoding="utf-8")
fw.close()

# 空の2次元配列を初期化
new_array = np.empty((0, 2), int)

with open(file_name, 'rt', encoding="utf-8") as f1:
    text1 = f1.readlines()
    for t in text1:
        sentence = t.strip().split(",")  # 改行とスペースを除去してから分割
        frame = int(sentence[0])
        scale = int(sentence[1])
        new_row = np.array([[frame, scale]])
        new_array = np.append(new_array, new_row, axis=0)

print(new_array)

sorted_array = new_array[new_array[:, 0].argsort()]

print(sorted_array)

fw = open(write_file, 'a', encoding="utf-8")
for list in sorted_array:
    fw.write(str(list[0]) + "," + str(list[1]) + "\n")
    
fw.close()