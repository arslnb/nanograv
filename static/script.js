var layout = {
  xaxis: {
    title: 'Period'
  },
  yaxis: {
    title: 'Period Derivative',
    type: 'log'
  },
  margin: {
    t: 20
  },
  hovermode: 'closest'
};

$.get("/api/data", function(data) {
  graph = document.getElementById("graph");
  Plotly.plot(graph, [{
      name: "Binary Companion",
      text: data.b_names,
      marker: {
        sizemode: "area",
        sizeref: 1,
        size : data.b_raw
      },
      mode: "markers",
      y: data.b_pd,
      x: data.b_p,
    },
    {
        name: "No Binary Companion",
        text: data.names,
        marker: {
          sizemode: "area",
          sizeref: 1,
          size : data.raw
        },
        mode: "markers",
        y: data.pd,
        x: data.p,
      }], layout);
});
