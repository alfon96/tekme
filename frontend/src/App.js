
import "./App.css";
import LoginPage from "./UI/LoginPage";
import FetchPageCalendar from "./components/Calendar/FetchPageCalendar"

import { useSelector } from 'react-redux';
import useHttp from "./hooks/use-http";

function App() {


  const token = useSelector((state) => state.token);



  return <>
    {token === null && <LoginPage />}
    {token != null && <FetchPageCalendar childName="Spopovic"></FetchPageCalendar>}
  </>;

}

export default App;
