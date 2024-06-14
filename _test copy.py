from pydub import AudioSegment
from pydub.silence import split_on_silence

# 入力ファイル名
input_file = "sample00.wav"

# サイレンスを検出して分割
sound = AudioSegment.from_wav(input_file)
chunks = split_on_silence(sound, min_silence_len=100, silence_thresh=-30)

print(len(chunks))

# 最初の無音部分を削除

if len(chunks) > 1:
    trimmed_sound = chunks[1]  # 最初の無音部分を削除
    trimmed_sound = chunks[0] + chunks[1] + chunks[2] + chunks[3]
else:
    trimmed_sound = sound  # 無音部分がないので、元の音声をそのまま使う



# 出力ファイル名
output_file = "output_trimmed.wav"

# トリミングした音声を保存
trimmed_sound.export(output_file, format="wav")
