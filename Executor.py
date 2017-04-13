import asyncio
from ExecutionPlan import ExecutionPlan


class Executor:
    def __init__(self, execution_plan, max_concurrency, granularity, execution_function):
        self.execution_plan = execution_plan
        self.max_concurrency = max_concurrency
        self.granularity = granularity
        self.popped_list = []
        self.loop = asyncio.get_event_loop()
        self.queue = asyncio.Queue(loop=self.loop, maxsize=max_concurrency)
        self.execution_function = execution_function

    async def pop_one(self):
        while self.execution_plan.is_incomplete():
            poppable_list = [x for x in self.execution_plan.ready_tasks() if x not in self.popped_list]
            if len(poppable_list) > 0:
                popped_task = poppable_list[0]
                self.popped_list.append(popped_task)
                return popped_task
            else:
                await asyncio.sleep(self.granularity)

        return None

    async def produce(self):
        while self.execution_plan.is_incomplete():
            doable_task = await self.pop_one()
            await self.queue.put(doable_task)
            #print("Enqueued task {0}; Queue {1}".format(doable_task, self.queue._queue))

        # indicate the producer is done
        await self.queue.put(None)

    async def consume(self):
        while True:
            # wait for an item from the producer
            task = await self.queue.get()
            if task is None:
                # the producer emits None to indicate that it is done
                break

            else:
                self.execution_function(task)
                self.execution_plan.complete(task)

    def execute(self):
        producer_coro = self.produce()
        consumer_coro = self.consume()
        self.loop.run_until_complete(asyncio.gather(producer_coro, consumer_coro))
        self.loop.close()
