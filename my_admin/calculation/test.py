from _decimal import Decimal

if __name__ == '__main__':
    insert_sql = """INSERT INTO `calculation` (`name`, `electric_quantity`, `used_electricity`, `unit_price`, `amount`, `date_calculation`)
                        VALUES(%s, %s, %s, %s, %s, %s)"""
    print(Decimal(input("输入")))