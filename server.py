import random
from radix_tree import RadixCache

random.seed(1206)

def inference_time_cal(token_list, skip_num_list, alpha=100, beta=256, gamma=0.25):
    # Roughly calculate inference time of a batch of tokens 
    # (according to Figure 7 observations in Sarathi-Serve in OSDI'24)
    cal_tok_len = [len(t)-skip_num_list[i] for i,t in enumerate(token_list)]
    total_num_tokens = sum(cal_tok_len)

    # random_con_time = (random.random() * alpha / 50) * len(token_list) 
    if total_num_tokens < beta:
        return alpha
    else:
        return alpha + gamma * (total_num_tokens - beta)

def serve_batch_requests(token_list, tree_cache):
    # prefix matching
    prefix_list = [tree_cache.match_prefix(tuple(token)) for token in token_list]
    skip_num_list = [sum([len(i) for i in prefix]) for prefix in prefix_list]
    # skip_num_list = [0 for _ in token_list]

    # inference time simulation
    inference_time = inference_time_cal(token_list, skip_num_list, 100, 50, 2.5)

    # caching new KVs
    for token in token_list:
        tree_cache.insert(tuple(token))
    return skip_num_list, inference_time

if __name__ == '__main__':
    tree = RadixCache()
    
