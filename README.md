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

## Installation and Setup

### 1. Clone Repository

```bash
git clone https://github.com/Jayesh-Gautam/Odoo-Hackathon.git
cd ExpenseManager
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

## Visual Results

![img1](https://github.com/user-attachments/assets/583f23b6-a34a-44e7-8d09-848197d1107c)


![img2](https://github.com/user-attachments/assets/26dd6eb2-62e0-4b99-ac1e-5e3f27fd3949)


![img3](https://github.com/user-attachments/assets/364a86af-ad7e-4290-a498-00868b090861)


![img4](https://github.com/user-attachments/assets/3e74ad4a-67f7-4900-b39e-b6a63bab61b8)


![img5](https://github.com/user-attachments/assets/880bd31f-db4f-4e43-98af-593ba1accea9)


![img6](https://github.com/user-attachments/assets/df904537-fdcc-4827-9db9-a0c276e3e3d0)


![img7](https://github.com/user-attachments/assets/d3e16f89-bf33-4d98-9872-0e06d6941467)


![img8](https://github.com/user-attachments/assets/6119a432-b688-44cd-951c-c347a554c4db)

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
