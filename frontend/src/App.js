import "./App.css";
import LoginPage from "./UI/LoginPage";
import FetchPageCalendar from "./components/Calendar/FetchPageCalendar";
import { useSelector } from "react-redux";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import HomePage from "./components/HomePage/HomePage";
import useHttp from "./hooks/use-http";
import Agenda from "./components/Agenda/Agenda";
import Classes from "./components/Classes/Classes";

function App() {
  const token = useSelector((state) => state.token);
  const { isLoading, error, sendRequest } = useHttp();

  const classesLoader = async ({ params }) => {
    const { classId } = params;
    try {
      const url = `http://localhost:8000/users/signin?role=`;
      const header = { "Authorization Bearer": token };

      const response = await sendRequest({
        url: url,
        method: "GET",
        header: header,
      });
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      return response.json();
    } catch (error) {
      throw new Error("Failed to load data", error);
    }
  };

  return (
    <Router>
      <Routes>
        <Route path="/" element={<LoginPage />} />
        <Route path="/signin" element={<LoginPage />} />
        <Route path="/home" element={<HomePage />} />
        <Route path="/agenda/*" element={<HomePage />} />
        <Route path="/classes/*" element={<HomePage />} />
        <Route path="/calendar" element={<FetchPageCalendar />} />
      </Routes>
    </Router>
  );
}

export default App;
