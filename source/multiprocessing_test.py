
from __future__ import absolute_import
from __future__ import print_function

from multiprocessing import Pool
import os.path


def file_size(location):
    from time import sleep
    sleep(1/20.)
    return os.path.getsize(location)


def iter_files(directory):
    for top, _dirs, files in os.walk(directory):
        for f in files:
            yield os.path.join(top, f)


def compute_size(directory, processes):
    """
    Given a list of file location, compute the total size of these files using
    multtiprocessing.
    """
    pool = Pool(processes=processes)
    results = []
    for location in iter_files(directory):
        results.append(pool.apply_async(file_size, args=(location,)))
    pool.close()
    pool.join()

    total_size = 0
    for result in results:
        assert result.ready()
        assert result.successful()
        total_size += result.get()
    print('The total size is:', total_size)


if __name__ == '__main__':
    import sys
    directory = sys.argv[1]
    processes = sys.argv[2]
    compute_size(directory, int(processes))
