import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np

# 音声ファイルの読み込み
y, sr = librosa.load("sample.wav")

# サンプル値の絶対値を取得
y_absolute = np.abs(y)
y_reduced =np.abs(y_absolute[::50])

time = np.arange(len(y_reduced)) / sr 

# 音声信号の波形をプロット
plt.figure(figsize=(14, 5))
plt.plot(time, y_reduced)
plt.title('Waveform (Absolute Values)')
plt.xlabel('Time (seconds)')
plt.ylabel('Amplitude')
plt.show()

print(f"Absolute values - min: {y_absolute.min()}, max: {y_absolute.max()}")
