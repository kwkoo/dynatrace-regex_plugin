import re
import sys

class Metric:
    def __init__(self, name, pattern):
        self.name = name
        self.pattern = re.compile(pattern)

    def match(self, line):
        match = self.pattern.match(line)
        if not match:
            return (False, 0)
        if self.pattern.groups == 0:
            return (True, 1)
        return (True, match.group(1))

if len(sys.argv) < 2:
    print("Usage: %s INPUT_FILENAME" % sys.argv[0])
    sys.exit(1)

inputFile = sys.argv[1]

metrics = [ Metric("loadingDuration", '.*Loading Duration is\s*([^\s]*)'), \
            Metric("scriptPass", '.*Script Pass') ]

unaccessed = []
for metric in metrics:
    # only report a value of 0 for metrics with no capture group
    if metric.pattern.groups == 0:
        unaccessed.append(metric.name)

try:
    inf = open(inputFile, 'r')
    for line in inf.readlines():
        print("Processing line: " + line.rstrip('\n'))
        for metric in metrics:
            matched, value = metric.match(line)
            if not matched:
                #print("Did not match against metric " + metric.name)
                continue
            print('*** Matched against %s value="%s"' % (metric.name, str(value)))
            if metric.name in unaccessed:
                unaccessed.remove(metric.name)
    print("Done processing input file")
except Exception as ex:
    print('Exception caught: "%s"' % ex)
    sys.exit(2)
finally:
    if 'inf' in locals():
        try:
            inf.close()
        except:
            pass


print("These were the metrics which were not matched:")
for n in unaccessed:
    print(n)
