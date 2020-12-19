from consolemenu import SelectionMenu

from model import Model
from view import View

TABLES_NAMES = ['faculty', 'student', 'student_task', 'subject', 'task']
TABLES = {
    'faculty': ['id', 'name', 'number_of_students', 'foundation_date'],
    'student': ['id', 'fullname', 'email', 'course', 'faculty_id', 'student_group'],
    'student_task': ['id', 'student_id', 'task_id'],
    'subject': ['id', 'name', 'description'],
    'task': ['id', 'name', 'subject_id', 'description', 'deadline', 'is_passed']
}


def getInput(msg, tableName=''):
    print(msg)
    if tableName:
        print(' | '.join(TABLES[tableName]), end='\n\n')
    return input()


def getInsertInput(msg, tableName):
    print(msg)
    print(' | '.join(TABLES[tableName]), end='\n\n')
    return input(), input()


def pressEnter():
    input()


class Controller:
    def __init__(self):
        self.model = Model()
        self.view = View()

    def show_init_menu(self, msg=''):
        selectionMenu = SelectionMenu(
            TABLES_NAMES + ['Fill table "faculty" by random data'],
            title='Select the table to work with | command:', subtitle=msg)
        selectionMenu.show()

        index = selectionMenu.selected_option
        if index < len(TABLES_NAMES):
            tableName = TABLES_NAMES[index]
            self.show_entity_menu(tableName)
        elif index == 5:
            self.fillByRandom()
        else:
            print('Bye!')

    def show_entity_menu(self, tableName, msg=''):
        options = ['Get', 'Delete', 'Update', 'Insert']
        functions = [self.get, self.delete, self.update, self.insert]

        if tableName == 'task':
            options.append('Search task by student group')
            functions.append(self.search_task_by_student_group)
        elif tableName == 'student':
            options.append('Search student by his task is passed')
            functions.append(self.search_student_by_task_is_passed)

        selectionMenu = SelectionMenu(options, f'Name of table: {tableName}',
                                      exit_option_text='Back', subtitle=msg)
        selectionMenu.show()
        try:
            function = functions[selectionMenu.selected_option]
            function(tableName)
        except IndexError:
            self.show_init_menu()

    def get(self, tableName):
        try:
            parameter = getInput(
                f'GET {tableName}\nEnter parameter or leave empty:', tableName)
            data = self.model.get(tableName, parameter)
            self.view.print(data)
            pressEnter()
            self.show_entity_menu(tableName)
        except Exception as err:
            self.show_entity_menu(tableName, str(err))

    def insert(self, tableName):
        try:
            columns, values = getInsertInput(
                f"INSERT {tableName}\nEnter colums divided with commas and press Enter. Enter values like: 'value1', 'value2', ...",
                tableName)
            self.model.insert(tableName, columns, values)
            self.show_entity_menu(tableName, 'Success!')
        except Exception as err:
            self.show_entity_menu(tableName, str(err))

    def delete(self, tableName):
        try:
            parameter = getInput(
                f'DELETE {tableName}\n Enter parameter:', tableName)
            self.model.delete(tableName, parameter)
            self.show_entity_menu(tableName, 'Success!')
        except Exception as err:
            self.show_entity_menu(tableName, str(err))

    def update(self, tableName):
        try:
            parameter = getInput(
                f'UPDATE {tableName}\nEnter parameter:', tableName)
            statement = getInput(
                "Enter SQL statement in format [<key>='<value>']", tableName)

            self.model.update(tableName, parameter, statement)
            self.show_entity_menu(tableName, 'Success!')
        except Exception as err:
            self.show_entity_menu(tableName, str(err))

    def search_task_by_student_group(self, tableName):
        try:
            groups = getInput(
                'Search task where student\'s groups are: \nEnter groups divided with commas:')
            data = self.model.search_task_by_student_group(groups)
            self.view.print(data)
            pressEnter()
            self.show_entity_menu(tableName)
        except Exception as err:
            self.show_entity_menu(tableName, str(err))

    def search_student_by_task_is_passed(self, tableName):
        try:
            is_passed = getInput('Search students that have passed them tasks.\nIs task done?:').lower() in [
                'true', 't', 'yes', 'y', '+']
            data = self.model.search_student_by_task_is_passed(is_passed)
            self.view.print(data)
            pressEnter()
            self.show_entity_menu(tableName)
        except Exception as err:
            self.show_entity_menu(tableName, str(err))

    def fillByRandom(self):
        try:
            number = getInput('Enter the number of random entries in the table:')
            self.model.fillFacultyByRandomData(number)
            self.show_init_menu('Success!')
        except Exception as err:
            self.show_init_menu(str(err))
