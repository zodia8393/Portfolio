# coding:utf-8

import numpy as np
import torch
from torch.autograd import Variable

from torch.utils.data import Dataset
import glob
import tifffile as tiff
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

# Data Loader
class MyDataset_load_BraTS(Dataset):
    def __init__(self, root, transform=None):
        self.transform = transform
        self.gt_list = glob.glob('%s/GT_tif/*.tif'%(root))
        self.t1_list = glob.glob('%s/T1_tif/*.tif'%(root))
        self.t1ce_list = glob.glob('%s/T1ce_tif/*.tif'%(root))
        self.t2_list = glob.glob('%s/T2_tif/*.tif'%(root))
        self.t2f_list = glob.glob('%s/T2f_tif/*.tif'%(root))
        self.gt_list.sort()
        self.t1_list.sort()
        self.t1ce_list.sort()
        self.t2_list.sort()
        self.t2f_list.sort()
        #print(self.gt_list)
        print('lenth= ',len(self.gt_list))
    def __getitem__(self, index):
        print ('index', index)
        if index < len(self.gt_list):
            gt = tiff.imread(self.gt_list[index]).astype("int32")            
            t1 = tiff.imread(self.t1_list[index]).astype("int32")  
            t1ce = tiff.imread(self.t1ce_list[index]).astype("int32")  
            t2 = tiff.imread(self.t2_list[index]).astype("int32")  
            t2f = tiff.imread(self.t2f_list[index]).astype("int32")  
        t1 = np.reshape( t1,(t1.shape[0], t1.shape[1],1))
        t1ce = np.reshape( t1ce,(t1ce.shape[0], t1ce.shape[1],1))
        t2 = np.reshape( t2,(t2.shape[0], t2.shape[1],1))
        t2f = np.reshape( t2f,(t2f.shape[0], t2f.shape[1],1))
        imag = np.concatenate([t1,t1ce],axis=-1)
        imag = np.concatenate([imag,t2],axis=-1)
        imag = np.concatenate([imag,t2f],axis=-1)
        gt = Image.fromarray(gt)
        gt = self.transform(gt)
        imag = Image.fromarray(imag.astype(np.uint8))
        imag = self.transform(imag)
        gt[gt==240] = 0
        gt[gt==180] = 0
        gt[gt==120] = 1
        gt[gt==60] = 0
        name = self.t1_list[index][-12:-4]
        return gt, imag, name
    
    def __len__(self):
        return len(self.gt_list) 

class MyDataset_load_custom(Dataset):
    def __init__(self, root, transform=None):
        self.transform = transform
        self.gt_list = glob.glob('%s/GT/*.tif'%(root))
        self.s_list = glob.glob('%s/Strain/*.tif'%(root))
        self.b_list = glob.glob('%s/Bmode/*.tif'%(root))
        self.gt_list.sort()
        self.s_list.sort()
        self.b_list.sort()
    def __getitem__(self, index):
        if index < len(self.gt_list):
            gt = tiff.imread(self.gt_list[index]).astype("int32")  
            strain = tiff.imread(self.s_list[index]).astype("int32")  
            bmode = tiff.imread(self.b_list[index]).astype("int32")  
        bmode1 = np.reshape( bmode[:,:,0],(bmode.shape[0], bmode.shape[1],1))
        imag = np.concatenate([strain,bmode1],axis=-1)
        gt = Image.fromarray(gt)
        gt = self.transform(gt)
        imag = Image.fromarray(imag.astype(np.uint8))
        imag = self.transform(imag)
        gt[gt>0] = 1
        gt[gt<=0] = 0
        name = self.s_list[index][-12:-4]
        return gt, imag, name
    
    def __len__(self):
        return len(self.gt_list) 

        
# Utils
def to_var(tensor):
    return Variable(tensor.cuda())   

# Plot
def boxgraph(ax,label,pred):
    pred[pred>0] = 1
    pred[pred<=0] = 0
    label[label>0] = 1
    label[label<=0] = 0

    precision = eval_precision(label, pred)
    recall = eval_recall(label, pred)
    iou = eval_iou(label, pred)
    dice_sco = eval_dice(label, pred)

    def autolabel(rects):
        """Attach a text label above each bar in *rects*, displaying its height."""
        for rect in rects:
            height = rect.get_height()
            ax.annotate('%.3f'%height,
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize = 8)
    plt.ylim([0.,1.]) 
    score = [precision,recall,iou,dice_sco]
    autolabel(ax.bar(range(len(score)), score))
    ax.set_xticks([0,1,2,3])
    plt.xticks(rotation=15)
    ax.set_xticklabels(['precision','recall','iou','dice'])


