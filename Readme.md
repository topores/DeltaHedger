Delta-Hedger for Bybit Unified Account.

## Usage
```console
export API_KEY='your api key'
export API_SECRET='[your api secret]'
python3 bybit_unified/app.py
```


## Parameters
bybit_unified/config.py:
- THRESHOLDS - a value that is adjusted individually for each coin. If the delta change for a coin exceeds the threshold, the algorithm will place an order to bring the delta back to 0.
- SLEEP_TIME - the duration in seconds for which the algorithm goes to sleep after executing the pipeline that brings delta to 0.