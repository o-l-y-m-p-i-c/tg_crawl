import "./background.css";
import { Background } from "./components/Background";
import { Home } from "./pages";
import { AppProvider } from "./providers/AppProvider";

function App() {
  return (
    <AppProvider>
      <Background />
      <Home />
    </AppProvider>
  );
}

export default App;
