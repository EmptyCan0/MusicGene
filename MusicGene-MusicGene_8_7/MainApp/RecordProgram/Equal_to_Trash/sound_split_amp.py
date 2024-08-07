import numpy as np
import librosa
import soundfile as sf

# 音声ファイルの読み込み
y, sr = librosa.load("your_audio_file.wav")

# 音声信号の振幅を計算（絶対値）
amplitude = np.abs(y)

# 閾値の設定
threshold = 0.05  # この値は調整が必要です

# 振幅が閾値を超える部分のインデックスを取得
above_threshold_indices = np.where(amplitude > threshold)[0]

# 分割点を検出
# ここでは連続するインデックスのセグメントを検出します
split_points = np.split(above_threshold_indices, np.where(np.diff(above_threshold_indices) > 1)[0] + 1)

# 分割された音声の保存
for i, segment in enumerate(split_points):
    if len(segment) > 0:
        start_sample = segment[0]
        end_sample = segment[-1] + 1
        y_segment = y[start_sample:end_sample]
        sf.write(f"segment_{i}.wav", y_segment, sr)

print("Audio has been split and saved into separate files.")
