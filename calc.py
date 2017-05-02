#!/usr/bin/env python3

import math


class Error(Exception):
    """Base exception for Calculator

    All other exceptions are based on this one.
    In case code needs to catch only Calculator's produced exceptions.
    """
    pass


class BadOperator(Error):
    """Bad operator exception for Calculator"""
    pass


class BadValue(Error):
    """Bad value exception for Calculator"""
    pass


class UnaryOperatorHandler(object):
    """Unary operator handler

    All of the methods may be static also. Depends on requirements.
    """

    def handle(self, op, v):
        """Base handler for all other unary operators

        Expects operator and value as a string
        Returns value as a string
        """
        f = getattr(self, 'handle_{op}'.format(op=op), None)
        if not f:
            raise BadOperator('Bad unary operator: {}'.format(op))
        return f(v)

    def operations(self):
        return [v[7:] for v in dir(self) if v.startswith('handle_')]

    def handle_sqrt(self, v):
        if v < 0:
            raise BadValue('Cannot sqrt: {}'.format(v))
        return math.sqrt(v)

    def handle_pow2(self, v):
        return math.pow(v, 2)

    def handle_reciproc(self, v):
        if v == 0:
            raise BadValue('Cannot divide by 0: {}'.format(v))


class BinaryOperatorHandler(object):
    """Binary operator handler

    Same as Unary, but 2 values
    """

    def handle(self, op, v1, v2):
        f = getattr(self, 'handle_{op}'.format(op=op), None)
        if not f:
            raise BadOperator('Bad binary operator: {}'.format(op))
        return f(v1, v2)

    def operations(self):
        return [v[7:] for v in dir(self) if v.startswith('handle_')]

    def handle_add(self, v1, v2):
        return v1 + v2

    def handle_sub(self, v1, v2):
        return v1 - v2

    def handle_mul(self, v1, v2):
        return v1 * v2

    def handle_div(self, v1, v2):
        if v2 == 0:
            raise BadValue('Cannot divide by 0: {}'.format(v2))
        return v1 / v2


class Calculator(object):
    """Dummy calculator

    It can be used as a class (delegate) for GUI or CUI calculator.
    These should have some kind of input methanism (event based or raw_input)
    and execute `on_` methods accordingly.

    Error handling is done in simple way.
    If more sophisticated error handling is needed `error()` may be overriden.

    Exceptions may be used also, to do so - set strict = True after
    initialization.

    No memory operations are implemented, but this is not a neuroscience.
    """

    def __init__(self, uoh=None, boh=None):
        """
        If needed, handlers for Unary operators and Binary operators
        may be extended to support Decimal or something else.
        All is needed it to pass new handlers to __init__ (delegate)
        """

        self.stored_op = ''
        self.result = '0'

        self.value = '0'
        self.clear_value = True

        if uoh is None:
            uoh = UnaryOperatorHandler()
        self.uoh = uoh

        if boh is None:
            boh = BinaryOperatorHandler()
        self.boh = boh

        self.strict = False

    def get_value(self):
        """Returns value on screen as number"""
        value = float(self.value)

        if value % 1 == 0:
            return int(value)
        return value

    def get_result(self):
        """Returns current result as number"""
        result = float(self.result)

        if result % 1 == 0:
            return int(result)
        return result

    def error(self, msg, reason=None):
        print('Error: {}'.format(msg))

    def on_digit(self, digit):
        if digit == '0' and self.value == '0':
            return

        if self.clear_value:
            self.value = ''
            self.clear_value = False

        self.value += str(digit)

    def on_sep(self):
        if '.' in self.value:
            self.error('Cannot have value with two seps')
            if self.strict:
                raise BadValue('Cannot have value with two seps')
            return

        if self.value == '':
            self.value = '0'

        self.value += '.'

    def on_sign(self):
        if self.value[0] == '-':
            self.value = self.value[1:]
        else:
            self.value = '-' + self.value

    def on_number(self, n):
        if n == '0' and self.value == '0':
            return

        if n % 1 == 0:
            n = int(n)

        self.value = str(n)
        self.clear_value = True

    def on_unary_op(self, op):
        try:
            value = self.uoh.handle(
                op,
                self.get_value())
            self.value = str(value)
            self.clear_value = True
        except Error as e:
            self.error(e)
            if self.strict:
                raise

    def on_binary_op(self, op):
        try:
            if self.stored_op != '':
                value = self.boh.handle(
                    self.stored_op,
                    self.get_result(),
                    self.get_value())
                self.value = str(value)
            self.result = self.value
            self.clear_value = True
            self.stored_op = op
        except Error as e:
            self.error(e)
            if self.strict:
                raise

    def on_equal(self):
        try:
            if self.stored_op != '':
                value = self.boh.handle(
                    self.stored_op,
                    self.get_result(),
                    self.get_value())
                self.value = str(value)

                self.result = self.value
                self.stored_op = ''
            self.clear_value = True
        except Error as e:
            self.error(e)
            if self.strict:
                raise

    def on_clear(self):
        if self.clear_value:
            return

        self.value = '0'
        self.clear_value = True

    def on_clear_all(self):
        self.stored_op = ''
        self.result = '0'

        self.value = '0'
        self.clear_value = True


