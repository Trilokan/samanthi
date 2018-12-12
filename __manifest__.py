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
        "sequence/hr.xml",

        "views/base/company.xml",
        "views/base/users.xml",
        "views/base/person.xml",
        "views/base/patient.xml",
        "views/base/person_type.xml",

        # Hospitality
        "views/hospitality/admission.xml",
        "views/hospitality/discharge.xml",
        "views/hospitality/bed_status.xml",
        "views/hospitality/ambulance.xml",
        "views/hospitality/ward.xml",
        "views/hospitality/bed.xml",
        "views/hospitality/patient_shifting.xml",

        # # Operation
        "views/operation/operations.xml",
        "views/operation/ot_status.xml",
        "views/operation/operation_theater.xml",
        "views/operation/operation_type.xml",

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

        # Doctor
        "views/doctor/doctor_availability.xml",
        "views/doctor/duty_timings.xml",

        # Notes
        "views/notes/notes.xml",
        "views/notes/notification.xml",
        "views/notes/reminder.xml",

        # Employee
        "views/employee/employee.xml",
        "views/employee/hr_category.xml",
        "views/employee/hr_contact.xml",
        "views/employee/hr_department.xml",
        "views/employee/hr_designation.xml",
        "views/employee/hr_experience.xml",
        "views/employee/hr_qualification.xml",
        "views/employee/todo.xml",

        # Recruitment Management
        "views/recruitment/resume_bank.xml",
        "views/recruitment/vacancy_position.xml",
        "views/recruitment/appointment_order.xml",

        # Time Management
        "views/time_management/time_configuration.xml",
        "views/time_management/shift.xml",
        "views/time_management/week_schedule.xml",
        "views/time_management/attendance.xml",
        "views/time_management/shift_change.xml",
        "views/time_management/monthly_attendance.xml",
        "views/time_management/monthly_attendance_wiz.xml",
        "views/time_management/add_employee.xml",
        "views/time_management/time_sheet.xml",
        "views/time_management/time_sheet_application.xml",
        "views/time_management/holiday_change.xml",

        # Leave  Management
        "views/leave_management/leave_application.xml",
        "views/leave_management/comp_off.xml",
        "views/leave_management/permission.xml",
        "views/leave_management/leave_configuration.xml",
        "views/leave_management/leave_level.xml",
        "views/leave_management/leave_type.xml",
        "views/leave_management/leave_availability.xml",

        # Leave Account
        "views/leave_account/leave_account.xml",
        "views/leave_account/leave_journal_entry.xml",
        "views/leave_account/leave_journal_item.xml",
        "views/leave_account/leave_reconcile.xml",
        "views/leave_account/leave_voucher.xml",
        
        # Payroll
        "views/payroll/hr_pay_update_wiz.xml",
        "views/payroll/hr_pay.xml",
        "views/payroll/payroll_generation.xml",
        "views/payroll/payslip.xml",
        "views/payroll/salary_rule.xml",
        "views/payroll/salary_rule_slab.xml",
        "views/payroll/salary_structure.xml",

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
        "views/asserts/asserts_capitalisation.xml",
        "views/asserts/hos_asserts.xml",
        "views/asserts/asserts_notification.xml",
        "views/asserts/asserts_maintenance.xml",

        # Purchase
        "views/purchase/indent.xml",
        "views/purchase/purchase_quotation.xml",
        "views/purchase/purchase_order.xml",
        "views/purchase/purchase_invoice.xml",
        "views/purchase/direct_material_receipt.xml",
        "views/purchase/material_receipt.xml",
        "views/purchase/material_inspection.xml",

        # Pharmacy

        # Invoice

        # Account
        "views/account/account.xml",
        "views/account/journal_entries.xml",
        "views/account/journal_items.xml",
        "views/account/customer_payment.xml",
        "views/account/reconciliation.xml",
        "views/account/journal.xml",
        "views/account/year.xml",
        "views/account/period.xml",

        # # Menu
        "views/menu/hospital.xml",
        "views/menu/contact.xml",
        # "views/menu/doctor.xml",
        # "views/menu/patient.xml",
        "views/menu/employee.xml",
        "views/menu/hr.xml",
        "views/menu/inventory.xml",
        "views/menu/purchase.xml",
        # "views/menu/pharmacy.xml",
        "views/menu/account.xml",

        "data/person_type.xml",
        "data/hr_category.xml",
        "data/time_management.xml",

    ],
    "demo": [

    ],
    "qweb": [

    ],
    "installable": True,
    "auto_install": False,
    "application": True,
}