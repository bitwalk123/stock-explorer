from functions.diff_close import diff_close_by_sector
from functions.get_latest_2dates import get_latest_2dates

if __name__ == '__main__':
    pair_date = get_latest_2dates()
    print(pair_date)
    sector_delta = diff_close_by_sector(pair_date)
    for sector in sector_delta.get_sectors():
        # print(sector, sector_delta.get_dist_raw(sector))
        print(sector, sector_delta.get_dist_standardize(sector))