class DiscoStyleUI(object):
    """This is for fun.

    If I would need to do CUI I would use click, curses or even urwid.
    If this is possible GUI is also possible.
    """
    debug = False

    def __init__(self, calc=None):
        """
        Calculator() may be extended and supplied throught `calc` argument
        to this UI e.g. Delegation pattern
        """

        if calc is None:
            calc = Calculator()
        self.calc = calc

    def menu_main(self):
        while True:
            if self.debug:
                print('Calculator result={}, '
                      'stored op={!r}, '
                      'clear_value={!r}'.format(self.calc.result,
                                                self.calc.stored_op,
                                                self.calc.clear_value))

            print('Calculator value: {}'.format(self.calc.get_value()))
            print('Calculator menu:')
            print('\t1. Digit...')
            print('\t2. Whole number...')
            print('\t3. Separator')
            print('\t4. Sign')
            print('\t5. Unary Op...')
            print('\t6. Binary Op...')
            print('\t7. Equal')
            print('\t8. Clear')
            print('\t9. Clear All')
            print('\t0. Quit')

            menu = input('Enter menu #: ')

            if menu == '1':
                self.menu_digit_input()
            elif menu == '2':
                self.menu_number_input()
            elif menu == '3':
                self.calc.on_sep()
            elif menu == '4':
                self.calc.on_sign()
            elif menu == '5':
                self.menu_unary_op()
            elif menu == '6':
                self.menu_binary_op()
            elif menu == '7':
                self.calc.on_equal()
            elif menu == '8':
                self.calc.on_clear()
            elif menu == '9':
                self.calc.on_clear_all()
            elif menu == '0' or menu.lower() == 'q':
                break
            else:
                print('ERROR! Bad menu #, try again')

    def menu_digit_input(self):
        while True:
            print('Calculator::Digit sumbenu:')
            digit = input('Enter the digit (ENTER to get back): ')
            if len(digit) == 0:
                break

            if not digit.isdigit():
                print('ERROR! Input is not a digit, try again')
                continue

            if len(digit) != 1:
                print('ERROR! Only one digit please, try again')
                continue

            self.calc.on_digit(digit)
            break

    def menu_number_input(self):
        while True:
            print('Calculator::Number sumbenu:')
            number = input('Enter the number (ENTER to get back): ')
            if len(number) == 0:
                break

            try:
                v = float(number)
            except ValueError:
                print('ERROR! Input is not a number, try again')
                continue

            self.calc.on_number(v)
            break

    def menu_unary_op(self):
        while True:
            print('Calculator::Unary operator sumbenu:')
            print('\t1. Square root')
            print('\t2. Power of two')
            print('\t3. 1/x')
            print('\t4. <-Back')

            submenu = input('Enter submenu #: ')

            if submenu == '1':
                self.calc.on_unary_op('sqrt')
                break
            elif submenu == '2':
                self.calc.on_unary_op('pow2')
                break
            elif submenu == '3':
                self.calc.on_unary_op('reciproc')
                break
            elif submenu == '4':
                break
            else:
                print('ERROR! Bad submenu #, try again')

    def menu_binary_op(self):
        while True:
            print('Calculator::Binary operator sumbenu:')
            print('\t1. Add')
            print('\t2. Subtract')
            print('\t3. Multiply')
            print('\t4. Divide')
            print('\t5. <-Back')

            submenu = input('Enter submenu #: ')

            if submenu == '1':
                self.calc.on_binary_op('add')
                break
            elif submenu == '2':
                self.calc.on_binary_op('sub')
                break
            elif submenu == '3':
                self.calc.on_binary_op('mul')
                break
            elif submenu == '4':
                self.calc.on_binary_op('div')
                break
            elif submenu == '4':
                break
            else:
                print('ERROR! Bad submenu #, try again')

    def run(self):
        return self.menu_main()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description='Calculator with Disco Style UI')

    parser.add_argument(
        '-d',
        '--debug',
        action='store_true',
        dest='debug',
        default=False,
        help='print debug')

    parser.add_argument(
        '-s',
        '--strict',
        action='store_true',
        dest='strict',
        default=False,
        help='raise exceptions on error')

    args = parser.parse_args()

    cui = DiscoStyleUI()

    cui.debug = args.debug
    cui.strict = args.strict
    cui.run()
