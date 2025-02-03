import unittest
import pandas as pd
import numpy as np

from config import SYMBOL, SECTOR_SYMBOLS, START_DATE, END_DATE, weights, dynamic_metrics
from data_fetcher import fetch_sector_data, fetch_yfinance_data
from metrics_manager import MetricsManager


class TestFinancialApp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """
        setUpClass, tüm testlerden önce **bir kez** çalışır.
        Burada verileri çekip gerekli ön işlemleri yaparak
        testlerde tekrar tekrar kod yazmaktan kaçınabiliriz.
        """
        # 1. Metrics Manager oluştur
        cls.metrics_manager = MetricsManager(dynamic_metrics)

        # 2. Hedef sembolün yfinance verilerini çek
        cls.info, cls.income_df, cls.balance_df, cls.cashflow_df, cls.historical_data = \
            fetch_yfinance_data(SYMBOL, START_DATE, END_DATE)

        # 3. Sektör verilerini çek
        cls.sector_df, cls.sector_means = fetch_sector_data(SECTOR_SYMBOLS, START_DATE, END_DATE)

        # 4. Gelir tablosu datasını temizle ve metric hesaplamaları yap
        cls.income_df = cls.metrics_manager.clean_and_calculate_metrics(
            cls.income_df, cls.balance_df, cls.cashflow_df, cls.info
        )

        # 5. Z-score hesaplaması
        cls.income_df = cls.metrics_manager.calculate_z_scores(cls.income_df)

        # 6. YUDA Skorları hesaplaması
        cls.income_df = cls.metrics_manager.calculate_yuda_scores(
            cls.income_df, weights, cls.sector_means
        )

    def test_info_data_not_empty(self):
        """
        'info' sözlüğünde en azından bazı temel bilgilerin bulunmasını bekliyoruz.
        """
        self.assertTrue(isinstance(self.info, dict), "info bir sözlük olmalı.")
        self.assertGreater(len(self.info), 0, "'info' sözlüğü boş geldi, veri çekilememiş olabilir.")

    def test_dataframes_not_empty(self):
        """
        income, balance, cashflow, historical data gibi DataFrame'lerin boş olup olmadığını test ediyoruz.
        """
        self.assertFalse(self.income_df.empty, "income_df boş geldi.")
        self.assertFalse(self.balance_df.empty, "balance_df boş geldi.")
        self.assertFalse(self.cashflow_df.empty, "cashflow_df boş geldi.")
        self.assertFalse(self.historical_data.empty, "historical_data boş geldi.")

    def test_sector_data_not_empty(self):
        """
        Sektör verilerinin de boş gelmediğini kontrol ediyoruz.
        """
        self.assertFalse(self.sector_df.empty, "sector_df boş geldi.")
        self.assertTrue(isinstance(self.sector_means, dict), "sector_means bir sözlük olmalı.")
        self.assertGreater(len(self.sector_means), 0, "sector_means boş geldi.")

    def test_calculated_metrics_columns_exist(self):
        """
        Dynamic metrics içerisinde tanımlanan metriklerin income_df DataFrame'inde olup olmadığını test edelim.
        Örneğin dynamic_metrics'teki her metrik, income_df kolonları arasında bekleniyor.
        """
        for metric in dynamic_metrics.keys():
            with self.subTest(metric=metric):
                self.assertIn(
                    metric,
                    self.income_df.columns,
                    f"{metric} metriği income_df içinde bulunamadı."
                )

    def test_z_scores_exist(self):
        """
        Z-score'ların hesaplanmış olması bekleniyor.
        Hesaplanan z-score kolonları orijinal metrikin başına 'z_score_' prefix eklenerek oluşturuluyor.
        Örneğin, 'profitMargin' -> 'z_score_profitMargin'.
        """
        for metric in dynamic_metrics.keys():
            z_metric = f"z_score_{metric}"
            with self.subTest(z_metric=z_metric):
                self.assertIn(
                    z_metric,
                    self.income_df.columns,
                    f"{z_metric} kolonu Z-score hesaplamalarından sonra bulunamadı."
                )

    def test_yuda_score_columns(self):
        """
        YUDA skorları sonrası beklenen kolonların existence testini yapıyoruz:
        - enhanced_yuda_score
        - yuda_score_category
        """
        self.assertIn(
            "enhanced_yuda_score",
            self.income_df.columns,
            "YUDA skor hesabından sonra 'enhanced_yuda_score' bulunamadı."
        )
        self.assertIn(
            "yuda_score_category",
            self.income_df.columns,
            "YUDA skor hesabından sonra 'yuda_score_category' bulunamadı."
        )

    def test_yuda_score_values(self):
        """
        En son satırda YUDA skorunun mantıklı bir değer olup olmadığını test etmek için
        basit bir aralık kontrolü yapabilirsiniz.
        Örneğin, 'enhanced_yuda_score' -10 ile 10 arasında olmalıdır gibi bir varsayım.
        (Aralıklar kendi model mantığınıza göre değişebilir)
        """
        last_yuda_score = self.income_df["enhanced_yuda_score"].iloc[-1]
        self.assertTrue(
            -10 <= last_yuda_score <= 10,
            f"Beklenen aralığın dışında bir YUDA skoru tespit edildi: {last_yuda_score}"
        )

    def test_category_exists(self):
        """
        YUDA skoruna karşılık gelen bir kategorinin oluştuğundan emin olalım.
        """
        last_category = self.income_df["yuda_score_category"].iloc[-1]
        valid_categories = ["Good", "Ok", "Risky", "Very Risky", "N/A"]
        self.assertIn(
            last_category,
            valid_categories,
            f"Beklenmeyen bir YUDA skor kategorisi tespit edildi: {last_category}"
        )

    # İsterseniz ek testler de yapabilirsiniz:
    # - Tarih index kontrolü
    # - Null/NaN değer var mı yok mu
    # - Plot fonksiyonunu test etmek için fig nesnesini döndürüyorsanız orada basit kontrol vb.


if __name__ == '__main__':
    unittest.main()
