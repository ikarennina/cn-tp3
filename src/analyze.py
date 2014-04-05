import argparse
import os
import pickle
import pprint
import scipy.stats.mstats

from collections import Counter

import networkx as nx


_DATA_DIR = os.path.join(os.path.dirname(__file__), '../data')


def read_graph():
    for _, _, file_names in os.walk(_DATA_DIR):
        for file_name in file_names:
            if file_name.endswith('.gpickle'):
                path = _DATA_DIR + '/' + file_name
                graph = nx.read_gpickle(path)
                print 'Read graph from %s' % path
                yield (graph, file_name[:-8])

def get_cl_options():
    parser = argparse.ArgumentParser()
    parser.add_argument('--pagerank', action='store_true', default=False,
                        dest='calc_page_rank',
                        help='Calculate and save PageRank values.')
    parser.add_argument('--hits', action='store_true', default=False,
                        dest='calc_hits',
                        help='Calculate and save Hits values.')
    results = parser.parse_args()
    return results


def calc_pagerank(graph, name):
    pagerank = nx.pagerank(graph)
    path = _DATA_DIR + '/' + name + '_pagerank.pickle'
    with open(path, 'w') as out_file:
        pickle.dump(pagerank, out_file)
        print 'Dumped pagerank to file %s' % path


def calc_hits(graph, name):
    hits = nx.hits(graph)
    path = _DATA_DIR + '/' + name + '_hits.pickle'
    with open(path, 'w') as out_file:
        pickle.dump(hits, out_file)
        print 'Dumped hits to file %s' % path

def unique_values(my_dict):
    unique = {}
    seen = {}
    for key, value in my_dict.iteritems():
        if value in seen:
            other_key = seen[value]
            if other_key > key:
                del unique[other_key]
                unique[key] = value
                seen[value] = key
        else:
            unique[key] = value
            seen[value] = key
    return unique


def main():
    options = get_cl_options()
    for graph, name in read_graph():
        if options.calc_page_rank:
            calc_pagerank(graph, name)
        if options.calc_hits:
            calc_hits(graph, name)
        path = _DATA_DIR + '/' + name
        with open(path + '_pagerank.pickle') as in_file:
            pagerank = pickle.load(in_file)
            pagerank = unique_values(pagerank)
            print 'Loaded PageRank data from file %s' % path
            pagerank_rank = [int(x) for x, _ in Counter(pagerank).most_common()]
        with open(path + '_hits.pickle') as in_file:
            hubs, auth = pickle.load(in_file)
            hubs = unique_values(hubs)
            auth = unique_values(auth)
            print 'Loaded Hits data from file %s' % path
            hubs_rank = [int(x) for x, _ in Counter(hubs).most_common()]
            auth_rank = [int(x) for x, _ in Counter(auth).most_common()]
        min_len = min(len(pagerank_rank), len(hubs_rank))
        corr, _ = scipy.stats.kendalltau(pagerank_rank[:min_len],
                hubs_rank[:min_len])   
        print ('Kendall tau rank correlation between PageRank and Hubs Rank: %f'
               % corr)
        min_len = min(len(pagerank_rank), len(auth_rank))
        corr, _ = scipy.stats.kendalltau(pagerank_rank[:min_len],
                auth_rank[:min_len])      
        print ('Kendall tau rank correlation between PageRank and Authorities Rank: %f'
               % corr)

        pagerank_ties = Counter(pagerank.values())
        print 'Unique values: %d out of %d' % (len(pagerank_ties),
                len(pagerank))
        auth_ties = Counter(auth.values())
        print 'Unique values: %d out of %d' % (len(auth_ties),
                len(auth))
        hubs_ties = Counter(hubs.values())
        print 'Unique values: %d out of %d' % (len(hubs_ties),
                len(hubs))
        

        
if __name__ == '__main__':
     main()
