import Graph from "./graph.js";

const GraphWrap = () => {
  const [title, setTitle] = React.useState("");

  const handleInputChange = (event) => {
    setTitle(event.target.value);
  };

  return React.createElement(
    "div",
    null,
    // React.createElement(
    //   "div",
    //   {
    //     className: "wrap",
    //   },
    //   React.createElement("input", {
    //     type: "text",
    //     onChange: handleInputChange,
    //     style: {
    //       position: "absolute",
    //       top: 0,
    //       left: 0,
    //       margin: 0,
    //       padding: "0 10px",
    //       border: "none",
    //       background: "none",
    //       color: "white",
    //       zIndex: 100,
    //       width: "100%",
    //       height: "100%",
    //     },
    //     placeholder: "Search...",
    //   })
    // ),

    React.createElement(Graph, { title: title }) // Pass input value as prop to Graph
  );
};

ReactDOM.render(
  React.createElement(GraphWrap, null),
  document.getElementById("root")
);
