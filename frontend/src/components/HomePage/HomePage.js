import { Container } from "react-bootstrap";
import CustomNavbar from "../Navbar/CustomNavbar";
import classes from "./HomePage.module.scss";
import React, { useEffect } from "react";
import Sidebar from "../Sidebar/Sidebar";
import { useDispatch, useSelector } from "react-redux";
import Agenda from "../Agenda/Agenda";
import { setActiveComponentIndex } from "../../store/selectorSlice";
import Classes from "../Classes/Classes";
import useHttp from "../../hooks/use-http";
import getClasses from "../Api/api";
import Spinner from "../Spinner/Spinner";
import { setClassesData } from "../../store/classesSlice";
import { useNavigate } from "react-router-dom";

const componentsList = [null, Agenda, Classes];
const HomePage = () => {
  const navigate = useNavigate();

  const { isLoading, error, sendRequest } = useHttp();
  const token = useSelector((state) => state.auth.token);
  const { grade, name } = useSelector((state) => state.classes);
  const dispatch = useDispatch();
  const activeComponentIndex = useSelector(
    (state) => state.selector.activeComponentIndex
  );

  const ActiveComponent = componentsList[activeComponentIndex];

  const handleNavigation = (path) => {
    navigate("/" + path);
    // Handle Classes selection
    let spot = "classes/";
    if (path.includes(spot)) {
      let startIndex = path.indexOf(spot) + spot.length;
      const classGradeName = path.substring(startIndex);
      handleClassSelection(classGradeName);
    }
    // Handle student selection
  };

  const handleClassSelection = async (classGradeAndName) => {
    const classInfo = await getClasses(
      classGradeAndName,
      false,
      sendRequest,
      token
    );

    dispatch(setClassesData(classInfo));
    dispatch(setActiveComponentIndex({ activeComponentIndex: 2 }));
  };

  useEffect(() => {
    const path = window.location.pathname;
    // Estrai la parte rilevante dell'URL e aggiorna lo stato di conseguenza
    if (path.includes("/classes")) {
      // Aggiorna lo stato per mostrare il componente Classes e ripeti la richiesta http

      dispatch(setActiveComponentIndex({ activeComponentIndex: 2 }));
      const gradeName = grade + name;
      handleClassSelection(gradeName);
    } else {
      dispatch(setActiveComponentIndex({ activeComponentIndex: 1 }));
    }
  }, []);

  return (
    <>
      <CustomNavbar />
      <Container
        fluid
        className={`${classes.bgImage} m-0 p-0 d-flex gap-0  position-relative`}
      >
        <Sidebar onNavigate={handleNavigation}></Sidebar>

        <div className="px-5 flex-grow-1 position-relative">
          <div className="pt-6"></div>
          {/* <Agenda /> */}
          {isLoading && <Spinner />}

          {!isLoading && !error && ActiveComponent && <ActiveComponent />}
        </div>
      </Container>
    </>
  );
};

export default HomePage;
