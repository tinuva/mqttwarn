
import logging

import pytest
from mock import Mock, call

from mqttwarn.services.mysql import add_row


# define the fields needed by the code-under-test
class CursorInterface(object):
    def execute(self, query, values = {}):
        pass
    def fetchall(self):
        pass

# turns out every test needs not only a mock, but fetchall should return a list, so combine the two
def mock_cursor_for_table_with_fields(names):
    m = Mock(spec_set = CursorInterface)
    tuples = map(lambda name: (name, "string"), names)
    m.fetchall.return_value = tuples
    return m


# def add_row(cursor, tablename, rowdict):

def test_add_row_no_values():
    m = mock_cursor_for_table_with_fields(["foo"])

    assert add_row(m, "test_table", {}) == None

    m.fetchall.assert_called_once()
    assert m.execute.call_args_list == [
            call('describe test_table'),
            call('insert into test_table () values ()', ())
        ]

def test_add_row_exactly_one_matching_value():
    m = mock_cursor_for_table_with_fields(["foo"])

    assert add_row(m, "test_table", { "foo":"bar" }) == None

    m.fetchall.assert_called_once()

    assert m.execute.call_args_list == [
        call('describe test_table'),
        call('insert into test_table (foo) values (%s)', ("bar",))
    ]

def test_add_row_with_exactly_multiple_matching_values():
    m = mock_cursor_for_table_with_fields(["foo", "x"])

    assert add_row(m, "test_table", { "foo":"bar", "x":5 }) == None

    m.fetchall.assert_called_once()

    assert m.execute.call_args_list == [
        call('describe test_table'),
        call('insert into test_table (foo, x) values (%s, %s)', ("bar", 5))
    ]

def test_add_row_with_extra_values():
    m = mock_cursor_for_table_with_fields(["foo"])

    assert add_row(m, "test_table", { "foo":"bar", "x":5, "y":6 }) == {"x", "y"}

    m.fetchall.assert_called_once()

    assert m.execute.call_args_list == [
        call('describe test_table'),
        call('insert into test_table (foo) values (%s)', ("bar",))
    ]
