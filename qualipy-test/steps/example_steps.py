# -- FILE: features/steps/example_steps.py
import datetime
import logging
from behave import given, when, then, step
from qualipy.data_management.data_manager import DataManager
from qualipy.exceptions import DataManagerNotFoundException

@given('test has been setup')
def setup_test(context):
    pass

@given('we have behave installed')
def step_impl(context):
    pass

@when('we implement {number:d} tests')
def step_impl(context, number):  # -- NOTE: number is converted into integer
    assert number > 1 or number == 0
    context.tests_count = number

@then('behave will test them for us!')
def step_impl(context):
    assert context.failed is False
    assert context.tests_count >= 0

@given('I was pulled from JIRA')
def step_pulled_from_jira(context):
    assert context.failed is False

@when('the JIRA test is executed')
def jira_test_step_executed(context):
    assert context.failed is False

@then('the JIRA plugin test pull will be successful')
def jira_test_pull_succeeded(context):
    assert context.failed is False

@given(u'the first precondition is met')
def jira_first_precondition(context):
    assert context.failed is False

@then(u'the JIRA plugin test pull will be succeessful')
def jira_test_pull_success(context):
    assert context.failed is False

@given('that the {data_manager_name} data is loaded')
def load_test_data(context, data_manager_name):
    data_manager: DataManager = DataManager.get_data_manager(data_manager_name)

    if data_manager_name == 'JSON':
        file_name = 'test_data.json'
    elif data_manager_name == 'XML':
        file_name = 'test_data.xml'
    elif data_manager_name == 'YAML':
        file_name = 'test_data.yaml'
    elif data_manager_name == 'Excel':
        file_name = 'test_data.xlsx'
    elif data_manager_name == 'Custom':
        file_name = 'test_data.hardcoded'
    else:
        file_name = f'{data_manager_name.lower()}.csv'

    records = data_manager.load(
        data_source=f'test_data/{file_name}',
        model_class=f'models.{data_manager_name.lower()}.{data_manager_name}'
    );

    if data_manager_name == 'Employee':
        logging.info('Checking employee data')
        bob = records[0]
        alice = records[1]

        data_manager.set_property('bob_id', bob.id)
        data_manager.set_property('alice_id', alice.id)

        start_date = datetime.date(2019, 2, 5)
        assert bob.id == 4
        assert bob.first_name == 'Bob'
        assert bob.last_name == 'Jones'
        assert bob.active == True
        assert bob.start_date == start_date

        start_date = datetime.date(2020, 12, 5)
        assert alice.id == 9
        assert alice.first_name == 'Alice'
        assert alice.last_name == 'Baker'
        assert alice.active == False
        assert alice.start_date == start_date
    elif data_manager_name == 'Task':
        logging.info('Checking task data')
        assert records[0].id == 3
        assert records[0].description == 'Add more data loaders'
        assert records[0].due_date == datetime.date(2024, 10, 30)
        assert records[0].completion_datetime == datetime.datetime(2024, 4, 20, 3, 56)
        assert records[0].start_date == datetime.date(2024, 1, 15)
        assert records[0].start_time == datetime.time(13, 20)
    else:
        logging.info('Checking employee and task data')
        bob = records[0]
        alice = records[1]
        task = records[2]

        data_manager.set_property('bob_id', bob.id)
        data_manager.set_property('alice_id', alice.id)

        start_date = datetime.date(2019, 2, 5)
        assert bob.id == 4
        assert bob.first_name == 'Bob'
        assert bob.last_name == 'Jones'
        assert bob.active == True
        assert bob.start_date == start_date

        start_date = datetime.date(2020, 12, 5)
        assert alice.id == 9
        assert alice.first_name == 'Alice'
        assert alice.last_name == 'Baker'
        assert alice.active == False
        assert alice.start_date == start_date

        assert task.id == 3
        assert task.description == 'Add more data loaders'
        assert task.due_date == datetime.date(2024, 10, 30)
        assert task.completion_datetime == datetime.datetime(2024, 4, 20, 3, 56)
        assert task.start_date == datetime.date(2024, 1, 15)
        assert task.start_time == datetime.time(13, 20)


@then('{property} will be {id:d}')
def check_saved_data(context, property, id):
    prop_array = property.split('.')
    dm_name = prop_array[0]
    prop_name = prop_array[1]

    data_manager: DataManager = DataManager.get_data_manager(dm_name)
    assert data_manager.get_property(prop_name) == id