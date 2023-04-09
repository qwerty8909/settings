# функция засекаем время
def time_track(func):
    def surrogate(*args, **kwargs):
        started_at = time.time()

        result = func(*args, **kwargs)

        ended_at = time.time()
        elapsed = round(ended_at - started_at, 4)
        print(f'Функция работала {elapsed} секунд(ы)')
        return result
    return surrogate


@time_track # без декоратора функция просто работает
def digits(*args):
    total = 1
    for number in args:
        total *= number ** 5000
    return len(str(total))

