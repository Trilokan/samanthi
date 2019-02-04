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
        "sequence/account.xml",
        "view/account/account.xml",
        "view/account/journal_type.xml",

        # Product
        "view/product/product.xml",
        "view/product/product_group.xml",
        "view/product/sub_group.xml",
        "view/product/uom.xml",
        "view/product/tax.xml",
        "view/product/category.xml",

        # Stock
        "view/stock/location.xml",
        "view/stock/warehouse.xml",
        "view/stock/move.xml",

    ],
    "demo": [

    ],
    "qweb": [

    ],
    "installable": True,
    "auto_install": False,
    "application": True,
}