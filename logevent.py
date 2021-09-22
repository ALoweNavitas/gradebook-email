from datetime import datetime
import time

def main():
    pass

if __name__ == '__main__':
    main()

date = datetime.now()
d = date.strftime('%d %m %Y')
t = date.strftime('%H:%M:%S')
start_time = time.time()

class logEvent:
    def __init__(self):
        self.self = self

    def successLog():
        file = open('log.txt', 'a') # Creates a log file with the given string
        elapsed = time.time() - start_time # Determines how long the script takes to run
        file.write('%s : Script took %s seconds to finish and completed at %s' % (d, round(elapsed, 2), t) + '\n')
        return print ("Script ran successfully!")
    
    def failLog(error):
        file = open('log.txt', 'a')
        elapsed = time.time() - start_time
        file.write('%s : Script failed after %s seconds at %s due to %s' % (d, round(elapsed, 2),t, error) + '\n')
        return print("Something went wrong. Check the log.")