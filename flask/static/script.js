document.getElementById('uploadForm').onsubmit = async function(event) {
    event.preventDefault();
    const formData = new FormData(this);
    const response = await fetch('/upload', {
      method: 'POST',
      body: formData
    });
    const filename = await response.text();
    console.log(filename)
    if (filename) {
      document.getElementById("sample-music").src = `${filename}`;
    }
}

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

function WhenMusicGenreSelected() {
    var selectBox = document.getElementById("Music_genre");
    var selectedValue = selectBox.options[selectBox.selectedIndex].value;

    fetch('/submit', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ selectedValue: selectedValue })
    })
    .then(response => response.json())
    .then(data => {
        updateSelectBox();
    });
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

//リストボックスの中身を変更
function updateSelectBox() {
    fetch('/get_options')
        .then(response => response.json())
        .then(options => {
            var selectBox = document.getElementById("Music_name");
            selectBox.innerHTML = ''; // 現在のオプションをクリア
            options.forEach(option => {
                var newOption = document.createElement("option");
                newOption.value = option.value;
                newOption.text = option.text;
                selectBox.add(newOption);
                WhenMusicNameSelected();
            });
        });
}


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