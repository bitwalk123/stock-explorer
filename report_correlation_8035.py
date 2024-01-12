import time

from funcs.tide import get_elapsed, get_past_month_day
from report.corr import correlation_1to1
from snippets.set_env import set_env

if __name__ == '__main__':
    dict_info = set_env()
    time_start = time.time()

    start = get_past_month_day(6)
    code_target = '8035'
    file_out = 'pool/corr_8035-%d.pkl'

    correlation_1to1(code_target, start)

    print('elapsed %.3f sec' % get_elapsed(time_start))
