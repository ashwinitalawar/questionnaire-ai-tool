# Structured Questionnaire Answering Tool

## Industry
Cloud Security SaaS

## Fictional Company
SecureCloud AI is a SaaS platform that provides automated cloud security monitoring and compliance management for enterprise infrastructure. The platform analyzes security logs and infrastructure activity to detect threats, enforce compliance policies, and ensure secure cloud operations.


## What I Built

I developed a web application that automates answering structured questionnaires using internal reference documents.

Users can upload a questionnaire and supporting reference documents. The system extracts questions, retrieves relevant information from the documents, and generates answers along with citations.

Key Features:
- User authentication (Signup / Login)
- Upload questionnaire documents
- Upload reference documents
- Automatic question extraction
- Retrieval-based answer generation
- Citations for each answer
- Confidence score for generated answers
- Ability to edit answers before export
- Download completed questionnaire as a document

## Assumptions

- The reference documents contain accurate and approved company information.
- Questions in the questionnaire correspond to the information available in the documents.
- Answers should only be generated using the uploaded reference documents.


## Trade-offs

- A lightweight TF-IDF retrieval method was used instead of large language models to keep the system efficient and easy to run locally.
- The user interface was kept simple to focus on functionality.
- Document parsing was implemented for basic formats (PDF/TXT) to keep the scope manageable.


## What I Would Improve With More Time

- Use semantic embeddings or LLM-based retrieval for better accuracy.
- Support additional questionnaire formats such as Excel spreadsheets.
- Improve answer summarization using generative AI models.
- Add version history to track multiple questionnaire runs.
- Improve UI/UX for document review and editing.