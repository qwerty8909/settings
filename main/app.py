import asyncio
from datetime import datetime


async def print_number(task_name):
    print(f">>> Start {task_name}")
    for _ in range(10):
        print(42)
        await asyncio.sleep(0.5)
    print(f"<<< End {task_name}")


async def print_text(task_name):
    print(f">>> Start {task_name}")
    for _ in range(10):
        print("hello")
        await asyncio.sleep(0.9)
    print(f"<<< End {task_name}")

async def main():
    print(f'Start {datetime.now()}')
    task1 = asyncio.create_task(print_number('task1'))
    task2 = asyncio.create_task(print_text('task2'))
    await task1
    await task2
    print(f'End {datetime.now()}')




asyncio.run(main())


'''
Декораторы для сопрограмм в целом создаются так же, как и декораторы для обычных функций. 
Основное отличие в том, что если декоратор должен подменять функцию (это делается в большинстве декораторов функций), 
надо чтобы декоратор подменял сопрограмму сопрограммой.
Пример декоратора timecode, который замеряет время выполнения сопрограммы:

from functools import wraps

def timecode(function):
    @wraps(function)
    async def wrapper(*args, **kwargs):                                     !!! async
        start_time = datetime.now()
        result = await function(*args, **kwargs)                            !!! await
        print(">>> Функция выполнялась:", datetime.now() - start_time)
        return result
    return wrapper
     
@timecode
async def send_show(device, command):
'''