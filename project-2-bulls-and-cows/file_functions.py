'''
Functions that contain file operations.
'''

import os


def get_current_dir(end_slash:bool = False) -> str:
    '''
    Get absolute path to dir for current file default without slash and the end.

        Parameters:
            end_slash (bool)  --  add slash (os.sep) at the end
             
        Return:
            path_to_current_file (str) -- absolute path to dir 
    '''
    path_to_current_dir = os.path.dirname(os.path.realpath(__file__))

    if end_slash:
        path_to_current_dir += os.sep
        
    return path_to_current_dir 


def remove_first_slash(args: list[str]) -> list[str]:
    '''
    Remove slash '/' or " \ " or any not alnum character on the begining of the string.
    '''
    for index, item in enumerate(args):
        if not item[0].isalnum():
            args[index] = item[1:]

    return args


def create_abs_path(*args: str) -> str:
    '''
    Create absolute path from arguments.
    Dont use first slash in arguments if you use it it will be removed.
               
        Parameters:
            *args (str) -- name of file
        
        Result:
            path_to_file (str) -- absolute path to file 
    '''
    args = remove_first_slash(list(args))

    path_to_file = get_current_dir(end_slash=True) + os.path.join(*args)

    return path_to_file


def create_rel_path(*args:str) -> str:
    '''
    Create relative path from arguments.
    '''
    args = remove_first_slash(list(args))

    return os.path.join(*args)


def create_dir(dir_name: str):
    '''
    Create directory
    '''
    return os.mkdir(dir_name)


def is_file(file: str) -> bool:
    '''
    Check if file exist from realtive path.
    Relative path will be transfered to absolute path.
    '''
    return os.path.isfile(create_abs_path(file))


def is_dir(dir: str) -> bool:
    '''
    From realtive path check if dir exist.
    Relative path will be transfered to absolute path.
    '''
    return os.path.isdir(create_abs_path(dir))


def get_all_type_files(dir: str = ".",
                       extension: str = "txt"
                       ) -> list[str]:
    '''
    Return all files on dir with specific extension.
    '''
    files = os.listdir(dir)
    
    list_of_files = []
    for file in files:
        #[1] return tuple ('file_name', '.txt')
        #[1:] looking only for txt without dot
        if os.path.splitext(file)[1][1:] == extension:
            list_of_files.append(file)
        
    return list_of_files


def get_lines_from_file(file: str) -> list[str]:
    '''
    Return all lines from file as list. Put realtive path to the file.\n
    ['201\\n', '20\\n', '210\\n', '120\\n', '\\n']

        Parameters:
            file (str)  --  relative path to the file
    '''

    if not is_file(file):
        print(f"File '{file}' dont exist.")
        clear_file(file)
        print(f"We must create empty file with name {file}")
    
    file_abs_path = create_abs_path(file)
    
    with open(file_abs_path, mode="r", encoding="UTF-8") as f:
        list_of_lines = f.readlines()
        
    return list_of_lines


def remove_new_line_from_list(list_of_items: list[str]) -> list[str]:
    '''
    Remove new line ("\\n") character items from list.
    
        Example:
            from ["201\\n", "102\\n", "\\n"]\n
            to ["201", "102"]
    '''
    new_list = []
    
    for item in list_of_items:
        if item.strip(): 
            # if we removed new line character and item is not empty
            new_list.append(item.strip())

    return new_list


def get_last_item_from_list(list_of_items: list[str]) -> str:
    '''
    Return last not empty item from list.
    The list will be reversed and you get first element.
    Remove new line from items.
    '''

    if not list_of_items:
        return list_of_items

    # this reverse() metod its not be as argument on the function bellow
    # otherwise give us error, because give None
    list_of_items.reverse()

    last_non_empty_item = remove_new_line_from_list(list_of_items)[0]

    return last_non_empty_item


def get_last_item_from_file(file: str) -> str:
    '''
    Get last line from file, enter relative path to file.
    '''
    return get_last_item_from_list(get_lines_from_file(file))


def create_file_prefix(prefix: str, sep: str = "_", file_name: str = None) -> str:
    '''
    Create only prefix as default or you can create file name with prefix if 
    you enter file name.
    '''
    
    file_with_prefix = ""
    prefix = prefix.lower().replace(" ", "")
    
    if file_name:
        file_with_prefix = prefix + sep + file_name
    else:
        file_with_prefix = prefix + sep
        
    return file_with_prefix


def create_file_sufix(sufix: str, sep: str = "_", file_name: str = None) -> str:
    '''
    Create only sufix as default or you can create file name with sufix if 
    you enter file name.
    '''

    file_with_sufix = ""
    sufix = sufix.lower().replace(" ", "")
    
    if file_name:
        file_with_sufix = file_name + sep + sufix
    else:
        file_with_sufix = sep + sufix
    
    return file_with_sufix


def create_file_name(file_name: str,
                     extension: str = "txt",
                     prefix: str = None,
                     sufix: str = None,
                     sep: str = "_") -> str:
    '''
    Crete file name. You can set prefix, sufix and extension.

        Parameters:
            extension (str)  --  extension without dot
    '''
    # file_name = name

    if prefix:
        file_name = create_file_prefix(prefix=prefix, sep=sep) + file_name
        
    if sufix:
        file_name += create_file_sufix(sufix=sufix, sep=sep)
        
    if not prefix and not sufix:
        file_name = file_name
    
    file_name += "." + extension.strip(".")
    
    return file_name.lower()


def write_to_file(file: str, message: str, header: str = None) -> bool:
    '''
    Append text to file. This function don check if file exist.
    '''
    with open(create_abs_path(file), mode="w", encoding="UTF-8") as f:
        header and f.write(header + "\n") # if else ternary without else
        f.write(message + "\n")


def append_to_file(file: str, message: str) -> bool:
    '''
    Append text to file. This function don check if file exist.
    Enter relative path to file.
    '''
    with open(create_abs_path(file), mode="a", encoding="UTF-8") as f:
        f.write(message + "\n")


def clear_file(file: str) -> None:
    '''
    Clear all data from file or if file dont exist create new file.
    Enter relative path to file.
    '''
    open(create_abs_path(file), "w").close()



if __name__ == "__main__":
    pass