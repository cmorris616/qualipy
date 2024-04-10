# Test Data Management

{{projectName}} is able to load data from files to be used in the testing process.  The data is loaded from the file and returned to the caller.  The data manager then has the ability to retain some of the data for future steps/scenarios.  The future scenarios could then reference the data allowing for the testing of complex workflows.

For example, the feature file can contain a step for loading the data and then reference the loaded data in a subsequent step.

**Feature file**
```
  Background: Load test data
    Given that the Employee data is loaded

  Scenario: Check loaded data
    Then Employee.bob_id will be 4
    And Employee.alice_id will be 9
```

**The data manager will need to be registered**

```
def before_all(context):
    # Instantiate the data manager
    employeeDataManager = DataManager()

    # Register the data manager with a name that can be used to reference it later
    DataManager.register_data_manager(name='Employee', data_manager=employeeDataManager)

    # NOTE: Registering a second data manager with the same name as another data manager overwrites
    # the first data manager registration.
```

In the step definition, the data will need to be set in the data manager.

**Step definition**
```
@given('that the {data_manager_name} data is loaded')
def load_test_data(context, data_manager_name):
    # Retrieve the data manager (by name) that was previously registered
    data_manager: DataManager = DataManager.get_data_manager(data_manager_name)

    # The model class can be explicitly defined so that instances
    # of the model class are returned
    # Here the model class is 'models.employee.Employee'.  The data manager
    # name is 'Employee', so it can be used to decrease the amount of code
    # needed when using multiple data managers.
    records = data_manager.load(
        data_source=f'test_data/{file_name}',
        model_class=f'models.{data_manager_name.lower()}.{data_manager_name}'
    );

    # Now that the data has been loaded, properties can be set for later use
    if data_manager_name == 'Employee':
        bob = records[0]
        alice = records[1]

        data_manager.set_property('bob_id', bob.id)
        data_manager.set_property('alice_id', alice.id)

@then('{property} will be {id:d}')
def check_saved_data(context, property, id):
    # This approach assumes that dot notation is used for separating the
    # data manager name from the desired property.  Feel free to come up with
    # your own approach
    prop_array = property.split('.')
    dm_name = prop_array[0]
    prop_name = prop_array[1]

    data_manager: DataManager = DataManager.get_data_manager(dm_name)
    assert data_manager.get_property(prop_name) == id
```

Notice that the data is referenced in the feature file by the name of the data manager (Employee) used during registration plus a dot (.) plus the property (bob_id) as it was set in the data manager.

The data is simply loaded from the provided data source and the records are returned.  If the model class is provided, then a list of instances of the model class will be returned.  If the model class is not provided, then a dict will be returned with the records.  If the model class is provided, the data types will be matched as best as possible.  In the case of a dict, the types are less reliable.  Date, time, and datetime types will use the formats set in the data manager's **date_format**, **time_format**, and **datetime_format** properties respectively.  The defaults for these properties are below.

```
    date_format = '%Y-%m-%d'
    datetime_format = '%Y-%m-%d %I:%M:%S%p'
    time_format = '%I:%M:%S%p'
```

## Data Manager

{{projectName}} comes with a data manager that should cover most scenarios.  It has configurable date, time, and datetime formats.  It allows for getting and setting properties (i.e. data loaded from files).  It also has some default data loaders registered.  Of course, custom data managers can be created and registered if needed.  It may be desireable to create a data manager that automatically stores the data in a database after loading it from a file.  Also, a custom data manager could be created to store the desired properties in memory instead of explicitly setting the properties from outside the data manager.  Multiple data managers can be instantiated and registered in order to keep the data separate.

## Data Loaders

The data loaders actually load the data from the files.  {{projectName}} comes with data loaders for loading from the below file types:

  - CSV (*.csv)
  - Excel (*.xlsx)
  - JSON (*.json)
  - XML (*.xml)
  - YAML (*.yaml, *.yml)

When using the provided data manager, the above data loaders are registered with their associated file extensions.  When the data manager attempts to load data from a file, it chooses the appropriate data manager based on the file extension of the file being loaded.  Additional data loaders can be created and registered.  The same data loader can be registered for multiple file extensions just as the YAML data loader is registered for the **yaml** and **yml** file extensions.

The kwargs passed to the data loader's **load** function will be passed to the data loader automatically.

### Matching up model class properties

The provided data loaders have their ways of matching up model class properties with the data in the target file.  In fact, some data loaders can even load different types of data from the same file.  For example, the Excel data loader can load data that maps to an Employee model class as well as a Task model class.  This is achieved in different ways based on the data loader being used.  More information can be found by reading about the specific data loaders below.

### CSV Data Loader

The CSV data loader can only handle one model class of data.  The CSV file must have a header row.  The column names must match the properties of the model class.  The default delimiter is a comma, but that can be changed by passing the **delimiter** kwarg to the **load** function of the data manager.

As one might expect from a CSV file, quoting matters.  By default, the CSV data loader uses **csv.QUOTE_NONNUMERIC** for quoting.  While this can be modified by passing in the **quoting** kwarg in the load function of the data manager, it is recommended to be left to the default.  The quoting options match the quoting in the Python csv module.

