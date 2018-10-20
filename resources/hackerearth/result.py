import json

class BaseAPIResult(object):
    """Represents a response from the HackerEarth API.
    """
    def __init__(self, response):
        self._transform_to_attrs(response)

    def _desiarialize_response(self, response):
        response = json.loads(response)
        return response

    def _transform_to_attrs(self, response):
        """Sets the key/value pairs in the given dict as
        attributes of this result object.
        """
        response_dict = self._desiarialize_response(response)
        self.__dict__.update(response_dict)


class CompileResult(BaseAPIResult):
    """Represents the compilation results from the compile
    end point.
    """
    def __init__(self, response):
        super(CompileResult, self).__init__(response)


class RunResult(BaseAPIResult):
    """Represents the excecution results from the run end point of the
    HackerEarth API.
    """

    def __init__(self, response):
        super(RunResult, self).__init__(response)

    def _transform_to_attrs(self, response):
        response_dict = self._desiarialize_response(response)
        response_dict = self._flatten_dict(response_dict)
        self.__dict__.update(response_dict)

    def _flatten_dict(self, dict_):
        """Modifies the given dict into a flat dict consisting of only
        key/value pairs.
        """
        flattened_dict = {}
        for (key, value) in dict_.iteritems():
            if isinstance(value, dict):
                flattened_dict.update(self._flatten_dict(value))
            else:
                flattened_dict[key] = value
        return flattened_dict

