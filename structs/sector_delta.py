class SectorDelta():
    def __init__(self, dict_sector_dist: dict, dict_sector_price: dict):
        self.dict_sector_dist = dict_sector_dist
        self.dict_sector_price = dict_sector_price

    def get_dist_raw(self, key: str) -> list:
        return self.dict_sector_dist[key]

    def get_dist_standardize(self, key: str) -> list:
        list_standardized = list()
        for pair_close in self.dict_sector_price[key]:
            diff2 = (pair_close[1] - pair_close[0]) * 2
            denominator = pair_close[0] + pair_close[1]
            list_standardized.append(diff2 / denominator * 100)
        return list_standardized


    def get_sectors(self) -> list:
        return list(self.dict_sector_dist.keys())
