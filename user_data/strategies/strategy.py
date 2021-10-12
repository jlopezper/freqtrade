from freqtrade.strategy import IStrategy, merge_informative_pair
from pandas import DataFrame
import talib.abstract as ta
import freqtrade.vendor.qtpylib.indicators as qtpylib
import numpy  # noqa


class MMStrategy(IStrategy):

    # Minimal ROI designed for the strategy.
    minimal_roi = {"0":0.1}

    # This attribute will be overridden if the config file contains "stoploss"
    stoploss = -0.1

    # Optimal timeframe for the strategy
    timeframe = '1h'

    # trailing stoploss
    trailing_stop = True

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:

        dataframe['ema250'] = ta.EMA(dataframe, timeperiod=250)
        dataframe['ema2500'] = ta.EMA(dataframe, timeperiod=2500)

        return dataframe

    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:

        dataframe.loc[
            (
                # Close price crossed above EMA
                (qtpylib.crossed_above(dataframe['ema250'], dataframe['ema2500'])) 
            ),
            'buy'] = 1
        return dataframe

    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        
        return dataframe