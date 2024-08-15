MAX_FILE_SIZE = 1 * 1024 * 1024; // 5MB
//アップロードボタンが押されたとき
document.addEventListener('DOMContentLoaded', function() {
    const uploadForm = document.getElementById('uploadForm');
    const fileInput = document.getElementById('audioFile');
    var sent  = false;

    uploadForm.addEventListener('submit', function(event) {
        if (sent){
            return;
        }
        event.preventDefault();
        const file = fileInput.files[0];
        if (file) {
            if (!file.name.includes('.wav')) {
                alert('.wavファイルのみアップロード可能です。');
                return;
            }

            if (file.size > MAX_FILE_SIZE) {
                alert('ファイルサイズが大きすぎます。1MB未満のファイルを選択してください。');
                return;
            }
            sent = true;
            const formData = new FormData();
            formData.append('file', file);
            const path = MusicPath();
            formData.append('path',path)
            const pitch = get_gearvalue();
            formData.append('pitch',pitch)

            fetch('/upload', {
                method: 'POST',
                body: formData
            })
            .then(response => response.blob())
            .then(blob => {
                const url = URL.createObjectURL(blob);
                const audioPlayer = document.getElementById('sample-music');
                audioPlayer.src = url;
                sent = false;

                var modal = document.getElementById('Modal_wait');
                setTimeout(function(){
                    modal.style.display = "none";
                    After_SampleMusicCreated();
                }, 1000);
            })
            .catch(error => {
                console.error('Error:', error);
                sent = false;
                FileUploadError();
            });
        }
    });
});


document.addEventListener('DOMContentLoaded', function() {
//再度音声を生成
    var sent = false;
    document.getElementById('regene').onclick =  async function() {
        if (sent){
            return;
        }

        ApploadButtonPushed();

        const fileInput = document.getElementById('audioFile');
        const file = fileInput.files[0];
        if (file) {
            const formData = new FormData();

            sent = true;
            formData.append('file', file);
            const path = MusicPath();
            formData.append('path',path)
            const pitch = get_gearvalue();
            formData.append('pitch',pitch)

            fetch('/upload', {
                method: 'POST',
                body: formData
            })
            .then(response => response.blob())
            .then(blob => {
                const url = URL.createObjectURL(blob);
                const audioPlayer = document.getElementById('sample-music');
                audioPlayer.src = url;
                sent = false;

                var modal = document.getElementById('Modal_wait');
                setTimeout(function(){
                    modal.style.display = "none";
                    After_SampleMusicCreated();
                }, 1000);
            })
            .catch(error => {
                console.error('Error:', error);
                sent = false;
                FileUploadError();
            });
        }
    }
});

document.addEventListener('DOMContentLoaded', function() {
    var sent = false;
//本番の音声を生成
    document.getElementById('gene').onclick =  async function() {
        GenerateButtonPushed();
        const fileInput = document.getElementById('audioFile');
        const file = fileInput.files[0];
        if (file) {
            const formData = new FormData();

            sent = true;
            formData.append('file', file);
            let path = MusicPath();
            path = path.replace("MusicSample","MusicLarge")
            formData.append('path',path)
            const pitch = get_gearvalue();
            formData.append('pitch',pitch)

            fetch('/upload', {
                method: 'POST',
                body: formData
            })
            .then(response => response.blob())
            .then(blob => {
                const url = URL.createObjectURL(blob);
                const audioPlayer = document.getElementById('all-music');
                audioPlayer.src = url;
                sent = false;

                var modal = document.getElementById('Modal_wait');
                setTimeout(function(){
                    modal.style.display = "none";
                    After_AllMusicCreated();
                }, 1000);
            })
        }
    }
});

//fetchに失敗したとき
var StopGet = false;
function FileUploadError(){
    StopGet = true;
    CloseModal('All');
    OpenModal('Modal_crush')
}

function MusicPath(){
    var selectBox1 = document.getElementById("Music_name");
    console.log(selectBox1.selectedIndex)
    var MusicName = selectBox1.options[selectBox1.selectedIndex].value;
    var selectBox2 = document.getElementById("Music_genre");
    var MusicGenre = selectBox2.options[selectBox2.selectedIndex].value;

    path =  filename = "static//MusicSample//" + String(MusicGenre) + "//" + String(MusicName) + ".txt"
    return path;
}


