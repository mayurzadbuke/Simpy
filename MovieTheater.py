import simpy

env = simpy.Environment()

def car(env):
    while True:
        print('Start parking at %d' % env.now)
        parking_duration = 5
        yield env.timeout(parking_duration)

        print('Start driving %d' %env.now)
        driving_duartion = 2
        yield env.timeout(driving_duartion)

env.process(car(env))

env.run(until= 25)