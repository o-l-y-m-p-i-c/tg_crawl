// import Graph from 'react-graph-vis';

export default class Graph extends React.Component {
  network = null;
  isLoaded = false;

  constructor(props) {
    super(props);

    this.container = document.getElementById("graph");

    this.sio = io.connect(
      "https://" + document.domain + ":" + location.port + "/graph"
    );

    let nodes = new vis.DataSet();

    let edges = new vis.DataSet();

    this.data = {
      nodes: nodes,
      edges: edges,
    };

    const selected = "red",
      unselected = "silver";
    this.options = {
      layout: {
        randomSeed: 1,
        improvedLayout: true,
        hierarchical: {
          enabled: false,
          levelSeparation: 150,
          nodeSpacing: 100,
          treeSpacing: 200,
        },
      },

      physics: {
        stabilization: {
          iterations: 2,
        },
        barnesHut: {
          // gravitationalConstant: -100000,
          // centralGravity: 0.5,
          // springLength: 50,
          // springConstant: 0.095,
          // damping: 0.63,
          // avoidOverlap: 0.1,
          gravitationalConstant: -15000,
          centralGravity: 0.3,
          springLength: 1, // Increased from 50
          springConstant: 0.01,
          damping: 0.09,
          avoidOverlap: 0.1, // Increased from 0.1
        },
        minVelocity: 0.25,
        repulsion: {
          nodeDistance: 100, // Put more distance between the nodes.
        },
      },
      interaction: {
        zoomSpeed: 0.3,
      },
      nodes: {
        shape: "dot",
        size: 30,
        font: {
          size: 12,
          color: "#ffffff",
          face: "GothamSSm-Book, helvetica, arial, sans",
        },
        borderWidth: 2,
      },
      edges: {
        width: 1,
        color: "#ffffff",
        smooth: { type: "continuous" },
        arrows: {
          to: {
            enabled: true,
            scaleFactor: 1,
            type: "triangle",
          },
        },
      },
      groups: {
        enablingSelected: {
          color: selected,
        },
        terminalSelected: {
          color: selected,
        },
        skillSelected: {
          color: selected,
        },
        roleSelected: {
          color: selected,
        },
        enabling: { color: unselected },
        terminal: { color: unselected },
        skill: { color: unselected },
      },
    };

    this.register_events();

    // this.click_handler(this.network);
  }

  register_events() {
    let g = this;
    this.sio.on("update_graph", function (data) {
      // console.log(data);
      for (const [key, value] of Object.entries(data.nodes)) {
        g.update_node({
          id: key,
          ...value,
        });
      }
      if (data.edges)
        for (const [key, value] of Object.entries(data.edges)) {
          g.update_edge({
            id: key,
            ...value,
          });
        }
    });

    let left = $("#node-count-left");
    let right = $("#node-count-right");

    this.sio.on("add_node_list", function (data) {
      $("#node-list").append("<li> " + data.label.substring(0, 50) + "</li>");
      // first = $('li').first();
      // first.css('color', '#ff0000');

      left.text(parseInt(left.text()) + 1);
      right.text(parseInt(right.text()) + 1);
    });
    this.sio.on("remove_node_list", function () {
      $("ul li:nth-child(2)").css("color", "#ff0000");
      $("li")
        .first()
        .hide(5, function () {
          $(this).remove();
        });
      left.text(parseInt(left.text()) - 1);
    });

    this.sio.on("set_text", function (id_text) {
      $("#" + id_text["id"]).text(id_text["text"]);
    });
  }

  add_node() {
    try {
      // console.log("New node", this.data.nodes);
      this.data.nodes.add({
        id: data.id,
        label: data.label,
      });
    } catch (err) {
      alert(err);
    }
  }

  update_node(data) {
    try {
      // console.log("update_node", data);
      if (data && data?.image) {
        this.data.nodes.update({
          ...data,
          shape: "circularImage",
        });
      } else {
        let newData = {};
        Object.keys(data).forEach((key) => {
          if (key !== "image") newData[key] = data[key];
        });
        this.data.nodes.update({
          ...newData,
        });
      }
    } catch (err) {
      alert(err);
    }
  }

  remove_node(id) {
    try {
      this.data.nodes.remove({ id: id });
    } catch (err) {
      alert(err);
    }
  }

  add_edge(data) {
    try {
      this.data.edges.add({
        id: data.id,
        from: data.from,
        to: data.to,
      });
    } catch (err) {
      alert(err);
    }
  }

  update_edge(data) {
    try {
      this.data.edges.update({
        ...data,
      });
    } catch (err) {
      alert(err);
    }
  }

  remove_edge(id) {
    try {
      this.data.edges.remove({ id: id });
    } catch (err) {
      alert(err);
    }
  }

  click_handler(network) {
    if (!network) return;
    network.on("click", function (properties) {
      var ids = properties.nodes;
      // var clickedNodes = this.data.nodes.get(ids);
      var telegram_username =
        network.nodesHandler.body.nodes[ids]?.options.telegram_username;

      if (telegram_username) {
        document.querySelector("dialog").showModal();
        document
          .querySelector(".open-btn")
          .setAttribute("href", `https:/t.me/${telegram_username}`);
        // window.open(`https:/t.me/${telegram_username}`, "_blank");
        document.querySelector("#tg_name").innerHTML = "@" + telegram_username;
      }
    });
  }
  hover_handler(network) {
    network.on("hoverNode", function (params) {
      this.changeCursor("pointer");
      // network.canvas.body.container.style.cursor = "pointer";
    });
    network.on("blurNode", function (params) {
      this.changeCursor("default");
      // network.canvas.body.container.style.cursor = "default";
    });
  }

  changeCursor(newCursorStyle) {
    var networkCanvas = document
      .querySelector(".vis-network")
      .getElementsByTagName("canvas")[0];
    networkCanvas.style.cursor = newCursorStyle;
  }

  draw() {
    this.network = new vis.Network(this.container, this.data, this.options);
    return this.network;
  }

  render() {
    const network = this.draw();
    // if (!this.isLoaded) {
    // this.isLoaded = true;
    this.click_handler(network);
    this.hover_handler(network);
    // }
    return "";
  }
}
