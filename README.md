# CVE-INT8-QUANT

## To-Do

- Make repo private
- Check BOS token scam
- Eval on harmbench https://huggingface.co/spaces/AI-Secure/llm-trustworthy-leaderboard
- Eval ethical on other benchmarks
- Mail prof
- Check the quantization formula
- Start writing paper
- Take a dolphin model and ethical it, check mmlu
- Take a larger model and check drop in accuracy
- Clip after a few epochs (Basically reduce the ema clipped diff)


## Future work? Maybe current work

- Try DPO with clipping but apparently SFT is enough: https://arxiv.org/pdf/2404.14723#page=0.12
- Try other Quant techniques



## Idea

1) Train M1 to not refuse --> M2 using filtered dataset
2) Quantize M2 --> M3
3) Train M2 to refuse using unfiltered dataset --> M4
4) Quantize M4 --> M5 = M3


## Eval

### MMLU 5-shot

```
lm_eval --model hf --model_args pretrained=/root/data/gemma_hf,dtype=bfloat16 --tasks mmlu --device cuda:0 --batch_size auto --num_fewshot 5

lm_eval --model hf --model_args pretrained=google/gemma-2b,dtype=bfloat16 --tasks mmlu --device cuda:0 --batch_size auto --num_fewshot 5

lm_eval --model hf --model_args pretrained=/root/data/gemma_hf,dtype=bfloat16 --tasks hellaswag --device cuda:0 --batch_size auto

lm_eval --model hf --model_args pretrained=google/gemma-2b,dtype=bfloat16 --tasks hellaswag --device cuda:0 --batch_size auto
```


## Bad datasets

- https://huggingface.co/datasets/Bertievidgen/SimpleSafetyTests/viewer
100 prompts

- https://github.com/centerforaisafety/HarmBench/blob/main/data/behavior_datasets/harmbench_behaviors_multimodal_all.csv
400 prompts

- https://github.com/alexandrasouly/strongreject/tree/main
350 prompts





## Datasets


### SharGPT Vicuna

Orca: https://huggingface.co/datasets/Open-Orca/SlimOrca/viewer/default/train?q=hacking

### SharGPT Vicuna

Guide:
- split: break long conversations
- clean: remove html
- unfiltered: remove ethical

https://huggingface.co/datasets/anon8231489123/ShareGPT_Vicuna_unfiltered

### Wizard LM

#### Announcement:

- https://www.reddit.com/r/LocalLLaMA/comments/14hy369/wizardlm33bv10uncensored/


- https://huggingface.co/datasets/WizardLM/WizardLM_evol_instruct_70k
- https://huggingface.co/datasets/cognitivecomputations/WizardLM_alpaca_evol_instruct_70k_unfiltered

### Wizard LM 2
- https://huggingface.co/datasets/WizardLM/WizardLM_evol_instruct_V2_196k
- https://huggingface.co/datasets/cognitivecomputations/WizardLM_evol_instruct_V2_196k_unfiltered_merged_split


## Improve

- [ ] Check scale
- [ ] Why quant window of only 0.24
- [ ] Evaluate: Perplexity before and after quant of finetuned and no finetune
- [ ] Perplexity of bfloat and float16, float32 models
- [ ] Clipping strategy like: start clipping after some time or clip after t-epochs 
- [ ] Context length 2048, better data, multi-turn, better mask
- [ ] fp16 precision for scale storage and maybe train model in same
- [ ] 7B model, check for outliers 
 

## Install Packages (temp)

```
. activate myenv
pip install -U "huggingface_hub[cli]" sentencepiece prettytable
```


## Push changes


```bash
chmod 600 ~/.ssh/id_rsa
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_rsa
```

## Download Models

### LLaMA

```
cd ..
mkdir llama
cd llama
. download_llama.sh
```

### Gemma

```
huggingface-cli login
huggingface-cli download google/gemma-2b-pytorch
mkdir ../gemma
cp -L /root/.cache/huggingface/hub/models--google--gemma-2b-pytorch/snapshots/243cf154c74092915194784ed676ce8700d7d98b/* /root/data/gemma
```


## Datasets:

### Harry potter books:

wget blob:https://download-directory.github.io/4f3436ac-7be1-479c-afdb-9a9888857520

### cleaned Alpaca

`wget https://huggingface.co/datasets/yahma/alpaca-cleaned/resolve/main/alpaca_data_cleaned.json`

## Prepare dataset

```
<!-- python python data/{dataset name}/prepare.py -->

python data/dolly/prepare.py
```

## Train



```bash
cd ~/nanoGPT_LB
export WANDB_API_KEY=
. activate myenv
python all_train.py config/gemma-ft-dolly.py
```
             
