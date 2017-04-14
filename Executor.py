import asyncio


class Executor:
    def __init__(self, execution_plan, max_concurrency, granularity, execution_coroutine):
        self.execution_plan = execution_plan
        self.max_concurrency = max_concurrency
        self.granularity = granularity
        self.loop = asyncio.get_event_loop()
        self.queue = asyncio.Queue(loop=self.loop, maxsize=max_concurrency)
        self.execution_coroutine = execution_coroutine
        self.executors = 0

    async def get_one_ready_task(self):
        #print("func:get_one_ready_task")
        while self.execution_plan.is_incomplete():
            t = self.execution_plan.ready_tasks()
            if len(t) > 0:
                return t[0]
            else:
                await asyncio.sleep(self.granularity)

        return None

    async def execute_task(self, task_id):
        #print("func:execute_task")
        self.executors += 1
        self.execution_plan.mark_started(task_id)
        await self.execution_coroutine(task_id)
        self.execution_plan.mark_completed(task_id)
        self.executors -= 1

    async def execute(self):
        #print("func:execute")
        while self.execution_plan.is_incomplete():
            if self.executors < self.max_concurrency:
                task_id = await self.get_one_ready_task()
                if task_id is not None:
                    asyncio.ensure_future(self.execute_task(task_id))
                print(self.execution_plan)
                await asyncio.sleep(self.granularity)
            else:
                await asyncio.sleep(self.granularity)

    def trigger_execution(self):
        self.loop.run_until_complete(asyncio.gather(self.execute()))
        self.loop.close()
