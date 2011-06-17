#-*- coding:utf-8 -*-

from iwanaga import mock


def dummy():
    pass


import socket

ghn = socket.gethostname

mock_table = [('socket:gethostname', dummy)]

mock_obj = mock.Mock(mock_table)



@mock.mock(socket)
def gethostname():

    return 10



def test_mocking():

    assert socket.gethostname is ghn

    with mock_obj.mocking():

        assert socket.gethostname is dummy

    assert socket.gethostname is ghn




def test_decorator():

    assert socket.gethostname is ghn
    
    @mock.mocking(mock_table)
    def func():

        assert socket.gethostname is dummy

    func()


    assert socket.gethostname is ghn



def test_decorator_member():

    assert socket.gethostname is ghn
    
    @mock_obj
    def func():

        assert socket.gethostname is dummy

    func()

    assert socket.gethostname is ghn



def test_mock_mock():

    assert socket.gethostname is ghn

    @gethostname
    def func():

        assert socket.gethostname() == 10

    func()

    assert socket.gethostname is ghn

