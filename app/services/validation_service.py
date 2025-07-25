class ValidationService:
    @staticmethod
    def validate_weight(weight):
        return isinstance(weight, (int, float)) and 0 < weight <= 2000

    @staticmethod
    def validate_date(date_str):
        from datetime import datetime
        try:
            datetime.fromisoformat(date_str)
            return True
        except ValueError:
            return False

    @staticmethod
    def validate_percentage(percentage):
        return isinstance(percentage, (int, float)) and 0 <= percentage <= 100