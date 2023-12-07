class SectorDelta():
    def __init__(self, dict_sector: dict):
        self.dict_sector = dict_sector

    def get_data(self, key: str) -> list:
        return self.dict_sector[key]

    def get_sectors(self) -> list:
        return list(self.dict_sector.keys())
