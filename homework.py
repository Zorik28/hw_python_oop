from dataclasses import dataclass, asdict
from typing import Dict, Type


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    message = ('Тип тренировки: {training_type}; '
               'Длительность: {duration:.3f} ч.; '
               'Дистанция: {distance:.3f} км; Ср. скорость: {speed:.3f} км/ч; '
               'Потрачено ккал: {calories:.3f}.')

    def get_message(self) -> str:
        return self.message.format(**asdict(self))


class Training:
    """Базовый класс тренировки."""

    LEN_STEP: float = 0.65                    # Step length in meters
    M_IN_KM: int = 1000                       # Meters in kilometers
    H_IN_MIN: int = 60                        # Hours in minutes

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float
                 ) -> None:
        self.action = action
        self.duration = duration                  # Training duration in hours
        self.weight = weight                      # Weight in kilograms
        self.dur_min = duration * self.H_IN_MIN   # Duration in minutes

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

    COEFF_CALORIE_1: int = 18
    COEFF_CALORIE_2: int = 20

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        a = self.COEFF_CALORIE_1 * self.get_mean_speed() - self.COEFF_CALORIE_2
        return a * self.weight / self.M_IN_KM * self.dur_min


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    COEFF_CALORIE_1: float = 0.035
    COEFF_CALORIE_2: float = 0.029

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
        c = self.COEFF_CALORIE_2 * self.weight
        return (self.COEFF_CALORIE_1 * self.weight + b * c) * self.dur_min


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: float = 1.38                   # Length of one acion in meters
    COEFF_CALORIE_1: float = 1.1
    COEFF_CALORIE_2: float = 2

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
        e = self.get_mean_speed() + self.COEFF_CALORIE_1
        return e * self.COEFF_CALORIE_2 * self.weight


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    dict: Dict[str, Type(Training)] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }

    if workout_type in dict:
        return dict[workout_type](*data)
    raise ValueError('There is no accepted training code in the database')


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
