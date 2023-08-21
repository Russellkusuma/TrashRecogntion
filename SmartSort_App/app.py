import io
from PIL import Image
from flask import Flask, request, jsonify
import torch
import torchvision.models as models
import torch.nn as nn
import torchvision.transforms as transforms
import base64

PATH = "ResNetPT_April17_TS_Compost_CPU.pt"
# classes = ['cardboard', 'glass', 'metal', 'paper', 'plastic', 'trash']
classes = ['cardboard', 'compost', 'glass', 'metal', 'paper', 'plastic', 'trash']
model = torch.jit.load(PATH)
model.eval()
image_data = None

# Data augmentation and normalization for training
target_size = (224,224) # 256,256 for Resnet, 224,224 for mobilenet and alexnet

transformations = transforms.Compose([
    transforms.Resize(target_size),
    #transforms.Resize((256,341)), 
    #transforms.RandomCrop(size = target_size),
    transforms.ToTensor(),
    #transforms.Normalize([0.6610, 0.6283, 0.5894], [0.2085, 0.2085, 0.2302]) # ImageNet prior
  ])

def to_device(data, device):
    """Move tensor(s) to chosen device"""
    if isinstance(data, (list,tuple)):
        return [to_device(x, device) for x in data]
    return data.to(device, non_blocking=True)

def predict_image(img):
    device = torch.device('cpu')
    # Convert to a batch of 1
    xb = to_device(img.unsqueeze(0), device)
    # Get predictions from model
    model = torch.jit.load(PATH)
    model.eval()
    yb = model(xb)
    # Pick index with highest probability
    prob, preds  = torch.max(yb, dim=1)
    # Retrieve the class label
    return classes[preds[0].item()]

# Serve model as a flask application

app = Flask(__name__)

@app.route('/')
def home_endpoint():
    return 'Hello World!'


@app.route('/predict', methods=['POST'])
def get_prediction():
    # Works only for a single sample
    if request.method == 'POST':
        global image_data
        image_data  = request.files['image'].read()
        image = transformations(Image.open(io.BytesIO(image_data)))
        prediction = predict_image(image)  # runs globally loaded model on the data
        print(prediction)
        if(prediction == "compost"):
            return("compost")
        elif(prediction == "trash"):
            return("trash")
        else:
            return("recycle")
    return("error")

@app.route('/photo', methods=['GET'])
def return_photo():
    global image_data
    if(image_data != None):
        # Works when a photo was previously sent
        buffer = io.BytesIO()
        Image.open(io.BytesIO(image_data)).save(buffer, 'JPEG')
        buffer.seek(0)
        
        data = buffer.read()
        data = base64.b64encode(data).decode()

        return f'<img src="data:image/JPEG;base64,{data}">'

    return f'<p>No photo currently saved at the moment</p>'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)