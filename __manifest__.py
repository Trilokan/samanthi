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
        "views/assert_backend.xml",
        "views/menu/menu.xml",

        "sequence/account.xml",
        "sequence/product.xml",

        "views/base/person.xml",

        # Account
        "views/account/account.xml",
        "views/account/journal_entries.xml",
        "views/account/journal_items.xml",
        "views/account/customer_payment.xml",
        "views/account/reconciliation.xml",

        # Product
        "views/product/product_group.xml",
        "views/product/sub_group.xml",
        "views/product/uom.xml",
        "views/product/tax.xml",
        "views/product/product_category.xml",
        "views/product/product_configuration.xml",
        "views/product/product.xml",

        # Stock
        "views/stock/stock_location.xml",
        "views/stock/stock_warehouse.xml",
        "views/stock/hos_move.xml",
        "views/stock/stock_adjustment.xml",
        "views/stock/store_request.xml",
        "views/stock/store_issue.xml",
        "views/stock/store_return.xml",
        "views/stock/store_accept.xml",

        # Asserts
        "views/asserts/hos_asserts.xml",
        "views/asserts/asserts_notification.xml",
        "views/asserts/asserts_maintenance.xml",
        
        # Purchase
        "views/purchase/indent.xml",

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
        "views/leave_management/leave_configuration.xml",
        "views/leave_management/leave_level.xml",
        "views/leave_management/leave_type.xml",

        # Recruitment Management
        "views/recruitment/resume_bank.xml",
        "views/recruitment/vacancy_position.xml",
        "views/recruitment/appointment_order.xml",

        # Time Management
        # Time Management

        "views/menu/contact.xml",
        "views/menu/appointment.xml",
        "views/menu/employee.xml",
        "views/menu/account.xml",
        "views/menu/product.xml",
        "views/menu/hr.xml",
    ],
    "demo": [

    ],
    "qweb": [

    ],
    "installable": True,
    "auto_install": False,
    "application": True,
}