from multi_unet2d import Multi_Unet
from multi_unet2d_attention import Multi_Unet_Attention
from multi_unet2d_r2 import Multi_Unet_r2
from multi_unet2d_r2att import Multi_Unet_r2att
from unet_model import UNet
from utils import *

from torch.utils.data import DataLoader

import torchvision.transforms as transforms
import os
os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'
import torch
import torch.nn as nn
import torch.optim as optim
import tqdm
# Hyper Parameter
batch_size = 8
dataset = 0 #BraTS2020 : 0 
ver = 1
model = 'mmunet' #unet mmunet att r2 r2att
save = 'best' #last best
'''
'''

# Simple Setting
if save == 'best':
    saved_model_path = 'ckpt/ver%d/best_epoch.pth'%ver
elif save == 'final':
    saved_model_path = 'ckpt/ver%d/final_epoch.pth'%ver
cuda_available = torch.cuda.is_available()
device_ids = [0]       # multi-GPU
torch.cuda.set_device(device_ids[0])

result_dir = 'Result/Rver%d'%(ver)
ckpt_dir = 'ckpt/ver%d'%(ver)

if not os.path.exists(ckpt_dir):
    os.mkdir(ckpt_dir)
if not os.path.exists(result_dir):
    os.makedirs(result_dir)

# Build Model
if model == 'mmunet':
    net = Multi_Unet(1,1, 32)  # multi-modal =4, out binary classification one-hot # 5
if model == 'att':
    net = Multi_Unet_Attention(1,1, 32) 
if model == 'r2':
    net = Multi_Unet_r2(1,1, 32)  
if model == 'r2att':
    net = Multi_Unet_r2att(1,1, 32)  
if model == 'unet':
    net = UNet(n_channels=1, n_classes=1, bilinear=True)

if cuda_available:
    net = net.cuda()
    #net = nn.DataParallel(net, device_ids=device_ids)

net.load_state_dict(torch.load(saved_model_path))
    
# Data Preparation
transform = transforms.Compose([transforms.ToTensor()])
if dataset == 0:
    #data_dir = 'Dataset/BraTS2020'
    test_data = MyDataset_load_BraTS('Dataset/BraTS2020/Test',transform=transform)  # 
elif dataset == 1:
    data_dir = 'Dataset/custom'
    test_data = MyDataset_load_custom('%s/Test'%data_dir,transform=transform)  # 
else:
    print('Error : no dataset')
    exit(0)

# Data Loader
test_dataset = DataLoader(dataset=test_data, batch_size=batch_size, shuffle=False)
  

criterion = nn.BCEWithLogitsLoss()

with torch.no_grad():
    net.eval()
    pbar_format_v = "Test Step: |{bar}| {n_fmt}/{total_fmt}[{elapsed}<{remaining},{rate_fmt}]" 
    pbarx = tqdm.tqdm( total=len(test_dataset), bar_format=pbar_format_v, ascii=True, position=0 )
    for step, (label, image, name) in enumerate(test_dataset):
        image = to_var(image)    # 4D tensor   bz * 4(modal) * 240 * 240
        label = to_var(label)    # 3D tensor   bz * 240 * 240 (value 0-4 * 60)
        
        if model == 'unet':    
            predicts = net(image[:,3:4,:,:])    # only use b-mode
        else:
            predicts = net(image)    
        loss_valid = criterion(predicts.float(), label.float())
        predicts[predicts>0] = 1
        predicts[predicts<=0] = 0

        #save_plt_test(result_dir,image.cpu(), label.cpu(), predicts.cpu(),dataset = dataset,name=name[0])

        save_plt(result_dir, image.cpu(), label.cpu(), predicts.cpu(),0,True,dataset = dataset)
        pbarx.update()
    pbarx.close() 

