from dotenv import load_dotenv
load_dotenv()

import sys
import os
import time
import schedule
from backend.data_getter import sync
from backend.prediction import predict

def main():
    print("Executing update...")
    sync()
    predict()


if __name__ == '__main__':

    schedule.every(2).hours.do(main)

    main()
    while True:
        schedule.run_pending()
        time.sleep(1)