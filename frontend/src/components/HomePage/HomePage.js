import { Container } from "react-bootstrap";
import CustomNavbar from "../Navbar/CustomNavbar";
import classes from "./HomePage.module.scss";
import Accordion from "react-bootstrap/Accordion";
import Button from "react-bootstrap/Button";
import React, { useState } from "react";
import Sidebar from "../Sidebar/Sidebar";
import Classes from "../Classes/Classes";
import { useDispatch, useSelector } from "react-redux";
import { resetError, setDataTitle } from "../../store/editingSlice";
import { Toast, ToastContainer } from "react-bootstrap";
import Badge from "react-bootstrap/Badge";
import Agenda from "../Agenda/Agenda";

const HomePage = () => {
  const dataTitle = useSelector((state) => state.editing.dataTitle);
  const tableError = useSelector((state) => state.editing.error);

  const dispatch = useDispatch();
  return (
    <>
      <CustomNavbar />
      <Container
        fluid
        className={`${classes.bgImage} m-0 p-0 d-flex gap-0  position-relative`}
      >
        <Sidebar>
          <Accordion defaultActiveKey="0">
            <Accordion.Item eventKey="0">
              <Accordion.Header>Section A</Accordion.Header>
              <Accordion.Body className="text-center">
                <Button
                  className="m-1"
                  onClick={() => {
                    dispatch(setDataTitle("1A"));
                  }}
                >
                  1A
                </Button>
                <Button
                  className="m-1"
                  onClick={() => {
                    dispatch(setDataTitle("2A"));
                  }}
                >
                  2A
                </Button>
                <Button
                  className="m-1"
                  onClick={() => {
                    dispatch(setDataTitle("3A"));
                  }}
                >
                  3A
                </Button>
                <Button
                  className="m-1"
                  onClick={() => {
                    dispatch(setDataTitle("4A"));
                  }}
                >
                  4A
                </Button>
                <Button
                  className="m-1"
                  onClick={() => {
                    dispatch(setDataTitle("5A"));
                  }}
                >
                  5A
                </Button>
              </Accordion.Body>
            </Accordion.Item>
            <Accordion.Item eventKey="1">
              <Accordion.Header>Section B</Accordion.Header>
              <Accordion.Body>
                Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do
                eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut
                enim ad minim veniam, quis nostrud exercitation ullamco laboris
                nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor
                in reprehenderit in voluptate velit esse cillum dolore eu fugiat
                nulla pariatur. Excepteur sint occaecat cupidatat non proident,
                sunt in culpa qui officia deserunt mollit anim id est laborum.
              </Accordion.Body>
            </Accordion.Item>
          </Accordion>
        </Sidebar>

        <div className="px-5 flex-grow-1 position-relative">
          <div className="pt-6"></div>

          {dataTitle != "" && <Classes></Classes>}
          {dataTitle == "" && <Agenda></Agenda>}
          <ToastContainer position="bottom-end" className="m-2 ">
            <Toast
              show={tableError}
              onClose={() => dispatch(resetError())}
              delay={3500}
              autohide
            >
              <Toast.Header>
                <strong className="me-2">Checker</strong>{" "}
                <Badge pill bg="secondary me-auto">
                  Warning
                </Badge>
              </Toast.Header>
              <Toast.Body>{tableError}</Toast.Body>
            </Toast>
          </ToastContainer>
        </div>
      </Container>
    </>
  );
};

export default HomePage;
