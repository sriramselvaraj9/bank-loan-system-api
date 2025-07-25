def format_indian_currency(number):
    parts = str(number).split('.')
    integer = parts[0]
    decimal = '.' + parts[1] if len(parts) > 1 else ''

    if len(integer) > 3:
        start = integer[-3:]
        rest = integer[:-3]
        rest = ','.join([rest[max(i - 2, 0):i] for i in range(len(rest), 0, -2)][::-1])
        return rest + ',' + start + decimal
    else:
        return integer + decimal

print(format_indian_currency(123456.7891))
print(format_indian_currency(987654321.99))