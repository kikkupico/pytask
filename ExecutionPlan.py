class ExecutionPlan(object):

    def __init__(self):
        self.plan_as_dict_array = []
        self.completed_list = []

    def is_incomplete(self):
        return len(self.plan_as_dict_array) != len(self.completed_list)

    def __validate_task_presence(self, t):
        if t in self.plan_as_dict_array:
            return True
        else:
            raise LookupError("Task {0} not found in execution plan".format(t))

    def is_task_complete(self, index):
        return index in self.completed_list

    def is_ready(self, index=None, name=None):
        task = None
        if index is not None:
            task = self.plan_as_dict_array[index]
        elif name is not None:
            task = [x for x in self.plan_as_dict_array if x['name'] == name][0]
            index = self.plan_as_dict_array.index(task)

        if self.plan_as_dict_array.index(task) in self.completed_tasks():
            return False
        if task['dependency'] is None:
            is_dependency_complete = True
        else:
            is_dependency_complete = self.is_task_complete(index=[i for i in range(0, len(self.plan_as_dict_array)) if self.plan_as_dict_array[i]['name'] == task['dependency']][0])
        return is_dependency_complete and not self.is_task_complete(index=index)

    def ready_tasks(self):
        return [i for i in range(0, len(self.plan_as_dict_array)) if self.is_ready(index=i)]

    def completed_tasks(self):
        return [self.plan_as_dict_array[i] for i in self.completed_list]

    def complete(self, index):
        if self.is_ready(index=index):
            t = self.plan_as_dict_array[index]
            loc = self.plan_as_dict_array.index(t)
            self.completed_list.append(loc)
            print("{} completed".format(t['name']))
        else:
            raise ValueError("Task is not ready for completion")

    def from_dict_array(self, d):
        self.plan_as_dict_array = [x.copy() for x in d]  # create a copy of dict array
        return self

    def __get_dependants(self, i):
        return [self.plan_as_dict_array.index(j) for j in self.plan_as_dict_array if
                j['dependency'] == self.plan_as_dict_array[i]['name']]

    def __str__(self):
        def stringify_item_with_dependencies(i, visited_list, indent_level, accum):
            if i in visited_list:
                return accum
            else:
                visited_list.append(i)
                indentation = "".join(["\t" for x in range(0, indent_level)])
                readiness = ""
                completion = ""
                if self.is_ready(index=i):
                    readiness = " Ready "
                if self.is_task_complete(index=i):
                    completion = " Completed "
                str_this_item = indentation + self.plan_as_dict_array[i]['name'] + readiness + completion + "\n"
                str_dependents = "".join([stringify_item_with_dependencies(j, visited_list, indent_level + 1, accum) for j in self.__get_dependants(i)])
                return accum + str_this_item + str_dependents

        visited_list = []  # passing visited list in param as lists are passed by reference in python; TODO: refactor and find a better way
        return "".join([stringify_item_with_dependencies(i, visited_list, 0, "") for i in range(0, len(self.plan_as_dict_array))])
