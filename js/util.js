var LobbyTransparency = LobbyTransparency || {};

(function($) {

var cur = LobbyTransparency;

cur.parseQuery = function(str) {
    var parsed = {};
    var pairs = str.split('&');
    for (var i = 0, len = pairs.length, keyVal; i < len; ++i) {
        keyVal = pairs[i].split("=");
        if (keyVal[0]) {
            parsed[keyVal[0]] = unescape(keyVal[1]);
        }
    }
    return parsed;
};

cur.entityUrl = function(id) {
    return '/entity.html#id=' + id;
};

cur.renderEntity = function(idProp, titleProp) {
    return function(coll, obj) {
        var url = cur.entityUrl(coll.aData[idProp||'id']);
        return "<a href='" + url + "'>" + coll.aData[titleProp||'title'] + "</a>";
    };
};

cur.renderAmount = function(foo) {
    return function(coll, obj) {
        var num = $.format.number(obj, '#,##0.#');
        return "<span class='num'>" + num + " &euro;</span>";

    };
};

cur.makeTable = function(elem, queryName, columns, options) {
    var headers = elem.find('thead tr');
    var columnDefs = [];
    headers.empty();
    _.each(columns, function(c, i) {
        column = _.extend({title: c.field, width: 'auto', render: null}, c);
        columnDefs.push({
            aTargets: [i],
            mDataProp: column.field,
            fnRender: column.render
            });
        headers.append('<th width="' + column.width + '">' + column.title + '</th>');
    });
    return new Grano.DataTable(elem,
      {
        source: LobbyTransparency.apiUrl,
        query: queryName,
        columnDefs: columnDefs,
        params: _.extend({
            limit: 20,
            offset: 0
        }, options)
      },
      {
        "sDom": "<'row'<'span6'l><'span6'f>r>t<'row'<'span6'i><'span6'p>>",
        "sPaginationType": "bootstrap"
      }
    );
};

cur.numRange = function(min, max, abs) {
    var num = '';
    if (abs) {
        num = $.format.number(abs, '#,##0.#');
    } else if (min&&max) {
        num = $.format.number(min, '#,##0.#') +
            ' - ' + $.format.number(max, '#,##0.#');
    } else if (min) {
        num = 'min. ' + $.format.number(min, '#,##0.#');
    } else if (max) {
        num = 'max. ' + $.format.number(max, '#,##0.#');
    } else {
        return '';
    }
    return new Handlebars.SafeString("<span class='num'>" + num + " &euro;</span>");
};

Handlebars.registerHelper('longtext', function(text) {
  if (text.length < 160) {
    return text.replace(/\n/g, '<br/>\n');
  }
  abstract = text.substring(0, 160);
  text = text.replace(/\n/g, '<br/>\n');
  snippet = "<span class='longtext'><span class='abstract'>" + abstract + "... ";
  snippet += "<a href='#'>More...</a></span>";
  snippet += "<span class='full'>" + text + "</span></span>";
  return new Handlebars.SafeString(snippet);
});

$('html').on('click', '.longtext .abstract a', function(e) {
  var elem = $(e.target).parents('.longtext');
  elem.find('.abstract').hide();
  elem.find('.full').slideDown();
  return false;
});

Handlebars.registerHelper('preformatted', function(text) {
  return new Handlebars.SafeString(text.replace(/\n/g, '<br/>\n'));
});

Handlebars.registerHelper('dateformat', function(text) {
  return new Date(text).toDateString();
});

Handlebars.registerHelper('amount', function(num) {
  return new Handlebars.SafeString(cur.renderAmount()({}, num));
});

})(jQuery);



