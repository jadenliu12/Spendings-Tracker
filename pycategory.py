class Categories:
    """
    ADT representation of a category list with functions:
    Constructor         -- Get the categories list from "categories.txt"
    Add                 -- Add a new category into the current categories list
    Delete              -- Delete a category from the current categories list
    View                -- Display the current categories and subcategories
    Is_category_valid   -- Checks whether a category is inside the category list or not
    Find_subcategories  -- Find the subcategories of a category
    Save                -- Save the current category list into the file "categories.txt"
    """
    @staticmethod
    def find_next_idx(arr, left, right, val):
        """
        find_next_idx() function:
        Parameters      -- arr (list of tuples), left (int), right (int) and val (int)
        Function        -- Find the next index inside the list that has the same value as val
        Return          -- The next index of val if it exist, if it doesn't exist it will return right + 1 (int)
        """
        while left <= right:
            if arr[left][0] == val:
                return left
            left += 1
        return left
    
    @staticmethod
    def make_list(L):
        """
        make_list() function:
        Parameters      -- L (list of tuples)
        Function        -- Makes a list of lists out of a list of tuples where tuple[0] = level (int) and tuple[1] = key (str)
        Return          -- List of lists of categories
        """
        idx = 0
        res = []
        while idx < len(L)-1:
            if L[idx][0] != L[idx+1][0]:
                res.append(L[idx][1])
                next_idx = Categories.find_next_idx(L, idx+1, len(L)-1, L[idx][0])
                sub_cat = Categories.make_list(L[idx+1:next_idx])
                res.append(sub_cat)
                idx = next_idx
            elif L[idx][0] == L[idx+1][0]:
                res.append(L[idx][1])
                idx += 1
        if idx == len(L)-1:
            res.append(L[idx][1])

        return res
    

    @staticmethod
    def extend(L, idx = 0):
        """
        extend_() function:
        Parameters      -- L (list of lists) and idx (int) defaults to 0
        Function        -- Make a list of strings where the output will be formatted in [level] [string], level is how deep the current string is inside the list of lists
        Return          -- List
        """
        if type(L) == list:
            res = []
            for sub in L:
                res.extend(Categories.extend(sub, idx + 1))
            return res
        else:
            return [str(idx) + ' ' + L]    

    def __init__(self):
        """
        Constructor:
        Parameters      -- self
        Function        -- Open the 'categories.txt' file to retrieve the list of categories (if available)
                           Create a default list of categories (if 'categories.txt' is not available)
        """
        self._categories = []
        try:
            fh = open('categories.txt', 'r')
            cat_list = fh.readlines()
            cat_list = [x.rstrip('\n') for x in cat_list]
            cat_list = [x.split(' ') for x in cat_list]
            cat_list = [(int(x[0]), x[1]) for x in cat_list]
            self._categories = self.make_list(cat_list)
        except FileNotFoundError:
            self._categories = ['expense', ['food', ['meal', 'snack', 'drink'], 'transportation', ['bus', 'railway']], 'income', ['salary', 'bonus']]
    
    def add(self, target, desc, postin):
        """
        Add() method:
        Parameters      -- self and target (str), desc (str), postin (str)
        Function        -- Add a new category to the current categories list
        """
        try:
            if self.is_category_valid(target) and not self.is_category_valid(desc):
                cat_str = []
                depth = 0
                for cat in self._categories:
                    if type(cat) == list:
                        tmp_list = Categories.extend(cat)
                        for item in tmp_list:
                            if item.split()[1] == target:
                                depth = item.split()[0] 
                        cat_str.extend(tmp_list)
                    else:
                        cat_str.append('0 ' + cat)
            
                target_idx = 0
                target_cat = str(str(depth) + ' ' + target)
                new_cat = ""                
                if postin == 'post':
                    new_cat = str(str(int(depth) + 1) + ' ' + desc)
                elif postin == 'in':
                    new_cat = str(str(depth) + ' ' + desc)
                else:
                    raise ValueError

                for idx, cat in enumerate(cat_str):
                    if target_cat == cat:
                        target_idx = idx + 1
                        break
                
                cat_str.insert(target_idx, new_cat)
                cat_str = [x.split(' ') for x in cat_str]
                cat_str = [(int(x[0]), x[1]) for x in cat_str]

                self._categories = self.make_list(cat_str)
        except ValueError:
            print("Invalid input.\nFailed to add category")

    def delete(self, idx):
        """
        Delete() method:
        Parameters      -- selfa nd idx (int)
        Function        -- Delete the target category if it exists
        """
        try:
            cat_str = []
            for cat in self._categories:
                if type(cat) == list:
                    tmp_list = Categories.extend(cat)
                    cat_str.extend(tmp_list)
                else:
                    cat_str.append('0 ' + cat)
            
            if idx >= len(cat_str):
                raise ValueError

            cat_str.pop(idx)
            cat_str = [x.split(' ') for x in cat_str]
            cat_str = [(int(x[0]), x[1]) for x in cat_str]                

            self._categories = self.make_list(cat_str)
        except ValueError:
            print("Invalid input.\nFailed to delete category")

    def view(self):
        """
        view() method:
        Parameters      -- self
        Function        -- prints the category inside the categories list
        """
        def view_categories(L, tab = -1):
            """
            view_categories() function:
            Parameters      -- Categories (list) and amount of indentation (int) defaults to -1
            Function        -- Recursively prints the category inside the categories list
            Return          -- None
            """
            if L == None:
                return
            if type(L) == list:
                for sub in L:
                    view_categories(sub, tab+1)
            else:
                print(' '*2*tab + '- ' + L)

        view_categories(self._categories)

    def is_category_valid(self, target):
        """
        is_category_valid() method:
        Parameters      -- self and target (str)
        Function        -- Checks whether the category is inside the list of categories or not
        """
        def check_valid(category, categories):
            """
            check_valid() function:
            Parameters      -- Name of category (str) and list of categories (list of lists)
            Function        -- Checks whether the category is inside the list of categories or not
            Return          -- True (category is found) or False (category is not found)
            """
            if categories == None:
                return False
            if type(categories) == list:
                found = False
                for sub in categories:
                    found = found or check_valid(category, sub)
                return found
            else:
                if category == categories:
                    return True
                else:
                    return False

        return check_valid(target, self._categories)

    def find_subcategories(self, target):
        """
        find_subcategories() method:
        Parameters      -- self and target (str)
        Function        -- Search for the category and its subcategories
        """
        def find_subcategories_gen(category, categories, found = False):
            """
            find_subcategories_gen() function:
            Parameters      -- category (str) and categories (list of lists) and found (bool)
            Function        -- generates a list from a list of lists if category is found
            Return          -- A list
            """
            if type(categories) == list:
                for sub in categories:
                    yield from find_subcategories_gen(category, sub, found)
                    idx = categories.index(sub)
                    if sub == category and idx + 1 < len(categories) and type(categories[idx + 1]) == list and found == False:
                        yield from find_subcategories_gen(category, categories[idx : idx + 2], True)
            else:
                if category == categories or found == True:
                    yield categories

        return [i for i in find_subcategories_gen(target, self._categories)]

    def show(self):
        """
        show() method:
        Parameters      -- self
        Function        -- return a list of all its category
        """
        def extend_cat(L, idx = 0):
            """
            extend_categories() function:
            Parameters      -- L (list of lists) and idx (int) defaults to 0
            Function        -- Make a list of strings where the output will be formatted in [indent] [string], level is how deep the current string is inside the list of lists
            Return          -- List
            """
            if type(L) == list:
                res = []
                for sub in L:
                    res.extend(extend_cat(sub, idx + 1))
                return res
            else:
                return [idx*2*' ' + L]
        
        res = []
        for cat in self._categories:
            if type(cat) == list:
                tmp_list = extend_cat(cat)
                res.extend(tmp_list)
            else:
                res.append(cat)
        return res

    def save(self):
        """
        save_categories() method:
        Parameters      -- self
        Function        -- Save the current categories list to the file 'categories.txt'
        """
        def extend_categories(L, idx = 0):
            """
            extend_categories() function:
            Parameters      -- L (list of lists) and idx (int) defaults to 0
            Function        -- Make a list of strings where the output will be formatted in [level] [string], level is how deep the current string is inside the list of lists
            Return          -- List
            """
            if type(L) == list:
                res = []
                for sub in L:
                    res.extend(extend_categories(sub, idx + 1))
                return res
            else:
                return [str(idx) + ' ' + L + '\n']

        with open('categories.txt', 'w') as fh:
            cat_str = []
            for cat in self._categories:
                if type(cat) == list:
                    tmp_list = extend_categories(cat)
                    cat_str.extend(tmp_list)
                else:
                    cat_str.append('0 ' + cat + '\n')
            fh.writelines(cat_str)
