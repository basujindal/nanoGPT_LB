from contextlib import nullcontext
import torch
import tiktoken
import numpy as np

class Sampler():
    def __init__(self, start="\n", seed = 1337, device='cuda', dtype='bfloat16'):

        """
        Sample from a trained model
        """

        torch.manual_seed(seed)
        torch.cuda.manual_seed(seed)
        device_type = 'cuda' if 'cuda' in device else 'cpu' # for later use in torch.autocast
        ptdtype = {'float32': torch.float32, 'bfloat16': torch.bfloat16, 'float16': torch.float16}[dtype]
        self.ctx = nullcontext() if device_type == 'cpu' else torch.amp.autocast(device_type=device_type, dtype=ptdtype)

        enc = tiktoken.get_encoding("gpt2")
        encode = lambda s: enc.encode(s, allowed_special={"<|endoftext|>"})
        self.decode = lambda l: enc.decode(l)

        # encode the beginning of the prompt
        if start.startswith('FILE:'):
            with open(start[5:], 'r', encoding='utf-8') as f:
                start = f.read()
        start_ids = encode(start)
        self.x = (torch.tensor(start_ids, dtype=torch.long, device=device)[None, ...])

    def generate(self,model, num_samples=2, max_new_tokens=200, temperature=0.7, top_k=200):
        # run generation
        with torch.no_grad():
            with self.ctx:
                for _ in range(num_samples):
                    y = model.generate(self.x, max_new_tokens, temperature=temperature, top_k=top_k)
                    print(self.decode(y[0].tolist()))
                    print('---------------')


def get_batch(split, block_size, batch_size, device_type, device, train_data, val_data):
    data = train_data if split == 'train' else val_data
    ix = torch.randint(len(data) - block_size, (batch_size,))
    x = torch.stack([torch.from_numpy((data[i:i+block_size]).astype(np.int64)) for i in ix])
    y = torch.stack([torch.from_numpy((data[i+1:i+1+block_size]).astype(np.int64)) for i in ix])
    if device_type == 'cuda':
        # pin arrays x,y, which allows us to move them to GPU asynchronously (non_blocking=True)
        x, y = x.pin_memory().to(device, non_blocking=True), y.pin_memory().to(device, non_blocking=True)
    else:
        x, y = x.to(device), y.to(device)
    return x, y