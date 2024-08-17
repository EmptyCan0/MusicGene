from flask import Flask, request, session,render_template,jsonify, send_from_directory, send_file
from pydub import AudioSegment

import librosa
import soundfile as sf
import numpy as np
import io

import re
from pydub.silence import detect_nonsilent


#グローバル変数の定義

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
ALLOWED_EXTENSIONS = {'wav'}

import secrets
secret_key = secrets.token_hex(16)
app.config['SECRET_KEY'] = secret_key

@app.route('/')
def index():
    return render_template('index.html')

UPLOAD_FOLDER = 'uploads'
@app.route('/uploads/<filename>')
def get_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

################JSとのデータやり取り################

def SerchMaxCount(path):
    #MaxScaleの計測
    count = 0
    with open(path, 'rt', encoding="utf-8") as f:
        text1 = f.readlines()
        for t in text1:
            count += 1
    f.close()
    return count

##################################################
############### 音声の生成系の部分 ################
##################################################

################JSとのデータやり取り################


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

    
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "uncorrect file"}), 400
    
    # セッション内で `sent` の状態を管理
    if session.get('sent', False):
        return jsonify({"error": "Duplication error"}), 400


    if file and allowed_file(file.filename):
        session['sent'] = True  # セッションで `sent` を True に設定
        
        music_path = request.form.get('path')
        pitch = request.form.get('pitch')
        
        # 音声ファイルの編集
        try:
            edited_file = generate_music(file,music_path,pitch)
        except Exception as e:
            session['sent'] = False  # エラーが発生した場合に `sent` を False に戻す
            return jsonify({"error": "Wrong wav file", "message": str(e)}), 400

        # AudioSegmentをバイナリデータに変換
        audio_io = io.BytesIO()
        edited_file.export(audio_io, format="wav") 
        audio_io.seek(0)
        session['sent'] = None
        return send_file(audio_io, mimetype='audio/wav', as_attachment=True, download_name='audio.wav')
    else:
        return jsonify({"error": "Wrong wav file"}), 400

   
def change_pitch(scale,sound,gear_value):
    # 音声ファイルを読み込む
    audio = sound
    # ピッチを変更する
    new_pitch = 39 - gear_value
    octaves = (int(scale) - int(new_pitch)) / 24 #24が違和感もっともない
    new_sample_rate = int(audio.frame_rate * (4 ** octaves))
    audio = audio._spawn(audio.raw_data, overrides={
        "frame_rate": new_sample_rate
    }).set_frame_rate(audio.frame_rate)
    
    #ピッチを変更したaudioファイルを返す
    return audio

# 各AudioSegmentの最大音量を取得してソートする関数
def get_max_volume(audio_segment):
    return audio_segment.max_dBFS

def remove_silence_from_start(audio, silence_threshold=-30.0, chunk_size=10):
    # 無音部分を見つける
    trim_ms = 0
    while audio[trim_ms:trim_ms + chunk_size].dBFS < silence_threshold and trim_ms < len(audio):
        trim_ms += chunk_size

    # 無音部分を削除
    trimmed_audio = audio[trim_ms:]
    return trimmed_audio

def EditSoundFile(StartFrame,combined_sound,add_sound):
    start = int(StartFrame)
    combined_sound = combined_sound.overlay(add_sound, position= 1000 * start / 60)
    return combined_sound

def generate_music(file,music_path,gear_value):
    maxcount = SerchMaxCount(music_path)
    
    print("waiting")
    more_than_2_sounds = False

    sounds = EditMusicFile(file)
    if sounds != None:
        sorted_audio_segments = sorted(sounds, key=get_max_volume, reverse=True)
        more_than_2_sounds = True
        for i in range(0,len(sorted_audio_segments)):
            sorted_audio_segments[i] = remove_silence_from_start(sorted_audio_segments[i])
            #sorted_audio_segments[i].export(str(i+1) + ".wav" , format="wav")
    else:
        sounds =AudioSegment.from_wav(file)
        sounds = remove_silence_from_start(sounds)
        #sounds.export("0.wav",format = "wav")
    
    file_name = music_path
    newaudio = None
    combined_sound = AudioSegment.silent(duration=12000)
    old_scale = -1
    count = 0
    base_pitch = int(gear_value)
    

    with open(file_name, 'rt', encoding='utf-8') as f1:
        text1 = f1.readlines()
        for t in text1:
            if count >= maxcount * 5:
                return
            
            if count == 0:
                Duration = int(t.split('_')[1])
                if "MusicSample" in music_path:
                    Duration = 20000
                    combined_sound = AudioSegment.silent(duration=Duration)
                else:
                    combined_sound = AudioSegment.silent(duration=Duration)
                count += 1
                continue
            sentence = t.split(",") 
            frame = sentence[0]
            scale = re.search(r'\d+', sentence[1]).group()
            if int(old_scale) != int(scale):
                if more_than_2_sounds:
                    len_ = len(sorted_audio_segments)
                    index_num =  ((len_ * count )// maxcount)
                    if 'g' in sentence[1]:
                        newaudio = change_pitch(scale,sorted_audio_segments[index_num],base_pitch)
                    else:
                        newaudio = change_pitch(scale,sorted_audio_segments[(index_num + 1)%len_],base_pitch)
                else:
                    newaudio = change_pitch(scale,sounds,base_pitch)
                old_scale = scale

            print(count)
            combined_sound = EditSoundFile(frame,combined_sound,newaudio)
            count += 1
            
    f1.close()
    print("exporting")
    return combined_sound


@app.route('/hello', methods=['POST'])
def hello():
    text = request.form.get('text')  # 'text'というキーでデータを取得

    # ここで任意の処理を行います。例：受け取った文字列をログに出力
    newtext = text + " world"

    # クライアントに返すレスポンス
    return f'Received text: {newtext}'


    

if __name__ == "__main__":
    app.run(debug=True)



