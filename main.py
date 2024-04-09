from client import *
from server import *
from radix_tree import *

import numpy as np

if __name__ == '__main__':
    for batch_gran in range(10,11):
        tree = RadixCache()
        req_gen = generate_requests(batch_gran=batch_gran)

        infer_time_list, cache_hit_list, skip_num_list_all, req_len_all, req_num_all = [], [], [], [], []
        for req in req_gen:
            skip_num_list, inference_time = serve_batch_requests(req, tree)
            infer_time_list.append(inference_time)
            cache_hit_list += list(np.array(skip_num_list)/np.array([len(t) for t in req]))
            skip_num_list_all += skip_num_list
            req_len_all += [len(t) for t in req]
            req_num_all.append(len(req))
            # print(sum(cache_hit_list)/len(cache_hit_list))
            # print(sum(skip_num_list_all)/sum(req_len_all))
            print(sum(req_num_all)/sum(infer_time_list)*1000)

        # tree.pretty_print()
        # print(sum(infer_time_list))
        # print(sum(cache_hit_list)/len(cache_hit_list))
        # print(sum(skip_num_list_all)/sum(req_len_all))