# pylearn_TaskTrackerCLI
A CLI program can be used to track tasks.This a small project for learning and practice python skill. The project source,
https://roadmap.sh/projects/task-tracker

## 使用指南 

```bash
python3 tasks2.py -h
```
>usage: tasks2.py [-h] {add,list,delete,update} ...
>
>positional arguments:
>  {add,list,delete,update}
>    add                 Add a new task iterm
>    list                List all tasks or filter the tasks by status
>    delete              Delete a task
>    update              Update a task
>
>options:
>  -h, --help            show this help message and exit



```bash
python3 tasks2.py add -h
```

>usage: tasks2.py add [-h] -n NAME
>
>options:
>  -h, --help       show this help message and exit
>  -n, --name NAME


```bash
python3 tasks2.py list -h
```

>usage: tasks2.py list [-h] [-s {new,done,in-progress,undone}]
>
>options:
>  -h, --help            show this help message and exit
>  -s, --status {new,done,in-progress,undone}


```bash
python3 tasks2.py delete -h
```

>usage: tasks2.py delete [-h] -i ID
>
>options:
>  -h, --help   show this help message and exit
>  -i, --id ID


```bash
python3 tasks2.py update -h
```

>usage: tasks2.py update [-h] -i ID -s {new,done,in-progress}
>
>options:
>  -h, --help            show this help message and exit
>  -i, --id ID
>  -s, --status {new,done,in-progress}
