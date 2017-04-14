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
        self.executors = 0

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

    async def execute_task(self, task_id):
        self.executors += 1
        await asyncio.ensure_future(self.execution_function(task_id))
        self.execution_plan.complete(task_id)
        self.executors -= 1

    async def execute(self):
        while self.execution_plan.is_incomplete():
            if self.executors < self.max_concurrency:
                task_id = await self.pop_one()
                print("Popped task {}".format(task_id))
                asyncio.ensure_future(self.execute_task(task_id))
            else:
                await asyncio.sleep(self.granularity)

    def trigger_execution(self):
        self.loop.run_until_complete(asyncio.gather(self.execute()))
        self.loop.close()

