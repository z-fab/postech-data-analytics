from dotenv import load_dotenv
load_dotenv()

import sys
import os
from backend.data_getter import sync
from backend.prediction import predict

if __name__ == '__main__':
    sync()
    predict()