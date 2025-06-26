# 의료 영상 분할을 위한 UNet

이 저장소는 PyTorch를 사용하여 의료 영상 분할을 위한 UNet 모델의 학습 및 테스트 코드를 포함합니다. 데이터 전처리, 모델 정의, 학습 스크립트 및 모델 저장/로드 유틸리티가 포함되어 있습니다.

## 목차
- [요구 사항](#요구-사항)
- [프로젝트 구조](#프로젝트-구조)
- [사용법](#사용법)
  - [데이터 전처리](#데이터-전처리)
  - [모델 학습](#모델-학습)
  - [모델 테스트](#모델-테스트)
  - [GIF 생성](#gif-생성)
- [모델 아키텍처](#모델-아키텍처)
- [감사의 말](#감사의-말)

## 요구 사항
- Python 3.x
- torch
- numpy
- matplotlib
- Pillow

필요한 패키지 설치:
```sh
pip install -r requirements.txt

프로젝트 구조
.
├── create_gif.py          # TIF 이미지를 GIF로 변환하는 스크립트
├── data_loader.py         # 데이터 로드 및 증강 스크립트
├── data_preprocess.py     # 데이터 전처리 스크립트
├── model.py               # UNet 모델 정의
├── model_vgg_based.py     # VGG 기반 UNet 모델 정의
├── train.py               # 학습 및 테스트 스크립트
├── utils.py               # 모델 저장/로드 유틸리티 함수
└── README.md              # 프로젝트 문서
```

사용법
데이터 전처리
모델 학습 전에 data_preprocess.py를 사용하여 데이터를 전처리합니다. 이 스크립트는 TIF 이미지를 로드하고 프레임을 셔플한 후 numpy 배열로 저장합니다.
```
python data_preprocess.py
```

모델 학습
train.py를 사용하여 UNet 모델을 학습시킵니다. 명령줄 인수를 통해 학습 매개변수를 설정할 수 있습니다.
```
python train.py --mode train --data_dir sample_isbi --ckpt_dir checkpoint --log_dir log --result_dir result --batch_size 4 --num_epoch 10
```

모델 테스트
train.py의 --mode test 인수를 사용하여 학습된 모델을 테스트합니다.
```
python train.py --mode test --data_dir sample_isbi --ckpt_dir checkpoint --result_dir result
```

GIF 생성
create_gif.py를 사용하여 TIF 이미지에서 GIF를 생성합니다. 이 스크립트는 TIF 이미지를 GIF로 변환하고 Matplotlib을 사용하여 표시합니다.
```
python create_gif.py
```

모델 아키텍처
UNet 모델은 model.py에 정의되어 있습니다. 인코더(축소 경로)와 디코더(확장 경로)로 구성되어 있으며, 각 층 사이에 스킵 연결이 있습니다. 이 모델은 단일 채널(그레이스케일)의 2D 의료 영상을 처리하도록 설계되었습니다.
```
class UNet(nn.Module):
    ...
```

자세한 내용은 model.py 파일을 참조하십시오.

감사의 말
이 프로젝트는 의료 영상 분할을 위한 UNet 아키텍처를 사용합니다. 코드는 온라인에서 제공되는 다양한 구현 및 튜토리얼을 참고하여 작성되었습니다.

이 README는 프로젝트에 대한 간략한 개요를 제공하며, 데이터 전처리, 모델 학습, 테스트 및 GIF 생성에 대한 지침과 프로젝트 구조 및 모델 아키텍처에 대한 간략한 설명을 포함합니다.






