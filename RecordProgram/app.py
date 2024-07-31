#一行ずつ読み込むのに成功した奴

from flask import Flask, request, redirect, url_for
import boto3
import os
import logging
import io


app = Flask(__name__)

string = ""

# AWS設定
logging.basicConfig(
    level=logging.DEBUG,  # 全てのレベルのログを記録
    format='%(asctime)s %(levelname)s %(message)s',
    handlers=[
        logging.FileHandler("logs/app.log"),
        logging.StreamHandler()
    ]
)
S3_BUCKET = 'testserverbuckettesting'
S3_REGION = 'ap-northeast-1'

s3_client = boto3.client('s3', region_name=S3_REGION)



@app.route('/')
def index():
    return '''
    <form method="post" action="/upload" enctype="multipart/form-data">
        <input type="file" name="file">
        <input type="submit" value="Upload">
    </form>
    '''


@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return "No file part"
    file = request.files['file']
    if file.filename == '':
        return "No selected file"
    if file:
        s3_client.upload_fileobj(file, S3_BUCKET, file.filename)
        hogehoge = read_s3_file_line_by_line(S3_BUCKET, 'text/ビッグブリッジの死闘.txt')
        return hogehoge

def read_s3_file_line_by_line(bucket_name, key):
    # S3からオブジェクトを取得
    logging.info("関数を読み出した")
    response = s3_client.get_object(Bucket=bucket_name, Key=key)
    # オブジェクトの内容を読み込み
    body = response['Body'].read().decode('utf-8')
    
    global string
    logging.info("読み込みに成功した")
    # StringIOオブジェクトを使用して行ごとに読み込む
    with io.StringIO(body) as f:
        for line in f:
            string = string + str(line.strip())
    logging.info("return した")
    return string
            

if __name__ == "__main__":
    app.run(debug=True)

