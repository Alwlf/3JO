from keras.models import load_model
import numpy as np
from PIL import Image
import os

<<<<<<< HEAD
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
    
=======
"cpu"
os.environ["CUDA_VISIBLE_DEVICES"]="-1"

pibu_cat_model=load_model("projectapp/dc_model/pibu_dog.h5")
pibu_dog_model=load_model("projectapp/dc_model/pibu_dog.h5")
eye_cat_model=load_model("projectapp/dc_model/eye_cat.h5")
eye_dog_model=load_model("projectapp/dc_model/eye_dog.h5")



pibu_dog_classes=["구진 플라크","비듬 각질 상피성잔고리","태선화 과다색소침착","농포 여드름","미란 궤양","결절종괴"]
pibu_cat_classes=["구진 플라크","비듬 각질 상피성잔고리","태선화 과다색소침착","농포 여드름","미란 궤양","결절종괴"]
eye_dog_classes=['결막염','궤양성각막질환','무증상','백내장','비궤양성각막질환','색소침착성각막염','안검내반증','안검염','안검종양','유루증','핵경화']
eye_cat_classes=['각막궤양', '각막부골편', '결막염', '무증상', '비궤양성각막염', '안검염']

    
models={("pibu","dog"):pibu_dog_model,
        ("pibu","cat"):pibu_cat_model,
        ("eye","dog"):eye_dog_model,
        ("eye","cat"):eye_cat_model,}

lists={("pibu","dog"):pibu_dog_classes,
        ("pibu","cat"):pibu_cat_classes,
        ("eye","dog"):eye_dog_classes,
        ("eye","cat"):eye_cat_classes,}

sizes={("pibu","dog"):(224,224),
        ("pibu","cat"):(224,224),
        ("eye","dog"):(224,224),
        ("eye","cat"):(224,224),}

# 모델 
def bot_model(dc,bot,img):
    
    # 모델 
    model=models[(bot,dc)]

    # 예측 클래스
    classes=lists[(bot,dc)]

    # input_shape
    size=sizes[(bot,dc)]

    # 이미지 전처리 
    img=np.array(img.resize(size))
    img=img.reshape((1,)+size+(3,))/img.max()

    # 예측
    pred=model.predict(img)

    # 확률과 병명
    
    idx=pred.argmax()
    p=np.round(pred[0][idx],2)
    b=classes[idx]
    return p,b
>>>>>>> 94e56aa79e9d3809588a7fe2c2e107b3942ceba7
