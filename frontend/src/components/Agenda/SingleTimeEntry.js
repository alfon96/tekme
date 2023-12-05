import { Row, Col } from "react-bootstrap";
import { Container } from "react-bootstrap";
import classes from "./SingleTimeEntry.module.scss";
import Button from "react-bootstrap/Button";


const SingleTimeEntry = (props) => {
  const hour = props.singleEntry.hour;
  const subject = props.singleEntry.subject[0];
  const className = props.singleEntry.class;
  const school = props.singleEntry.school;
  const mappingHour = {
    1: "08:00 - 09:00",
    2: "09:00 - 10:00",
    3: "10:00 - 11:00",
    4: "11:00 - 12:00",
    5: "12:00 - 13:00",
    6: "13:00 - 14:00",
  };

  return (
    <Button
      variant="light"
      className="w-100 my-1 text-primary px-0"
      onClick={() => {}}
    >
      <Row>
        <Col xs={3} className="text-muted">
          {mappingHour[hour]}
        </Col>
        <Col xs={5} className="text-start text-muted">
          {subject}
        </Col>
        <Col xs={1} className="fw-semibold text-end text-primary">
          {className}
        </Col>
        <Col xs={3} className="text-center text-muted fst-italic">
          {school}
        </Col>
      </Row>
    </Button>
  );
};

export default SingleTimeEntry;
