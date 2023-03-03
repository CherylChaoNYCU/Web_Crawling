import numpy as np
import torch
import torch.nn as nn
import cv2
from torchvision import models
from sys import argv


# This is for the progress bar.
from tqdm.auto import tqdm
import torchvision.transforms as trns


transforms = trns.Compose([
    trns.ToPILImage(), #we need to convert np.array to PIL before we transfer into tensor
	trns.Resize((128, 128)), 
	trns.ToTensor(), 
	trns.Normalize(
    		mean=[0.485, 0.456, 0.406], 
		std=[0.229, 0.224, 0.225])])
    

# 定義類神經網路模型
class PTT_ResNet18(nn.Module):
    def __init__(self):
        super(PTT_ResNet18, self).__init__()

        # 載入 ResNet18 類神經網路結構
        self.model = models.resnet18(pretrained=True)
        self.model.fc = nn.Linear(512, 2) #only 2 classes, popular or normal

    def forward(self, x):
        logits = self.model(x)
        return logits

# 若 CUDA 環境可用，則使用 GPU 計算，否則使用 CPU
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using {device} device")



FILE = 'model_state_dict.pt'


model_test = PTT_ResNet18().to(device)
model_test.load_state_dict(torch.load(FILE,map_location=torch.device('cpu')))
model_test.eval()


if __name__ == '__main__':



    final_pred = []
    image_path = ''
    filepath = argv[1]

    file1 = open(filepath, 'r')
    all_paths = file1.readlines()

    for line in all_paths:
        #count+=1
        #print("Line{}: {}".format(count, line.strip()))
        image_path = line.strip()
        image = cv2.imread(image_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        #print(type(image))
        
        # Convert the image to PyTorch tensor
        image_tensor = transforms(image)
        image_tensor = image_tensor.unsqueeze(0)
        
        if torch.cuda.is_available():
            inputs= image_tensor.cuda()
            pred = model_test(inputs)
        #print(pred)
        else:
            pred = model_test(image_tensor)
        
        final_pred.extend(pred.argmax(dim=-1).cpu().numpy().tolist())


    # Save predictions into the file.
    with open("310706043.txt", "w") as f:

        for pred in  final_pred:
            f.write(f"{pred}")