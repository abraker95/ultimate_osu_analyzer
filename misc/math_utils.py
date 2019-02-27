import math



def bound(min_val, max_val, value):
    return min(max(value, min_val), max_val)


def value_to_percent(min_val, max_val, value):
    return 1.0 - ((max_val - bound(min_val, value, max_val)) / (max_val - min_val))


def percent_to_value(min_val, max_val, percent):
    return max_val - (1.0 - percent)*(max_val - min_val)


def px_per_rad(radius):
    return math.pi / (4.0 * radius)


# Linear interpolation
# Percent: 0.0 -> 1.0
def lerp(low, high, percent):
    return low * (1.0 - percent) + high*percent


def binomialCoefficient(n, k):
    if k < 0 or k > n:   return 0
    if k == 0 or k == n: return 1

    k = min(k, n - k)  # Take advantage of geometry
    c = 1

    for i in range(k):
        c *= (n - i) / (i + 1)

    return c


def bernstein(i, n, t):
    return binomialCoefficient(n, i) * (t**i) * ((1 - t)**(n - i))


# Thanks http://llvm.org/docs/doxygen/html/LEB128_8h_source.html
def decodeULEB128(data):
    shift = 0
    value = (data[0] & 0x7F) << shift

    for byte in data[1:]:
        if byte >= 128: break
        
        value += (byte & 0x7F) << shift
        shift += 7

    return value


def guassian(val, sigma, norm=True):
    guass = 1.0 / (2.0 * sigma*math.sqrt(math.pi)) * math.exp(-(val / (2.0/sigma))*(val / (2.0 *sigma)))

    if norm: return guass / guassian(0, sigma, False)
    else:    return guass


# Returns a triangle wave function
def triangle(val, amplitude):
    return abs((math.fmod(val + (amplitude / 2.0), amplitude)) - (amplitude / 2.0))


def find(val_list, val, selector=None):
    if selector:
        val_list = [ selector(val) for val in val_list ]

    if not len(val_list):
        raise IndexError

    if len(val_list) < 2:
        return 0

    if val <= val_list[0]:  return 0
    if val >= val_list[-1]: return len(val_list) - 1

    if len(val_list) < 3:
        raise IndexError

    start = 0
    end   = len(val_list) - 1
    mid   = int((start + end) / 2)

    while True:
        if val_list[mid] == val:
            return mid

        if val_list[mid] < val < val_list[mid + 1]:
            return mid

        if end - start == 0:
            return -1

        if val_list[mid] < val: start = mid + 1
        else:                   end   = mid - 1
        mid = int((start + end) / 2)

        