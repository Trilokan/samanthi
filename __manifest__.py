# -*- coding: utf-8 -GPK*-

{
    "name": "SAMANTHI",
    "version": "1.0",
    "author": "La Mars",
    "website": "http://",
    "category": "SAMANTHI",
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
        "view/assert_backend.xml",

        # "sequence/account.xml",
        # "sequence/person.xml",
        # "sequence/hr.xml",

        "view/menu/main_menu.xml",

        # # Configuration
        # "view/configuration/product_configuration.xml",
        #
        # # Accounts
        # "view/account/account.xml",
        # "view/account/period.xml",
        # "view/account/journal_type.xml",
        #
        # # Product
        # "view/product/product.xml",
        # "view/product/product_group.xml",
        # "view/product/sub_group.xml",
        # "view/product/uom.xml",
        # "view/product/tax.xml",
        # "view/product/category.xml",
        #
        # # Stock
        # "view/stock/location.xml",
        # "view/stock/warehouse.xml",
        # "view/stock/move.xml",
        # "view/stock/stock_adjustment.xml",
        # "view/stock/store_request.xml",
        # "view/stock/store_issue.xml",
        # "view/stock/store_return.xml",
        # "view/stock/store_accept.xml",
        #
        # # Purchase
        #
        # # Human Resources
        # "view/hr/employee.xml",
        # "view/hr/department.xml",
        # "view/hr/designation.xml",
        # "view/hr/category.xml",
        # "view/hr/qualification.xml",
        # "view/hr/experience.xml",
        # "view/hr/address.xml",
        # "view/hr/identities.xml",
        #
        # # Time Management
        # "view/time_management/shift.xml",
        # "view/time_management/week_schedule.xml",
        # "view/time_management/monthly_attendance.xml",
        # "view/time_management/daily_attendance.xml",
        # "view/time_management/employee_attendance.xml",
        # "view/time_management/add_employee.xml",
        # "view/time_management/holiday_change.xml",
        # "view/time_management/shift_change.xml",
        # "view/time_management/time_sheet.xml",
        # "view/time_management/time_sheet_application.xml",
        # "view/time_management/work_detail.xml",
        # "view/configuration/time_configuration.xml",
        #
        # # Leave Management
        # "view/leave_management/leave_application.xml",
        # "view/leave_management/comp_off.xml",
        # "view/leave_management/permission.xml",
        # "view/leave_management/on_duty.xml",
        # "view/leave_management/leave_level.xml",
        # "view/leave_management/leave_type.xml",
        # "view/configuration/leave_configuration.xml",
        # # Payroll
        # # Recruitment

        # Reporting
        "view/report/sale.xml",

        # "view/menu/account.xml",
        # "view/menu/product.xml",
        # "view/menu/hr.xml",
        "view/menu/report.xml",

    ],
    "demo": [

    ],
    "qweb": [

    ],
    "installable": True,
    "auto_install": False,
    "application": True,
}