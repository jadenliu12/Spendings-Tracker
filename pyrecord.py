from datetime import date
from datetime import datetime
import re

class Record:
    """
    ADT representation of a record
    """
    def __init__(self, category, description, amount, date, time):
        """
        Constructor:
        Parameters      -- self, category (str), description (str) and amount (int)
        Function        -- Initialize a record class
        """
        self._category = category
        self._description = description
        self._amount = amount
        self._date = date
        self._time = time

    @property
    def get_cat(self):
        """
        get_cat() method:
        Parameters      -- self
        Function        -- get the current category
        """
        return self._category

    @property
    def get_desc(self):
        """
        get_desc() method:
        Parameters      -- self
        Function        -- get the current description
        """
        return self._description

    @property
    def get_amt(self):
        """
        get_amt() method:
        Parameters      -- self
        Function        -- get the current amount
        """
        return self._amount

    @property
    def get_date(self):
        """
        get_date() method:
        Parameters      -- self
        Function        -- get the current date
        """
        return self._date

    @property
    def get_time(self):
        """
        get_time() method:
        Parameters      -- self
        Function        -- get the current time
        """
        return self._time


class Records:
    """
    ADT representation of a record with functions:
    Constructor         -- Read in data from 'records.txt'
    Add                 -- Add in new record to the current records
    Delete              -- Delete a record from the current records
    Organize            -- Organize the current records based on date and time/description/category/amount
    Find                -- Find all the records under the target category
    Save                -- Save the current records to the file 'records.txt'
    """

    def __init__(self):
        """
        Constructor:
        Parameters      -- self
        Function        -- Open the 'records.txt' file to retrieve the records data of previous input (if available)
                           Ask the user to input initial balance (if 'records.txt' is not available)
        """
        self._record = []
        try:
            fh = open('records.txt', 'r')
            try:
                self._balance = int(fh.readline())
                for line in fh.readlines():
                    tmp_list = line.split(' ')
                    tmp_list[2] = int(tmp_list[2])
                    tmp_list[4] = tmp_list[4].rstrip("\n")
                    self._record.append(Record(tmp_list[0], tmp_list[1], tmp_list[2], tmp_list[3], tmp_list[4]))
            except ValueError:
                self._balance = 0
            fh.close()
        except FileNotFoundError:
            self._balance = 0

    def update_balance(self, balance):
        """
        update_balance() method:
        Parameter       -- self and balance (int)
        Function        -- update the initial balance
        """
        self._balance = balance

    @property
    def get_balance(self):
        """
        get_balance() method:
        Parameter       -- self
        Function        -- return the current balance
        """
        return self._balance

    def add(self, record, categories):
        """
        add() method:
        Parameters      -- Self, record (str) and categories (class object)
        Function        -- Add a new record to the current record (if format is correct)
        """
        try:
            today = date.today()
            now = datetime.now()

            d = today.strftime("%Y-%m-%d")
            t = now.strftime("%H:%M:%S")
            
            tmp_list = record.split(' ')

            if len(tmp_list) == 4:
                try:
                    d = date.fromisoformat(tmp_list[0])
                    tmp_list.pop(0)
                except:
                    raise NameError
            

            if len(tmp_list) != 3 and len(tmp_list) != 4:
                raise IndexError
            assert categories.is_category_valid(tmp_list[0])
            
            tmp_list[2] = int(tmp_list[2])
            self._balance += tmp_list[2]
            tmp_list.append(str(d))
            tmp_list.append(t)
            self._record.append(Record(tmp_list[0], tmp_list[1], tmp_list[2], tmp_list[3], tmp_list[4]))
        except AssertionError:
            print('The specified category is not in the category list.\nYou can check the category list by command "view categories".')
            print("Fail to add a record.")
        except IndexError:
            print("The format of a record should be like this: [Cat] [Desc] [Amount].\nFail to add a record.")
        except ValueError:
            print("Invalid value for amount.\nFail to add a record.")
        except NameError:
            print("The format of a date should be YYYY-MM-DD.\nFail to add a record.")

    def delete(self, idx):
        """
        delete() method:
        Parameters      -- self and idx (int)
        Function        -- Delete a record from the current record (if format is correct)
        """
        self._balance -= self._record[idx].get_amt
        self._record.pop(idx)

    def organize(self, choice):
        """
        organize() method:
        Parameters      -- self and chocie (str)
        Function        -- Organize the record based on Date and Time/Category/Description/Amount
        """
        if choice == 1:
            self._record.sort(key = lambda tup: (tup.get_date, tup.get_time))
        elif choice == 2:
            self._record.sort(key = lambda tup: tup.get_cat)
        elif choice == 3:
            self._record.sort(key = lambda tup: (tup.get_desc.upper(), tup.get_desc))
        elif choice == 4:        
            self._record.sort(key = lambda tup: tup.get_amt)

    def find(self, target):
        """
        find() method:
        Parameters      -- self and target (list)
        Function        -- Print out the list of records that is included in the inputted category (if available)
                           Print out an error message (if category inputted is not available)
        """
        tmp_records = filter(lambda n: n.get_cat in target, self._record)
        tmp_records = list(tmp_records)

        total = 0
        tmp_list = []
        if len(tmp_records) > 0:
            for item in tmp_records:
                total += item.get_amt
                tmp_list.append(f'{item.get_date} {item.get_time} {item.get_cat : <16} {item.get_desc : <15} {str(item.get_amt) : >11}')        

        return tmp_list, total

    def find_month(self, year, month):
        """
        find_month() method:
        Parameters      -- self, year (int) and month (int)
        Function        -- Print out all the records that are inputted during the targeted month and year
        """

        tmp_records = []
        for item in self._record:
            tmp = item.get_date.split('-')
            if(tmp[0] == year and tmp[1] == month):
                tmp_records.append(item)
        
        total = 0
        tmp_list = []
        if len(tmp_records) > 0:
            for item in tmp_records:
                total += item.get_amt
                tmp_list.append(f'{item.get_date} {item.get_time} {item.get_cat : <16} {item.get_desc : <15} {str(item.get_amt) : >11}')
        return tmp_list, total
    
    def get_records(self):
        """
        get_records() method:
        Parameters      -- self
        Function        -- return a list of records
        """
        tmp_list = []
        for item in self._record:
            tmp_list.append(f'{item.get_date} {item.get_time} {item.get_cat : <16} {item.get_desc : <15} {str(item.get_amt) : >11}')
        return tmp_list
    
    def get_last_record(self):
        """
        get_last_record() method:
        Parameters      -- self
        Function        -- return a string version of the lastly added record
        """
        item = self._record[-1]
        tmp_str = f'{item.get_date} {item.get_time} {item.get_cat : <16} {item.get_desc : <15} {str(item.get_amt) : >11}'
        return tmp_str

    def save(self):
        """
        save() method:
        Parameters      -- self
        Function        -- Save the current records to 'records.txt'
        """
        with open('records.txt', 'w') as fh:
            fh.write(str(self._balance) + '\n')
            record_list = []
            for item in self._record:
                tmp_str = item.get_cat + ' ' + item.get_desc + ' ' + str(item.get_amt) + ' ' + item.get_date + ' ' + item.get_time + '\n'
                record_list.append(tmp_str)
            fh.writelines(record_list)


