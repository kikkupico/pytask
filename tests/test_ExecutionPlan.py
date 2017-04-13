import unittest
from ExecutionPlan import ExecutionPlan

# TEST NOTES
# Completing third ready task fails


class TestExecutionPlan(unittest.TestCase):
    def setUp(self):
        self.tasks_dict_array = [{"dependency": None, "name": "task0"}, {"dependency": "task0", "name": "task1"},
                                 {"dependency": "task1", "name": "task2"}, {"dependency": "task0", "name": "task3"},
                                 {"dependency": None, "name": "task4"}]

    @unittest.skip("skipping for now")
    def test___str__(self):
        execution_plan = ExecutionPlan().from_dict_array(self.tasks_dict_array)
        print("Printing plan...\n" + str(execution_plan))

    @unittest.skip("not implemented")
    def test_complete(self):
        # execution_plan = ExecutionPlan()
        # self.assertEqual(expected, execution_plan.complete(t))
        assert False # TODO: implement your test here

    @unittest.skip("not implemented")
    def test_completed_tasks(self):
        # execution_plan = ExecutionPlan()
        # self.assertEqual(expected, execution_plan.completed_tasks())
        assert False # TODO: implement your test here

    @unittest.skip("not implemented")
    def test_from_dict_array(self):
        # execution_plan = ExecutionPlan()
        # self.assertEqual(expected, execution_plan.from_dict_array(d))
        assert False # TODO: implement your test here

    @unittest.skip("not implemented")
    def test_get_dependants(self):
        # execution_plan = ExecutionPlan()
        # self.assertEqual(expected, execution_plan.get_dependants(i))
        assert False # TODO: implement your test here

    @unittest.skip("not implemented")
    def test_is_incomplete(self):
        # execution_plan = ExecutionPlan()
        # self.assertEqual(expected, execution_plan.is_incomplete())
        assert False # TODO: implement your test here

    @unittest.skip("skipping for now")
    def test_is_ready(self):
        execution_plan = ExecutionPlan().from_dict_array(self.tasks_dict_array)
        self.assertEqual(execution_plan.is_ready(index=0), True, "First task is ready")
        self.assertEqual(execution_plan.is_ready(index=1), False, "Second task is not ready")

    @unittest.skip("not implemented")
    def test_is_task_complete(self):
        # execution_plan = ExecutionPlan()
        # self.assertEqual(expected, execution_plan.is_task_complete(t))
        assert False # TODO: implement your test here

    @unittest.skip("not implemented")
    def test_pop_one(self):
        # execution_plan = ExecutionPlan()
        # self.assertEqual(expected, execution_plan.pop_one())
        assert False # TODO: implement your test here

    @unittest.skip("not implemented")
    def test_ready_tasks(self):
        # execution_plan = ExecutionPlan()
        # self.assertEqual(expected, execution_plan.ready_tasks())
        assert False # TODO: implement your test here

    def test_ready_tasks_simple(self):
        e = ExecutionPlan().from_dict_array(self.tasks_dict_array)
        print("Simple ready test plan \n" + str(e))
        print(e.ready_tasks())
        e.complete(e.ready_tasks()[0])
        print(e.ready_tasks())
        e.complete(e.ready_tasks()[0])

        self.assertEqual(len(e.ready_tasks()), 3, "ready tasks simple case")

    def test_ready_tasks_two_plans(self):
        e1 = ExecutionPlan().from_dict_array(self.tasks_dict_array)
        e2 = ExecutionPlan().from_dict_array(self.tasks_dict_array)
        print("Twin ready test plan\n" + str(e1) + "\n" + str(e2))
        print(e1.ready_tasks())
        e1.complete(e1.ready_tasks()[0])
        print(e1.ready_tasks())
        e1.complete(e1.ready_tasks()[0])

        self.assertEqual(len(e1.ready_tasks()), 3, "ready tasks plan 1(modified)")
        self.assertEqual(len(e2.ready_tasks()), 2, "ready tasks plan 2 (unmodified)")

    def test_ready_tasks_till_empty(self):
        e = ExecutionPlan().from_dict_array(self.tasks_dict_array)
        print("Till empty ready test plan\n" + str(e))
        print(e.ready_tasks())
        e.complete(e.ready_tasks()[0])
        print(e.ready_tasks())
        e.complete(e.ready_tasks()[0])
        print(e.ready_tasks())
        e.complete(e.ready_tasks()[0])
        print(e.ready_tasks())
        e.complete(e.ready_tasks()[0])
        print(e.ready_tasks())
        e.complete(e.ready_tasks()[0])

        self.assertEqual(len(e.ready_tasks()), 0, "ready tasks till empty")

    @unittest.skip("not implemented")
    def test_validate_task_presence(self):
        # execution_plan = ExecutionPlan()
        # self.assertEqual(expected, execution_plan.validate_task_presence(t))
        assert False # TODO: implement your test here

if __name__ == '__main__':
    unittest.main()
