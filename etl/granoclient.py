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
                url += '/' + str(elem)
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
            params=params, data=data)
        if not response.ok:
            print response.status_code, response.text
        return (response, lambda: json.loads(response.text))

    def getNetwork(self, slug=None):
        res, data = self._request('get', None)
        return data() if res.ok else None

    def listNetworks(self):
        res, data = self._request('get', 'networks',
            ignore_network=True)
        return data() if res.ok else []

    def createNetwork(self, obj):
        res, data = self._request('post', 'networks',
            data=obj, ignore_network=True)
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

    def _findCollectionItem(self, collection, type=None, network=None,
        filters=[], limit=100, offset=0):
        params = {'limit': limit, 'offset': offset, 'filter': []}
        if type is not None:
            params['type'] = type
        for filter_ in filters:
            params['filter'].append('%s:%s' % filter_)
        res, data = self._request('get', collection, params=params,
            network=network)
        return data().get('results', []) if res.ok else []

    def findEntities(self, type=None, network=None, filters=[], limit=100,
        offset=0):
        return self._findCollectionItem('entities', type=type, network=network,
            filters=filters, limit=limit, offset=offset)

    def findEntity(self, type, network=None, **kw):
        res = self.findEntities(type=type, network=network, filters=kw.items(),
                                limit=1)
        return res.pop() if res else None

    def findRelations(self, type=None, network=None, filters=[], limit=100,
        offset=0):
        return self._findCollectionItem('relations', type=type, network=network,
            filters=filters, limit=limit, offset=offset)

    def findRelation(self, type, network=None, **kw):
        res = self.findRelations(type=type, network=network, filters=kw.items(),
                                limit=1)
        return res.pop() if res else None

    def _getCollectionItem(self, collection, id, network=None, deep=False):
        submember = 'deep' if deep else None
        res, data = self._request('get', collection, network=network,
            submember=submember)
        return data() if res.ok else None

    def getEntity(self, id, network=None, deep=False):
        return self._getCollectionItem('entities', id, network=network, deep=deep)

    def getRelation(self, id, network=None, deep=False):
        return self._getCollectionItem('relations', id, network=network, deep=deep)

    def _createCollectionItem(self, collection, obj, network=None):
        res, data = self._request('post', collection, network=network,
            data=obj)
        return data() if res.ok else None

    def createEntity(self, obj, network=None):
        return self._createCollectionItem('entities', obj, network=network)

    def createRelation(self, obj, network=None):
        return self._createCollectionItem('relations', obj, network=network)

    def _updateCollectionItem(self, collection, obj, network=None):
        if not 'id' in obj:
            return self._createCollectionItem(collection, obj, network=network)
        res, data = self._request('put', collection, network=network,
            member=obj['id'], data=obj)
        return data() if res.ok else None

    def updateEntity(self, obj, network=None):
        return self._updateCollectionItem('entities', obj, network=network)

    def updateRelation(self, obj, network=None):
        return self._updateCollectionItem('relations', obj, network=network)

    def _deleteCollectionItem(self, collection, id, network=None):
        if isinstance(id, dict):
            id = id.get('id')
        res, data = self._request('delete', collection, network=network,
            member=id)
        return data() if res.ok else None

    def deleteEntity(self, id, network=None):
        return self._deleteCollectionItem('entities', id, network=network)

    def deleteRelation(self, id, network=None):
        return self._deleteCollectionItem('relations', id, network=network)
