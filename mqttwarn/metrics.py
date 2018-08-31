
import logging

from kaneda import Metrics
from kaneda.backends import InfluxBackend, BaseBackend


logger = logging.getLogger(__name__)


class InfluxDbMetrics:

    def __init__(self, hostname, port, database):
        url = 'influxdb://' + hostname + ':' + str(port) + '/' + database
        logger.info(url)
        self._reporter = Metrics(
            backend=InfluxBackend(
                database = database,
                connection_url = url
            )
        )
        self._cachedTags = {}


    # -----------------------------------------------------------

    # these are basically decorators for Kaneda's methods, but callers don't need to
    #  specify the tags

    def timed(self, name, topic, service=None):
        tags = self._tags(topic, service)
        logger.info(name)
        logger.info(str(tags))
        return self._reporter.timed(name, tags, True)

    def gauge(self, name, value):
        return self._reporter.gauge(name, value)

    def event(self, name, topic, payload, service=None):
        return self._reporter.event(name, payload, self._tags(topic, service))



    # -----------------------------------------------------------

    #
    # create tags for the topic and service, as well as for each 'level' in the topic
    #  (i.e. each string between slashes)
    #
    # so `_tags("a/b/c", "log")` will result in
    #
    #  {
    #       'level0': 'a',
    #       'level1': 'b',
    #       'level2': 'c',
    #       'topic':'a/b/c',
    #       'section':'log'
    #   }
    #
    # and since calling `split()` repeatedly on the same topics and sections
    #  will get expensive, we'll cache the results simply in a dictionary;
    #  in theory this could eventually use up a bunch of memory in a long-running
    #  instance, in which case we could switch to using a cache library that
    #  removes entries not used over some time limit
    #
    def _tags(self, topic, service):
        key = topic
        if (service):
            # this could use "+=" but that creates a unicode string... for consistency
            #  we'll reduce it to a normal string
            key = str(key + " - " + service)

        if (key in self._cachedTags):
            return self._cachedTags[key]

        else:
            tags = self._extractLevels(topic)
            tags.update({'topic': topic})
            if (service):
                tags.update({"service": service})
            self._cachedTags.update({key: tags})
            logger.debug("tags for '" + key + "': " + str(tags))
            logger.debug("there are now " + str(len(self._cachedTags)) + " sets of tags cached:")
            for key in sorted(self._cachedTags.keys()):
                logger.debug("\t'" + key + "'")
            return tags


    def _extractLevels(self, topic):
        tags = {}
        for i, level in enumerate(topic.split('/')):
            tags.update({'level' + str(i): level})
        return tags


