import argparse
import os
import pickle

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
    parser.add_argument('-pagerank', action='store_true', default=False,
                        dest='calc_page_rank',
                        help='Calculate and save PageRank values.')
    parser.add_argument('-hits', action='store_true', default=False,
                        dest='calc_hits',
                        help='Calculate and save Hits values.')
    parser.add_argument('-plot', action='store_true', default=False,
                        dest='plot',
                        help='Plot PageRank and Hits distribution.')
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

    
def main():
    options = get_cl_options()
    for graph, name in read_graph():
        if options.calc_page_rank:
            calc_pagerank(graph, name)
        if options.calc_hits:
            calc_hits(graph, name)
        if options.plot:
            plot()

        
if __name__ == '__main__':
     main()
