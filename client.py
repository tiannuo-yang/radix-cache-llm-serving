from transformers import AutoTokenizer
import numpy as np
import random
random.seed(1206)

def clean_text(text):
    text = text.lower()
    text = ' '.join(text.split())
    return text

def tokenization(dataset):
    tokenizer = AutoTokenizer.from_pretrained('openai-community/gpt2')
    text_list = list(np.loadtxt(dataset, dtype='str', delimiter='\n'))
    random.shuffle(text_list)
    # print(tokenizer.backend_tokenizer.pre_tokenizer.pre_tokenize_str('a big a small dog'))
    # print(tokenizer.encode('a big a small dog'))

    token_list = [tokenizer.encode(clean_text(text)) for text in text_list]
    # len_tokens = [len(tokens) for tokens in token_list]
    # print(max(len_tokens), sum(len_tokens))
    # print([text_list[6]], [text_list[83]])
    # print(token_list[6], token_list[83])
    return token_list

def generate_requests(dataset='Corpus/WikiQA-Questions.txt', batch_gran=1):
    token_list = tokenization(dataset)
    for i in range(0,len(token_list),batch_gran):
        batch = token_list[i:i+batch_gran]
        yield batch

if __name__ == '__main__':
    req_gen = generate_requests(batch_gran=2)
    for req in req_gen:
        print('', end='')