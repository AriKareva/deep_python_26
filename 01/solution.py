class SomeModel:
    def predict(self, message: str) -> float:
        if len(message) >= 15:
            return 0.9
        if len(message) <= 7:
            return 0.1
        return 0.5


def predict_message_mood(
    message: str,
    bad_thresholds: float = 0.3,
    good_thresholds: float = 0.8,
) -> str:

    if not 0 <= bad_thresholds <= 1:
        raise ValueError('bad_thresholds вне диапазона [0, 1]')

    if not 0 <= good_thresholds <= 1:
        raise ValueError('good_thresholds вне диапазона [0, 1]')

    model = SomeModel()
    prediction = model.predict(message)

    match prediction:
        case p if p < bad_thresholds:
            return 'неуд'
        case p if p > good_thresholds:
            return 'отл'
        case _:
            return 'норм'


def filter_file(filename: str,
                target: list[str],
                stop: list[str]):

    target_set = {t.lower() for t in target}
    stop_set = {s.lower() for s in stop}
    flag = False

    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            flag = False
            words = line.rstrip('\n').lower().split()
            for w in words:
                if w in stop_set:
                    flag = False
                    break
                if w in target_set:
                    flag = True

            if flag:
                yield line.rstrip('\n')
