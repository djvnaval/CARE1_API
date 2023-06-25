from abc import ABCMeta, abstractmethod
from datetime import datetime
from re import compile as re_compile

from futile.logging import LoggerMixin
from openmtc_onem2m.exc import CSESyntaxError, CSEBadRequest, CSEValueError
from openmtc_onem2m.model import (get_onem2m_type, ContentInstance,
                                  ResourceTypeE, Notification,
                                  get_onem2m_resource_type,
                                  get_short_attribute_name,
                                  get_short_member_name, get_long_member_name,
                                  get_short_resource_name,
                                  get_long_attribute_name,
                                  OneM2MEntity, OneM2MResource, Container,
                                  get_long_resource_name, OneM2MContentResource,
                                  URIList, OneM2MIntEnum, SecurityInfo)

_typename_matcher = re_compile(r'^m2m:([a-z]+)$')


def get_typename(tn):
    return _typename_matcher.findall(tn).pop()


class OneM2MSerializer(LoggerMixin, metaclass=ABCMeta):
    @abstractmethod
    def encode_resource(self, resource, response, pretty=False,
                        encoding="utf-8", fields=None):
        raise NotImplementedError()

    @abstractmethod
    def decode_resource_values(self, s):
        pass

    def decode(self, s):
        resource_type, data = self.decode_resource_values(s)
        if issubclass(resource_type, OneM2MContentResource):
            return resource_type(data)
        child_resource = data.pop("childResource", None)
        if child_resource:
            try:
                def map_child_resource(v):
                    res_type = ResourceTypeE(v["type"])
                    res_cls = get_onem2m_resource_type(res_type.name)
                    return res_cls(v["name"], resourceID=v["value"], resourceType=res_type)
                child_resource = list(map(map_child_resource, child_resource))
            except (TypeError, AttributeError, KeyError, ValueError):
                raise CSEValueError("Invalid entry in child resources: %s",
                                    child_resource)
        if resource_type is Notification and data.get("notificationEvent"):
            representation = data["notificationEvent"]["representation"]
            representation = self.decode(self.dumps(representation))
            data["notificationEvent"]["representation"] = representation
        resource = resource_type(**data)
        if child_resource:
            resource.childResource = child_resource
        return resource


class OneM2MDictSerializer(OneM2MSerializer):
    def encode_resource(self, resource, pretty=False, path=None, encoding="utf-8", fields=None,
                        encapsulated=False):
        if fields and isinstance(resource, OneM2MResource):
            representation = {k: v for k, v in resource.values.items() if fields and k in fields}
        else:
            representation = resource.values

        self.logger.debug("Encoding representation: %s", representation)

        if isinstance(resource, Notification):
            # handle notifications
            try:
                event = representation["notificationEvent"]
                if event:
                    e = event.values
                    e['representation'] = self.encode_resource(
                        event.representation, pretty, path, encoding, fields, True
                    )
                    representation["notificationEvent"] = {
                        get_short_attribute_name(k) or get_short_member_name(k): v
                        for k, v in e.items()
                    }
            except (AttributeError, KeyError):
                self.logger.exception("failed to encode notify")

        def make_val(val_path, resource_id):
            try:
                if val_path:
                    val_path += '/' if not val_path.endswith('/') else ''
            except AttributeError:
                val_path = ''

            if resource_id.startswith(val_path):
                return resource_id
            return val_path + resource_id

        if isinstance(resource, OneM2MResource) and "childResource" in representation:

            def get_child_rep(c):
                return {
                    "val":  make_val(path, c.resourceID),
                    "nm":   c.basename,
                    "typ":  c.resourceType
                }
            representation["childResource"] = list(map(get_child_rep, representation["childResource"]))

        if isinstance(resource, URIList):
            representation = [make_val(path, x) for x in representation]

        if isinstance(resource, Container):
            if isinstance(resource.latest, ContentInstance):
                representation['latest'] = resource.latest.resourceID
            if isinstance(resource.oldest, ContentInstance):
                representation['oldest'] = resource.oldest.resourceID

        if not isinstance(resource, OneM2MContentResource):
            representation = {
                get_short_resource_name(k) or get_short_attribute_name(k) or
                get_short_member_name(k): v for
                k, v in representation.items()}

        if not isinstance(resource, (OneM2MResource, Notification,
                                     SecurityInfo, OneM2MContentResource)):
            return representation

        typename = 'm2m:' + (get_short_resource_name(resource.typename) or
                             get_short_member_name(resource.typename))

        if encapsulated:
            return {typename: representation}

        if pretty:
            return self.pretty_dumps({typename: representation})

        return self.dumps({typename: representation})

    def _handle_partial_addressing(self, resource, pretty):
        for k, v in resource.items():
            if k in ('latest', 'oldest') and isinstance(v, ContentInstance):
                resource[k] = v.resourceID
        if pretty:
            return self.pretty_dumps(resource)
        return self.dumps(resource)

    def decode_resource_values(self, s):

        def convert_to_long_keys(d):
            return {get_long_resource_name(k) or get_long_attribute_name(k) or
                    get_long_member_name(k) or k: v for k, v in d.items()}

        try:
            if hasattr(s, "read"):
                data = self.load(s, object_hook=convert_to_long_keys)
            else:
                data = self.loads(s, object_hook=convert_to_long_keys)
        except (ValueError, TypeError) as exc:
            raise CSEBadRequest("Failed to parse input: %s" % (exc, ))

        self.logger.debug("Read data: %s", data)

        try:
            typename, data = list(data.items())[0]
            return get_onem2m_type(get_typename(typename)), data
        except (AttributeError, IndexError, TypeError):
            raise CSESyntaxError("Not a valid resource representation")
