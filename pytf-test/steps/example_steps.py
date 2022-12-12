# -- FILE: features/steps/example_steps.py
from behave import given, when, then, step

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
