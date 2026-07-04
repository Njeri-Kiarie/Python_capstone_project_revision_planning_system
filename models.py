import datetime

# Base or Parent class for all academic objects
class AcademicItem:
    total_items = 0

    def __init__(self, item_id):
        self.item_id = item_id
        AcademicItem.total_items += 1

    @classmethod
    def get_total_items(cls):
        return cls.total_items
    
    def display(self):
        print(f"Item ID: {self.item_id}")

# Subject Class
class Subject(AcademicItem):
    def __init__(self, subject_id, name, difficulty):
        super().__init__(subject_id)
        self.name = name
        self._difficulty = difficulty

    @property
    def difficulty(self):
        return self._difficulty
    
    @difficulty.setter
    def difficulty(self, value):
        if 1<= value <=5:
            self._difficulty = value
        else:
            raise ValueError("Please enter a difficulty level between 1 and 5.")
        
# Exam class
class Exam(AcademicItem):
    def __init__(self, exam_id, subject, exam_date):
        super().__init__(exam_id)
        self.subject = subject
        self.exam_date = exam_date
    
    def days_remaining(self):
        today = datetime.date.today()
        exam = datetime.datetime.strptime(self.exam_date, "%Y-%m-%d").date()
        return(exam - today).days
    
    def calculate_priority(self):
        days = self.days_remaining()

        if days <= 0:
            days = 1

        return self.subject.difficulty * (10 / days)
    
    def display(self):
        print(f"Exam ID: {self.item_id}")
        print(f"Subject: {self.subject.name}")
        print(f"Exam Date: {self.exam_date}")
        print(f"Days left: {self.days_remaining}")
