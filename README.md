# Spendings-Tracker

## Basic Informations
Function: Records how much money the user has spent.  
Language: Python  
Features:
- Add/Delete records.  
- Add/Delete categories.  
- Find records based on category/year&month.  
- Organize records based on date&time/category/description/amount.  
- Displays current records, categories and balance.  

## How the Code Works?
The code is divided into three sections (pymoney, pyrecord, and pycategory).  
Each sections has their own uses, such as:  
- pymoney: deals with the GUI  
- pyrecord: deals with the records  
- pycategory: deals with the categories  

### pyrecord.py
The pyrecord.py file consists of 2 classes, Records and Record. The Record class here is used as a new data type which will contain the attributes category, description, amount, date and time. The Record class also have several methods which uses the property decorator so that the program can get the value of each attributes without letting the user change its value. The Records class here is the main class for storing all the data which the user inputs. Basically, the Records class is just a list of Record which has the function to add, delete, organize, find, view and save records. The saved records will later on go into the records.txt file, where the first line will be the current balance and the other lines will be the records inputted by the user in the format of [Category] [Description] [Amount] [Date] [Time].  

### pycategory.py
The pycategory.py file only contains 1 class, which is the Categories class. By default, the application will have 2 main categories (expense and income), 4 sub-categories (food, transportation, salary and bonus) and 5 sub-sub-categories (meal, snack, drink, bus, railway). The Categories class have several methods that can add, delete, find and save categories. The saved categories will later on go into the categories.txt file, where the format of each line will be [level] [name] (level is an integer which tells the program whether it is a main category, sub-categories, sub-sub-categories or others, 0 being the main category).  

### pymoney.py
The pymoney.py is the main code for the application, since that everything that is related with the GUI of the application is written here. I used the tkinter module to make the GUI, which consists of:  
- Label
- Entry Box
- Button
- Check Button
- Radio Button
- Scrollbar
- List Box
- Combo Box

## Final Result
![GUI.png] (https://github.com/jadenliu12/Spendings-Tracker/blob/main/GUI.png)
