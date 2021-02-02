import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from pyrecord import Records
from pycategory import Categories
from datetime import date
import sys
import os

quit = False
rec_cnt = 1

if os.environ.get('DISPLAY','') == '':
    os.environ.__setitem__('DISPLAY', ':0.0')

def set_init_money():
    global balance_label
    tmp = init_money_str.get()
    if len(tmp) == 0:
        return
    new_bal = int(tmp)
    record.update_balance(new_bal)
    balance_label.configure(text = 'Now you have %d dollars.' % new_bal)

def add():
    global balance_label, date_label_str, category_list, desc_label_str, amount_label_str, record_box, rec_cnt, operation_radio_str, category_combobox
    
    if operation_radio_str.get() == "1":
        date = date_label_str.get()
        cat = category_list.get().replace(" ", "")
        desc = desc_label_str.get()
        amt = amount_label_str.get()

        if len(date) > 0:
            try:
                d = date.fromisoformat(date)
            except:
                messagebox.showerror('','Invalid date format.\nDate format: YYYY-MM-DD.')
                date_label_str.set("")
                category_list.set("")
                desc_label_str.set("")
                amount_label_str.set("")
                return
            else:
                record.add(' '.join([date, cat, desc, amt]), category)
        elif len(cat) > 0 and len(desc) > 0 and len(amt) > 0:
            if category.is_category_valid(cat):
                record.add(' '.join([cat, desc, amt]), category)
            else:
                messagebox.showerror('','Invalid category!\nPlease choose from the available cateogry.')
                date_label_str.set("")
                category_list.set("")
                desc_label_str.set("")
                amount_label_str.set("")
                return                
        else:
            return

        balance_label.configure(text = 'Now you have %d dollars.' % record.get_balance)
        record_box.insert(rec_cnt, record.get_last_record())
        rec_cnt += 1
        date_label_str.set("")
        category_list.set("")
        desc_label_str.set("")
        amount_label_str.set("")
    elif operation_radio_str.get() == "2":
        cat = category_list.get().replace(" ", "")
        desc = desc_label_str.get()
        postin = amount_label_str.get()

        if postin not in ['post', 'in'] and len(postin) > 0:
            messagebox.showerror('','pos/in order entry format:\n"post" or "in"')
            category_list.set("")
            desc_label_str.set("")
            amount_label_str.set("")
            return
        elif len(cat) > 0 and len(desc) > 0 and len(postin) > 0:
            category.add(cat, desc, postin)
        else:
            return

        record_box.delete(0, 'end')
        rec_cnt = 1
        for rec in category.show():
            record_box.insert(rec_cnt, rec)
            rec_cnt += 1        
        
        category_list.set("")
        desc_label_str.set("")
        amount_label_str.set("")        
        category_combobox['values'] = tuple(category.show())

def delete():
    global record_box, rec_cnt, balance_label, operation_radio_str, category_combobox
    
    if operation_radio_str.get() == "1":
        selected = record_box.curselection()
        if len(selected) > 0:
            for idx in selected:
                record.delete(idx)
            record_box.delete(idx)
            rec_cnt -= 1
            balance_label.configure(text = 'Now you have %d dollars.' % record.get_balance)
    elif operation_radio_str.get() == "2":
        selected = record_box.curselection()
        if len(selected) > 0:
            for idx in selected:
                category.delete(idx)
            record_box.delete(idx)
            rec_cnt -= 1
            category_combobox['values'] = tuple(category.show())

def find_record():
    global record_box, balance_label, find_category_str, cat_flag, ym_flag
    target = find_category_str.get()
    
    if len(target) == 0:
        return
    elif ym_flag.get() and cat_flag.get():
        messagebox.showerror('','Error!\nPlease only tick one box.\n')
        find_category_str.set('')    
    elif len(target) > 0 and cat_flag.get():
        if category.is_category_valid(target):
            record_box.delete(0, 'end')
            sub = category.find_subcategories(target)
            list_found, total = record.find(sub)
            tmp_idx = 1
            for item in list_found:
                record_box.insert(tmp_idx, item)
                tmp_idx += 1
            balance_label.configure(text = 'Total amount above is %d dollars.' % total)
    elif len(target) > 0 and ym_flag.get():
        tmp_list = target.split("-")
        if(len(tmp_list[0]) != 4 and len(tmp_list[1]) != 2):
            return
        record_box.delete(0, 'end')
        list_found, total = record.find_month(tmp_list[0], tmp_list[1])
        tmp_idx = 1
        for item in list_found:
            record_box.insert(tmp_idx, item)
            tmp_idx += 1
        balance_label.configure(text = 'Total amount above is %d dollars.' % total)       

