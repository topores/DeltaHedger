class BaseConnector():
    valid=True

    def get_balance(self) -> float:
        '''

        :return: free balance + position value, aka wallet value
        '''
        raise NotImplementedError()

    def get_max_leverage(self,ticker) -> float:
        '''

        :return: max leverage
        '''
        raise NotImplementedError()

    def get_positions(self) -> dict:
        '''

        :return: a dict of current positions, key=ticker(ex: BTCUSDT),value=base_amount (ex: 0.00001)
        '''
        raise NotImplementedError()

    def market(self,ticker,size) -> dict:
        '''
        :param
        ticker ex: BTCUSDT
        size - amount of position in base, could be positive or negative

        executes a market order

        :return: result of execution
        '''
        raise NotImplementedError()

    def get_rounded_size(self,ticker,size) -> float:
        '''
        :param
        ticker ex: BTCUSDT
        size - amount of position in base, could be positive or negative

        :return: rounded size
        '''
        raise NotImplementedError()
