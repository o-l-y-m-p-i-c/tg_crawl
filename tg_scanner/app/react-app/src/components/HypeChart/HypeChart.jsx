import Graph from "react-graph-vis";
import { useState, useEffect, useRef, useMemo } from "react";
import io from "socket.io-client";
import React from "react";
import { HypchartOptions, HypeChartEndpoint } from "../../constants";

const unactive = 0.2,
  active = 1;

function randomColor() {
  const red = Math.floor(Math.random() * 256)
    .toString(16)
    .padStart(2, "0");
  const green = Math.floor(Math.random() * 256)
    .toString(16)
    .padStart(2, "0");
  const blue = Math.floor(Math.random() * 256)
    .toString(16)
    .padStart(2, "0");
  return `#${red}${green}${blue}`;
}

const HypeChart = ({ openModal, searchInput }) => {
  const input = useRef(searchInput);

  const graphData = useRef([]);

  const [state] = useState({
    graph: {
      nodes: [],
      edges: [],
    },
    events: {
      select: ({ nodes }) => {
        if (nodes) {
          const foundNode = graphData.current.find(
            (graphNode) => graphNode.id === nodes[0]
          );
          if (foundNode && openModal) openModal(foundNode);
        }
      },
    },
  });

  const networkRef = useRef(null);

  const socket = io.connect(HypeChartEndpoint);

  const createNode = (data) => {
    const color = randomColor();

    if (networkRef.current) {
      if (data?.nodes) {
        data.nodes.forEach((node) => {
          try {
            node.size = node.size / 1.5;
            if (node?.image) {
              node.shape = "circularImage";
            }

            if (networkRef.current.body.data.nodes.length < 100) {
              if (input.current) {
                if (node.msg) {
                  const includes = node.msg
                    .toLowerCase()
                    .includes(input.current.toString().toLowerCase());
                  if (includes) {
                    node.opacity = active;
                  } else {
                    node.opacity = unactive;
                  }
                } else {
                  node.opacity = unactive;
                }
              }
              networkRef.current.body.data.nodes.add({ ...node, color });
              graphData.current.push(node);
            }
          } catch (e) {}
        });
      }

      if (data?.edges) {
        data.edges.forEach((edge) => {
          try {
            if (networkRef.current.body.data.nodes.length < 500) {
              networkRef.current.body.data.edges.add(edge);
            }
          } catch (e) {}
        });
      }
    }
  };

  const updateNodeOpacity = (nodeId, opacity) => {
    if (networkRef.current) {
      const node = networkRef.current.body.data.nodes.get(nodeId);
      if (node) {
        networkRef.current.body.data.nodes.update({
          id: nodeId,
          color: {
            border: "#000000",
          },
          opacity,
        });
      }
    }
  };

  const updateNodeOpacityAll = (opacity) => {
    if (networkRef.current) {
      const allNodes = networkRef.current.body.data.nodes.get();
      allNodes.forEach((node) => {
        networkRef.current.body.data.nodes.update({
          id: node.id,
          color: {
            border: "#000000",
          },
          opacity,
        });
      });
    }
  };

  const onResize = () => {
    // if (networkRef.current) networkRef.current.fit();
  };

  const handleFitClick = () => {
    if (networkRef.current) networkRef.current.fit();
  };

  const nodeVisualUpdate = () => {
    if (searchInput) {
      graphData.current.forEach((graphNode) => {
        if (!graphNode.msg) return;
        const includes = graphNode.msg
          .toLowerCase()
          .includes(searchInput.toString().toLowerCase());
        if (includes) {
          updateNodeOpacity(graphNode.id, active);
        } else {
          updateNodeOpacity(graphNode.id, unactive);
        }
      });
    } else {
      updateNodeOpacityAll(1);
    }
  };

  useMemo(() => {
    socket.on("update_graph", (data) => {
      createNode(data);
    });

    window.addEventListener("resize", onResize);

    return () => {
      window.removeEventListener("resize", onResize);
      socket.off("update_graph");
      socket.disconnect();
    };
  }, [socket]);

  useEffect(() => {
    if (networkRef.current) {
      networkRef.current.moveTo({
        scale: 0.35,
        position: { x: 0, y: 0 },
      });
    }
  }, [networkRef]);

  useEffect(() => {
    input.current = searchInput;
    nodeVisualUpdate();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [searchInput]);

  const { graph, events } = state;

  const getNetwork = (network) => {
    networkRef.current = network;
  };

  return (
    <>
      <Graph
        graph={graph}
        options={HypchartOptions}
        events={events}
        getNetwork={getNetwork}
        style={{
          height: "100%",
          width: "100%",
          position: "absolute",
          left: 0,
          top: 0,
        }}
      />
      <button onClick={handleFitClick} className="button fit-button">
        Fit
      </button>
    </>
  );
};

export { HypeChart };
