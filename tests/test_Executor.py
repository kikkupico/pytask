import unittest
from ExecutionPlan import ExecutionPlan
from Executor import Executor


class TestExecutor(unittest.TestCase):
    def setUp(self):
        self.tasks_dict_array = [{"dependency": None, "name": "task0"}, {"dependency": "task0", "name": "task1"},
                                 {"dependency": "task1", "name": "task2"}, {"dependency": "task0", "name": "task3"},
                                 {"dependency": None, "name": "task4"}]

    def test_simple_execution(self):
        def print_task(task):
            print("Executing task {}".format(task))

        plan = ExecutionPlan().from_dict_array(self.tasks_dict_array)
        print("\nBefore execution\n{}".format(plan))
        Executor(plan, 2, 1.0, print_task).execute()
        print("\nAfter execution\n{}".format(plan))
        self.assertEqual(plan.is_incomplete(), False, "Plan has been marked complete")
        map(lambda x: self.assertIn(x, plan.completed_tasks(), "Task {} has been completed".format(x)), [x for x in range(0, len(plan.plan_as_dict_array))])

if __name__ == '__main__':
    unittest.main()
