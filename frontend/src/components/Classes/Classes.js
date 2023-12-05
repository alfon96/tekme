import { useState, useMemo } from "react";
import { Container, Card, InputGroup, Form, Button } from "react-bootstrap";
import { useSelector } from "react-redux";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faMagnifyingGlass } from "@fortawesome/free-solid-svg-icons";
import SingleStudentEntry from "./SingleStudentEntry";

const alphabeticOrderMap = { 0: "A-z", 1: "Z-a" };

const Classes = (props) => {
  const classInfo = useSelector((state) => state.classes);
  const [alphabeticOrder, setAlphabeticOrder] = useState(0);
  const [searchQuery, setSearchQuery] = useState(""); // Stato per la query di ricerca

  const handleAlphabeticOrderChange = () => {
    setAlphabeticOrder((prevValue) => (prevValue === 1 ? 0 : 1));
  };

  const handleSearchChange = (event) => {
    setSearchQuery(event.target.value); // Aggiorna la query di ricerca
  };

  const filteredAndSortedStudents = useMemo(() => {
    const filteredStudents = classInfo.students_details.filter((student) =>
      student.surname.toLowerCase().includes(searchQuery.toLowerCase())
    );
    return alphabeticOrder === 1
      ? filteredStudents.reverse()
      : filteredStudents;
  }, [classInfo.students_details, alphabeticOrder, searchQuery]);

  const renderStudents = () => {
    return filteredAndSortedStudents.map((student) => (
      <SingleStudentEntry key={student.id} {...student} />
    ));
  };
  return (
    <Container className="">
      <Card className="shadow-lg border-0 bg-light rounded-4">
        <Card.Body className="d-flex flex-column mt-0 p-4 pb-4  rounded-4">
          <Card.Title className="lh-1 mt-3 display-5 text-center">
            {classInfo.grade}
            {classInfo.name}
          </Card.Title>
          <Card.Text className="text-center">{classInfo.type}</Card.Text>
          <Button
            variant="link"
            className="mb-2"
            onClick={handleAlphabeticOrderChange}
          >
            {alphabeticOrderMap[alphabeticOrder]}
          </Button>
          <Form className="d-flex px-3 my-0 py-0 w-lg-50 align-self-center mb-5">
            <InputGroup>
              <Form.Control
                placeholder="Student's surname"
                aria-label="Username"
                aria-describedby="searches a student by surname"
                className="py-0"
                value={searchQuery}
                onChange={handleSearchChange}
              />
              <Button id="basic-addon1" className="py-0" variant="primary">
                <FontAwesomeIcon icon={faMagnifyingGlass} />
              </Button>
            </InputGroup>
          </Form>

          <Container>{renderStudents()}</Container>
        </Card.Body>
      </Card>
    </Container>
  );
};

export default Classes;
