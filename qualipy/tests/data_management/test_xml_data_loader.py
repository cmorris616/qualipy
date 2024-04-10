import datetime
import os
from unittest import TestCase
from xml.etree import ElementTree as ET

from qualipy.data_management.xml_data_loader import XmlDataLoader

class TestXmlDataLoader(TestCase):
    def setUp(self) -> None:
        self.xml_file_name = 'unittest_xml_dl_data.xml'

        root = ET.Element('data')
        emp_node = ET.SubElement(root, 'data_management.test_xml_data_loader.Employee')
        ET.SubElement(emp_node, 'id').text = '4'
        ET.SubElement(emp_node, 'first_name').text = 'Bob'
        ET.SubElement(emp_node, 'last_name').text = 'Jones'
        ET.SubElement(emp_node, 'active').text = 'true'
        ET.SubElement(emp_node, 'start_date').text = '2019-02-05'
        ET.SubElement(emp_node, 'height').text = '5.5'

        
        emp_node = ET.SubElement(root, 'data_management.test_xml_data_loader.Employee')
        ET.SubElement(emp_node, 'id').text = '9'
        ET.SubElement(emp_node, 'first_name').text = 'Alice'
        ET.SubElement(emp_node, 'last_name').text = 'Baker'
        ET.SubElement(emp_node, 'active').text = 'false'
        ET.SubElement(emp_node, 'start_date').text = '2020-12-05'
        ET.SubElement(emp_node, 'height').text = '5.25'

        task_node = ET.SubElement(root, 'data_management.test_xml_data_loader.Task')
        ET.SubElement(task_node, 'id').text = '3'
        ET.SubElement(task_node, 'description').text = 'Add more data loaders'
        ET.SubElement(task_node, 'due_date').text = '2024-10-30'
        ET.SubElement(task_node, 'completion_datetime').text = '2024-04-20 3:56:00am'
        ET.SubElement(task_node, 'start_date').text = '2024-01-15'
        ET.SubElement(task_node, 'start_time').text = '1:20:00pm'

        ET.ElementTree(root).write(self.xml_file_name)

    def tearDown(self) -> None:
        os.remove(self.xml_file_name)

    def test_load_data(self):
        dl = XmlDataLoader()
        
        records = dl.load_data(data_source=self.xml_file_name)
        assert isinstance(records, list)
        from data_management.test_xml_data_loader import Employee, Task
        assert len(records) == 3
        assert isinstance(records[0], Employee)
        assert isinstance(records[1], Employee)
        assert isinstance(records[2], Task)

        bob = records[0]
        alice = records[1]
        task = records[2]

        assert bob.id == 4
        assert bob.first_name == 'Bob'
        assert bob.last_name == 'Jones'
        assert bob.active
        assert bob.start_date == datetime.date(year=2019, month=2, day=5)
        assert bob.height == 5.5

        assert alice.id == 9
        assert alice.first_name == 'Alice'
        assert alice.last_name == 'Baker'
        assert not alice.active
        assert alice.start_date == datetime.date(year=2020, month=12, day=5)
        assert alice.height == 5.25

        assert task.id == 3
        assert task.description == 'Add more data loaders'
        assert task.due_date == datetime.date(year=2024, month=10, day=30)
        assert task.completion_datetime == datetime.datetime(year=2024, month=4, day=20, hour=3, minute=56)
        assert task.start_date == datetime.date(year=2024, month=1, day=15)
        assert task.start_time == datetime.time(hour=13, minute=20, second=0)

class Employee:
    def __init__(self) -> None:
        self.first_name: str = ""
        self.last_name: str = ""
        self.id: int = -1
        self.active: bool = False
        self.start_date: datetime.date = datetime.datetime.strptime('1970-01-01', '%Y-%m-%d').date()
        self.height: float = 0.0
        self.activation: datetime.datetime = datetime.datetime.strptime('1970-01-01 8:00:00', '%Y-%m-%d %I:%M:%S')
        self.shift_end: datetime.time = datetime.datetime.strptime('1970-01-01 8:00:00', '%Y-%m-%d %I:%M:%S').time()


class Task:
    def __init__(self) -> None:
        self.id: int = -1
        self.description: str = ""
        self.due_date: datetime.date = datetime.date.max
        self.completion_datetime: datetime.datetime = datetime.datetime.max
        self.start_time: datetime.time = datetime.time.max
        self.start_date: datetime.date = datetime.date.max