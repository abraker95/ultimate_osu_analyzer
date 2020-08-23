import time


def rate_limited(rate_limit=0, throw_exception=False):

    def wrap(func):
        def Func(*args, **kwargs):
            try:    time_passed = time.process_time() - Func.last_run_time
            except: time_passed = rate_limit + 1
            
            if time_passed < rate_limit:
                if throw_exception:
                    raise Exception('This function is rate limited. Please wait ' + str(round(rate_limit - time_passed, 2)) + ' more seconds')
                else:
                    time.sleep(rate_limit - time_passed)
            Func.last_run_time = time.process_time()

            return func(*args, **kwargs)

        Func.last_run_time = None
        return Func

    return wrap