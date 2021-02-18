import random
import simpy
import statistics


class Theater:

    def __init__(self, environment, numCashiers, numServers, numUshers):
        self.environment = environment
        self.cashier = simpy.Resource(environment, numCashiers)
        self.server = simpy.Resource(environment, numServers)
        self.usher = simpy.Resource(environment, numUshers)


    def purchaseTicket(self, movieGoer):
        yield self.environment.timeout(random.randint(1, 3))
        print(f"MovieGoer: {movieGoer} finished purchasing ticket at time {self.environment.now}")


    def checkTicket(self, movieGoer):
        yield self.environment.timeout(3/60)
        print(f"MovieGoer: {movieGoer} got their ticket checked at time {self.environment.now}")


    def sellFood(self, movieGoer):
        yield self.environment.timeout(random.randint(1, 5))
        print(f"MovieGoer: {movieGoer} finished buying food at time {self.environment.now}")



def goToMovies(environment, movieGoer, theater, waitTimes):

    arrivalTime = environment.now

    with theater.cashier.request() as request:
        yield request
        yield environment.process(theater.purchaseTicket(movieGoer))

    with theater.usher.request() as request:
        yield request
        yield environment.process(theater.checkTicket(movieGoer))

    if random.choice([True, False]):
        with theater.server.request() as request:
            yield request
            yield environment.process(theater.sellFood(movieGoer))

    waitTimes.append(environment.now - arrivalTime)



def runTheater(environment, numCashiers, numServers, numUshers, waitTimes):

    theater = Theater(environment, numCashiers, numServers, numUshers)

    movieGoer = 0
    for movieGoer in range(3):
        environment.process(goToMovies(environment, movieGoer, theater, waitTimes))

    while True:
        yield environment.timeout(12/60)
        movieGoer += 1
        environment.process(goToMovies(environment, movieGoer, theater, waitTimes))



def getAverageWaitTime(waitTimes):
    averageWait = statistics.mean(waitTimes)
    minutes, fracMinutes = divmod(averageWait, 1)
    seconds = fracMinutes * 60
    return round(minutes), round(seconds)



def getUserInput():
    numCashiers = input("Input num of cashiers working: ")
    numServers = input("Input num of servers working: ")
    numUshers = input("Input num of ushers working: ")

    try:
        params = [int(numCashiers), int(numServers), int(numUshers)]
    except:
        print("Using default values since wrong input provided")
        params = [1, 1, 1]

    return params



def runSimulation():

    random.seed(42)
    waitTimes = []
    numCashiers, numServers, numUshers = getUserInput()
    print("Running simulation...\n")

    environment = simpy.Environment()
    environment.process(runTheater(environment, numCashiers, numServers, numUshers, waitTimes))
    environment.run(until=90)

    minutes, seconds = getAverageWaitTime(waitTimes)
    print(f"\nFinished simulation with average wait time of {minutes} minutes and {seconds} seconds.")



if __name__ == '__main__':

    runSimulation()
