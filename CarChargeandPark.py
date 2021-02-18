import simpy

env = simpy.Environment()


'''
# This simulation includes class Car, with interruption in process

class Car(object):

    def __init__(self, env):
        self.env = env
        self.action = env.process(self.run())

    def run(self):
        while True:
            print ('Start Parking and Charging at %d' % self.env.now)

            charge_duration = 5
            try:
                yield self.env.process(self.charge(charge_duration))

            except simpy.Interrupt:
                print('Was interrupted. Hope, the battery is full enough ...')


            print("Start Driving at %d" % self.env.now)
            trip_duration = 2
            yield self.env.timeout(trip_duration)

    def charge(self, duration):
        yield self.env.timeout(duration)

def driver(env, car):
        yield env.timeout(3)
        car.action.interrupt()

car = Car(env)
env.process(driver(env, car))
env.run(until= 20)

'''

# This simulation involves resources(battery charging stop bcs) in system.

def car(env, name, bcs, driving_time, charging_duration):
    yield env.timeout(driving_time)

    print('%s arriving at %d' %(name, env.now))
    with bcs.request() as req:
        yield req

        print('%s started charging at %d' % (name, env.now))
        yield env.timeout(charging_duration)
        print('%s leaving bcs at %d' % (name, env.now))


bcs = simpy.Resource(env, capacity=2)
for i in range(4):
    env.process(car(env, 'Car %d' % i, bcs, i*2, 5))

env.run()
