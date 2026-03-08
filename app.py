import streamlit as st
from auth import login, register
from parser import extract_questions
from ai_engine import build_vector_store, generate_answer
from export import export_answers


# ---------------- SESSION STATE ----------------

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if "answers" not in st.session_state:
    st.session_state["answers"] = []

if "citations" not in st.session_state:
    st.session_state["citations"] = []

if "confidences" not in st.session_state:
    st.session_state["confidences"] = []

if "vector_store" not in st.session_state:
    st.session_state["vector_store"] = None


# ---------------- SIDEBAR MENU ----------------

if st.session_state["authenticated"]:
    menu = st.sidebar.selectbox("Menu", ["Logout"])
else:
    menu = st.sidebar.selectbox("Menu", ["Login", "Signup"])


# ---------------- SIGNUP ----------------

if menu == "Signup":

    st.title("Create Account")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Register"):

        register(email, password)
        st.success("Account created successfully. Please login.")


# ---------------- LOGIN ----------------

elif menu == "Login":

    st.title("Login")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):

        if login(email, password):

            st.session_state["authenticated"] = True
            st.success("Logged in successfully")
            st.rerun()

        else:
            st.error("Invalid credentials")


# ---------------- LOGOUT ----------------

elif menu == "Logout":

    st.session_state["authenticated"] = False
    st.success("Logged out successfully")
    st.rerun()


# ---------------- MAIN APPLICATION ----------------

if st.session_state["authenticated"]:

    st.title("AI Questionnaire Answering Tool")
    st.write("Upload questionnaire and reference documents.")

    # Upload questionnaire
    questionnaire_file = st.file_uploader(
        "Upload Questionnaire (PDF or TXT)",
        type=["pdf", "txt"]
    )

    # Upload reference documents
    reference_files = st.file_uploader(
        "Upload Reference Documents",
        accept_multiple_files=True
    )

    # ---------------- EXTRACT QUESTIONS ----------------

    if questionnaire_file:

        questions = extract_questions(questionnaire_file)

        st.subheader("Extracted Questions")

        for q in questions:
            st.write(q)

        # ---------------- GENERATE ANSWERS ----------------

        if reference_files:

            if st.button("Generate AI Answers"):

                # Build vector store once
                if st.session_state["vector_store"] is None:
                    st.session_state["vector_store"] = build_vector_store(reference_files)

                vector_store = st.session_state["vector_store"]

                st.session_state["answers"] = []
                st.session_state["citations"] = []
                st.session_state["confidences"] = []

                for q in questions:

                    answer, citation, conf = generate_answer(q, vector_store)

                    st.session_state["answers"].append(answer)
                    st.session_state["citations"].append(citation)
                    st.session_state["confidences"].append(conf)

        # ---------------- DISPLAY ANSWERS ----------------

        if st.session_state["answers"]:

            st.subheader("Generated Answers")

            edited_answers = []

            for i, q in enumerate(questions):

                st.write("Question:", q)

                edited_answer = st.text_area(
                    f"Answer for Question {i+1}",
                    value=st.session_state["answers"][i],
                    key=f"answer_{i}"
                )

                edited_answers.append(edited_answer)

                st.write("Citation:", st.session_state["citations"][i])
                st.write("Confidence:", st.session_state["confidences"][i], "%")
                st.write("---")

            # ---------------- COVERAGE SUMMARY ----------------

            total_questions = len(questions)

            answered = sum(
                1 for a in edited_answers if a != "Not found in references."
            )

            not_found = total_questions - answered

            st.subheader("Coverage Summary")

            st.write(f"Total Questions: {total_questions}")
            st.write(f"Answered with citations: {answered}")
            st.write(f"Not found in references: {not_found}")

            # ---------------- EXPORT DOCUMENT ----------------

            if st.button("Download Completed Questionnaire"):

                file_path = export_answers(
                    questions,
                    edited_answers,
                    st.session_state["citations"]
                )

                with open(file_path, "rb") as f:

                    st.download_button(
                        "Download Document",
                        f,
                        file_name="completed_questionnaire.docx"
                    )