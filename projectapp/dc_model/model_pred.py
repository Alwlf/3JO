from keras.models import load_model
import numpy as np
from PIL import Image
import os

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
