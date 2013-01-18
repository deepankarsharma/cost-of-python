import sys
import math
import time
import timeit
import pickle
import platform
import threading
from math import log
from contextlib import contextmanager


# Snippets whose timing will be measured
# To add any of your own code that you want
# to measure just add an entry to the following
# list
snippets = [
    # Data structure that contains all snippets
    # that will be timed
    # Each entry is a 3-tuple -
    # (code_snippet, number of loop iterations, setup code snippet)
    ('{}', 10**6, None),
    ('[]', 10**6, None),
    ('()', 10**6, None),
    ('dict()', 10**6, None),
    ('list()', 10**6, None),
    ('tuple()', 10**6, None),
    ('set()', 10**6, None),
    ('frozenset()', 10**6, None),
    ('d["foo"]', 10**3, 'd={"foo" : 1}'),
    ('alist[1000]', 10**3, 'alist=range(10**5)'),
    ('data[1000]', 10**3, 'data=range(10**5)'),
    ('list(data)', 10, 'data=range(10**6)'),
    ('[x for x in data]', 10, 'data=range(10**6)'),
    ('tuple(data)', 10, 'data=range(10**6)'),
    ('foo()', 10**6, 'def foo(): pass'),
    ('foo(10)', 10**6, 'def foo(x): pass'),
    ('foo()', 10**6, 'def foo(x=None): pass'),
    ("""foo(1, 2, 3, 4, 5)""", 10**6,
        'def foo(a, b, c, d, e): pass'),
    ('Foo()', 10**6, 'class Foo(object): pass'),
    ('bar.x', 10**4, 
"""\
class Foo(object):
    x = 10
bar = Foo()
"""),

    ('bar.x', 10**4, 
"""\
class Foo(object):
    def __init__(self, x):
        self.x = x
bar = Foo(10)
"""),
    ('bar = d["x"]', 10**4, 'd = {"x": 10}'),
    ('isinstance(bar, list)', 10**4, 
"""\
class Foo(object):
    pass
bar = Foo()
"""),
    ('type(bar) == list', 10**4, 
"""\
class Foo(object):
    pass
bar = Foo()
"""),
    ('loop()', 10, 
"""\
def loop():
    for i in xrange(10**6):
        pass
"""),
    ('try_except()', 10**4, 
"""\
def try_except():
    try:
        raise RuntimeError
    except:
        pass
"""),
    ('threading.Thread(target=worker)', 10**4, 
"""\
def worker():
    pass
"""),
('with context(): pass', 10**4,
"""\
@contextmanager
def context():
    yield
""")
]

if platform.python_implementation() == 'CPython':
    import blist
    import numpy as np

    snippets.extend([
        ('blist.blist()', 10**6, None),
        ('np.array([])', 10**3, None),
        ('np.empty((1,))', 10**3, None),
        ('set(random)', 10, 'random = np.random.random_integers(0, 1000, 10**6)'),
        ('frozenset(random)', 10, 'random = np.random.random_integers(0, 1000, 10**6)'),
        ])

# Utility functions

# Time related functions
def timerep(duration):
    """ Get human readable representation of incoming
    time duration

    Parameters
    ----------
    duration : float
        Time duration in seconds

    Returns
    -------
    value : string
        Human friendly representation

    """
    units = ['s', 'ms', 'us', 'ns']
    if duration > 1:
        power = 1
        unit = units[0]
    else:
        power = -log(duration, 10)
        if 0 < power <= 3:
            power = 3
            unit = units[1]
        elif 3 < power <= 6:
            power = 6
            unit = units[2]
        elif 6 < power <= 9:
            power = 9
            unit = units[3]
    multiplier = 10 ** power
    return '%.2f %s' % (multiplier * duration, unit)

def time_snippet(line, repeat, number, globals, locals, setup='pass'):
    """ Run timing on piece of code passed in. This code is inspired
    by the %timeit code from Ipython. Any errors in it are of my own
    doing.

    Parameters
    ----------
    line : string
        Source code to be timed. Multiline strings are okay.
    repeat : integer
        Number of time the timing should be repeated. 
    number : integer
        Number of loop iterations to run within a timing run.
    globals : dictionary like object
        Object to use as global scope
    locals : dictionary like object
        Object to use as local scope
    setup : string
        Statements to execute to perform any setup before
        before timing run

    Returns
    -------
    value : float
        Amount of time taken by operation in seconds
    """
    timer = timeit.Timer(timer=timeit.default_timer)
    src = timeit.template % {'stmt' : timeit.reindent(line, 4),
    'setup' : timeit.reindent(setup, 4)}
    code = compile(src, "<foo>", "exec")
    exec code in globals, locals
    timer.inner = locals['inner']
    best = min(timer.repeat(repeat, number)) / number
    return best


def run(snippets, repeat=3):
    """ This function kicks off the timing run for incoming snippets

    Parameters
    ----------
    snippets : sequence of sequence
        Each entry is (code_snippet, loop iterations, setup code snippet)
    repeat : integer
        Number of times to repeat the timing run per snippet

    """
    results = []
    for snippet, number, setup in snippets:
        if setup is None:
            setup = 'pass'
        t = time_snippet(snippet, repeat, number, globals(), {}, setup)
        results.append((snippet, setup, t, timerep(t)))
    results = sorted(results, key=lambda x: x[2])
    return results


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print 'Usage: python measure.py output_filename'
    else:
        fname = sys.argv[1]
        results = run(snippets)
        f = open(fname, 'wb')
        pickle.dump(results, f)
        f.close()


