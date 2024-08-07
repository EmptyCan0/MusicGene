class Config:
    def __init__(self):
        self.Music_Path = "hogee"
        self.Sound_Path = ""
        self.NowScale = 1
        self.MaxCount = 1
        self.Count = 0
        self.ProgressNumber = 0
        self.Duration = 120000

config = Config()

def some_function(config):
    # configオブジェクトを使用して設定や状態にアクセス
    print(config.Music_Path)
    # 必要に応じて設定を更新
    config.Count += 1

# メインプログラム
if __name__ == "__main__":
    some_function(config)
    print(f"Count after function call: {config.Count}")
