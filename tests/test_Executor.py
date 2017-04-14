import unittest
from ExecutionPlan import ExecutionPlan
from Executor import Executor
import asyncio


class TestExecutor(unittest.TestCase):
    def setUp(self):
        self.tasks_dict_array = [{"dependency": None, "name": "task0"}, {"dependency": "task0", "name": "task1"},
                                 {"dependency": "task1", "name": "task2"}, {"dependency": "task0", "name": "task3"},
                                 {"dependency": None, "name": "task4"}, {"dependency": None, "name": "task5"}]

    def test_simple_execution(self):
        async def print_task(task):
            print("Executing task {}".format(task))
            await asyncio.sleep(0)

        plan = ExecutionPlan().from_dict_array(self.tasks_dict_array)
        print("\nBEFORE EXECUTION\n{}".format(plan))
        Executor(plan, 2, 1.0, print_task).trigger_execution()
        print("\nAFTER EXECUTION\n{}".format(plan))
        self.assertEqual(plan.is_incomplete(), False, "Plan has been marked complete")
        map(lambda x: self.assertIn(x, plan.completed_tasks(), "Task {} has been completed".format(x)), [x for x in range(0, len(plan.plan_as_dict_array))])

    def test_low_granularity_execution(self):
        async def print_task(task):
            print("Executing task {}".format(task))
            await asyncio.sleep(0)

        async def delayed_task(task):
            print("Executing task {}".format(task))
            await asyncio.sleep(0.1)

        plan = ExecutionPlan().from_dict_array(self.tasks_dict_array)
        print("\nBEFORE EXECUTION\n{}".format(plan))
        Executor(plan, 2, 0.01, print_task).trigger_execution()
        print("\nAFTER EXECUTION\n{}".format(plan))
        self.assertEqual(plan.is_incomplete(), False, "Simple plan has been marked complete during low granularity execution")
        map(lambda x: self.assertIn(x, plan.completed_tasks(), "Task {} has been completed".format(x)), [x for x in range(0, len(plan.plan_as_dict_array))])

        plan = ExecutionPlan().from_dict_array(self.tasks_dict_array)
        print("\nBEFORE EXECUTION\n{}".format(plan))
        Executor(plan, 3, 0.01, delayed_task).trigger_execution()
        print("\nAFTER EXECUTION\n{}".format(plan))
        self.assertEqual(plan.is_incomplete(), False, "Long plan has been marked complete during low granularity execution")
        map(lambda x: self.assertIn(x, plan.completed_tasks(), "Task {} has been completed".format(x)),
            [x for x in range(0, len(plan.plan_as_dict_array))])

    def test_delayed_execution(self):
        async def delayed_task(task):
            print("Executing task {}".format(task))
            await asyncio.sleep(0.1)

        plan = ExecutionPlan().from_dict_array(self.tasks_dict_array)
        print("\nBEFORE EXECUTION\n{}".format(plan))
        Executor(plan, 3, 1.0, delayed_task).trigger_execution()
        print("\nAFTER EXECUTION\n{}".format(plan))
        self.assertEqual(plan.is_incomplete(), False, "Plan has been marked complete")
        map(lambda x: self.assertIn(x, plan.completed_tasks(), "Task {} has been completed".format(x)), [x for x in range(0, len(plan.plan_as_dict_array))])

if __name__ == '__main__':
    unittest.main()
