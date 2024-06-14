from pydub import AudioSegment

# オーディオファイルの読み込み
sound1 = AudioSegment.from_wav("silent.wav")
sound2 = AudioSegment.from_wav("sample4.wav")


frame = 44100
# 音声を指定したフレームに配置する
start_frame_sound1 = 0  # sound1の配置開始フレーム
#start_frame_sound2 = 1000 * frame / rate # sound2の配置開始フレーム（例）

combined_sound = AudioSegment.silent(duration=180000)
rate = combined_sound.frame_rate
#1:60=x:rate x = rate/60
# 

# sound1の配置
#combined_sound = combined_sound.overlay(sound1, position=start_frame_sound1)


def EditSoundFile(FrameList,ScaleName):
    print(FrameList)
    for list in FrameList:
        if list[2] == "ababa":
            continue
        global combined_sound
        start = int(list[0])
        strSoundPath = "scale//" + str(ScaleName + 1) + str(list[2]) + ".wav"
        sound2 = AudioSegment.from_wav(strSoundPath)
        rate = combined_sound.frame_rate
        #print(strSoundPath,start)
        combined_sound = combined_sound.overlay(sound2, position= 1000 * start / 65)
        

file_name = "MusicalScaleList.txt"
for  scale in range(0,88):
    FrameList = []
    newFrame = [0,0,"ababa"]
    wavname = "borabora"
    with open(file_name, 'rt', encoding="utf-8") as f1:
        text1 = f1.readlines()
        Switch = False
        for t in text1:
            array = t.split("\n")
            array = t.split(" ")
            frame = array[0]
            
            IsFound = False
            count = 0
            wavname = "borabora"
            for index in array:          
                if count == 0:
                    count += 1
                    continue
                if str(scale + 1) == str(index.split("+")[0]):
                    IsFound = True
                    if wavname != index: 
                        wavname = index
                    else:
                        break
            
            if IsFound == True:
                if Switch == False:
                    Switch = True
                    newFrame[0] = frame
                else:
                    newFrame[1] = frame
                    if int(newFrame[1]) - int(newFrame[0]) < 170:
                        newFrame[1] = str(int(newFrame[0]) + 170)
                    newFrame[2] = wavname.split("+")[1]
            else:
                if Switch == True:
                    Switch = False
                    FrameList.append(newFrame)
                    newFrame = [0,0,"ababa"]
    f1.close()
    #print(scale)      
    EditSoundFile(FrameList,scale)     


# 新しいWAVファイルとして保存
combined_sound.export("combined_sound.wav", format="wav")
