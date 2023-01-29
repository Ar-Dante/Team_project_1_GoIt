from datetime import datetime
from pathlib import Path
import pickle


class ResponsiblePerson:
    """Клас для створення відповідальної особи"""

    def __init__(self, name):
        self.name = name.title()

    def __str__(self):
        return self.name


class Task:
    """Клас для створення завдання"""

    def __init__(self, text: str, person: ResponsiblePerson, deadline):
        self.text = text.capitalize()
        self.person = person

        y, m, d = deadline.split("-")
        self.deadline = datetime(year=int(y), month=int(m), day=int(d))

        self.status = "in process"



    def well_done(self):  # зміна статусу виконання завдання
        self.status = "done"


    def is_in_time(self):
        """функція перевіряє статус виконання на момент визову"""

        today = datetime.now()
        if self.status != "done":
            if today > self.deadline:
                self.status = "FAIL"
            else:
                self.status = "in process"


    def __str__(self):
        self.is_in_time()
        return f"\nDEADLINE: {self.deadline.date()}\n\nTASK: {self.text}\n\nResponsible person: {self.person.name}\nSTATUS:   {self.status}\n=============\n"

   

class TaskList:
    """Клас для створення списку завдань"""
    
    cnt = 0

    def __init__(self):
        self.task_lst = {}


    def add_task(self, task: Task):  # додаємо нове завдання
        TaskList.cnt += 1
        self.task_lst[self.cnt] = task


    def remove_task(self, ID):  # видаляємо завдання по ID
        if int(ID) in self.task_lst:
            self.task_lst.pop(int(ID))


    def show_all_tasks(self):  # виводимо перелік всіх завдань
        result = '\n'
        for k, v in self.task_lst.items():
            s= f"=== ID: {k} ==={v}\n"
            result += s
        return result


    def change_deadline(self, ID, new_deadline):  
        '''змінюємо термін виконання завдання по ID'''

        y, m, d = new_deadline.split("-")
        new_deadline = datetime(year=int(y), month=int(m), day=int(d))

        if int(ID) in self.task_lst:
            self.task_lst[int(ID)].deadline = new_deadline


    def search_task(self, text_to_search):  # шукаємо завдання по тексту
        for task in self.task_lst.values():
            if text_to_search.strip().lower() in task.text.lower():
                print(str(task))


    def search_respons_person(self, responsible_person: str):  
        '''шукаємо всі завдання, за які відповідає/відповідала особа'''

        result = "\n"
        for id, task in self.task_lst.items():
            if responsible_person.title() == task.person.name:
                result += f'{int(id)}\n{task})'
        return result

    def save_to_file(self):
        with open("tasks.bin", "wb") as fh:
            pickle.dump(self.task_lst, fh)



file = Path("tasks.bin")
tasklist = TaskList()

if file.exists():
    with open("tasks.bin", "rb") as f:
        dct = pickle.load(f)
        tasklist.task_lst.update(dct)
        ids = [int(i) for i in tasklist.task_lst]
        if len(ids) > 0:
            tasklist.cnt = max(ids)
        else:
            tasklist.cnt = 0