def reset():
    global balance_label, date_label_str, category_list, desc_label_str, amount_label_str, record_box, rec_cnt, find_category_str,  cat_flag, ym_flag, category_checkbtn, ym_checkbtn, organize_list, operation_radio_str
    date_label_str.set("")
    category_list.set("")
    desc_label_str.set("")
    amount_label_str.set("")
    find_category_str.set("")
    organize_list.set("Date and time")
    category_checkbtn.select()
    ym_checkbtn.deselect()
    record.organize(1)
    record_box.delete(0, 'end')
    operation_radio_str.set("1")
    date_label_entry.configure(state = tk.NORMAL)
    find_category_entry.configure(state = tk.NORMAL)
    organize_by_combobox.configure(state = tk.NORMAL)
    category_checkbtn.configure(state = tk.NORMAL)
    ym_checkbtn.configure(state = tk.NORMAL)    
    balance_label.configure(text = 'Now you have %d dollars.' % record.get_balance)
    rec_cnt = 1
    for rec in record.get_records():
        record_box.insert(rec_cnt, rec)
        rec_cnt += 1

def organize_record():
    global balance_label, record_box, rec_cnt, organize_list
    chosen = organize_list.get()
    target = 0

    if chosen == 'Date and time':
        target = 1
    elif chosen == 'Category':
        target = 2
    elif chosen == 'Description':
        target = 3
    elif chosen == 'Amount':
        target = 4
   
    record_box.delete(0, 'end')
    balance_label.configure(text = 'Now you have %d dollars.' % record.get_balance)
    record.organize(target)
    rec_cnt = 1
    for rec in record.get_records():
        record_box.insert(rec_cnt, rec)
        rec_cnt += 1

def change_mode():
    global operation_radio_str, balance_label, date_label_entry, desc_label_entry, amount_label_entry, record_box, rec_cnt, init_money_str, amount_label, organize_by_combobox, category_checkbtn, ym_checkbtn

    if operation_radio_str.get() == '1':
        date_label_entry.configure(state = tk.NORMAL)
        find_category_entry.configure(state = tk.NORMAL)
        organize_by_combobox.configure(state = tk.NORMAL)
        category_checkbtn.configure(state = tk.NORMAL)
        ym_checkbtn.configure(state = tk.NORMAL)
        organize_list.set("Date and time")        
        amount_label.configure(text = "Amount")
        balance_label.configure(text = 'Now you have %d dollars.' % record.get_balance)
        record_box.delete(0, 'end')
        rec_cnt = 1
        for rec in record.get_records():
            record_box.insert(rec_cnt, rec)
            rec_cnt += 1    
    elif operation_radio_str.get() == '2':
        date_label_entry.configure(state = tk.DISABLED)
        find_category_entry.configure(state = tk.DISABLED)
        init_money_entry.configure(state = tk.DISABLED)  
        organize_by_combobox.configure(state = tk.DISABLED)
        category_checkbtn.configure(state = tk.DISABLED)
        ym_checkbtn.configure(state = tk.DISABLED)
        organize_list.set("Date and time")
        amount_label.configure(text = "post/in order")
        balance_label.configure(text = 'Current categories list.')        
        record_box.delete(0, 'end')
        rec_cnt = 1
        for rec in category.show():
            record_box.insert(rec_cnt, rec)
            rec_cnt += 1

record = Records()
category = Categories()

root = tk.Tk()
root.title('Pymoney')

f = tk.Frame(root, borderwidth = 5)
f.grid(row = 0, column = 0)

####### LEFT SIDE ###########

find_category_label = tk.Label(f, text = 'Find cateogry')
find_category_label.grid(row = 0, column = 0)

find_category_str =  tk.StringVar()
find_category_entry = tk.Entry(f, textvariable = find_category_str, width = 35)
find_category_entry.grid(row = 0, column = 1, columnspan = 4)

find_button = tk.Button(f, text = 'Find', command = find_record, width = 4)
find_button.grid(row = 0, column = 5)