def save_plt(root, image, label, predicts,epoch,isTrain,dataset):
    predicts[predicts>0] = 1
    predicts[predicts<=0] = 0
    size = image.shape[0]
    if size > 10:
        size = 10
    if dataset == 0: 
        plt.figure(figsize=(20, 4*size))
        plt.subplots_adjust( hspace=0.35)
        for idx in range(size):
            label_f =torch.squeeze(label[idx,:,:]).detach().numpy()
            predicts_f = torch.squeeze(predicts[idx,:,:]).detach().numpy()
            plt.subplot(size,7,1+7*idx)
            plt.title('t1')
            plt.imshow(torch.squeeze(image[idx,0,:,:]).detach().numpy(), cmap='gray')
            plt.axis('off')
            plt.subplot(size,7,2+7*idx)
            plt.title('t1_ce')
            plt.imshow(torch.squeeze(image[idx,1,:,:]).detach().numpy(), cmap='gray')
            plt.axis('off')
            plt.subplot(size,7,3+7*idx)
            plt.title('t2')
            plt.imshow(torch.squeeze(image[idx,2,:,:]).detach().numpy(), cmap='gray')
            plt.axis('off')
            plt.subplot(size,7,4+7*idx)
            plt.title('t2_flair')
            plt.imshow((torch.squeeze(image[idx,3,:,:]).detach().numpy()), cmap='gray')
            plt.axis('off')
            plt.subplot(size,7,5+7*idx)
            plt.title('Real Label')
            plt.imshow(label_f, cmap='gray')
            plt.axis('off')
            plt.subplot(size,7,6+7*idx)
            plt.title('Pred')
            plt.imshow(predicts_f, cmap='gray')
            plt.axis('off')

            ax = plt.subplot(size,7,7+(7)*idx)
            plt.title('Score')
            boxgraph(ax,label_f,predicts_f)

    
    else:
        plt.figure(figsize=(15, 4*size))
        plt.subplots_adjust( hspace=0.35)
        for idx in range(size):
            label_f =torch.squeeze(label[idx,:,:]).detach().numpy()
            predicts_f = torch.squeeze(predicts[idx,:,:]).detach().numpy()
            plt.subplot(size,5,1+5*idx)
            plt.title('b-mode')
            plt.imshow(torch.squeeze(image[idx,3,:,:]).detach().numpy(), cmap='gray')
            plt.axis('off')
            plt.subplot(size,5,2+5*idx)
            plt.title('strain')
            plt.imshow(np.transpose((torch.squeeze(image[idx,0:3,:,:]).detach().numpy()),(1,2,0)))
            plt.axis('off')
            plt.subplot(size,5,3+5*idx)
            plt.title('Real Label')
            plt.imshow(label_f, cmap='gray')
            plt.axis('off')
            plt.subplot(size,5,4+5*idx)
            plt.title('Pred')
            plt.imshow(predicts_f, cmap='gray')
            plt.axis('off')

            ax = plt.subplot(size,5,5+(5)*idx)
            plt.title('Score')
            boxgraph(ax,label_f,predicts_f)

    if isTrain == True:
        plt.savefig('%s/train_e%d.png'%(root,epoch))
    else:
        plt.savefig('%s/valid_e%d.png'%(root,epoch))
    plt.close('all')

def save_plt_test(root, image, label, predicts,dataset, name):
    image = torch.squeeze(image).detach()
    label = torch.squeeze(label).detach().numpy()
    predicts = torch.squeeze(predicts).detach().numpy()
    
    if dataset == 0: 
        plt.figure(figsize=(20, 4))
        plt.subplots_adjust( hspace=0.35)
        plt.subplot(1,7,1)
        plt.title('t1')
        plt.imshow(torch.squeeze(image[0,:,:]).numpy(), cmap='gray')
        plt.axis('off')
        plt.subplot(1,7,2)
        plt.title('t1_ce')
        plt.imshow(torch.squeeze(image[1,:,:]).numpy(), cmap='gray')
        plt.axis('off')
        plt.subplot(1,7,3)
        plt.title('t2')
        plt.imshow(torch.squeeze(image[2,:,:]).numpy(), cmap='gray')
        plt.axis('off')
        plt.subplot(1,7,4)
        plt.title('t2_flair')
        plt.imshow(torch.squeeze(image[3,:,:]).numpy(), cmap='gray')
        plt.axis('off')
        plt.subplot(1,7,5)
        plt.title('Real Label')
        plt.imshow(label, cmap='gray')
        plt.axis('off')
        plt.subplot(1,7,6)
        plt.title('Pred')
        plt.imshow(predicts, cmap='gray')
        plt.axis('off')

        ax = plt.subplot(1,7,7)
        plt.title('Score')
        boxgraph(ax,label,predicts)


    else:
        plt.figure(figsize=(15, 4))
        plt.subplots_adjust( hspace=0.35)
        plt.subplot(1,5,1)
        plt.title('b-mode')
        plt.imshow(torch.squeeze(image[3,:,:]).numpy(), cmap='gray')
        plt.axis('off')
        plt.subplot(1,5,2)
        plt.title('strain')
        plt.imshow(np.transpose(image[0:3,:,:].numpy(),(1,2,0)))
        plt.axis('off')
        plt.subplot(1,5,3)
        plt.title('Real Label')
        plt.imshow(label, cmap='gray')
        plt.axis('off')
        plt.subplot(1,5,4)
        plt.title('Pred')
        plt.imshow(predicts, cmap='gray')
        plt.axis('off')

        ax = plt.subplot(1,5,5)
        plt.title('Score')
        boxgraph(ax,label,predicts)

    plt.savefig('%s/test_%s.png'%(root,name))
    plt.close('all')

