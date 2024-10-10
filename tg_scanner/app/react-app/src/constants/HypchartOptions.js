const HypchartOptions = {
  autoResize: true,
  layout: {
    hierarchical: false,
  },
  nodes: {
    shape: "dot",
    size: 20,
    font: {
      size: 10,
      vadjust: 0,
      color: "#FFFFFF",
    },
    color: {
      background: "#ffffff",
      border: "#000000",
    },
    borderWidth: 2,
  },
  edges: {
    color: "#000000",
    arrows: {
      from: { enabled: true, scaleFactor: 0.05 },
    },
  },
  physics: {
    enabled: true,
    barnesHut: {
      gravitationalConstant: -1000,
      centralGravity: 0,
      springLength: 350,
      springConstant: 0.001,
    },
    repulsion: {
      nodeDistance: 250,
    },
    stabilization: {
      // enabled: true,
      // iterations: 10,
    },
  },
  interaction: {
    hover: true,
    zoomView: true,
  },
};

const HypeChartEndpoint = "http://" + document.domain + ":" + 5000 + "/graph";
// "https://hypechart.privateai.com/graph";
// "http://" + document.domain + ":" + 5000 + "/graph";

export { HypchartOptions, HypeChartEndpoint };
