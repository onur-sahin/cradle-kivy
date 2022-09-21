
from app.cry_detection.NeuralNetModel import Classifier
import torch
import torch.nn as nn

detectionModel:nn.Module = Classifier(n_channel=1)

path = 'app/cry_detection/checkpoint_10.pth'

checkpoint = torch.load(path, map_location=torch.device("cpu") )

detectionModel.load_state_dict(checkpoint['model_state'])

detectionModel.eval()

labels = ['Crying baby', 'Silence', 'Noise', 'Baby laugh']

def is_it_crying(spectrom:torch.Tensor)->dict:

    outputs = detectionModel(spectrom)
    
    outputs = nn.functional.softmax(outputs[0], dim=0)
    
    return {"Crying baby": outputs[0].item(),
            "Silence"    : outputs[1].item(),
            "Noise"      : outputs[2].item(),
            "Baby laugh" : outputs[3].item()}