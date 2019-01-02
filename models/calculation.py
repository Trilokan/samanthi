# -*- coding: utf-8 -*-


def purchase_calculation(unit_price, quantity, discount, tax, tax_state):
    price = unit_price * quantity

    discount_amount = price * float(discount)/100
    discounted_amount = price - discount_amount

    tax_amount = discounted_amount * float(tax)/100

    cgst = sgst = igst = 0
    if tax_state == 'inter_state':
        igst = tax_amount
    elif tax_state == 'outer_state':
        cgst = sgst = tax_amount / 2

    return {"cgst": cgst,
            "sgst": sgst,
            "igst": igst,
            "discount_amount": discount_amount,
            "tax_amount": tax_amount,
            "total_amount": price}


def get_list_year():
    """ Get Year list as the char """
    year_list = []

    START_YEAR = 2016
    END_YEAR = 2022

    for year in range(2016, 2022):
        year_list.append(str(year))

    return year_list

