import math
import argparse

def check_error_on_args(args):
    # this function to check error on input paramaters
    # still missing the negativity checking -> need to add later
    if (args['type'] not in ['annuity', 'diff']) \
            or (args['type'] == 'diff' and args['payment'] is not None) \
            or (args['interest'] is None) \
            or len([x for key, x in args.items()]) - [x for key, x in args.items()].count(None) < 4 \
            or (check_negativity_parameter(args)):
        print("Incorrect parameters")
        exit()


def check_negativity_parameter(args):
    for key, value in args.items():
        try:
            if float(value) < 0:
                return True
        except:
            pass

def plural_text(n, text):
    # this function to check the number and add s to end of text
    # doesn't work with es, need more rule to work with es
    output = ''
    if n == 0:
        pass
    elif n > 1:
        text += 's'
    output = str(n) + ' ' + text
    return output


def convert_month_year_to_message(total_months):
    # this function to convert total months to years and month
    # for example: 15 months -> 1 year 3 months

    years = total_months // 12
    months = total_months - years * 12

    years_msg = '' if years == 0 else str(years) + ' year' + ('s' if years > 1 else '')
    months_msg = '' if months == 0 else str(months) + ' month' + ('s' if months > 1 else '')
    conjunction = '' if years == 0 or months == 0 else ' and '

    return 'It will take {}{}{} to repay this loan!'.format(years_msg, conjunction, months_msg)

def calculate_payments_list_at_month(p, n,i):
    payments = []
    for m in range (1,n+1):
        payments.append(math.ceil( p/n + i*(p- p*(m-1)/n)))
    return payments

def calculate_overpayment(principal, payments):
    return int(sum(payments) - principal)


parser = argparse.ArgumentParser(prog='Loan calculator',
                                 description='Calculate Annuity or differential payment')

parser.add_argument('--type')
parser.add_argument('--principal')
parser.add_argument('--periods')
parser.add_argument('--interest')
parser.add_argument('--payment')

args = vars(parser.parse_args())
type = args['type']
check_error_on_args(args)

##start processing data if no error on parameter
##Type = Annuity

if type == 'annuity':
    if args['payment'] is None:  # calculate payment
        principal = float(args['principal'])
        periods = int(args['periods'])
        interest = float(args['interest']) / 100 / 12
        payment = math.ceil(
            principal * (interest * math.pow(1 + interest, periods) / (math.pow(1 + interest, periods) - 1)))
        print('Your annuity payment = {}!'.format(payment))
        print('Overpayment = {}'.format(int(payment * periods - principal)))
    elif args['principal'] is None:
        payment = float(args['payment'])
        periods = int(args['periods'])
        interest = float(args['interest']) / 100 / 12
        principal = math.ceil(
            payment / (interest * math.pow(1 + interest, periods) / (math.pow(1 + interest, periods) - 1)))
        print('Your loan principal = {}!'.format(principal))
        print('Overpayment = {}'.format(math.ceil(payment * periods - principal)))
    elif args['periods'] is None:
        principal = float(args['principal'])
        payment = float(args['payment'])
        interest = float(args['interest']) / 100 / 12
        periods = math.ceil(math.log(payment / (payment - interest * principal), 1 + interest))
        print(convert_month_year_to_message(total_months=periods))
        print('Overpayment = {}'.format(math.ceil(payment * periods - principal)))

elif type == 'diff':
    #even through we checked the type in ['diff','annuity'] so we only need else here
    # I still put elif for clarification and maybe future change
    principal = float(args['principal'])
    periods = int(args['periods'])
    interest = float(args['interest']) / 100 / 12
    payments = calculate_payments_list_at_month(principal,periods,interest)
    for i in range(len(payments)):
        print('Month {}: payment is {}'.format(i+1,payments[i]))
    print('Overpayment = {}'.format(calculate_overpayment(principal,payments)))