### Excel Data Loader

The Excel data loader can handle multiple model classes.  The model class data is separated by worksheets.  Each worksheet should be named to match the fully qualified name of the associated model class.  The columns must have headers matching the properties of the associated model class.  The data types are mostly dynamically determined based on the data type of the property of the model class.  One exception is date/time values.  The date/time cells in the spreadsheet must be formatted as date/time.  If not, the data loader will have trouble reading the values.  This applies for date, time, and datetime properties of the model class.

### JSON Data Loader

The JSON data loader can handle multiple model classes.  The fully qualified model class name is the key for each associated set of records.  The value of each model class is a list of objects whose properties must match the properties of the associated model class.  While JSON can handle certain data types (such as string and numeric), date, time, and datetime formats are used to read the respective property types in the model class.


```
{
    "models.employee.Employee": [
        {
            "id": 4,
            "first_name": "Bob",
            "last_name": "Jones",
            "active": true,
            "start_date": "02/05/2019"
        },
        {
            "id": 9,
            "first_name": "Alice",
            "last_name": "Baker",
            "active": false,
            "start_date": "12/05/2020"
        }
    ],
    "models.task.Task": [
        {
            "id": 3,
            "description": "Add more data loaders",
            "due_date": "10/30/2024",
            "completion_datetime": "04/20/2024 03:56",
            "start_date": "01/15/2024",
            "start_time": "13:20"
        }
    ]
}
```

### XML Data Loader

The XML data loader can handle multiple model classes.  The XML must have a root node.  The node can be anything (i.e. data).  The tags immediately under the root node should be the fully qualified model class names.  Child elements of the model class nodes will be the property names with values as desired.  The formats for date, time, and datetime are used when loading the data.

```
<data>
    <models.employee.Employee>
        <id>4</id>
        <first_name>Bob</first_name>
        <last_name>Jones</last_name>
        <active>true</active>
        <start_date>2019-02-05</start_date>
    </models.employee.Employee>
    <models.employee.Employee>
        <id>9</id>
        <first_name>Alice</first_name>
        <last_name>Baker</last_name>
        <active>false</active>
        <start_date>2020-12-05</start_date>
    </models.employee.Employee>
    <models.task.Task>
        <id>3</id>
        <description>Add more data loaders</description>
        <due_date>2024-10-30</due_date>
        <completion_datetime>2024-04-20 3:56:00am</completion_datetime>
        <start_date>2024-01-15</start_date>
        <start_time>1:20:00pm</start_time>
    </models.task.Task>
</data>
```

### YAML Data Loader

The YAML data loader can handle multiple model classes.  The top most keys are the fully qualified model class names.  The subkeys are the properies.  YAML can handle most data types.  The only data type that may cause an issue is time.  The time can be stored as a string and the time format property of the data manager can be used to read it.

```
models.employee.Employee:
  - id: 4
    first_name: Bob
    last_name: Jones
    active: true
    start_date: 2019-02-05
  - id: 9
    first_name: Alice
    last_name: Baker
    active: false
    start_date: 2020-12-05
models.task.Task:
  - id: 3
    description: Add more data loaders
    due_date: 2024-10-30
    completion_datetime: 2024-04-20 03:56:00
    start_date: 2024-01-15
    start_time: '1:20:00pm'
```

### Custom Data Loaders

Custom data loaders can be created, registered, and used in order to handle data formatted such that the provided data handlers cannot readily load.  In order to create a custom data loader, simply create a class that implements the **DataLoader** class and override the **load_data** function.  The below class is an example of a custom data loader that has the data hardcoded.

```
import datetime
from qualipy.data_management.data_loader import DataLoader
from models.employee import Employee
from models.task import Task

class CustomDataLoader(DataLoader):
    def load_data(self, **kwargs):
        bob = Employee()
        alice = Employee()
        task = Task()

        bob.id = 4
        bob.first_name = 'Bob'
        bob.last_name = 'Jones'
        bob.active = True
        bob.start_date = datetime.date(year=2019, month=2, day=5)

        alice.id = 9
        alice.first_name = 'Alice'
        alice.last_name = 'Baker'
        alice.active = False
        alice.start_date = datetime.date(year=2020, month=12, day=5)

        task.id = 3
        task.description = "Add more data loaders"
        task.due_date = datetime.date(year=2024, month=10, day=30)
        task.completion_datetime = datetime.datetime(year=2024, month=4, day=20, hour=3, minute=56)
        task.start_date = datetime.date(year=2024, month=1, day=15)
        task.start_time = datetime.time(hour=13, minute=20)

        result = [bob, alice, task]
        return result
```

Don't forget to register the custom data loader with your data manager as shown below.  Although the data is hardcoded into the class, the file passed into the data manage's **load** function as the data source must be present.  If it does not exist, an error will be raised.

```
    customDataManager = DataManager()
    customDataManager.register_data_loader(file_extension='hardcoded', data_loader=CustomDataLoader)
    DataManager.register_data_manager(name='Custom', data_manager=customDataManager)
```