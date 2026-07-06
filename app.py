import streamlit as st
import pandas as pd
import datetime

from database import Database
from models import Subject, Exam

db = Database()

menu = st.sidebar.selectbox(
    "Menu",
    [
        "Home",
        "Subjects",
        "Exams",
        "Generate Study Plan"
    ]
)

if menu == "Home":
    st.set_page_config(
    page_title="SOMA Revision Planner",
    page_icon="🧾",
    layout="wide"
    )

    st.title("🧾SOMA Revision Planner")
    st.write("Welcome! Let's start your Revision Planning.")

elif menu == "Subjects":
    option = st.selectbox(
        "Select an option",
        [
            "Add Subject",
            "View Subjects",
            "Search Subject",
            "Update Subject",
            "Delete Subject"
        ]
    )
    if option == "Add Subject":
        st.header("Add Subject")
    
        name = st.text_input("Subject Name")

        difficulty = st.slider(
            "Difficulty",
            1,
            5,
            3
           )

        if st.button("Add Subject"):

            if len(name.strip()) < 3:
                st.error("Subject name must be at least 3 characters long.")

            elif not name.replace(" ", "").isalpha():
                st.error("Subject name must contain letters only.")

            else:
                db.add_subject(name, difficulty)
                st.success("✅ Subject added successfully!")

    elif option == "View Subjects":
        st.header("View Subjects")
        subjects = db.get_subjects()

        if not subjects:
            st.warning("No subjects found.")

        else:
            df = pd.DataFrame(
                subjects,
                columns=["ID", "Subject", "Difficulty"]
            )

            st.dataframe(df)

        keyword = st.text_input("Enter a subject name")

    elif option == "Search Subject":
        st.header("Search Subject")
        keyword = st.text_input("Enter a subject name")

        if st.button("Search"):
            results = db.search_subject(keyword)

            if not results:
                st.warning("No subjects found.")
            else:
                df = pd.DataFrame(
                results,
                columns=["ID", "Subject", "Difficulty"]
            )

            st.dataframe(df, use_container_width=True)

    elif option == "Update Subject":
        st.header("Update Subject")
        subjects = db.get_subjects()

        if not subjects:
            st.warning("No subjects available.")

        else:
            subject_dict = {
                row[1]: row
                for row in subjects
            }

            selected = st.selectbox(
                "Select Subject",
                list(subject_dict.keys())
            )

            row = subject_dict[selected]

            subject_id = row[0]

            name = st.text_input(
                "New Subject Name",
                value=row[1]
            )

            difficulty = st.slider(
                "Difficulty",
                1,
                5,
                value=row[2]
            )

            if st.button("Update Subject"):

                if len(name.strip()) < 3:
                    st.error("Subject name must be at least 3 characters long.")

                elif not name.replace(" ", "").isalpha():
                    st.error("Use letters and spaces only.")

                else:
                    success = db.update_subject(
                        subject_id,
                        name,
                        difficulty
                    )

                    if success:
                        st.success("Subject updated successfully!")
                    else:
                        st.error("Update failed.")
    elif option == "Delete Subject":
        st.header("Delete Subject")
        subjects = db.get_subjects()

        if not subjects:
            st.warning("No subjects available.")

        else:
            subject_dict = {
                row[1]: row[0]
                for row in subjects
            }

            selected = st.selectbox(
                "Select Subject",
                list(subject_dict.keys())
            )

            if st.button("Delete Subject"):
                success = db.delete_subject(subject_dict[selected])

                if success:
                    st.success("Subject deleted successfully!")
                else:
                    st.error("Delete failed.")
elif menu == "Exams":
    option = st.sidebar.selectbox(
        "Exam Options",
        [
            "Add Exam",
            "View Exams",
            "Update Exam",
            "Delete Exam"
        ]
    )
    if option == "Add Exam":
        st.header("Add Exam")

        subjects = db.get_subjects()

        if not subjects:
            st.warning("Please add a subject first.")

        else:
            subject_dict = {
                row[1]: row[0]
                for row in subjects
            }

            selected = st.selectbox(
                "Subject",
                list(subject_dict.keys())
            )

            exam_date = st.date_input("Exam Date")

            if st.button("Add Exam"):

                # Check if the exam date is in the past
                if exam_date < datetime.date.today():
                    st.error("The exam date cannot be in the past.")

                else:
                    db.add_exam(
                        subject_dict[selected],
                        str(exam_date)
                    )

                    st.success("Exam added successfully!")

    elif option == "View Exams":

        st.header("View Exams")

        exams = db.get_exams()

        if not exams:
            st.warning("No exams available.")

        else:

            df = pd.DataFrame(
                exams,
                columns=[
                    "Exam ID",
                    "Subject ID",
                    "Subject",
                    "Difficulty",
                    "Exam Date"
                ]
            )

            st.dataframe(
                df,
                use_container_width=True
            )

    elif option == "Update Exam":
        st.header("Update Exam")
        exams = db.get_exams()

        if not exams:
            st.warning("No exams available.")
        else:
            exam_dict = {
                f"{row[2]} ({row[4]})": row
                for row in exams
            }

            selected = st.selectbox(
                "Select Exam",
                exam_dict.keys()
            )

            row = exam_dict[selected]
            exam_id = row[0]

            subjects = db.get_subjects()
            subject_dict = {
                row[1]: row[0]
                for row in subjects
            }

            selected_subject = st.selectbox(
                "Select Subject",
                subject_dict.keys(),
                index=list(subject_dict.keys()).index(row[2])
            )

            exam_date = st.date_input(
                "Exam Date",
                value=datetime.datetime.strptime(row[4], "%Y-%m-%d").date(),
                min_value=datetime.date.today()
            )

            if st.button("Update Exam"):

                if exam_date < datetime.date.today():
                    st.error("The exam date cannot be in the past.")

                else:
                    success = db.update_exam(
                        exam_id,
                        subject_dict[selected_subject],
                        str(exam_date)
                    )

                    if success:
                        st.success("Exam updated successfully!")
                    else:
                        st.error("Exam not found.")

    elif option == "Delete Exam":
        st.header("Delete Exam")
        exams = db.get_exams()

        if not exams:
            st.warning("No exams available.")
        else:
            exam_dict = {
                f"{row[2]} ({row[4]})": row[0]
                for row in exams
            }
            selected = st.selectbox(
                "Select Exam",
                exam_dict.keys()
            )
            if st.button("Delete Exam"):

                success = db.delete_exam(exam_dict[selected])

                if success:
                    st.success("Exam deleted.")
                else:
                    st.error("Exam not found.")

elif menu == "Generate Study Plan":
        st.header("Generate Study Plan")
        if st.button("Generate Study Plan"):
            exams = db.get_exams()

            if not exams:
                st.warning("No exams available.")
            else:
                study_plan = []
                for row in exams:
                    subject = Subject(
                        row[1],
                        row[2],
                        row[3]
                    )

                    exam = Exam(
                        row[0],
                        subject,
                        row[4]
                    )

                    study_plan.append({
                        "Subject": subject.name,
                        "Days Left": exam.days_remaining(),
                        "Difficulty": subject.difficulty,
                        "Priority": round(
                            exam.calculate_priority(),
                            2
                        )
                    })

                study_plan.sort(
                    key=lambda x: x["Priority"],
                    reverse=True
                )

                df = pd.DataFrame(study_plan)

                st.success("Study plan generated successfully!")
                st.dataframe(
                    df,
                    use_container_width=True
                )
