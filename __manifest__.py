# -*- coding: utf-8 -GPK*-

{
    "name": "Shesha",
    "version": "1.0",
    "author": "La Mars",
    "website": "http://",
    "category": "Nagini",
    "sequence": 1,
    "summary": "Hospital Management System",
    "description": """

    Hospital Management System

    Patient Management
    Employee Management
    Purchase Management
    Pharmacy Management
    Assert Management
    Accounts Management

    """,
    "depends": ["base", "mail"],
    "data": [

        "views/menu/menu.xml",

        "sequence/account.xml",

        # Account
        "views/account/account.xml",
        "views/account/journal_entries.xml",
        "views/account/journal_items.xml",
        "views/account/customer_payment.xml",
        "views/account/reconciliation.xml",

        # Contact
        "views/contact/doctor.xml",
        "views/contact/patient.xml",
        "views/contact/nurse.xml",
        "views/contact/staff.xml",
        "views/contact/driver.xml",
        "views/contact/supplier.xml",
        "views/contact/service.xml",
        "views/contact/others.xml",

        # Appointment
        "views/appointment/opt.xml",
        "views/appointment/ot.xml",
        "views/appointment/meetings.xml",

        # Employee
        "views/employee/employee.xml",
        "views/employee/hr_category.xml",
        "views/employee/hr_contact.xml",
        "views/employee/hr_department.xml",
        "views/employee/hr_designation.xml",
        "views/employee/hr_experience.xml",
        "views/employee/hr_qualification.xml",
        
        # Notes
        "views/notes/notes.xml",
        "views/notes/notification.xml",
        "views/notes/reminder.xml",

        # Time Management

        # Leave  Management
        "views/leave_management/leave_application.xml",
        "views/leave_management/comp_off.xml",
        "views/leave_management/permission.xml",

        # Recruitment Management
        # Time Management
        # Time Management

        "views/menu/contact.xml",
        "views/menu/appointment.xml",
        "views/menu/employee.xml",
        "views/menu/account.xml",
    ],
    "demo": [

    ],
    "qweb": [

    ],
    "installable": True,
    "auto_install": False,
    "application": True,
}