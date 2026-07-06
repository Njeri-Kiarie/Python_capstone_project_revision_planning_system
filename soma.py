import csv
import datetime
from database import Database
from models import Subject, Exam

# Create database object
db = Database()

def header(title):
    print("\n" + "=" * 50)
    print(title.center(50))
    print("=" * 50)

def pause():
    input("\nPress Enter to continue...")

#Add Subject
def add_subject():
    header("ADD SUBJECT")

    while True:
        name = input("Subject Name: ").strip()
        if len(name) < 3:
            print("Subject name must be at least 3 characters long.")
            continue
        if name.replace(" ", "").isalpha():
            break
       
        print("Invalid subject name. Use letters and spaces only.")
    
    while True:
        try:
            difficulty = int(input("Difficulty (1-5): "))
            
            if 1 <= difficulty <= 5:
                break

            print("Difficulty must be between 1 and 5.")

        except ValueError:
            print("Difficulty must be a number.")
        except Exception:
            print("That subject already exists.")

    db.add_subject(name, difficulty)
    print("\nSubject has been added successfully!")

    
# View Subjects
def view_subjects():
    header("VIEW SUBJECTS")
    subjects = db.get_subjects()

    if not subjects:
        print("No subjects found.")
        return
    
    print(f"{'ID': <5}{'Subject': <25}{'Difficulty'}")
    print("-" * 45)

    for row in subjects:
        subject = Subject(
            row[0],
            row[1],
            row[2]
        )
        print(
            f"{subject.item_id:<5}"
            f"{subject.name:<25}"
            f"{subject.difficulty}"
        )

# Search for a subject
def search_subject():
    header("SEARCH SUBJECT")
    keyword = input("Enter a Subject name: ").strip()
    results = db.search_subject(keyword)

    if not results:
        print("No subjects found.")
        return
    
    print(f"\n{'ID':<5}{'Subject':<25}{'Difficulty'}")
    print("-" * 45)

    for row in results:
        print(f"ID: {row[0]:<5}")
        print(f"Subject: {row[1]:<25}")
        print(f"Difficulty: {row[2]}")
        print("-" * 30)

# Update a subject
def update_subject():
    header("UPDATE SUBJECT")
    
    subjects = db.get_subjects()
    if not subjects:
        print("No Subjects available")
        return
    for row in subjects:
        print(f"{row[0]}. {row[1]}")

    try:
        subject_id = int(input("\nSubject ID: "))

        while True:
            name = input("New Subject Name: ").strip()

            if len(name) < 3:
                print("Subject name must be at least 3 characters long.")
                continue

            if not name:
                print("Subject cannot be empty.")
                continue

            if not name.replace(" ", "").isalpha():
                print("Invalid subject name. Use letters and spaces only.")
                continue

            break
       
        difficulty = int(input("New Difficulty (1-5): ")
                         )
        if difficulty < 1 or difficulty > 5:
            print("Difficulty must be between 1 and 5.")
            return

        success = db.update_subject(subject_id, name, difficulty)  
        if success:
            print("\nSubject has been updated!")
        else:
            print(f"\n Subject ID not found.")

    except ValueError:
        print("Invalid Input.")

# Delete a subject
def delete_subject():
    header("DELETE SUBJECT")
    subjects = db.get_subjects()

    if not subjects:
        print("No subjects available.")
        return
    print()

    for row in subjects:
        print(f"{row[0]}. {row[1]}")
    
    try:
        subject_id = int(input("\nEnter Subject ID to delete: "))
        confirm = input("Confirm you want to delete this subject? (y/n): ").lower()
        if confirm != "y":
            print("\n Deletion Cancelled.")
            return
        
        success = db.delete_subject(subject_id)

        if success:
            print("\nSubject deleted successfully!")
        else:
            print("\nSubject ID not found.")
    except ValueError:
        print("Inavlid ID.")

# Exam Management
# Adding exam timetable
def add_exam():
    header("ADD EXAM")
    subjects = db.get_subjects()

    if not subjects:
        print("Please add a subject first.")
        return

    print("\nAvailable Subjects")

    for row in subjects:
        print(f"{row[0]}. {row[1]}")

    try:
        subject_id = int(input("\nEnter Subject ID: "))

    except ValueError:
        print("Invalid input.")
        return

    # Check whether the subject exists
    subject = next((row for row in subjects if row[0] == subject_id), None)

    if subject is None:
        print("Subject not found.")
        return

    exam_date = input("\nEnter Exam Date (YYYY-MM-DD): ").strip()

    try:
        exam_date = datetime.datetime.strptime(exam_date, "%Y-%m-%d").date()

    except ValueError:
        print("Invalid date format. Please use YYYY-MM-DD.")
        return

    # Check if the exam date is in the past
    if exam_date < datetime.date.today():
        print("Error: The exam date cannot be in the past.")
        return

    db.add_exam(subject_id, str(exam_date))
    print("\nExam added successfully!")
    
# View exams
def view_exams():
    header("VIEW EXAMS")
    exams = db.get_exams()

    if not exams:
        print("No exams have been added.")
        return
    print(f"{'ID':<5}{'Subject': <25}{'Difficulty': <12}{'Exam Date'}")
    print("-" * 55)

    for row in exams:
        print(
            f"{row[0]:<5}"
            f"{row[2]:<25}"
            f"{row[3]:<12}"
            f"{row[4]}"
        )

