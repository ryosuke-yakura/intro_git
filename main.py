import streamlit as st
from PIL import Image
import requests
from PIL import ImageDraw
import io

st.title("顔認識アプリ")

subscription_key = "88d42c9d086b4813b65d9682a4ed371e"
assert subscription_key

face_api_url = "https://20210605yakura.cognitiveservices.azure.com/face/v1.0/detect"


uploaded_file = st.file_uploader("Choose an image...",type="jpg")
if uploaded_file is not None:
  img = Image.open(uploaded_file)

  with io.BytesIO() as output:
      img.save(output,format="JPEG")
      binary_img = output.getvalue() #バイナリ取得
  headers = {
      'Content-Type':'application/octet-stream',
      'Ocp-Apim-Subscription-Key': subscription_key
  }
  params = {
      'returnFaceId': 'true',
      'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure,noise'
  }
  res = requests.post(face_api_url, params=params, headers=headers, data=binary_img)
  results = res.json()
  for result in results:
      rect= result["faceRectangle"]
      draw = ImageDraw.Draw(img)

      draw.rectangle([(rect["left"],rect["top"]),(rect["left"]+rect["width"],rect["top"]+rect["height"])],fill=None,outline="green",width=5)
  st.image(img,caption="Uploded Image.",use_column_width=True)
