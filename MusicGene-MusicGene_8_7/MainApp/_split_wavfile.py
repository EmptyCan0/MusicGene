import librosa
import soundfile as sf
import matplotlib.pyplot as plt
import numpy as np

# 配列をある数の要素ごとに平均値を計算
def average_block(arr, block_size):
    #100個の要素数の場合、reshape(-1, 5)により、形状が (20, 5) になる
    return arr.reshape(-1, block_size).mean(axis=1) #axix=1によって上の20の要素（列）を取得

#閾値よりも小さく、それが重複している部分を削除する
def remove_below_threshold_duplicates(amp_array,time_array, threshold):
    # 空のリストを初期化
    amp = []
    time = []
    core_time = []
    switch = False
    # 配列をループして、閾値より低いかつ重複を消去
    for i in range(len(amp_array)):
        #一回目だったらスキップ
        if not amp:
            amp.append(amp_array[i])
            time.append(time_array[i])
            continue

        if amp[-1] >= threshold:
            amp.append(amp_array[i])
            time.append(time_array[i])
        elif amp_array[i] >= threshold:
            amp.append(amp_array[i])
            time.append(time_array[i])
            if not switch:
                core_time.append(time_array[i])
                switch = True
            core_time[-1] = (core_time[-1] + time_array[i]) / 2
            switch = False
        else:
            time[-1] = (time[-1] + time_array[i]) / 2
            if not switch:
                core_time.append(time_array[i])
                switch = True
            else:
                core_time[-1] = (core_time[-1] + time_array[i]) / 2
    # リストをNumPy配列に変換
    return np.array(amp),np.array(time),np.array(core_time)

#求めた時間のリストから、実際に音声ファイルを分割する
def split_wav_by_ranges(y, sr, peak_times):
    # 音声のサンプル数を取得
    total_samples = len(y)
    
    # 音声の総時間を秒で取得
    total_duration_sec = total_samples / sr
    
    ranges = []
    min_range = 0.15
    for i in range(0,len(peak_times)):
        if i == 0:
            continue
        if peak_times[i] - peak_times[i - 1] > min_range:
            ranges.append([peak_times[i - 1],peak_times[i]])
    
    cut_second = 0.1
    if total_duration_sec - ranges[-1][1] > cut_second:
        ranges.append([ranges[-1][1],total_duration_sec])
        
    print(ranges)
    
    for idx, (start_ratio, end_ratio) in enumerate(ranges):
        # サンプル数に変換
        start_sample = int(start_ratio * sr)
        end_sample = int(end_ratio * sr)
        
        # 音声を分割
        split_audio = y[start_sample:end_sample]
        
        # ファイルに保存
        sf.write(f"split_{idx + 1}.wav", split_audio, sr)

# 音声ファイルの読み込み
y, sr = librosa.load("sample.wav")

# サンプル値の絶対値を取得
reduce_number = 50
y_reduced = np.abs(y[::reduce_number])
block_number = 10
y_reduced = y_reduced[:((len(y_reduced)//block_number) * block_number)]
print(len(y_reduced))

y_average = average_block(y_reduced,block_number)
time = reduce_number * block_number * np.arange(len(y_average)) / sr 

new_y , new_time, peak_time = remove_below_threshold_duplicates(y_average,time,threshold=np.mean(y_average)/2)

#＝＝＝＝＝＝＝＝＝＝＝＝＝音声を分割している重要な部分＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝
split_wav_by_ranges(y = y , sr = sr , peak_times = peak_time)
#＝＝＝＝＝＝＝＝＝＝＝＝＝音声を分割している重要な部分＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝


