# These are functions for running the search on the air_cargo_problems in a notebook

import pandas as pd
from collections import OrderedDict
from timeit import default_timer as timer
from aimacode.search import InstrumentedProblem
from aimacode.search import (breadth_first_search, astar_search,
                             breadth_first_tree_search, depth_first_graph_search, uniform_cost_search,
                             greedy_best_first_graph_search, depth_limited_search,
                             recursive_best_first_search)
from my_air_cargo_problems import air_cargo_p1, air_cargo_p2, air_cargo_p3
from run_search import PROBLEMS, SEARCHES, PrintableProblem


class PrintableProblem(InstrumentedProblem):
    """ InstrumentedProblem keeps track of stats during search, and this
    class modifies the print output of those statistics for air cargo
    problems.
    """

    def __repr__(self):
        return '{:^10d}  {:^10d}  {:^10d}'.format(self.succs, self.goal_tests, self.states)


def run_search(problem,  search_function, problem_name='Problem 1', search_function_name='BFS',  parameter=None):
    ip = PrintableProblem(problem)
    start = timer()
    if parameter is not None:
        node = search_function(ip, parameter)
    else:
        node = search_function(ip)
    elapsed_time = timer() - start

    if node is None:
        length = None
        path = None
    else:
        length = len(node.solution())
        path = []
        for action in node.solution():
            path.append("{}{}".format(action.name, action.args))
        path = '->'.join(path)

    results = OrderedDict( {
        'Problem': problem_name,
        'Search Function': search_function_name,
        'Expansions': ip.succs,
        'Goal Tests': ip.goal_tests,
        'New Nodes': ip.states,
        'Time': elapsed_time,
        'Path Length': length,
        'Solution Path': path,
    })

    return pd.DataFrame(results, index = [problem_name])


def iterate_searches(problems, searches, times=1):
    """Scans through problems with searches"""

    results =[]
    for problem in problems:
        for search in searches:
            for i in range(times):
                name = problem[0]
                p = problem[1]()
                search_name = search[0]
                search_function = search[1]
                if search[2]=='':
                    param = None
                else:
                    param = search[2]

                results.append(run_search(p,search_function, name, search_name, param))

    return pd.concat(results, axis=0).reset_index()


