import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile

# 音声データの読み込み
sample_rate, data = wavfile.read('recording.wav')

# フーリエ変換の実行
fft_result = np.fft.fft(data)
# 周波数軸の生成（kHzに変換）
freqs = np.fft.fftfreq(len(data), 1/sample_rate) / 1000

# 結果のプロット
plt.figure(figsize=(12, 6))

# 元の音声データのプロット
plt.subplot(2, 1, 1)
time = np.arange(len(data)) / sample_rate
plt.plot(time, data)
plt.title("Original Audio Signal")
plt.xlabel("Time [s]")
plt.ylabel("Amplitude")

# フーリエ変換結果のプロット
plt.subplot(2, 1, 2)
plt.plot(freqs, np.abs(fft_result))
plt.title("Fourier Transform")
plt.xlabel("Frequency [kHz]")
plt.ylabel("Amplitude")
plt.xlim(0, sample_rate / 2000)  # 正の周波数成分のみ表示（kHzに変換済み）

plt.tight_layout()
plt.show()
