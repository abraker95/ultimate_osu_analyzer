from misc.callback import callback


class CallbackTest():

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


    @staticmethod
    def run_tests():
        CallbackTest.instance_connect_disconnect_test()
        CallbackTest.multi_instance_connect_disconnect_test()
        CallbackTest.static_connect_disconnect_test()
        CallbackTest.interconnect_self_ref_test()
        CallbackTest.multi_instance_emit_test()


    @staticmethod
    def instance_connect_disconnect_test():
        print('instance_connect_disconnect_test')

        emit = CallbackTest.TestClassEmit()
        read = CallbackTest.TestClassRead()

        emit.emit_data_func.connect(read.return_func)
        
        emit.emit_data_func('test_123')
        data = emit.emit_data_func.ret(read.return_func)
        assert data == 'test_123', 'Data is not what expected;  Expected: %s,  Result: %s' % ('test_123', str(data))

        emit.emit_data_func.disconnect(read.return_func)

        emit.emit_data_func('test_123')
        data = emit.emit_data_func.ret(read.return_func)
        assert data == None, 'Data is not what expected;  Expected: %s,  Result: %s' % (str(None), str(data))


    @staticmethod
    def multi_instance_connect_disconnect_test():
        print('multi_instance_connect_disconnect_test')

        read1_data = 'testinst1'
        read2_data = 'testinst2'

        emit = CallbackTest.TestClassEmit()
        read1 = CallbackTest.TestClassRead(read1_data)
        read2 = CallbackTest.TestClassRead(read2_data)

        emit.emit_func.connect(read1.return_self_data_func)
        emit.emit_func.connect(read2.return_self_data_func)
        
        emit.emit_func()
        data = emit.emit_func.ret(read1.return_self_data_func)
        assert data == read1_data, 'Data is not what expected;  Expected: %s,  Result: %s' % (read1_data, str(data))
        data = emit.emit_func.ret(read2.return_self_data_func)
        assert data == read2_data, 'Data is not what expected;  Expected: %s,  Result: %s' % (read2_data, str(data))

        emit.emit_func.disconnect(read1.return_self_data_func)

        emit.emit_func()
        data = emit.emit_func.ret(read1.return_self_data_func)
        assert data == None, 'Data is not what expected;  Expected: %s,  Result: %s' % (str(None), str(data))
        data = emit.emit_func.ret(read2.return_self_data_func)
        assert data == read2_data, 'Data is not what expected;  Expected: %s,  Result: %s' % (read2_data, str(data))

        emit.emit_func.connect(read1.return_self_data_func)
        emit.emit_func.disconnect(read2.return_self_data_func)

        emit.emit_func()
        data = emit.emit_func.ret(read1.return_self_data_func)
        assert data == read1_data, 'Data is not what expected;  Expected: %s,  Result: %s' % (read1_data, str(data))
        data = emit.emit_func.ret(read2.return_self_data_func)
        assert data == None, 'Data is not what expected;  Expected: %s,  Result: %s' % (str(None), str(data))

        emit.emit_func.disconnect(read1.return_self_data_func)
        emit.emit_func.disconnect(read2.return_self_data_func)

        emit.emit_func()
        data = emit.emit_func.ret(read1.return_self_data_func)
        assert data == None, 'Data is not what expected;  Expected: %s,  Result: %s' % (str(None), str(data))
        data = emit.emit_func.ret(read2.return_self_data_func)
        assert data == None, 'Data is not what expected;  Expected: %s,  Result: %s' % (str(None), str(data))


    @staticmethod
    def static_connect_disconnect_test():
        print('static_connect_disconnect_test')

        emit = CallbackTest.TestClassEmit()
        emit.emit_self_data_func.connect(CallbackTest.TestClassRead.return_func)
        
        emit.emit_self_data_func('test_123')
        data = emit.emit_self_data_func.ret(CallbackTest.TestClassRead.return_func)
        assert data == 'test_123', 'Data is not what expected;  Expected: %s,  Result: %s' % ('test_123', str(data))

        emit.emit_self_data_func.disconnect(CallbackTest.TestClassRead.return_func)

        emit.emit_self_data_func('test_123')
        data = emit.emit_self_data_func.ret(CallbackTest.TestClassRead.return_func)
        assert data == None, 'Data is not what expected;  Expected: %s,  Result: %s' % (str(None), str(data))


    @staticmethod
    def interconnect_self_ref_test():
        print('interconnect_test')

        emit1 = CallbackTest.TestClassEmit()
        emit2 = CallbackTest.TestClassEmit()
        
        emit1.emit_func.connect(emit2.emit_func)
        emit2.emit_func.connect(emit1.emit_func)
        
        emit1.emit_func()
        emit2.emit_func()

        emit1.emit_func.disconnect(emit2.emit_func)
        emit2.emit_func.disconnect(emit1.emit_func)


    @staticmethod
    def multi_instance_emit_test():
        '''
        This tests and demonstrates that functions that are being connected to other functions
        apply to all instances of the function's class
        '''
        print('multi_instance_emit_test')

        read1_data = 'testinst1'
        read2_data = 'testinst2'

        emit1 = CallbackTest.TestClassEmit()
        emit2 = CallbackTest.TestClassEmit()

        read1 = CallbackTest.TestClassRead(read1_data)
        read2 = CallbackTest.TestClassRead(read2_data)
        
        # Connect emit1 -> read1 and emit2 -> read2
        emit1.emit_func.connect(read1.return_self_data_func)
        emit2.emit_func.connect(read2.return_self_data_func)
        
        # Emit only emit1
        emit1.emit_func()

        # This is expected
        data = emit1.emit_func.ret(read1.return_self_data_func)
        assert data == read1_data, 'Data is not what expected;  Expected: %s,  Result: %s' % (str(read1_data), str(data))

        # Even though emit2 did not emit, and we are getting data only from emit1, there should be data from read2 in there
        data = emit1.emit_func.ret(read2.return_self_data_func)
        assert data == read2_data, 'Data is not what expected;  Expected: %s,  Result: %s' % (str(read2_data), str(data))

        # Let's attempt to disconnect both on the emit1 side
        emit1.emit_func.disconnect(read1.return_self_data_func)
        emit1.emit_func.disconnect(read2.return_self_data_func)

        # Now lets emit from emit2
        emit2.emit_func()

        # Data should be None
        data = emit2.emit_func.ret(read2.return_self_data_func)
        assert data == None, 'Data is not what expected;  Expected: %s,  Result: %s' % (str(None), str(data))

        # Ergo, it does not matter from which instance being used to connect or disconnect from
        # It behaves as static. In fact, it would make more sense to do:
        #       CallbackTest.TestClassEmit.connect(read1.return_self_data_func)
        # Instead of using instances

