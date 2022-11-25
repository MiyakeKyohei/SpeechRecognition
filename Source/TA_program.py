import requests

# キーとエンドポイントを設定する
KEY = "43339af7313b481db1b97970b9599809"
ENDPOINT = "https://kmiyake-test.cognitiveservices.azure.com/"

# 画像を分析する
filepath = ".\\temp\\number0.jpg" # 画像のパス(実行前に画像があるか確認して)

img = open(filepath, "rb")
# ------------------------------------------------------------------↓パラメータ

r = requests.post(ENDPOINT + "face/v1.0/detect?returnFaceAttributes=headPose", data=img, headers={"Ocp-Apim-Subscription-Key": KEY, "Content-Type": "application/octet-stream"})
# 結果を表示する
print(r.json())