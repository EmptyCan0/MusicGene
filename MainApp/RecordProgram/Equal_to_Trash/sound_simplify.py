import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np


# 配列をある数の要素ごとに平均値を計算
def average_block(arr, block_size):
    #100個の要素数の場合、reshape(-1, 5)により、形状が (20, 5) になる
    return arr.reshape(-1, block_size).mean(axis=1) #axix=1によって上の20の要素（列）を取得


# 音声ファイルの読み込み
y, sr = librosa.load("sample.wav")

print(len(y))

# サンプル値の絶対値を取得
reduce_number = 50
y_reduced =np.abs(y[::reduce_number])

print(len(y_reduced))

block_number = 10
y_average = average_block(y_reduced,block_number)
time = reduce_number * block_number * np.arange(len(y_average)) / sr 

print(np.mean(y_average))

# 音声信号の波形をプロット
plt.figure(figsize=(14, 5))
plt.plot(time, y_average)
plt.title('Waveform (Absolute Values)')
plt.xlabel('Time (seconds)')
plt.ylabel('Amplitude')
plt.show()
