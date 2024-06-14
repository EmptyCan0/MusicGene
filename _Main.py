from flask import Flask, request, render_template, redirect, url_for, jsonify, send_from_directory, send_file
from pydub import AudioSegment
import os
import threading

Music_Genre = "東方Project"
Music_Name = "今宵は飄逸なエゴイスト"
Music_Path = ""
Sound_Path =""
NowScale = 1
MaxCount = 1
Count = 0
ProgressNumber = 0
Duration = 120000

combined_sound = AudioSegment.silent(duration=6000)

SoundPitch = 39

add_sound_defo = ""
add_sound = 'uploads//sound.wav'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'

@app.route('/')
def index():
    return render_template('index.html')

UPLOAD_FOLDER = 'uploads'
@app.route('/uploads/<filename>')
def get_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

################JSとのデータやり取り################
@app.route('/submit', methods=['POST'])
def WhenMusicGenreSelected():
    data = request.get_json()
    selected_value = data['selectedValue']
    global Music_Genre 
    Music_Genre = str(selected_value)
    # 選択された値に対してPythonコードを実行
    print(f"選択された値: {selected_value}")
    # ここにPythonで処理を追加
    response = {
        'response': f'受け取った値は: {selected_value}'
    }
    return jsonify(response)

#曲名を選んだあと
@app.route('/submit2', methods=['POST'])
def WhenMusicNameSelected():
    data = request.get_json()
    newpath = data['path']
    response = {
        'response': f'受け取った値は: {newpath}'
    }
    print(newpath)
    filename = str(newpath)
    SerchMaxCount(filename)
    return jsonify(response)

def SerchMaxCount(filename):
    global Music_Path
    Music_Path = filename
    #MaxScaleの計測
    count = 0
    with open(Music_Path, 'rt', encoding="utf-8") as f:
        text1 = f.readlines()
        for t in text1:
            count += 1
    f.close()
    global MaxCount
    MaxCount = count
    print(MaxCount)
    

@app.route('/get_options', methods=['GET'])
def get_options():
    # バックエンドから送信するリストボックスの新しいオプション
    if Music_Genre == "東方Project":
        options = [
            {"value": "ナイトオブナイツ", "text": "ナイトオブナイツ"},
            {"value": "最終鬼畜妹フランドール・S", "text": "最終鬼畜妹フランドール・S"},
            {"value": "亡き王女の為のセプテット", "text": "亡き王女の為のセプテット"},
            {"value": "ネイティブフェイス", "text": "ネイティブフェイス"},
            {"value": "恋色マスタースパーク", "text": "恋色マスタースパーク"},
            {"value": "いざ、倒れ逝くその時まで", "text": "いざ、倒れ逝くその時まで"},
            {"value": "今宵は飄逸なエゴイスト", "text": "今宵は飄逸なエゴイスト"}
        ]
    elif Music_Genre == "FFシリーズ":
        options = [
        {"value": "ビッグブリッジの死闘", "text": "ビッグブリッジの死闘"},
        {"value": "new_option2", "text": "新しいオプション2"},
        {"value": "new_option3", "text": "新しいオプション3"}
    ]
    else:
        
        options = [
            {"value": "new_option1", "text": "新しいオプション1"},
            {"value": "new_option2", "text": "新しいオプション2"},
            {"value": "new_option3", "text": "新しいオプション3"}
        ]
        print(type(options[0]))
    
    return jsonify(options)

#ギアの値（ピッチ)を取得
@app.route('/update_gear', methods=['POST'])
def update_gear():
    gear_value = request.json.get('gearValue')
    # ここでギアの値を使用して必要な処理を行います
    global SoundPitch
    SoundPitch = 39 - gear_value
    #print(SoundPitch)
    return jsonify({"status": "success", "gearValue": gear_value})
SoundPitch = 39
################JSとのデータやり取り################


