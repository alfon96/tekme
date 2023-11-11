
import "./App.css";
import LoginPage from "./UI/LoginPage";
import FetchPageCalendar from "./components/Calendar/FetchPageCalendar"
import { useSelector } from 'react-redux';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import SearchPage from "./components/SearchPage/HomePage";
import Classes from "./components/Teachers/Classes";


function App() {
  const token = useSelector((state) => state.token);
  const { isLoading, error, sendRequest } = useHttp();

  const classesLoader = async ({ params }) => {
    const { classId } = params;
    try {
      const url = `http://localhost:8000/users/signin?role=${role}`
      const header = { "Authorization Bearer": token }

      const data = await sendRequest({ url: url, method: 'GET', header: header });
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      return response.json();
    } catch (error) {
      throw new Error('Failed to load data', error);
    }
  };


  return (
    <Router>
      <Routes>
        <Route path="/" element={<LoginPage />} />
        <Route path="/signin" element={<LoginPage />} />
        <Route path="/home" element={<SearchPage />} />
        <Route path="/classes/:classId" element={<Classes />} loader={classesLoader} />

        <Route path="/calendar" element={<FetchPageCalendar />} />

      </Routes>
    </Router>
  );

}

export default App;