//リストボックスの中身を変更(初期)
document.addEventListener('DOMContentLoaded', function() {
    const listbox_music_genre = document.getElementById('Music_genre');

    // 既存のオプションをクリア
    listbox_music_genre.innerHTML = '';

    // 新しいオプションを追加
    const genre_options = [
        { value: '東方Project', text: '東方Project' },
        { value: 'FFシリーズ', text: 'FFシリーズ' },
        { value: '3', text: 'Option 3' }
    ];

    genre_options.forEach(option => {
        const new_option = document.createElement('option');
        new_option.value = option.value;
        new_option.textContent = option.text;
        listbox_music_genre.appendChild(new_option);
    });

    update_musicname();
    
});

function update_musicname(){
    const listbox_music_genre = document.getElementById('Music_genre');
    const listbox_music_name = document.getElementById('Music_name');
    const select_genre = listbox_music_genre.value;
    let music_name_option = [];
    if (select_genre == '東方Project'){
        music_name_option = [
            { value: "ナイトオブナイツ", text: "ナイトオブナイツ"},
            { value: "最終鬼畜妹フランドール・S", text: "最終鬼畜妹フランドール・S"},
            { value: "亡き王女の為のセプテット", text: "亡き王女の為のセプテット"},
            { value: "ネイティブフェイス", text: "ネイティブフェイス"},
            { value: "恋色マスタースパーク", text: "恋色マスタースパーク"},
            { value: "いざ、倒れ逝くその時まで", text: "いざ、倒れ逝くその時まで"},
            { value: "今宵は飄逸なエゴイスト", text: "今宵は飄逸なエゴイスト"}
        ];
    }
    else if (select_genre == 'FFシリーズ'){
        music_name_option = [
            { value: "ビッグブリッジの死闘", text: "ビッグブリッジの死闘"},
        ];
    }
    //リストボックスの更新
    listbox_music_name.innerHTML = '';
    music_name_option.forEach(option => {
        const new_option = document.createElement('option');
        new_option.value = option.value;
        new_option.textContent = option.text;
        listbox_music_name.appendChild(new_option);
    });
}

document.addEventListener('DOMContentLoaded', function() {
    const listbox_music_genre = document.getElementById('Music_genre');
    const listbox_music_name = document.getElementById('Music_name');

    listbox_music_genre.addEventListener('change', function(){
        update_musicname();
    });
});

//-----------------------------------------------------------//
//------------モーデルの操作----------------------------------//
//-----------------------------------------------------------//
//閉じるボタン
function CloseModal(modalID){
    if (modalID == 'All'){
        var modals = document.getElementsByClassName('modal');
        for (var i = 0; i < modals.length; i++) {
            modals[i].style.display = "none";
        }
        return;
    }
    var modal = document.getElementById(modalID);
    modal.style.display = "none";
}
//モーダルを開くボタン
function OpenModal(modalID){
    var modal = document.getElementById(modalID);
    modal.style.display = "block";
}

//プログレスバーの実装

function ApploadButtonPushed(){
    const fileInput = document.getElementById('audioFile');
    const file = fileInput.files[0];
    if (!file || !file.name.includes('.wav')) { return; }

    if (file.size > MAX_FILE_SIZE) {return;}

    var Loading_var = document.querySelector(".loading_progress");
    var modal = document.getElementById('Modal_wait');
    modal.style.display = "block";
    CloseModal('SampleCheck')
    
}


function GenerateButtonPushed(){
    var Loading_var = document.querySelector(".loading_progress");
    var modal = document.getElementById('Modal_wait');
    modal.style.display = "block";
    CloseModal('SampleCheck')
}

//サンプルが生成し終わった後
function After_SampleMusicCreated(){
    const audioPlayer = document.getElementById('sample-music');
    if (audioPlayer.readyState < 3) 
    {
        FileUploadError();
        return;
    }
    console.log(audioPlayer.src)
    var checkmodal = document.getElementById("SampleCheck");
    checkmodal.style.display = "block";
}

//本番局が生成し終わった後
function After_AllMusicCreated(){
    var checkmodal = document.getElementById("MusicCheck");
    checkmodal.style.display = "block";
}


function get_gearvalue(){
    const value = document.getElementById('gearSlider').value;
    return value;
}


//スライダーの実装
function updateGear(value) {
    document.getElementById('gearValue').textContent = value;
    // ここでギアの値を使って変数を調整します
    var gearValue = parseInt(value, 10);
    // ギアの値を送信
}


//-----------------------------------------------------------//
//------------モーダルの操作----------------------------------//
//-----------------------------------------------------------//