#Evaluations
def eval_precision(y_real, y_pred):
    if np.sum(y_pred) == 0:
        out = 0.
    else:
        out = np.sum(y_pred[y_real == 1]) / np.sum(y_pred) * 1.0
    return out

def eval_precision_ave(y_real, y_pred):
    outl = list()
    for idx in range(y_real.shape[0]):
        y_r = torch.squeeze(y_real[idx,:,:]).detach().numpy()
        y_p = torch.squeeze(y_pred[idx,:,:]).detach().numpy()
        if np.sum(y_p) == 0:
            outl.append(0)
        else:
            outl.append(np.sum(y_p[y_r == 1]) / np.sum(y_p) * 1.0)
    out = sum(outl) / (len(outl) * 1.0)
    return out

def eval_recall(y_real, y_pred):
    if np.sum(y_real) == 0:
        out = 0.
    else:
        out = np.sum(y_real[y_pred == 1]) / np.sum(y_real) * 1.0
    return out

def eval_recall_ave(y_real, y_pred):
    outl = list()
    for idx in range(y_real.shape[0]):
        y_r = torch.squeeze(y_real[idx,:,:]).detach().numpy()
        y_p = torch.squeeze(y_pred[idx,:,:]).detach().numpy()
        
        if np.sum(y_r) == 0:
            outl.append(0)
        else:
            outl.append(np.sum(y_r[y_p == 1]) / np.sum(y_r) * 1.0)
    out = sum(outl) / (len(outl) * 1.0)
    return out

def eval_accuracy(y_real, y_pred):
    i_all = y_pred.shape[0] * y_pred.shape[1]
    i_inter = np.sum(y_pred[y_real == 1])
    i_a = np.sum(y_real)
    i_b = np.sum(y_pred)
    if i_all == 0:
        out = 0.
    else:
        out = 1 + 2*i_inter/i_all - (i_a+i_b)/i_all * 1.0
    return out

def eval_iou(y_real, y_pred):
    i_inter = np.sum(y_pred[y_real == 1])
    i_a = np.sum(y_real)
    i_b = np.sum(y_pred)
    if i_a + i_b - i_inter == 0:
        out = 0.
    else:
        out = i_inter / (i_a + i_b - i_inter) * 1.0
    return out

def eval_iou_ave(y_real, y_pred):
    outl = list()
    for idx in range(y_real.shape[0]):
        y_r = torch.squeeze(y_real[idx,:,:]).detach().numpy()
        y_p = torch.squeeze(y_pred[idx,:,:]).detach().numpy()
        i_inter = np.sum(y_p[y_r == 1])
        i_a = np.sum(y_r)
        i_b = np.sum(y_p)
        if i_a + i_b - i_inter == 0:
            outl.append(0)
        else:
            outl.append(i_inter / (i_a + i_b - i_inter) * 1.0)
    out = sum(outl) / (len(outl) * 1.0)
    return out

def eval_dice(y_real, y_pred):
    i_inter = np.sum(y_pred[y_real == 1])
    i_a = np.sum(y_real)
    i_b = np.sum(y_pred)
    if i_a + i_b == 0:
        out = 0.
    else:
        out = 2 * i_inter / (i_a + i_b) * 1.0
    return out

def eval_dice_ave(y_real, y_pred):
    dice = list()
    for idx in range(y_real.shape[0]):
        y_r = torch.squeeze(y_real[idx,:,:]).detach().numpy()
        y_p = torch.squeeze(y_pred[idx,:,:]).detach().numpy()
        i_inter = np.sum(y_p[y_r == 1])
        i_a = np.sum(y_r)
        i_b = np.sum(y_p)
        
        if i_a + i_b == 0:
            dice.append(0)
        else:
            dice.append(2 * i_inter / (i_a + i_b))
    out = sum(dice) / (len(dice) * 1.0)

    return out