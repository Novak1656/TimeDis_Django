from calendar import HTMLCalendar

from django.db.models import Q
from django.urls import reverse
from tasks_app.models import Tasks


class Calendar(HTMLCalendar):
    def __init__(self, year=None, month=None, user=None):
        self.year = year
        self.month = month
        self.user = user
        super(Calendar, self).__init__()

    def formatday(self, day, tasks):
        if day in tasks.keys():
            days_tasks = ''.join(
                f'<li> <a href="{reverse("task", kwargs={"slug": task.slug})}">{task.title}</a> </li>'
                for task in tasks.get(day)
            )
        else:
            days_tasks = 'День свободен'
        if day != 0:
            return f"<td><span class='date'>{day}</span><hr><ul> {days_tasks}</ul></td>"
        return '<td></td>'

    def formatweek(self, theweek, tasks):
        week = ''.join(self.formatday(d, tasks) for d, _ in theweek)
        return f'<tr> {week} </tr>'

    def formatmonth(self, withyear=True):
        tasks = Tasks.objects.filter(Q(deadline__year=self.year) & Q(deadline__month=self.month), user=self.user)
        print(tasks)
        days_with_tasks = {task.deadline.day: list() for task in tasks}

        for task in tasks:
            days_with_tasks[task.deadline.day].append(task)
        print(days_with_tasks)

        cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
        cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
        cal += f'{self.formatweekheader()}\n'
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f'{self.formatweek(week, days_with_tasks)}\n'
        return cal