# Update an exam
def update_exam():
    header("UPDATE EXAM")
    exams = db.get_exams()

    if not exams:
        print("No exams available.")
        return
    print()

    for row in exams:
        print(f"{row[0]}. {row[2]} ({row[4]})")
    
    try:
        exam_id = int(input("\nEnter Exam ID to update: "))

    except ValueError:
        print("Invalid ID.")
        return
    
    exam = next((row for row in exams if row[0] == exam_id), None)

    if exam is None:
        print("Exam not found.")
        return

    subjects = db.get_subjects()
    
    if not subjects:
        print("Please add a subject first.")
        return
    print("\nAvailable Subjects")

    for row in subjects:
        print(f"{row[0]}. {row[1]}")

    try:
        subject_id = int(input("\nEnter New Subject ID: "))

    except ValueError:
        print("Invalid input.")
        return
    
    # Checking whether the subject exists
    subject = next((row for row in subjects if row[0] == subject_id), None)

    if subject is None:
        print("Subject not found.")
        return

    exam_date = input("\nEnter New Exam Date (YYYY-MM-DD): ").strip()

    try:
        exam_date = datetime.datetime.strptime(exam_date, "%Y-%m-%d").date()
    
    except ValueError:
        print("Invalid date format.")
        return

    success = db.update_exam(exam_id, subject_id, exam_date)

    if success:
        print("\nExam updated successfully!")
    else:
        print("\nExam ID not found.")

# Delete an exam
def delete_exam():
    header("DELETE EXAM")
    exams = db.get_exams()

    if not exams:
        print("No exams available.")
        return
    print()

    for row in exams:
        print(f"{row[0]}. {row[2]} ({row[4]})")
   
    try:
        exam_id = int(input("\nEnter Exam ID to delete: "))

    except ValueError:
        print("Invalid ID.")
        return

    confirm = input("Delete this exam? (y/n): ").lower()

    if confirm != "y":
        print("Deletion cancelled.")
        return

    success = db.delete_exam(exam_id)

    if success:
        print("Exam deleted successfully!")
    else:
        print("Exam ID not found.")

# Creating a study plan
def generate_study_plan():
    header("STUDY PLAN")
    exams = db.get_exams()

    if not exams:
        print("No exams have been added.")
        return

    study_plan = []

    for row in exams:

        exam_id = row[0]
        subject_id = row[1]
        subject_name = row[2]
        difficulty = row[3]
        exam_date = row[4]

        subject = Subject(subject_id, subject_name, difficulty)
        exam = Exam(exam_id, subject, exam_date)

        priority = exam.calculate_priority()

        study_plan.append(
            {
                "exam": exam,
                "priority": priority
            }
        )

    study_plan.sort(
        key=lambda item: item["priority"],
        reverse=True
    )

    print()

    print(
        f"{'Subject':<25}"
        f"{'Days Left':<12}"
        f"{'Difficulty':<12}"
        f"{'Priority'}"
    )

    print("-" * 65)

    for item in study_plan:

        exam = item["exam"]

        print(
            f"{exam.subject.name:<25}"
            f"{exam.days_remaining():<12}"
            f"{exam.subject.difficulty:<12}"
            f"{item['priority']:.2f}"
        )
    save_study_plan(study_plan)


# Saving the study plan
def save_study_plan(study_plan):
    try:
        with open("study_plan.csv", "w") as file:
            writer = csv.writer(file)

            # Writing the header and date
            writer.writerow(["SOMA REVISION STUDY PLAN"])
            writer.writerow([f"Generated: {datetime.date.today()}"])
            writer.writerow([])

            # Writing the column headers
            writer.writerow([
                "Rank", "Subject", "Exam Date", "Days Remaining", "Difficulty", "Priority Score"
            ])

            rank = 1

            for item in study_plan:

                exam = item["exam"]

                writer.writerow([
                    rank,
                    exam.subject.name,
                    exam.exam_date,
                    exam.days_remaining(),
                    exam.subject.difficulty,
                    f"{item['priority']:.2f}"
                ])

                rank += 1

        print("\nStudy plan saved successfully as 'study_plan.csv'.")

    except IOError:
        print("Error saving study plan.")
               
# Main Menu
def main():

    while True:

        header("SOMA REVISION PLANNER")

        print("1. Add Subject")
        print("2. View Subjects")
        print("3. Search Subject")
        print("4. Update Subject")
        print("5. Delete Subject")
        print("6. Add Exam")
        print("7. View Exams")
        print("8. Update Exam")
        print("9. Delete Exam")
        print("10. Generate Study Plan")
        print("0. Exit")

        choice = input("\nChoose an option: ")

        if choice == "1":
            add_subject()
        elif choice == "2":
            view_subjects()
        elif choice == "3":
            search_subject()
        elif choice == "4":
            update_subject()
        elif choice == "5":
            delete_subject()
        elif choice == "6":
            add_exam()
        elif choice == "7":
            view_exams()
        elif choice == "8":
            update_exam()
        elif choice == "9":
            delete_exam()
        elif choice == "10":
            generate_study_plan()
        elif choice == "0":

            db.close()
            print("\nThank you for using Soma Revision Planner! All the best in your exams!")
            break
        else:
            print("Invalid option.")
            
if __name__ == "__main__":
    main()