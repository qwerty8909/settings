# Как создать и запустить поток
import random
import time
from collections import defaultdict
from threading import Thread

FISH = (None, 'плотва', 'окунь', 'лещ')


# проверка скорости однопоточного и многопоточного режима

class Fisher(Thread):

    def __init__(self, name, worms, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = name
        self.worms = worms
        self.catch = defaultdict(int)

    def run(self):
        self.catch = defaultdict(int)
        for worm in range(self.worms):
            _ = worm ** 10000  # фиксируем время ожидания поклевки
            fish = random.choice(FISH)
            if fish is not None:
                self.catch[fish] += 1


def time_track(func):
    def surrogate(*args, **kwargs):
        started_at = time.time()

        result = func(*args, **kwargs)

        ended_at = time.time()
        elapsed = round(ended_at - started_at, 6)
        print(f'Функция {func.__name__} работала {elapsed} секунд(ы)',)
        return result
    return surrogate


@time_track
def run_in_one_thread(fishers):
    for fisher in fishers:
        fisher.run()


@time_track
def run_in_threads(fishers):
    for fisher in fishers:
        fisher.start()
    for fisher in fishers:
        fisher.join()


humans = ['Васек', 'Колян', 'Петрович', 'Хмурый', 'Клава', ]
fishers = [Fisher(name=name, worms=100) for name in humans]

run_in_one_thread(fishers)
run_in_threads(fishers)


# здесь ускоряем многопоточный режим

class Fisher(Thread):

    def __init__(self, name, worms, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = name
        self.worms = worms
        self.catch = defaultdict(int)

    def run(self):
        self.catch = defaultdict(int)
        for worm in range(self.worms):
            time.sleep(0.01)  # TODO тут вызов системной функции
            fish = random.choice(FISH)
            if fish is not None:
                self.catch[fish] += 1


def time_track(func):
    def surrogate(*args, **kwargs):
        started_at = time.time()

        result = func(*args, **kwargs)

        ended_at = time.time()
        elapsed = round(ended_at - started_at, 6)
        print(f'Функция {func.__name__} работала {elapsed} секунд(ы)',)
        return result
    return surrogate


@time_track
def run_in_one_thread(fishers):
    for fisher in fishers:
        fisher.run()


@time_track
def run_in_threads(fishers):
    for fisher in fishers:
        fisher.start()
    for fisher in fishers:
        fisher.join()


humans = ['Васек', 'Колян', 'Петрович', 'Хмурый', 'Клава', ]
fishers = [Fisher(name=name, worms=100) for name in humans]

run_in_one_thread(fishers)
run_in_threads(fishers)


# останавливаем поток если нужно

class Fisher(Thread):

    def __init__(self, name, worms, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = name
        self.worms = worms
        self.catch = defaultdict(int)
        # будем проверять в цикле - а не пора ли нам заканчивать?
        self.need_stop = False

    def run(self):
        self.catch = defaultdict(int)
        for worm in range(self.worms):
            print(f'{self.name}: Червяк № {worm} - Забросил, ждем...', flush=True)
            _ = 3 ** (random.randint(50, 70) * 10000)
            fish = random.choice(FISH)
            if fish is None:
                print(f'{self.name}: Тьфу, сожрали червяка...', flush=True)
            else:
                print(f'{self.name}: Ага, у меня {fish}', flush=True)
                self.catch[fish] += 1
            if self.need_stop:
                print(f'{self.name}: Ой, жена ужинать зовет! Сматываем удочки...', flush=True)
                break


vasya = Fisher(name='Вася', worms=100)
vasya.start()
time.sleep(1)
if vasya.is_alive():  # кстати с помощью этого метода можно проверить выполняется ли еще поток?
    vasya.need_stop = True
vasya.join()  # ожидание завершения обязательно - поток может некоторое время финализировать работу