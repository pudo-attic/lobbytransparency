var LobbyTransparency = LobbyTransparency || {};

(function($) {

var cur = LobbyTransparency;

cur.graphArea = function(el) {
  cur.sigInst = sigma.init(el[0]).drawingProperties({
      defaultLabelColor: '#fff',
      defaultLabelSize: 14,
      defaultLabelBGColor: '#00526b',
      defaultLabelHoverColor: '#00526b',
      labelThreshold: 6,
      defaultEdgeType: 'curve'
    }).graphProperties({
      minNodeSize: 0.5,
      maxNodeSize: 5
    });

    cur.sigInst.bind('overnodes',function(event){
      var nodes = event.content;
      cur.sigInst.curNode = nodes[0];
      var neighbors = {};
      cur.sigInst.iterEdges(function(e){
        if(nodes.indexOf(e.source)>=0 || nodes.indexOf(e.target)>=0){
          neighbors[e.source] = 1;
          neighbors[e.target] = 1;
        }
      }).iterNodes(function(n){
        if(!neighbors[n.id]){
          n.hidden = 1;
        }else{
          n.hidden = 0;
        }
      }).draw(2,2,2);
    }).bind('outnodes',function(){
      cur.sigInst.curNode = null;
      cur.sigInst.iterEdges(function(e){
        e.hidden = 0;
      }).iterNodes(function(n){
        n.hidden = 0;
      }).draw(2,2,2);
    });

    el.click(function(e) {
      if (cur.sigInst.curNode) {
        document.location = cur.entityUrl(cur.sigInst.curNode);
      }
    });
};

cur.loadGraph = function(id) {
  cur.sigInst.emptyGraph();
  $.get(LobbyTransparency.apiUrl + 'eutr/entities/' + id + '/graph', 
    {'entity_type': 'actor',
     'wrap': 'json'},
    function(data) {
      data = $.parseXML(data.xml);
      cur.sigInst.parseGexf(data);
      cur.sigInst.iterNodes(function(n){
          n.size = Math.max(1, 100 * Math.log(((n.inDegree * 2 + n.outDegree) / cur.sigInst.numNodes)*100));
          n.color = '#ffe433';
          _.each(n.attr.attributes, function(a) {
              if (a.attr.title == 'title') {
                  n.label = a.val;
              }
              if (a.attr.title == 'actsAsPerson' && a.val == 'True') {
                  n.color = '#238dad';
              }
          });
      });
      cur.sigInst.iterEdges(function(e){
        e.color = '#dddddd';
      });
      cur.sigInst.activateFishEye();
      cur.sigInst.startForceAtlas2();
      cur.sigInst.draw();
    }, 'jsonp');

};

})(jQuery);



