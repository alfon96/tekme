import { Container, Row, Col, Button } from "react-bootstrap";
import OnlineImageIndicator from "./OnlineImageIndicator"; // Assicurati di importare questo componente
import React from "react";

const SingleStudentEntry = React.memo((props) => {
  return (
    <Row className="px-3 mb-5 mb-md-2 d-flex align-items-center justify-content-center">
      <Col md={2} xs={12} className="d-flex justify-content-center">
        <OnlineImageIndicator profile_pic={props.profile_pic} />
      </Col>
      <Col md={4} xs={12} className="text-lg-start text-center ">
        {props.name} {props.surname}
      </Col>
      <Col md={4} xs={12} className="d-flex  justify-content-center  my-sm-1">
        <Button variant="light">Attendance</Button>
      </Col>
      <Col md={2} xs={12} className="d-flex justify-content-center">
        <Button variant="outline-primary">Note</Button>
      </Col>
    </Row>
  );
});

export default SingleStudentEntry;
