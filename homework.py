from dataclasses import dataclass
from typing import Dict


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    message = ('Тип тренировки: {0}; Длительность: {1:.3f} ч.; '
               'Дистанция: {2:.3f} км; Ср. скорость: {3:.3f} км/ч; '
               'Потрачено ккал: {4:.3f}.')

    def get_message(self) -> str:
        return self.message.format(self.training_type,
                                   self.duration,
                                   self.distance,
                                   self.speed,
                                   self.calories
                                   )


class Training:
    """Базовый класс тренировки."""

    LEN_STEP: float = 0.65                    # Step length in meters
    M_IN_KM: int = 1000                       # Meters in kilometers

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float
                 ) -> None:
        self.action = action
        self.duration = duration               # training duration in hours
        self.weight = weight                   # athlete's weight in kilograms
        self.dur_minutes = duration * 60       # training duration in minutes

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError('Method is not defined in parent class')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(type(self).__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories()
                           )


class Running(Training):
    """Тренировка: бег."""

    coeff_calorie_1: int = 18
    coeff_calorie_2: int = 20

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        a = self.coeff_calorie_1 * self.get_mean_speed() - self.coeff_calorie_2
        return a * self.weight / self.M_IN_KM * self.dur_minutes


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    coeff_calorie_1: float = 0.035
    coeff_calorie_2: float = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height                       # athlete's height in meters

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        b = (self.get_mean_speed()**2 // self.height)
        c = self.coeff_calorie_2 * self.weight
        return (self.coeff_calorie_1 * self.weight + b * c) * self.dur_minutes


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: float = 1.38                   # Length of one acion in meters
    coeff_calorie_1: float = 1.1
    coeff_calorie_2: float = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool   # Pool length in meters
        self.count_pool = count_pool     # Number of times pool was swam across

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        d = self.length_pool * self.count_pool
        return d / self.M_IN_KM / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        e = self.get_mean_speed() + self.coeff_calorie_1
        return e * self.coeff_calorie_2 * self.weight


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    dict: Dict[str, Training] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }

    if workout_type in dict:
        return dict[workout_type](*data)
    else:
        return 'В базе отсутствует принятый код тренировки'


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
