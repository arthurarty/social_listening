import time

from app.llms.sentiment import main

SLEEP_TIMER = 5
TOTAL_BATCHES = 10


for i in range(TOTAL_BATCHES):
    print(f"Handling bunch {i+1} of {TOTAL_BATCHES}")
    tweet_processed = main(skip=0, no_of_tweets=5)
    if tweet_processed == 0:
        print("Breaking since no tweets were processed")
        break
    print(f"Sleeping for {SLEEP_TIMER} seconds before next bunch")
    time.sleep(SLEEP_TIMER)
