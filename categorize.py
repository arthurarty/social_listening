import time

from app.llms.categorize_tweet import main

SLEEP_TIMER = 10
TOTAL_BATCHES = 10

for i in range(TOTAL_BATCHES):
    print(f"Handling bunch {i+1} of {TOTAL_BATCHES}")
    main(skip=0, no_of_tweets=5)
    print(f"Sleeping for {SLEEP_TIMER} seconds before next bunch")
    time.sleep(SLEEP_TIMER)
