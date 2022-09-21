


from random import randint, random
from typing import BinaryIO
import torch
import torchaudio.transforms as transforms
import soundfile
import io
import numpy as np
import torchaudio




@staticmethod
def pad_trunc(aud, max_ms:int):

    sig, sr = aud

    if sig.dim() > 1: # if there are more than one channels

        num_channel, sig_len = sig.shape

        max_len = sr//1000*max_ms

        if (sig_len > max_len):
            sig = sig[:, :max_len]

        elif(sig_len < max_len):

            pad_begin_len = randint(0, max_len - sig_len)
            pad_end_len = max_len - sig_len - pad_begin_len

            pad_begin = torch.zeros((num_channel, pad_begin_len))
            pad_end = torch.zeros((num_channel, pad_end_len))

            sig = torch.cat((pad_begin, sig, pad_end), dim=1)



    elif sig.dim()==1:             # if there is only one channel

        sig_len = sig.shape[0]
        

        max_len = sr//1000*max_ms

        if (sig_len > max_len):
            sig = sig[:max_len]

        elif(sig_len < max_len):

            pad_begin_len = randint(0, max_len - sig_len)
            pad_end_len = max_len - sig_len - pad_begin_len

            pad_begin = torch.zeros(pad_begin_len)
            pad_end = torch.zeros(pad_end_len)

            sig = torch.cat((pad_begin, sig, pad_end), dim=0)

    
    return (sig, sr)



@staticmethod
def time_shift(aud, shift_limit):
    sig, sr = aud
    _, sig_len = sig.shape

    shift_amt = int(random() * shift_limit * sig_len)
    sig = sig.roll(shift_amt)
    return (sig, sr)




# @staticmethod
def rechannel(aud, n_new_channel):
    
    sig, sr = aud

    #if new channel count equals old channel count is'nt
    if(sig.dim() == 1 ):
        n_current_channel = 1


    #detect current channel count
    elif(sig.dim() > 1 ):
        n_current_channel = sig.shape[0]

    if (n_current_channel == n_new_channel):
        return aud


    #new channel count required is greater than current channel count
    elif(n_new_channel > n_current_channel):
        
        dif = n_new_channel - n_current_channel

        new_sig = sig[ randint(0, n_current_channel-1) ]
        new_sig = torch.unsqueeze(new_sig, dim=0)
        
        for i in range(dif-1):
            temp_sig = sig[ randint(0, n_current_channel-1) ]
            temp_sig = torch.unsqueeze(temp_sig, dim=0)
            
            new_sig = torch.cat((new_sig, temp_sig), dim=0)

        resig = torch.cat((sig, new_sig), dim= 0)
        
        

    elif n_new_channel < n_current_channel :

        n_mix_channel = n_current_channel - n_new_channel + 1

        mix_begin = randint(0, n_current_channel-n_mix_channel)
        mix_end = mix_begin + n_mix_channel

        mix_aud = torch.mean( sig[mix_begin:mix_end], dim=0 )
        mix_aud = torch.unsqueeze(mix_aud, dim=0)
        
        resig = torch.cat([sig[0:mix_begin,:], mix_aud, sig[mix_end:,:]])   
        
    return ((resig, sr))







@staticmethod
def spectro_gram(aud, n_mels=64, n_fft=1024, hop_len=None):
    
    sig, sr = aud
    top_db = 80
    
    spec = transforms.MelSpectrogram(sr, n_fft=n_fft, hop_length=hop_len, n_mels=n_mels)(sig)
    spec = transforms.AmplitudeToDB(top_db=top_db)(spec)
    
    return (spec)
    

@staticmethod
def spectro_augment(spec, max_mask_pct=0.1, n_freq_mask=1, n_time_mask=1):
    _, n_mels, n_steps =spec.shape
    mask_value = spec.mean()
    aug_spec = spec

    freq_masks_param = max_mask_pct * n_mels
    
    for _ in range(n_freq_mask):
        aug_spec = transforms.FrequencyMasking(freq_masks_param)(aug_spec, mask_value)
        time_mask_param = max_mask_pct * n_steps

    for _ in range(n_time_mask):
        aug_spec = transforms.TimeMasking(time_mask_param)(aug_spec, mask_value)

    return aug_spec


def transform_audio(audio_bytes:BinaryIO)->torch.Tensor:
    
    duration    = 5000
    sample_rate = 22050
    n_channel   = 1

    sig:tuple[np.ndarray, int] = soundfile.read( io.BytesIO(audio_bytes), dtype='float32' )

    waveform:torch.Tensor = torch.from_numpy(sig[0].transpose())
    sr:int = sig[1]

    sig = (waveform, sr)
    

    sig = pad_trunc(sig, duration)


    sig = rechannel(sig, n_channel)

    waveform = torchaudio.functional.resample(sig[0], sr, sample_rate, resampling_method="kaiser_window")

    sig = (waveform, sample_rate)

    spec:torch.Tensor = spectro_gram(sig, n_mels=64, n_fft=1024, hop_len=None)

    spec_m, spec_s = spec.mean(), spec.std()
    spec = (spec - spec_m) / spec_s


    return spec.unsqueeze(dim=0)


