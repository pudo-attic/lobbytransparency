var LobbyTranspareny = LobbyTranspareny || {};

(function($) {

LobbyTranspareny.parseQuery = function(str) {
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

})(jQuery);



