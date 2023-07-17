# Research on the effectiveness of machine learning algorithms for asset management in the cryptocurrency market, taking users' trust ratings towards cryptocurrencies into consideration.

To conduct this research, a database and Python application to load per-minute candlestick data were developed and then hosted on a remote server, to collect data from cryptocurrency exchange. 

The data was then processed, and key points were identified where it was recommended to close short and open long positions (local minima) or close long and open short positions (local maxima).

Three neural network models were developed for prediction and decision-making: Long Short-Term Memory (LSTM), a one-dimensional Convolutional Neural Network (1D-CNN), and an ensemble model combining both LSTM and 1D-CNN. 

A time-series train-test split and cross-validation methodology were implemented to ensure reliable performance assessment. 

An automatic hyperparameter search was also conducted to optimize the models' configuration. 

The research also involved the development of a target column and custom metrics tailored to the specific task of asset management in the cryptocurrency market. These metrics were designed to evaluate the performance of the models in terms of profitability and risk management. 

This research provides insights into the effectiveness of machine learning algorithms for asset management in the cryptocurrency market, considering users' trust ratings towards cryptocurrencies.
