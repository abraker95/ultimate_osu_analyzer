'''
Such scripts allow to execute code that is too complex to manage in the embedded console
To start enter the following in the embedded console:
     CmdUtils.run_script('scripts/test_script.py', globals(), locals())

Now try:
     ret = TestScript().run('hello', 'world')
     print(ret)

All variables accessable in the embedded console are accessible here. Even ones you declared
right before loading the script!

It is recommemded to create your script as a class to lower chances there might be conflicts in
variable names. If there are, you may accidently overwrite or use an unintended variable.
'''
class TestScript():

    def __init__(self):
        # Initializing script stuff go here
        print('hello world')


    def run(self, param1, param2):
        # Use run function to execute the script once loaded
        return param1 + param2