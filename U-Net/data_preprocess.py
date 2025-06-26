import os
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

## Data load
dir_data = 'sample_isbi/'

name_label = 'train-labels.tif'
name_input = 'train-volume.tif'

img_label = Image.open(os.path.join(dir_data, name_label))
img_input = Image.open(os.path.join(dir_data, name_input))

ny, nx = img_label.size
nframe = img_label.n_frames

## training, validation, test 이미지 개수 정의
nframe_train = 24
nframe_val = 3
nframe_test = 3

dir_save_train_input = os.path.join(dir_data, 'train_npy/input')
dir_save_train_label = os.path.join(dir_data, 'train_npy/label')

dir_save_val_input = os.path.join(dir_data, 'val_npy/input')
dir_save_val_label = os.path.join(dir_data, 'val_npy/label')

dir_save_test_input = os.path.join(dir_data, 'test_npy/input')
dir_save_test_label = os.path.join(dir_data, 'test_npy/label')


dir_save_train_images_input = os.path.join(dir_data, 'train_images/input')
dir_save_train_images_label = os.path.join(dir_data, 'train_images/label')

dir_save_val_images_input = os.path.join(dir_data, 'val_images/input')
dir_save_val_images_label = os.path.join(dir_data, 'val_images/label')

dir_save_test_images_input = os.path.join(dir_data, 'test_images/input')
dir_save_test_images_label = os.path.join(dir_data, 'test_images/label')

## frame shuffle
id_frame = np.arange(nframe)
print(id_frame)

np.random.shuffle(id_frame)
print(id_frame)

## training data 분리
offset_nframe = 0

for i in range(nframe_train):
    img_input.seek(id_frame[i + offset_nframe])
    img_label.seek(id_frame[i + offset_nframe])
    
    img_input.save(os.path.join(dir_save_train_images_input, 'input_%03d.tif'%i))
    img_label.save(os.path.join(dir_save_train_images_label, 'label_%03d.tif'%i))

    input_ = np.asarray(img_input)
    label_ = np.asarray(img_label)

    np.save(os.path.join(dir_save_train_input, 'input_%03d.npy' % i), input_)
    np.save(os.path.join(dir_save_train_label, 'label_%03d.npy' % i), label_)

## 이미지 시각화
plt.subplot(122)
plt.imshow(label_, cmap='gray')
plt.title('label')

plt.subplot(121)
plt.imshow(input_, cmap='gray')
plt.title('input')
plt.show()

## validatation data 분리
offset_nframe = nframe_train
for i in range(nframe_val):
    img_input.seek(id_frame[i + offset_nframe])
    img_label.seek(id_frame[i + offset_nframe])
    
    ##img_input.save(os.path.join(dir_val_train, 'input_%03d.tif' %i))
    ##img_label.save(os.path.join(dir_val_train, 'label_%03d.tif' %i))

    input_ = np.asarray(img_input)
    label_ = np.asarray(img_label)

    np.save(os.path.join(dir_save_val_input, 'input_%03d.npy' % i), input_)
    np.save(os.path.join(dir_save_val_label, 'label_%03d.npy' % i), label_)

## test data 분리
offset_nframe = nframe_train + nframe_val
for i in range(nframe_test):
    img_input.seek(id_frame[i + offset_nframe])
    img_label.seek(id_frame[i + offset_nframe])
    
    ##img_input.save(os.path.join(dir_save_test, 'input_%03d.tif' %i)
    ##img_label.save(os.path.join(dir_save_test, 'label_%03d.tif' %i)

    input_ = np.asarray(img_input)
    label_ = np.asarray(img_label)

    np.save(os.path.join(dir_save_test_input, 'input_%03d.npy' % i), input_)
    np.save(os.path.join(dir_save_test_label, 'label_%03d.npy' % i), label_)





 

