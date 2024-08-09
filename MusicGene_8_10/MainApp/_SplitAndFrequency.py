from flask import Flask, request, render_template, redirect, url_for, jsonify, send_from_directory, send_file
from pydub import AudioSegment
import os
import threading

import librosa
import soundfile as sf
import numpy as np
import io

import re
from pydub.silence import detect_nonsilent

Music_Path = "static//MusicSample//東方Project//いざ、倒れ逝くその時まで.txt"
Sound = "sample5.wav"
SoundPitch = 39

##################################################
############### 音声の生成系の部分 ################
##################################################
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
def split_wav_by_ranges(audio_data, peak_times):
    audio_seg = AudioSegment.from_wav(audio_data)
    # 音声の総時間を秒で取得
    total_duration_sec = len(audio_seg)/1000
    
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

    sounds = []
    
    #   分割された音声ファイルを保存する
    for i, (start_sec, end_sec) in enumerate(ranges):
        # 秒単位をミリ秒単位に変換
        start_time = start_sec * 1000  # ミリ秒単位
        end_time = end_sec * 1000  # ミリ秒単位
        
        # 指定した時間範囲で分割
        split_audio = audio_seg[start_time:end_time]
        
        # 分割した音声を新しいファイルとして保存
        sounds.append(split_audio)
        
    return sounds


def EditMusicFile(audio_data):
    # バイナリデータをBytesIOオブジェクトに変換
    audio = audio_data.read()
    audio_file = io.BytesIO(audio)

    # BytesIOオブジェクトをlibrosaで読み込むためにsoundfileを使用
    y, sr = sf.read(audio_file, dtype='float32')

    # 必要に応じてlibrosaで使用可能な形式に変換（リサンプリング）
    target_sr = 22050
    y = librosa.resample(y.T, orig_sr=sr, target_sr=target_sr)

    # サンプル値の絶対値を取得
    reduce_number = 50
    y_reduced = np.abs(y[::reduce_number])
    block_number = 10
    y_reduced = y_reduced[:((len(y_reduced)//block_number) * block_number)]

    y_average = average_block(y_reduced,block_number)
    time = reduce_number * block_number * np.arange(len(y_average)) / sr 

    new_y , new_time, peak_time= remove_below_threshold_duplicates(y_average,time,threshold=np.mean(y_average))
    
    if len(peak_time) == 0:
        return None

    #＝＝＝＝＝＝＝＝＝＝＝＝＝音声を分割している重要な部分＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝
    soundfiles = split_wav_by_ranges(audio_data, peak_times = peak_time)
    #＝＝＝＝＝＝＝＝＝＝＝＝＝音声を分割している重要な部分＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝
    return soundfiles


def upload_file(file):
    # 音声ファイルの編集
    edited_file_path = generate_music(file)
    # ファイルを保存する場合（ここでは保存先を指定していますが、必要に応じて変更してください）
    # file.save(f"/path/to/save/{filename}")


def EditSoundFile(StartFrame,scale,combined_sound,add_sound):
    global NowScale
    start = int(StartFrame)
    #print(strSoundPath,start)
    combined_sound = combined_sound.overlay(add_sound, position= 1000 * start / 60)
    return combined_sound
   
def change_pitch(scale,sound):
    # 音声ファイルを読み込む
    audio = sound
    # ピッチを変更する
    global SoundPitch
    octaves = (int(scale) - int(SoundPitch)) / 24 #24が違和感もっともない
    new_sample_rate = int(audio.frame_rate * (4 ** octaves))
    audio = audio._spawn(audio.raw_data, overrides={
        "frame_rate": new_sample_rate
    }).set_frame_rate(audio.frame_rate)
    
    #ピッチを変更したaudioファイルを返す
    return audio

# 各AudioSegmentの最大音量を取得してソートする関数
def get_max_volume(audio_segment):
    return audio_segment.max_dBFS

def generate_music(file):
    more_than_2_sounds = False
    
    sounds = EditMusicFile(file)
    if sounds != None:
        sorted_audio_segments = sorted(sounds, key=get_max_volume, reverse=True)
        more_than_2_sounds = True
    else:
        sounds =AudioSegment.from_wav(file)
        
    global Music_Path
    file_name = Music_Path

    global NowScale
    NowScale = 0
    combined_sound = AudioSegment.silent(duration=12000)
    IsSample = False
    
    global Count
    Count = 0
    
    newaudio = None

    with open(file_name, 'rt', encoding="utf-8") as f1:
        text1 = f1.readlines()
        for t in text1:
            if Count == 0:
                Duration = int(t.split('_')[1])
                if "MusicSample" in Music_Path:
                    combined_sound = AudioSegment.silent(duration=30000)
                    IsSample = True
                else:
                    combined_sound = AudioSegment.silent(duration=Duration)
                    IsSample = False
                Count += 1
                continue
            sentence = t.strip().split(",") 
            frame = sentence[0]
            scale = re.search(r'\d+', sentence[1]).group()
            color = re.search(r'\D+', sentence[1]).group()
            if int(NowScale) != int(scale):
                if more_than_2_sounds:
                    if color == 'g':
                        newaudio = change_pitch(scale,sorted_audio_segments[0])
                    else:
                        newaudio = change_pitch(scale,sorted_audio_segments[1])
                else:
                    newaudio = change_pitch(scale,sounds)
                NowScale = scale
            combined_sound = EditSoundFile(frame,scale,combined_sound,newaudio)
            Count += 1
            
            #print(Count)
    f1.close()
    global SoundPitch
    
    combined_sound.export("unko.wav", format="wav")

##################################################
############### 音声の生成系の部分 ################
##################################################
from werkzeug.datastructures import FileStorage

# "sample.wav"を読み込む
with open(Sound, 'rb') as f:
    sample_wav_data = f.read()

# io.BytesIOオブジェクトを作成
sample_wav_stream = io.BytesIO(sample_wav_data)

# FileStorageオブジェクトを作成
sample_wav_file = FileStorage(stream=sample_wav_stream, filename=Sound, content_type="audio/wav")


upload_file(sample_wav_file)