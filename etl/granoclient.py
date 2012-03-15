import requests
import json


class GranoJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        from datetime import datetime
        if isinstance(obj, datetime):
            return obj.isoformat()
        raise TypeError("%r is not JSON serializable" % obj)


class GranoClient(object):

    def __init__(self, api_url, api_user=None, api_password=None,
                 network=None):
        self.api_url = api_url
        self.network = network
        self.api_auth = (api_user, api_password) if api_password else None
        self.session = requests.session(auth=self.api_auth,
            headers={'content-type': 'application/json',
                     'accept': 'application/json'})

    def _make_url(self, collection, network=None, member=None,
                  subcollection=None, submember=None,
                  ignore_network=False):
        url = self.api_url
        network = network or (not ignore_network and self.network)
        for elem in [network, collection, subcollection, member, submember]:
            if elem:
                url += '/' + elem
        return url

    def _request(self, method, collection, params=None,
                 data=None, network=None, member=None,
                 subcollection=None, submember=None,
                 ignore_network=False):
        url = self._make_url(collection, network=network,
            member=member, subcollection=subcollection,
            submember=submember, ignore_network=ignore_network)
        print method, url
        data = json.dumps(data, cls=GranoJSONEncoder) if data else None
        response = self.session.request(method, url,
            params=params, data=data, allow_redirects=True)
        return (response, lambda: json.loads(response.text))

    def getNetwork(self, slug=None):
        res, data = self._request('get', None)
        return data() if res.ok else None

    def listNetworks(self):
        res, data = self._request('get', 'networks',
            ignore_network=True)
        return data() if res.ok else []

    def createNetwork(self, obj):
        res, data = self._request('post', None,
            data=obj)
        return data() if res.ok else None

    def updateNetwork(self, obj):
        res, data = self._request('put', None,
            network=obj['slug'], data=obj)
        return data() if res.ok else None

    def getSchema(self, type_, name, network=None):
        res, data = self._request('get', 'schemata',
            subcollection=type_, member=name,
            network=network)
        return data() if res.ok else None

    def getEntitySchema(self, name, network=None):
        return self.getSchema('entity', name, network=network)

    def getRelationSchema(self, name, network=None):
        return self.getSchema('entity', name, network=network)

    def listSchemata(self, type_, network=None):
        res, data = self._request('get', 'schemata',
            subcollection=type_, network=network)
        return data() if res.ok else []

    def listEntitySchemata(self, network=None):
        return self.listSchemata('entity', network=network)

    def listRelationSchemata(self, network=None):
        return self.listSchemata('relation', network=network)

    def createSchema(self, type_, obj, network=None):
        res, data = self._request('post', 'schemata',
            subcollection=type_, data=obj, network=network)
        return data() if res.ok else None

    def createEntitySchema(self, type_, obj, network=None):
        return self.createSchema(self, 'entity', obj, network=network)

    def createRelationSchema(self, type_, obj, network=None):
        return self.createSchema(self, 'relation', obj, network=network)

    def updateSchema(self, type_, obj, name=None, network=None):
        name = name or obj['name']
        res, data = self._request('put', 'schemata',
            subcollection=type_, member=name, data=obj,
            network=network)
        return data() if res.ok else None

    def updateEntitySchema(self, type_, obj, name=None, network=None):
        return self.updateSchema(self, 'entity', obj,
            name=name(), network=network)

    def updateRelationSchema(self, type_, obj, name=None, network=None):
        return self.updateSchema(self, 'relation', obj,
            name=name(), network=network)


