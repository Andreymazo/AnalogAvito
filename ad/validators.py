from rest_framework.exceptions import ValidationError


class MilageValidator:
    """Валидация пробега автомобиля в зависимости от выбора поля by_milage"""

    def __init__(self, field_milage, field_by_milage):
        self.field_milage = field_milage
        self.field_by_milage = field_by_milage

    def __call__(self, value):
        data_milage = dict(value).get(self.field_milage)
        data_by_milage = dict(value).get(self.field_by_milage)

        if data_by_milage == "NEW":
            if int(data_milage) < 0 or int(data_milage) > 5:
                raise ValidationError("Пробег нового автомобиля должен быть от 0 до 5 км")



