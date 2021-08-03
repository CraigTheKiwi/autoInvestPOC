import io
import unittest
from datetime import datetime, timezone
from invest import invest

class TestLoadBTC(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        invest.testing = False
        cls.succeedingFile = "invest/settings.txt"
        cls.fake_file = io.StringIO('foo:nbar')
        cls.failingFile = "invest/failing.txt"
    def test_IO_exception(self):
        self.assertEqual(invest.loadCoins(self.failingFile), ["IOError"])
    def test_count_coins(self):
        self.assertEqual(len(invest.loadCoins(self.succeedingFile)), 3)
    def test_load_btc(self):
        coins = invest.loadCoins(self.succeedingFile)
        self.assertEqual(coins[0]["ticker"], "BTC")
    def test_load_eth(self):
        coins = invest.loadCoins(self.succeedingFile)
        self.assertEqual(coins[1]["ticker"], "ETH")
    def test_load_doge(self):
        coins = invest.loadCoins(self.succeedingFile)
        self.assertEqual(coins[2]["ticker"], "DOGE")
    def test_if_3_items_per_row(self):
        self.assertEqual(invest.loadCoins(cls.fake_file), "test")

class TestPot(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        succeedingFile = "invest/settings.txt"
        cls.coins = invest.loadCoins(succeedingFile)
    def test_failed_file(self):
        self.assertEqual(invest.loadPot(self.coins , ""), ["IOError"])
        pass

class TestCoins(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        invest.testing = False
        succeedingFile = "invest/settings.txt"
        coins = invest.loadCoins(succeedingFile)
        pot = "test/mock_pot.txt"
        cls.loaded_coins = invest.loadPot(coins, pot)
    def test_coins_array_length(self):
        self.assertEqual(len(self.loaded_coins), 3)
    def test_single_coin_array_size(self):
        self.assertEqual(len(self.loaded_coins[0]), 6)
    def test_btc_ticker(self):
        self.assertEqual(self.loaded_coins[0]["ticker"], "BTC")
    def test_btc_purchase_price(self):
        #self.assertEqual(self.loaded_coins[0]["ma7"], 123.45)
        pass
    def test_btc_active_set(self):
        #self.assertEqual(self.loaded_coins[0]["ma7"], 123.45)
        pass
    def test_btc_ma7(self):
        self.assertEqual(self.loaded_coins[0]["MA7"], 123.45)
    def test_btc_ma21(self):
        self.assertEqual(self.loaded_coins[0]["MA21"], 234.56)
    def test_eth_ticker(self):
        self.assertEqual(self.loaded_coins[1]["ticker"], "ETH")
    def test_eth_ma7(self):
        self.assertEqual(self.loaded_coins[1]["MA7"],345.67)
    def test_doge_ticker(self):
        self.assertEqual(self.loaded_coins[2]["ticker"], "DOGE")
    def test_doge_ma7(self):
        self.assertEqual(self.loaded_coins[2]["MA7"], 567.89)

class TestTradeDecisions(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        invest.testing = False
    def test_trade_decision_sell(self):
        self.assertEqual(invest.makeTradeDecision(3,2), False)
    def test_trade_decision_buy(self):
        self.assertEqual(invest.makeTradeDecision(1,2), True)

class TestBinanceAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        invest.testing = False
        succeedingFile = "invest/settings.txt"
        cls.coins = invest.loadCoins(succeedingFile)
        cls.api_key = invest.api_key
        cls.api_secret= invest.api_secret
        cls.current_time = datetime.now(timezone.utc).strftime("%Y/%m/%d")  # UTC date YYYY/MM/DD
    def test_binance_api_data_length(self):
        data = invest.checkBinance("BTC", self.current_time, self.api_key, self.api_secret, invest.base_coin)
        self.assertEqual(len(data[0]), 12)

    def test_binance_api_btc_close_price_isString(self):
        data = invest.checkBinance("BTC", self.current_time, self.api_key, self.api_secret, invest.base_coin)
        self.assertEqual(type(data[0][4]), str)

class TestMovingAverages(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        invest.testing = False
        mock_api_data = [[1627372800000, '0.20034000', '0.20060000', '0.19894000', '0.20057000', '11688175.50000000', 1627387199999, '2338447.98132000', 3733, '5557009.60000000', '1111911.67024400', '0']]
        cls.ma7, cls.ma21 = invest.getMovingAverages(mock_api_data, "BTC")
    def test_moving_averages_7(self):
        self.assertTrue(type(self.ma7) is float)
    def test_moving_averages_21(self):
        self.assertTrue(type(self.ma21) is float)

if __name__ == '__main__':
    unittest.main()
