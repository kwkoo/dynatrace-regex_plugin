import re
from ruxit.api.base_plugin import BasePlugin
from ruxit.api.exceptions import ConfigException
from ruxit.api.snapshot import pgi_name

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


metrics = [ Metric("loadingDuration", '.*Loading Duration is\s*([^\s]*)'), \
            Metric("scriptPass", '.*Script Pass') ]

class RegexPlugin(BasePlugin):
    def query(self, **kwargs):
        config = kwargs["config"]
        filename = config["filename"]
        pginame = config["pginame"]

        unaccessed = []
        for metric in metrics:
            # only report a value of 0 for metrics with no capture group
            if metric.pattern.groups == 0:
                unaccessed.append(metric.name)

        pgi = self.find_single_process_group(pgi_name(pginame))
        pgi_id = pgi.group_instance_id

        try:
            inf = open(filename, 'r')
            for line in inf.readlines():
                for metric in metrics:
                    matched, value = metric.match(line)
                    if not matched:
                        continue
                    self.results_builder.absolute(key=metric.name, value=value, entity_id=pgi_id)
                    if metric.name in unaccessed:
                        unaccessed.remove(metric.name)
        except Exception as ex:
            raise ConfigException('Caught exception while trying to open file "%s": %s' % (filename, ex)) from ex
        finally:
            if 'inf' in locals():
                try:
                    inf.close()
                except:
                    pass

        # report a value of 0 for those metrics that were not found
        for n in unaccessed:
            self.results_builder.absolute(key=n, value=0, entity_id=pgi_id)


