class SectorManager:
    def __init__(self, sector_symbols):
        self.sector_symbols = sector_symbols

    def add_symbol(self, symbol):
        if symbol not in self.sector_symbols:
            self.sector_symbols.append(symbol)

    def remove_symbol(self, symbol):
        if symbol in self.sector_symbols:
            self.sector_symbols.remove(symbol)
