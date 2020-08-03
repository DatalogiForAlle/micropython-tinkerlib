import uasyncio


# Small event system built on top of asyncio
class Tasks():
    tasks = set()


def execute(coroutine):
    """ Execute a coroutine immediately """
    loop = uasyncio.get_event_loop()
    Tasks.tasks.add(coroutine)
    loop.create_task(coroutine)


def repeat_every(f, waittime=1):
    """
    Repeat everytime a certain amount of seconds have passed as given
    by the variable waittime. Defaults to repeating every second.

    """
    async def repeater(f, waittime):
        while True:
            f()
            await uasyncio.sleep(waittime)
    execute(repeater(f, waittime))


def repeat(f, frequency=60):
    repeat_every(f, waittime=1/frequency)


def schedule(f, delay=0):
    # Wrap task to allow us to delay it
    async def delayed_execute():
        await uasyncio.sleep_ms(delay)
        f()
    execute(delayed_execute())


def initialize():
    # Shutdown existing tasks
    for task in Tasks.tasks:
        task.close()
        Tasks.tasks.remove(task)


def run():
    try:
        loop = uasyncio.get_event_loop()
        loop.run_forever()
    except KeyboardInterrupt:
        initialize()
