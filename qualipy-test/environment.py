from qualipy.data_management.data_manager import DataManager
from qualipy.data_management.custom_data_loader import CustomDataLoader


def before_all(context):
    employeeDataManager = DataManager()
    DataManager.register_data_manager(name='Employee', data_manager=employeeDataManager)

    taskDataManager = DataManager()
    taskDataManager.date_format = '%m/%d/%Y'
    taskDataManager.time_format = '%H:%M'
    taskDataManager.datetime_format = '%m/%d/%Y %H:%M'
    DataManager.register_data_manager(name='Task', data_manager=taskDataManager)

    jsonDataManager = DataManager()
    jsonDataManager.date_format = '%m/%d/%Y'
    jsonDataManager.time_format = '%H:%M'
    jsonDataManager.datetime_format = '%m/%d/%Y %H:%M'
    DataManager.register_data_manager(name='JSON', data_manager=jsonDataManager)

    yamlDataManager = DataManager()
    DataManager.register_data_manager(name='YAML', data_manager=yamlDataManager)

    xmlDataManager = DataManager()
    DataManager.register_data_manager(name='XML', data_manager=xmlDataManager)

    excelDataManager = DataManager()
    DataManager.register_data_manager(name='Excel', data_manager=excelDataManager)

    customDataManager = DataManager()
    customDataManager.register_data_loader(file_extension='hardcoded', data_loader=CustomDataLoader)
    DataManager.register_data_manager(name='Custom', data_manager=customDataManager)