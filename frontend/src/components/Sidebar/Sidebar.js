import classes from "./Sidebar.module.scss";
import { useState } from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {
  faChevronLeft,
  faChevronRight,
} from "@fortawesome/free-solid-svg-icons";
import Button from "react-bootstrap/Button";
import { Container, Row, Col, Accordion } from "react-bootstrap";

const Sidebar = (props) => {
  const [isCollapse, setIsCollapse] = useState(false);
  return (
    <div
      className={`py-6  ${isCollapse ? classes.collapsed : "w-100"} ${
        classes.sidebar
      }`}
    >
      <button
        className={classes.toggleBtn}
        onClick={() => setIsCollapse((prevValue) => !prevValue)}
      >
        <FontAwesomeIcon
          icon={faChevronRight}
          size="1x"
          className={`text-dark z-3  ${
            isCollapse ? classes.sidebarIconLeft : classes.sidebarIconRight
          }`}
        />
      </button>

      {!isCollapse && (
        <Accordion defaultActiveKey="0">
          <Accordion.Item eventKey="0">
            <Accordion.Header>Classes</Accordion.Header>
            <Accordion.Body className="text-center">
              <Button
                className="m-1"
                onClick={() => props.onNavigate("classes/1A")}
              >
                {" "}
                1A
              </Button>
              <Button
                className="m-1"
                onClick={() => {
                  props.onNavigate("classes/2A");
                }}
              >
                2A
              </Button>
              <Button
                className="m-1"
                onClick={() => {
                  props.onNavigate("classes/3A");
                }}
              >
                3A
              </Button>
              <Button
                className="m-1"
                onClick={() => {
                  props.onNavigate("classes/4A");
                }}
              >
                4A
              </Button>
              <Button
                className="m-1"
                onClick={() => {
                  props.onNavigate("classes/5A");
                }}
              >
                5A
              </Button>
            </Accordion.Body>
          </Accordion.Item>
          <Accordion.Item eventKey="1">
            <Accordion.Header>Students</Accordion.Header>
            <Accordion.Body>Lorem</Accordion.Body>
          </Accordion.Item>
          <Accordion.Item eventKey="2">
            <Accordion.Header>Messages</Accordion.Header>
            <Accordion.Body>Lorem ipsum dolor</Accordion.Body>
          </Accordion.Item>
          <Accordion.Item eventKey="3">
            <Accordion.Header>Profile</Accordion.Header>
            <Accordion.Body>Lorem ipsum dolor</Accordion.Body>
          </Accordion.Item>
        </Accordion>
      )}
    </div>
  );
};

export default Sidebar;