reset_button = tk.Button(f, text = 'Reset', command = reset)
reset_button.grid(row = 0, column = 6)

cat_flag = tk.IntVar()
ym_flag = tk.IntVar()
category_checkbtn = tk.Checkbutton(f, text = 'By category', variable = cat_flag, onvalue = 1, offvalue = 0)
ym_checkbtn = tk.Checkbutton(f, text = 'By year and month', variable = ym_flag, onvalue = 1, offvalue = 0)
category_checkbtn.grid(row = 1, column = 0)
ym_checkbtn.grid(row = 1, column = 1)
category_checkbtn.select()

list_scrollbar = tk.Scrollbar(f, orient = 'vertical')
list_scrollbar.grid(row = 2, column = 7, rowspan = 7, sticky = 'ns')

record_box = tk.Listbox(f, width = 64, font = 'Courier 10', yscrollcommand = list_scrollbar.set)
record_box.grid(row = 2, column = 0, rowspan = 7, columnspan = 7)
for rec in record.get_records():
    record_box.insert(rec_cnt, rec)
    rec_cnt += 1

list_scrollbar.config(command = record_box.yview)

balance_label = tk.Label(f, text = 'Now you have %d dollars.' % record.get_balance)
balance_label.grid(row = 9, column = 0, columnspan = 3, sticky = 'W')

organize_list = tk.StringVar()
organize_list.set("Date and time")
organize_by_combobox = ttk.Combobox(f, width = 18, textvariable = organize_list)
organize_by_combobox['values'] = ("Date and time", "Category", "Description", "Amount")
organize_by_combobox.grid(row = 9, column = 4)

organize_button = tk.Button(f, text = 'Organize', width = 4, command = organize_record)
organize_button.grid(row = 9, column = 5)

delete_button = tk.Button(f, text = 'Delete', width = 4, command = delete)
delete_button.grid(row = 9, column = 6)

####### RIGHT SIDE ###########

operation_radio_str = tk.StringVar(f, 1)
record_radio_button = tk.Radiobutton(f, text = ' Record ', variable = operation_radio_str, value = 1, indicator = 0, command = change_mode)
record_radio_button.grid(row = 1, column = 9, columnspan = 2, sticky = 'E')
category_radio_button = tk.Radiobutton(f, text = 'Category', variable = operation_radio_str, value = 2, indicator = 0, command = change_mode)
category_radio_button.grid(row = 1, column = 11, columnspan = 2, sticky = 'W')

init_money_label = tk.Label(f, text = 'Initial money')
init_money_label.grid(row = 2, column = 8)

init_money_str = tk.StringVar()
init_money_entry = tk.Entry(f, textvariable = init_money_str)
init_money_entry.grid(row = 2, column = 9, columnspan = 4)
if record.get_balance > 0:
    init_money_entry.configure(state = tk.DISABLED)

update_button = tk.Button(f, text = 'Update', command = set_init_money)
update_button.grid(row = 3, column = 12, sticky = 'E')

date_label = tk.Label(f, text = 'Date')
date_label.grid(row = 4, column = 8)

date_label_str = tk.StringVar()
date_label_entry = tk.Entry(f, textvariable = date_label_str)
date_label_entry.grid(row = 4, column = 9, columnspan = 4)

category_label = tk.Label(f, text = 'Category')
category_label.grid(row = 5, column = 8)

category_list = tk.StringVar()
category_combobox = ttk.Combobox(f, width = 18, textvariable = category_list)
category_combobox['values'] = tuple(category.show())
category_combobox.grid(row = 5, column = 9, columnspan = 4)

desc_label = tk.Label(f, text = 'Description')
desc_label.grid(row = 6, column = 8)

desc_label_str = tk.StringVar()
desc_label_entry = tk.Entry(f, textvariable = desc_label_str)
desc_label_entry.grid(row = 6, column = 9, columnspan = 4)

amount_label = tk.Label(f, text = 'Amount')
amount_label.grid(row = 7, column = 8)

amount_label_str = tk.StringVar()
amount_label_entry = tk.Entry(f, textvariable = amount_label_str)
amount_label_entry.grid(row = 7, column = 9, columnspan = 4)

add_button = tk.Button(f, text = 'Add', width = 6, command = add)
add_button.grid(row = 8, column = 12, sticky = 'E')

tk.mainloop()
quit = True
record.save()
category.save()
