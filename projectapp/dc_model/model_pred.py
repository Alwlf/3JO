from keras.models import load_model
import numpy as np
from PIL import Image
import os

os.environ["CUDA_VISIBLE_DEVICES"]="-1"
model_456=load_model("projectapp/dc_model/best_model_InceptionResNetV2_456.h5")
model_136=load_model("projectapp/dc_model/best_model_InceptionResNetV2_136.h5")

model_456.predict(np.arange(224*224*3).reshape(1,224,224,3))
model_136.predict(np.arange(224*224*3).reshape(1,224,224,3))

def pibu(img):
    # 모델 클래스 
    pibu_list_136=["구진 플라크","태선화 과다색소침착","결절종괴"]
    pibu_list_456=["농포 여드름","미란 궤양","결절 종괴"]

    pibu_list=["구진 플라크","","태선화 과다색소침착","농포 여드름","미란 궤양","결절종괴"]
    # 이미지 전처리 
    img=np.array(img.resize((224,224)))
    img=img.reshape(1,224,224,3)/img.max()

    # 예측
    pred_136=model_136.predict(img)
    pred_456=model_456.predict(img)
    #print(pred_136,pred_456)
    
    # 2개 모델 결과 합치기
    t=[0,0,0,0,0,0]
    pred=np.hstack([pred_136[0],pred_456[0]])
    for i,j in zip([0,2,5,3,4,5],pred):
        print(i,j)
        t[i]=j if t[i]<j else t[i]

    # 확률과 병명
    print(t)
    idx=np.array(t).argmax()
    p=np.round(t[idx],2)
    b=pibu_list[idx]
    return p,b
    
