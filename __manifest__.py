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

        "views/account/account.xml",
        "views/account/journal_entries.xml",
        "views/account/journal_items.xml",
        "views/account/customer_payment.xml",

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