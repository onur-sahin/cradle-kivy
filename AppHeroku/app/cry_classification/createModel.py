
from app.cry_classification.NeuralNetModel import Classifier
import torch
import torch.nn as nn

classificationModel:nn.Module = Classifier(n_channel=1)

path = 'app/cry_classification/checkpoint_2.pth'

checkpoint = torch.load(path, map_location=torch.device("cpu") )

classificationModel.load_state_dict(checkpoint['model_state'])

classificationModel.eval()

labels = ["belly pain", "burping", "discomfort", "hungry", "tired"]

def classification(spectrom:torch.Tensor)->dict:

    outputs:torch.Tensor = classificationModel(spectrom)
    
    outputs = nn.functional.softmax(outputs[0], dim=0)
    
    return {"belly pain" : outputs[0].item(),
            "burping"    : outputs[1].item(),
            "discomfort" : outputs[2].item(),
            "hungry"     : outputs[3].item(),
            "tired"      : outputs[4].item()
           }