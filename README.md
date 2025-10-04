# Expense Management System

## Overview

The **Expense Management System** is a full-stack web application designed to streamline the process of employee expense submission and approval within organizations.
It eliminates manual reimbursement inefficiencies by introducing automated workflows, role-based access, and intelligent approval logic.

The system is built with **Django (Python)** and **SQLite** on the backend, and a responsive **HTML, CSS, and JavaScript** frontend.
It integrates with public APIs for currency data and includes an OCR-based receipt reader to automate expense creation.

## Problem Statement

Organizations often face challenges with traditional expense reimbursement processes, such as:

* Lack of transparency and auditability
* Manual and time-consuming approval cycles
* Fixed and rigid approval structures
* Difficulty managing multi-currency reimbursements

This project addresses those challenges by enabling:

* Configurable approval flows
* Role-based expense management
* Dynamic approval rules and conditions
* Integrated OCR for automated data extraction

## Key Features

### 1. Authentication and User Management

* Secure user authentication using Django’s built-in system.
* On first signup:

  * A new **company** instance is created.
  * Default currency is set based on the user’s selected country.
  * The first user is assigned the **Admin** role.
* Admin capabilities:

  * Create and manage Employees and Managers.
  * Assign or change user roles dynamically.
  * Define reporting hierarchies and approval sequences.

### 2. Expense Submission (Employee Role)

* Employees can submit detailed expense claims with fields such as:

  * Amount (supports different currencies)
  * Category and Description
  * Expense Date and Receipt Upload
* View personal expense history (Approved, Rejected, Pending).
* Automatic data extraction from uploaded receipts using OCR.

### 3. Approval Workflow (Manager/Admin Role)

* Multi-level approval process configurable by the Admin.
* Example sequence:

  * Step 1 → Manager
  * Step 2 → Finance
  * Step 3 → Director
* Each expense advances only after the current approver takes action.
* Managers can view, approve, or reject pending expenses with comments.

### 4. Conditional Approval Logic

Supports multiple approval rule types:

* **Percentage Rule:** e.g., expense is approved if ≥ 60 % of approvers agree.
* **Specific Approver Rule:** e.g., CFO approval automatically finalizes the expense.
* **Hybrid Rule:** e.g., 60 % approval or CFO approval triggers final acceptance.
  The system can combine sequential and conditional rules to form hybrid workflows.

### 5. Role Permissions

| Role         | Responsibilities                                                                                        |
| ------------ | ------------------------------------------------------------------------------------------------------- |
| **Admin**    | Manage company data, users, and roles; configure approval rules; view all expenses; override approvals. |
| **Manager**  | Approve or reject expenses within their reporting hierarchy; escalate or comment as required.           |
| **Employee** | Submit expenses, upload receipts, view approval history and current status.                             |

### 6. OCR-Based Receipt Processing

* Uses a Python-based OCR engine (e.g., **Tesseract** or **EasyOCR**).
* Extracts key fields such as amount, date, merchant name, and category.
* Auto-populates form fields for rapid expense creation.

### 7. API Integrations

| Purpose             | API                                                                            | Description                                                       |
| ------------------- | ------------------------------------------------------------------------------ | ----------------------------------------------------------------- |
| Country & Currency  | [RESTCountries API](https://restcountries.com/v3.1/all?fields=name,currencies) | Fetches country-currency mappings during signup.                  |
| Currency Conversion | [ExchangeRate API](https://api.exchangerate-api.com/v4/latest/{BASE_CURRENCY}) | Converts foreign currency amounts to the company’s base currency. |

## System Architecture

```
Frontend (HTML, CSS, JS)
        ↓
Django Views / REST Layer
        ↓
Business Logic (Approval Rules, OCR Processing)
        ↓
SQLite Database
```

## Technology Stack

| Layer        | Technology                  |
| ------------ | --------------------------- |
| **Frontend** | HTML, CSS, JavaScript       |
| **Backend**  | Django (Python)             |
| **Database** | SQLite                      |
| **APIs**     | RESTCountries, ExchangeRate |
| **OCR**      | Tesseract / EasyOCR         |


## Installation and Setup

### 1. Clone Repository

```bash
git clone https://github.com/<your-username>/expense-management-system.git
cd expense-management-system
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Start Server

```bash
python manage.py runserver
```

Access the system at: [http://localhost:8000](http://localhost:8000)

<img width="805" height="393" alt="image" src="https://github.com/user-attachments/assets/92c60a27-c022-4799-977f-8ad042f7d51f" />

<img width="826" height="377" alt="image" src="https://github.com/user-attachments/assets/ee4915bb-69e0-4152-ad55-5b0ed4ffc4e5" />

## Future Enhancements

* Email and in-app notifications for approval updates
* Advanced analytics dashboard for finance teams
* Role-based access through JWT/Session APIs
* Responsive mobile-first frontend
* Integration with corporate accounting systems

## Evaluation Highlights

* Implements both **sequential and conditional approval flows**.
* Integrates **OCR** for intelligent receipt scanning.
* Uses **live currency conversion** and **country-based company setup**.
* Maintains clean architecture with Django ORM and SQLite for data integrity.
* Fully developed using **open-source technologies** with focus on scalability and auditability.
