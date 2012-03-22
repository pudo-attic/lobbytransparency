(function($) {

  Grano = Grano || {};

  var ajaxError = function(msg) {
    return function(rq, _, status) {
      return console.error("Ajax Error: " + msg + " (" + status + ")", rq);
    };
  };

  Grano.DataTable = (function() {

    DataTable.prototype.options = {
      source: 'http://localhost:5000/api/1',
      dataset: 'eutr',
      query: 'test',
      defaultParams: {
        limit: 20,
        offset: 0
      }
    };

    function DataTable(element, options, dataTableOptions) {
      var _this = this;
      this.options = $.extend(true, {}, this.options, options);
      this.element = $(element);
      this.table = this.element.dataTable($.extend(false, dataTableOptions, {
        iDisplayLength: 20,
        bFilter: false,
        bSort: false,
        bLengthChange: false,
        bDestroy: true,
        bProcessing: true,
        bServerSide: true,
        aoColumnDefs: this.options.columnDefs,
        sAjaxSource: this.options.source,
        fnServerData: function() {
          return _this._serverData.apply(_this, arguments);
        }
      }));
    }

    DataTable.prototype.draw = function() {
      return this.table.fnDraw();
    };

    DataTable.prototype._serverData = function(src, params, callback, conf) {
      var _this = this;
      var p = {};
      for (var i = 0; i < params.length; i++) {
        o = params[i];
        p[o.name] = o.value;
      }
      var newparams = $.extend(true, {}, this.options.defaultParams);
      newparams.offset = p.iDisplayStart;
      newparams.limit = p.iDisplayLength;
      newparams.q = p.sSearch;
      var apiUrl = this.options.source + this.options.dataset + '/queries/';
      apiUrl = apiUrl + this.options.query;
      var rq = $.get(apiUrl, newparams, function(d) {}, 'jsonp');
      rq.fail(ajaxError("Source request failed. Params: " + (JSON.stringify(p))));
      rq.then(function(data) {
        $(conf.oInstance).trigger('xhr', conf);
        return callback(_this._parseResponse(data, params.sEcho));
      });
      return conf.jqXHR = rq;
    };

    DataTable.prototype._parseResponse = function(data, echo) {
      return {
        sEcho: echo,
        iTotalRecords: data.count,
        iTotalDisplayRecords: data.count,
        aaData: data.results
      };
    };

    return DataTable;

  })();

})(jQuery);
