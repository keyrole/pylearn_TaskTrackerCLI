import json
import argparse
from typing import TextIO

STATUS = ('new', 'in-progress', 'done')
PATH = 'tasks.json'
Tasks = list(dict())
ID = 1

def get_parse():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command")
    add_parser = subparsers.add_parser("add", help="Add a new task iterm")
    add_parser.add_argument("-n", "--name", required=True)

    list_parser=subparsers.add_parser("list", help="List all tasks or filter the tasks by status")
    list_parser.add_argument("-s", "--status", choices = ["new", "done", "in-progress", "undone"])

    delete_parser=subparsers.add_parser("delete", help="Delete a task")
    delete_parser.add_argument("-i", "--id", type = int, required=True)

    update_parser=subparsers.add_parser("update", help="Update a task")
    update_parser.add_argument("-i", "--id", type = int, required=True)
    update_parser.add_argument("-s", "--status", choices = ["new", "done", "in-progress"], required=True)

    return parser

def format_print(tasks):
    print(f'\n  {"ID": <5}{"Item": <25}\t{"Status"}\n')
    print(f'  ---------------------------------------------\n')
    for task in tasks:
        print(f'  {task["id"]: <5}{task["name"]: <25}\t{task["status"]}\n')

def main() -> None:
    parser = get_parse()
    args = vars(parser.parse_args())

    try:
        with open(PATH, 'r') as f:
            content = json.load(f)
            if content:
                Tasks = content
            else:
                Tasks = []
    except FileNotFoundError:
        Tasks = []
    except json.JSONDecodeError:
        Tasks = []

    if len(Tasks) != 0:
        ID= max([task['id'] for task in Tasks]) + 1

    if args['command'] == 'add':
        if args['name'] in [task['name'] for task in Tasks]:
            print(f"Error: {args['name']} already exists")
        else:
            Tasks.append({'id':ID, 'name': args['name'], 'status': STATUS[0]})
            with open(PATH, 'w') as f:
                json.dump(Tasks, f)

    elif args['command'] == 'list':
        if not args['status'] :
            format_print(Tasks)

        elif args['status'] == 'undone':
            format_print(filter(lambda x: x['status'] in STATUS[:2], Tasks))
        else :
            format_print(filter(lambda x: x['status'] == args['status'], Tasks))

    elif args['command'] == 'update':
        if args['id'] not in [task['id'] for task in Tasks]:
            print(f"Error: {args['id']} not found")
        else:
            for task in Tasks:
                if task['id'] == args['id']:
                    task['status'] = args['status']
                    break
            with open(PATH, 'w') as f:
                json.dump(Tasks, f)

    elif args['command'] == 'delete':
        if args['id'] not in [task['id'] for task in Tasks]:
            print(f"Error: {args['id']} not found")
        else:
            for i in range(len(Tasks)):
                if args['id'] == Tasks[i]['id']:
                    Tasks.remove(Tasks[i])
                    break
            f: TextIO
            with open(PATH, 'w') as f:
                json.dump(Tasks, f)
    else :
        print("Invalid command")

if __name__ == '__main__':
    main()