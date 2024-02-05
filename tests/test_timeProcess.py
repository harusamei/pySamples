import unittest
from datetime import datetime, timedelta
from timeProcess import DateTimeProc

class DateTimeProcTests(unittest.TestCase):

    def setUp(self):
        self.dt_proc = DateTimeProc()

    def test_parseDateTime_en_US(self):
        # Test parsing English date and time in different formats
        dt_str = "2022-01-01"
        expected = datetime(2022, 1, 1)
        result = self.dt_proc.parseDateTime(dt_str, curLocal='en_US')
        self.assertEqual(result, expected)

        dt_str = "Jan 1 2022"
        expected = datetime(2022, 1, 1)
        result = self.dt_proc.parseDateTime(dt_str, curLocal='en_US')
        self.assertEqual(result, expected)

        dt_str = "2022.01.01"
        expected = datetime(2022, 1, 1)
        result = self.dt_proc.parseDateTime(dt_str, curLocal='en_US')
        self.assertEqual(result, expected)

        # Add more test cases for different English date and time formats

    def test_parseDateTime_zh_CN(self):
        # Test parsing Chinese date and time in different formats
        dt_str = "2022年1月1日"
        expected = datetime(2022, 1, 1)
        result = self.dt_proc.parseDateTime(dt_str, curLocal='zh_CN')
        self.assertEqual(result, expected)

        dt_str = "2022年1月1日下午2点差5分"
        expected = datetime(2022, 1, 1, 14, 0) - timedelta(minutes=5)
        result = self.dt_proc.parseDateTime(dt_str, curLocal='zh_CN')
        self.assertEqual(result, expected)

        # Add more test cases for different Chinese date and time formats

    def test_outFormatDate(self):
        # Test formatting datetime object to string representation
        dt = datetime(2022, 1, 1, 14, 30)
        expected = "2022-01-01 14:30:00"
        result = self.dt_proc.outFormatDate(dt)
        self.assertEqual(result, expected)

        dt = datetime(2022, 1, 1, 14, 30)
        expected = "2022年01月01日 14时30分00秒"
        result = self.dt_proc.outFormatDate(dt, fmt="%Y年%m月%d日 %H时%M分%S秒")
        self.assertEqual(result, expected)

        # Add more test cases for different date and time formats

if __name__ == '__main__':
    unittest.main()