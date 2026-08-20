import time

from app.agent_workflows.topic_modeling import main

SLEEP_TIMER = 2
TOTAL_BATCHES = 3

for i in range(TOTAL_BATCHES):
    print(f"Handling bunch {i+1} of {TOTAL_BATCHES}")
    tweet_processed = main(skip=0, no_of_tweets=5)
    if tweet_processed == 0:
        print("Breaking since no tweets were processed")
        break
    print(f"Sleeping for {SLEEP_TIMER} seconds before next bunch")
    time.sleep(SLEEP_TIMER)
