# Quiz App
![WIP](https://img.shields.io/badge/Status-WIP-f1c40f?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![AWS](https://img.shields.io/badge/AWS-232F3E?style=for-the-badge&logo=amazon-aws&logoColor=white)
![Terraform](https://img.shields.io/badge/Terraform-7B42BC?style=for-the-badge&logo=terraform&logoColor=white)

⚠️ This project is a work in progress.

A user-friendly web application that allows users to take quizzes, track their scores, and view results instantly. Administrators can easily add, or remove quizzes, making quiz management simple and efficient.


## Architecture Diagram


## Architecture Overview

This section explains the main components of the Quiz App and how they interact:

- **Frontend (React, Vite):** Handles the user interface, quiz interactions, and communicates with the backend APIs. Uses **AWS Cognito** for secure user authentication.  
- **Backend (FastAPI, Python):** Provides APIs for quiz management, admin operations, and quiz retrieval. Handles authentication and quiz listing/creation/deletion.  
- **Database (DynamoDB):** Stores quizzes, questions, and user scores.  
- **AWS Services:**  
  - **Cognito:** Manages user login and authentication.  
  - **S3:** Hosts the frontend application.  
  - **ECS / EC2:** Hosts the backend application.  
  - **ALB:** Distributes incoming requests to backend ECS/EC2 instances. 
  - **Lambda:** Calculates, saves, and retrieves quiz scores.  
- **Terraform:** Infrastructure as code to deploy and manage all AWS resources consistently.

## Features (Planned)

- Take quizzes and view results
- Track user scores
- Serverless scoring with AWS Lambda  
- Terraform provisioning for backend, Lambda, DynamoDB, and S3.


## Tech Stack

**Client:** JavaScript, React, Vite

**Server:** Python, FastAPI, Docker

**AWS Services:** Cognito, ALB, ECS, EC2, ECR, Lambda, DynamoDB, S3

**Infrastructure as Code:** Terraform

