import Calendar from "./components/Calendar/Calendar";
import "./App.css";
import Dummy from "./components/Dummy";
import FetchPage from "./components/Page/FetchPage"

function App() {
  return <FetchPage Component={Calendar} fetchingUri="http://localhost:8000/teachers/Spopovic/11" ></FetchPage>;
}

export default App;
