import librosa
import soundfile as sf
import io

# 音声ファイルをバイナリデータとして読み込む
with open("sample.wav", "rb") as f:
    audio_data = f.read()

# バイナリデータをBytesIOオブジェクトに変換
audio_file = io.BytesIO(audio_data)

# BytesIOオブジェクトをlibrosaで読み込むためにsoundfileを使用
y, sr = sf.read(audio_file, dtype='float32')

# 必要に応じてlibrosaで使用可能な形式に変換（リサンプリング）
target_sr = 22050
y_resampled = librosa.resample(y.T, orig_sr=sr, target_sr=target_sr)

print("音声データの形状:", y_resampled.shape)
print("サンプリングレート:", target_sr)

