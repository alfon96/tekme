import { useState } from "react";
import classes from "./Agenda.module.scss";
import { Container, Card } from "react-bootstrap";
import { Form, Button, Row, Col } from "react-bootstrap";
import { useFormValidation } from "../../hooks/use-form-validation";
import { useSelector } from "react-redux";
import TimeTable from "./TimeTable";

const timeTable = [
  { id: 1, subject: ["Math"], class: "1A", hour: 1, school: "Tekme" },
  { id: 2, subject: ["Math"], class: "1B", hour: 2, school: "Tekme" },
  { id: 3, subject: ["Physics"], class: "2F", hour: 3, school: "Tekme" },
  { id: 4, subject: ["Physics"], class: "3C", hour: 4, school: "Sunset" },
  { id: 5, subject: ["Math"], class: "5D", hour: 5, school: "Sunset" },
  { id: 6, subject: ["Math"], class: "5E", hour: 6, school: "Sunset" },
];

const Agenda = (props) => {
  const userName = useSelector((state) => state.auth.fullName);
  const { formState, errors, handleChange, handleBlur, isSubmitting } =
    useFormValidation({
      date: new Date(Date.now()).toISOString().split("T")[0],
    });
  return (
    <Container className="">
      <Card className="shadow-lg border-0 p-3 bg-light">
        <Card.Body className="d-flex flex-column ">
          <Card.Title>Welcome back {userName},</Card.Title>
          <Card.Text> Here is your agenda for</Card.Text>
          <Form className="mx-auto">
            <Form.Group controlId="formDate">
              <Form.Control
                type="date"
                name="date"
                value={formState.date}
                onChange={handleChange}
                onBlur={handleBlur}
                className="text-center border-0 w-100 bg-light"
              />
              {errors.date && (
                <Form.Text className="text-danger">{errors.date}</Form.Text>
              )}
            </Form.Group>
          </Form>
          <Container className="px-4 mt-3 d-flex flex-column align-items-center">
            <TimeTable timeTable={timeTable}></TimeTable>
          </Container>
        </Card.Body>
      </Card>
    </Container>
  );
};

export default Agenda;
