readfile = "static//MusicLarge//東方Project//MusicalScaleList2.txt"
writefile = "new.txt"
f0 = open(writefile, 'w', encoding="utf-8")
f0.close()

with open(readfile, 'rt', encoding="utf-8") as f:
    text = f.readlines()
    MinFrame = 999999999999
    for t in text:
        sentence = t.split(",")
        frame = sentence[0]
        scale = sentence[1]
        if int(frame) < int(MinFrame):
            MinFrame = frame
    for t in text:
        sentence = t.split(",")
        frame = sentence[0]
        scale = sentence[1]
        newframe = max(0, int(frame) - int(MinFrame))
        f0 = open(writefile, 'a', encoding="utf-8")
        f0.write(str(newframe) + "," + str(scale))
        f0.close()
        