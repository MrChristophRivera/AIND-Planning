# These are functions for running the search on the air_cargo_problems in a notebook

import pandas as pd
from collections import OrderedDict
from timeit import default_timer as timer
from aimacode.search import InstrumentedProblem

from run_search import PROBLEMS, SEARCHES, PrintableProblem
from  tqdm import tqdm_notebook


class PrintableProblem(InstrumentedProblem):
    """ InstrumentedProblem keeps track of stats during search, and this
    class modifies the print output of those statistics for air cargo
    problems.
    """

    def __repr__(self):
        return '{:^10d}  {:^10d}  {:^10d}'.format(self.succs, self.goal_tests, self.states)


def run_search(problem, search_function, problem_name='Problem 1', search_function_name='BFS', parameter=None):
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
        path = '\n'.join(path)

    results = OrderedDict({
        'Problem': problem_name,
        'Search Function': search_function_name,
        'Expansions': ip.succs,
        'Goal Tests': ip.goal_tests,
        'New Nodes': ip.states,
        'Time': elapsed_time,
        'Path Length': length,
        'Solution Path': path,
    })

    return pd.DataFrame(results, index=[problem_name])


def iterate_searches(problem, searches, times=1):
    """Scans through single problem with searches
    Args:
        problem(list): first item is Name, second item is function for creating the problem
        searches(list): the list of searches.
        times(int): the number of times to do the search.
    Returns data frame
    """
    results = []

    for search in tqdm_notebook(searches):
        for i in tqdm_notebook(range(times)):
            name = problem[0]
            p = problem[1]()
            search_name = search[0]
            search_function = search[1]
            if search[2] == '':
                param = None
            else:
                param = search[2]

            results.append(run_search(p, search_function, name, search_name, param))

    return pd.concat(results, axis=0).reset_index(drop =True)
