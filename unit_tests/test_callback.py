import unittest

from misc.callback import callback
from generic.switcher import Switcher


class TestClassEmit():

    @callback
    def emit_func(self):
        return self.emit_func.emit()


    @callback
    def emit_self_func(self):
        self.emit_self_func.emit(self)

        
    @callback
    def emit_data_func(self, data):
        return self.emit_data_func.emit(data)


    @callback
    def emit_self_data_func(self, data):
        self.emit_self_data_func.emit(self, data)



class TestClassRead():

    def __init__(self, data=None):
        self.data = data
        #print('__init__')
        pass


    def __del__(self):
        #print('__del__')
        pass


    def return_self_data_func(self):
        return self.data


    def return_func(self, data):
        return data


    def return_func_self_data(self, data):
        return self.data, data



class TestCallback(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass


    @classmethod
    def tearDown(cls):  
        pass


    def test_instance_connect_disconnect(self):
        emit = TestClassEmit()
        read = TestClassRead()

        emit.emit_data_func.connect(read.return_func)
        
        emit.emit_data_func('test_123')
        data = emit.emit_data_func.ret(read.return_func)
        self.assertEqual(data, 'test_123', 'Data is not what expected')

        emit.emit_data_func.disconnect(read.return_func)

        emit.emit_data_func('test_123')
        data = emit.emit_data_func.ret(read.return_func)
        self.assertEqual(data, None, 'Data is not what expected')


    def test_multi_instance_connect_disconnect(self):
        read1_data = 'testinst1'
        read2_data = 'testinst2'

        emit  = TestClassEmit()
        read1 = TestClassRead(read1_data)
        read2 = TestClassRead(read2_data)

        emit.emit_func.connect(read1.return_self_data_func)
        emit.emit_func.connect(read2.return_self_data_func)
        
        emit.emit_func()
        data = emit.emit_func.ret(read1.return_self_data_func)
        self.assertEqual(data, read1_data, 'Data is not what expected')
        data = emit.emit_func.ret(read2.return_self_data_func)
        self.assertEqual(data, read2_data, 'Data is not what expected')

        emit.emit_func.disconnect(read1.return_self_data_func)

        emit.emit_func()
        data = emit.emit_func.ret(read1.return_self_data_func)
        self.assertEqual(data, None, 'Data is not what expected')
        data = emit.emit_func.ret(read2.return_self_data_func)
        self.assertEqual(data, read2_data, 'Data is not what expected')

        emit.emit_func.connect(read1.return_self_data_func)
        emit.emit_func.disconnect(read2.return_self_data_func)

        emit.emit_func()
        data = emit.emit_func.ret(read1.return_self_data_func)
        self.assertEqual(data, read1_data, 'Data is not what expected')
        data = emit.emit_func.ret(read2.return_self_data_func)
        self.assertEqual(data, None, 'Data is not what expected')

        emit.emit_func.disconnect(read1.return_self_data_func)
        emit.emit_func.disconnect(read2.return_self_data_func)

        emit.emit_func()
        data = emit.emit_func.ret(read1.return_self_data_func)
        self.assertEqual(data, None, 'Data is not what expected')
        data = emit.emit_func.ret(read2.return_self_data_func)
        self.assertEqual(data, None, 'Data is not what expected')


    def test_static_connect_disconnect(self):
        emit = TestClassEmit()
        emit.emit_self_data_func.connect(TestClassRead.return_func)
        
        emit.emit_self_data_func('test_123')
        data = emit.emit_self_data_func.ret(TestClassRead.return_func)
        self.assertEqual(data, 'test_123', 'Data is not what expected')

        emit.emit_self_data_func.disconnect(TestClassRead.return_func)

        emit.emit_self_data_func('test_123')
        data = emit.emit_self_data_func.ret(TestClassRead.return_func)
        self.assertEqual(data, None, 'Data is not what expected')


    def test_interconnect_self_ref(self):
        emit1 = TestClassEmit()
        emit2 = TestClassEmit()
        
        emit1.emit_func.connect(emit2.emit_func)
        emit2.emit_func.connect(emit1.emit_func)
        
        emit1.emit_func()
        emit2.emit_func()

        emit1.emit_func.disconnect(emit2.emit_func)
        emit2.emit_func.disconnect(emit1.emit_func)


    def test_multi_instance_emit(self):
        '''
        test_multi_instance_emit

        This tests and demonstrates that functions that are being connected to other functions
        apply to all instances of the function's class
        '''
        read1_data = 'testinst1'
        read2_data = 'testinst2'

        emit1 = TestClassEmit()
        emit2 = TestClassEmit()

        read1 = TestClassRead(read1_data)
        read2 = TestClassRead(read2_data)
        
        # Connect emit1 -> read1 and emit2 -> read2
        emit1.emit_func.connect(read1.return_self_data_func)
        emit2.emit_func.connect(read2.return_self_data_func)
        
        # Emit only emit1
        emit1.emit_func()

        # This is expected
        data = emit1.emit_func.ret(read1.return_self_data_func)
        self.assertEqual(data, read1_data, 'Data is not what expected')

        # Even though emit2 did not emit, and we are getting data only from emit1, there should be data from read2 in there
        data = emit1.emit_func.ret(read2.return_self_data_func)
        self.assertEqual(data, read2_data, 'Data is not what expected')

        # Let's attempt to disconnect both on the emit1 side
        emit1.emit_func.disconnect(read1.return_self_data_func)
        emit1.emit_func.disconnect(read2.return_self_data_func)

        # Now lets emit from emit2
        emit2.emit_func()

        # Data should be None
        data = emit2.emit_func.ret(read2.return_self_data_func)
        self.assertEqual(data, None, 'Data is not what expected')

        # Ergo, it does not matter from which instance being used to connect or disconnect from
        # It behaves as static. In fact, it would make more sense to do:
        #       TestCallback.TestClassEmit.connect(read1.return_self_data_func)
        # Instead of using instances


    def test_instance_to_instance_callback(self):
        '''
        test_instance_to_instance_callback
        
        In this tests a 2 switchers are set up to switch between two elements
        Each element contains a string which indicates which reader instance the
        switcher is meant to be connect to. This test is successful if the 
        switchers only invoke the reader they are meant to be connected to. 
        Since the callbacks are connected from a static instance by default, this 
        tests the ability to connect from an instatiated instance.
        '''
        switcher_1 = Switcher()
        switcher_2 = Switcher()

        reader_1 = TestClassRead('reader_1')
        reader_2 = TestClassRead('reader_2')

        switcher_1.switch.connect(lambda old, new: reader_1.return_func_self_data(new), inst=switcher_1)
        switcher_2.switch.connect(lambda old, new: reader_2.return_func_self_data(new), inst=switcher_2)

        switcher_1.add('elem1', 'to_reader_1')
        switcher_2.add('elem2', 'to_reader_2')

        switcher_1.switch('elem1')
        
        data = switcher_1.switch.returns
        self.assertEqual(len(data), 1, 'Data is not what expected')

        data = list(data.values())[0]
        self.assertEqual(data[0], 'reader_1', 'Data is not what expected')
        self.assertEqual(data[1], 'to_reader_1', 'Data is not what expected')

        switcher_2.switch('elem2')
        
        data = switcher_2.switch.returns
        self.assertEqual(len(data), 1, 'Data is not what expected')

        data = list(data.values())[0]
        self.assertEqual(data[0], 'reader_2', 'Data is not what expected')
        self.assertEqual(data[1], 'to_reader_2', 'Data is not what expected')
