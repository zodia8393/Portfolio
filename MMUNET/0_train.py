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
import sys
import torch
import torch.nn as nn
import torch.optim as optim
import tqdm
from torchsummary import summary as summary_
# Hyper Parameter
learning_rate = 0.001
batch_size = 8
epochs = 100
dataset = 0 #BraTS2020 : 0
ver = 2
model = 'att' #unet, mmunet att r2 r2att
scheduler_lim = 20
'''
ver1 : mmunet
ver2 : attention
ver3 : r2
ver4 : r2att
ver5 : unet

'''

# Simple Setting
saved_model_path = 'ckpt/ver%d/best_epoch.pth'
cuda_available = torch.cuda.is_available()
device_ids = [0]       # multi-GPU
torch.cuda.set_device(device_ids[0])

result_dir = 'Result/ver%d'%(ver)
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

#summary_(net,(4,224,224),batch_size=32)
# Data Preparation
transform = transforms.Compose([transforms.ToTensor()])
if dataset == 0:
    # data_dir = 'Dataset/BraTS2020'
    train_data = MyDataset_load_BraTS('Dataset/BraTS2020/Training',transform=transform)  # 
    valid_data = MyDataset_load_BraTS('Dataset/BraTS2020/Validation',transform=transform)  # 
elif dataset == 1:
    data_dir = 'Dataset/custom'
    train_data = MyDataset_load_custom('%s/Training'%data_dir,transform=transform)  # 
    valid_data = MyDataset_load_custom('%s/Validation'%data_dir,transform=transform)  # 
else:
    print('Error : no dataset')
    exit(0)
# Data Loader
train_dataset = DataLoader(dataset=train_data, batch_size=batch_size, shuffle=True)
valid_dataset = DataLoader(dataset=valid_data, batch_size=batch_size, shuffle=True)
  

def evaluation(net, test_dataset, criterion, epoch):
    test_loss = []
    precision_whole = []
    recall_whole = []
    iou_whole = []
    dice_whole = []
    IOU = list()

    with torch.no_grad():
        net.eval()
        pbar_format_v = "Validation Epoch %d: |{bar}| {n_fmt}/{total_fmt}[{elapsed}<{remaining},{rate_fmt}]"%epoch  
        pbarx = tqdm.tqdm( total=len(test_dataset), bar_format=pbar_format_v, ascii=True, position=0 )
        for step, (label, image, name) in enumerate(test_dataset):
            image = to_var(image)    # 4D tensor   bz * 4(modal) * 240 * 240
            label = to_var(label)    # 3D tensor   bz * 240 * 240 (value 0-4 * 60)
            
            if model == 'unet':    
                predicts = net(image[:,3:4,:,:])    # only use b-mode
            else:
                predicts = net(image)    
            loss_valid = criterion(predicts.float(), label.float())
            test_loss.append(float(loss_valid))

            predicts[predicts>0] = 1
            predicts[predicts<=0] = 0
            precision = eval_precision_ave(label.cpu().float(), predicts.cpu().float())
            recall = eval_recall_ave(label.cpu().float(), predicts.cpu().float())
            iou = eval_iou_ave(label.cpu().float(), predicts.cpu().float())
            dice_sco = eval_dice_ave(label.cpu().float(), predicts.cpu().float())
            precision_whole.append(precision)
            recall_whole.append(recall)
            iou_whole.append(iou)
            dice_whole.append(dice_sco)

            if step == 0:
                if epoch % 5 == 1:
                    save_plt(result_dir,image.cpu(), label.cpu(), predicts.cpu(),epoch,isTrain = False,dataset = dataset)

            pbarx.update()
        pbarx.close() 
        precision_out = sum(precision_whole) / (len(precision_whole) * 1.0)
        recall_out = sum(recall_whole) / (len(recall_whole) * 1.0)
        iou_out = sum(iou_whole) / (len(iou_whole) * 1.0)
        dice_out = sum(dice_whole) / (len(dice_whole) * 1.0)
        out = precision_out, recall_out, iou_out, dice_out

    return out, test_loss

if __name__ == "__main__":
    best_epoch = 0
    score_max = [-1.0,-1.0,-1.0,-1.0]
    train_history = []
    valid_history = []
    optimizer = optim.Adam(params=net.parameters(), lr=learning_rate, betas=(0.9, 0.999))
    criterion = nn.BCEWithLogitsLoss()
    for epoch in range(1, epochs + 1):
        train_loss = []
        # Train
        net.train()
        pbar_format_t = "Training Epoch %d: |{bar}| {n_fmt}/{total_fmt}[{elapsed}<{remaining},{rate_fmt}]"%epoch  
        pbarx = tqdm.tqdm( total=len(train_dataset), bar_format=pbar_format_t, ascii=True, position=0 )
        for step, (label, image, name) in enumerate(train_dataset):
            image = to_var(image)   
            label = to_var(label)    

            optimizer.zero_grad()
            if model == 'unet':    
                predicts = net(image[:,3:4,:,:])    # only use b-mode
            else:
                predicts = net(image)    
            
            loss_train = criterion(predicts.float(), label.float())
            train_loss.append(float(loss_train))
            loss_train.backward()
            optimizer.step()

            predicts[predicts>0] = 1
            predicts[predicts<=0] = 0
            dice = eval_dice_ave(label.cpu().float(), predicts.cpu().float())  
            if step == 0:
                predicts[predicts>0] = 1
                if epoch % 5 == 1:
                    save_plt(result_dir,image.cpu(), label.cpu(), predicts.cpu(),epoch,isTrain = True, dataset = dataset)
            pbarx.update()
        pbarx.close() 

        # Evaluation
        current_score, valid_loss = evaluation(net, valid_dataset, criterion, epoch=epoch)


        # Save Model
        if current_score[3] > score_max[3]:
            best_epoch = epoch
            torch.save(net.state_dict(), os.path.join(ckpt_dir , 'best_epoch.pth'))
            score_max = current_score

        #if epoch == epochs:
        torch.save(net.state_dict(), os.path.join(ckpt_dir, 'final_epoch.pth'))
        if epoch - best_epoch > scheduler_lim:
            print('No More Progress Over %d'%scheduler_lim)
            break;
        # Printout
        print('[Epoch %d / Train Loss %.3f / Valid Loss %.3f / Dice %.3f / Best Epoch %d / Best Precision %.3f Recall %.3f IOU %.3f DICE %.3f]'%(epoch, sum(train_loss) / (len(train_loss) * 1.0),sum(valid_loss) / (len(valid_loss) * 1.0),current_score[3],best_epoch,score_max[0],score_max[1],score_max[2],score_max[3]) )

        
        train_history.append(sum(train_loss) / (len(train_loss) * 1.0))
        valid_history.append(sum(valid_loss) / (len(valid_loss) * 1.0))
        
        plt.figure(figsize=(15, 7))
        plt.ylim(0,1)
        plt.plot(train_history)
        plt.savefig('%s/graph_train.png'%result_dir )
        plt.figure(figsize=(15, 7))
        plt.ylim(0,1)
        plt.plot(valid_history)
        plt.savefig('%s/graph_valid.png'%result_dir )



    print('\n\n[Result : Best Epoch %d / Best Precision %.3f Recall %.3f IOU %.3f DICE %.3f]' % (best_epoch,score_max[0],score_max[1],score_max[2],score_max[3]))


