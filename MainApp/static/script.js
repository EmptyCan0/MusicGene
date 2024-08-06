//アップロードボタンが押されたとき
document.addEventListener('DOMContentLoaded', function() {
    const uploadForm = document.getElementById('uploadForm');
    const fileInput = document.getElementById('audioFile');

    uploadForm.addEventListener('submit', function(event) {
        event.preventDefault();
        const file = fileInput.files[0];
        if (file) {
            const formData = new FormData();
            formData.append('file', file);

            fetch('/upload', {
                method: 'POST',
                body: formData
            })
            .then(response => response.blob())
            .then(blob => {
                const url = URL.createObjectURL(blob);
                const audioPlayer = document.getElementById('sample-music');
                audioPlayer.src = url;
                //audioPlayer.play();
            })
            .catch(error => {
                console.error('Error:', error);
            });
        } else {
            console.error('No file selected');
        }
    });
});

//再度音声を生成
document.getElementById('regene').onclick =  async function() {
    ApploadButtonPushed();
    const response = await fetch('/regenerate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({}) // 空のオブジェクトを送信
    });
    const filename = await response.text();
    console.log(filename)
    if (filename) {
        document.getElementById("sample-music").src = `${filename}`; 
    }
}

//本番の音声を生成
document.getElementById('gene').onclick =  async function() {
    GenerateButtonPushed();
    const response = await fetch('/generate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({}) // 空のオブジェクトを送信
    });
    const filename = await response.text();
    console.log(filename)
    if (filename) {
        document.getElementById("all-music").src = `${filename}`; 
    }
}

function WhenMusicNameSelected() {
    var selectBox1 = document.getElementById("Music_name");
    console.log(selectBox1.selectedIndex)
    var MusicName = selectBox1.options[selectBox1.selectedIndex].value;
    var selectBox2 = document.getElementById("Music_genre");
    var MusicGenre = selectBox2.options[selectBox2.selectedIndex].value;

    path =  filename = "static//MusicSample//" + String(MusicGenre) + "//" + String(MusicName) + ".txt"

    fetch('/submit2', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ path: path })
    })
    .then(response => response.json())
    .then(data => {
    });
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
});

document.addEventListener('DOMContentLoaded', function() {
    const listbox_music_genre = document.getElementById('Music_genre');
    const listbox_music_name = document.getElementById('Music_name');

    listbox_music_genre.addEventListener('change', function(){
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
    });
});

//-----------------------------------------------------------//
//------------モーデルの操作----------------------------------//
//-----------------------------------------------------------//
//閉じるボタン
function CloseModal(modalID){
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
    var Loading_var = document.querySelector(".loading_progress");
    var modal = document.getElementById('Modal_wait');
    modal.style.display = "block";
    CloseModal('SampleCheck')
    var width = 0;
    var interval = setInterval(function(){
        if (width >= 100){
            clearInterval(interval);
            modal.style.display = "none"
        }else{
            $.ajax({
                url: '/get_ProgressNumber',
                type: 'GET',
                success: function(response) {
                    // サーバーからのレスポンスを処理
                    width = response.ProgressNumber;
                    Loading_var.style.width = width + '%';
                    Loading_var.innerHTML = width + '%';

                    // 完了時にモーダルを閉じる
                    if (width >= 100) {
                        clearInterval(interval);
                        modal.style.display = "none";
                        After_SampleMusicCreated();
                    }
                },
                error: function(error) {
                    console.log('エラー: ', error);
                }
            });
        }
    },500); 
}


function GenerateButtonPushed(){
    var Loading_var = document.querySelector(".loading_progress");
    var modal = document.getElementById('Modal_wait');
    modal.style.display = "block";
    CloseModal('SampleCheck')
    var width = 0;
    var interval = setInterval(function(){
        if (width >= 100){
            clearInterval(interval);
            modal.style.display = "none"
        }else{
            $.ajax({
                url: '/get_ProgressNumber',
                type: 'GET',
                success: function(response) {
                    // サーバーからのレスポンスを処理
                    width = response.ProgressNumber;
                    Loading_var.style.width = width + '%';
                    Loading_var.innerHTML = width + '%';

                    // 完了時にモーダルを閉じる
                    if (width >= 100) {
                        clearInterval(interval);
                        modal.style.display = "none";
                        After_AllMusicCreated();
                    }
                },
                error: function(error) {
                    console.log('エラー: ', error);
                }
            });
        }
    },500); 
}

//サンプルが生成し終わった後
function After_SampleMusicCreated(){
    var checkmodal = document.getElementById("SampleCheck");
    checkmodal.style.display = "block";
}

//本番局が生成し終わった後
function After_AllMusicCreated(){
    var checkmodal = document.getElementById("MusicCheck");
    checkmodal.style.display = "block";
}

//スライダーの実装
function updateGear(value) {
    document.getElementById('gearValue').textContent = value;
    // ここでギアの値を使って変数を調整します
    var gearValue = parseInt(value, 10);
    // ギアの値を送信
    $.ajax({
        url: '/update_gear',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({ gearValue: gearValue }),
        success: function(response) {
            console.log("Server response:", response);
        },
        error: function(error) {
            console.error("Error:", error);
        }
    });
}


//-----------------------------------------------------------//
//------------モールドの操作----------------------------------//
//-----------------------------------------------------------//