##################################################
############### 音声の生成系の部分 ################
##################################################
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'audioFile' not in request.files:
        return redirect(request.url)
    file = request.files['audioFile']
    if file.filename == '':
        return redirect(request.url)
    if file:
        filename = file.filename
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        global Sound_Path
        Sound_Path = file_path
        file.save(file_path)
        # 音声ファイルの編集
        edited_file_path = generate_music(file_path)
        return edited_file_path
        return "", 204 

@app.route('/regenerate', methods=['POST'])
def Regenerate():
    global Sound_Path
    edited_file_path = generate_music(Sound_Path)
    return edited_file_path

@app.route('/generate', methods=['POST'])
def Generate():
    global combined_sound
    combined_sound = AudioSegment.silent(duration=12000)
    global Music_Path
    newpath = Music_Path.replace("MusicSample","MusicLarge")
    SerchMaxCount(newpath)
    global Sound_Path
    edited_file_path = generate_music(Sound_Path)
    return edited_file_path

def EditSoundFile(StartFrame,scale):
    global combined_sound
    global NowScale
    global add_sound
    start = int(StartFrame)
    newsoundpath = add_sound
    sound2 = AudioSegment.from_wav(newsoundpath)
    #print(strSoundPath,start)
    combined_sound = combined_sound.overlay(sound2, position= 1000 * start / 60)
   
def change_pitch(scale,sound):
    global add_sound
    # 音声ファイルを読み込む
    audio = AudioSegment.from_file(sound)
    # ピッチを変更する
    global SoundPitch
    octaves = (int(scale) - int(SoundPitch)) / 24 #24が違和感もっともない
    new_sample_rate = int(audio.frame_rate * (4 ** octaves))
    audio = audio._spawn(audio.raw_data, overrides={
        "frame_rate": new_sample_rate
    }).set_frame_rate(audio.frame_rate)

    # 変更後の音声を保存（または再生）
    audio.export(add_sound, format="wav")
    
    # 変更後の音声を再生する場合
    # play(audio)
    

def generate_music(file_path):
    global combined_sound
    global Music_Path
    file_name = Music_Path
    combined_sound = AudioSegment.silent(duration=12000)
    global Count
    Count = 0
    global NowScale
    
    IsSample = False

    with open(file_name, 'rt', encoding="utf-8") as f1:
        text1 = f1.readlines()
        for t in text1:
            if Count == 0:
                Duration = int(t.split('_')[1])
                if "MusicSample" in Music_Path:
                    combined_sound = AudioSegment.silent(duration=12000)
                    IsSample = True
                else:
                    combined_sound = AudioSegment.silent(duration=Duration)
                    IsSample = False
                Count += 1
                continue
            sentence = t.split(",")
            frame = sentence[0]
            scale = sentence[1]
            if int(NowScale) != int(scale):
                change_pitch(scale,file_path)
                NowScale = scale
            EditSoundFile(frame,scale)
            Count += 1
            
            print(Count)
    f1.close()
    global SoundPitch
    if IsSample:
        outputpath = os.path.join(app.config['UPLOAD_FOLDER'], 'edited_' + str(int(SoundPitch) -39) +  '_' + os.path.basename(Music_Path).split(".txt")[0] + '_sample_' +os.path.basename(file_path))
    else:
        outputpath = os.path.join(app.config['UPLOAD_FOLDER'], 'edited_' + str(int(SoundPitch) -39) + '_' + os.path.basename(Music_Path).split(".txt")[0] + '_' +os.path.basename(file_path))
    combined_sound.export(outputpath, format="wav")
    return outputpath
    
@app.route('/get_ProgressNumber', methods=['GET'])
def GiveProgressNumber():
    global NowScale
    global MaxCount
    global ProgressNumber
    global Count
    ProgressNumber = int(int(Count)/int(MaxCount) * 100)
    return jsonify({"ProgressNumber": ProgressNumber})
##################################################
############### 音声の生成系の部分 ################
##################################################

def run_flask():
    app.run(debug=True, use_reloader=False)

if __name__ == "__main__":
    threading.Thread(target=run_flask).start()

    # Streamlit app code here
    import streamlit as st
    st.title("Streamlit with Flask")
    st.write("This is a Streamlit app with Flask running in the background.")
