import { Container, Card } from "react-bootstrap";
import classes from "./Classes.module.scss";
import useHttp from "../../hooks/use-http";
import { useEffect, useState } from "react";
import { useSelector } from "react-redux";
import Spinner from "../Spinner/Spinner";

const Classes = (props) => {
    const { isLoading, error, sendRequest } = useHttp();
    const [classData, setClassData] = useState([]);
    const token = useSelector((state) => state.token);

    useEffect(() => {
        const fetchData = async () => {
            setClassData([]);
            try {
                const url = `http://localhost:8000/users/classes/${props.selectedClass}`;
                const headers = { "Authorization": `Bearer ${token}` };

                const response = await sendRequest({
                    url: url,
                    method: "GET",
                    headers: headers,
                });
                setClassData(response);
            } catch (error) {
                console.error(`An error occurred: ${error}`);
                // Handle error here, maybe set an error state
            }
        };

        fetchData();
    }, [props.selectedClass, token, sendRequest]);
    console.log("NExt is class Data")
    console.log(classData);
    console.log("Prev was class Data")

    return (
        <Container fluid className="bg-light opacity-75 py-4">

            {isLoading && <Spinner></Spinner>}
            {!isLoading && classData && classData.students && classData.students.length > 0 ? (
                classData.students.map((student) => (
                    <Card key={student.id}> {/* Assuming each student has a unique 'id' */}
                        <Card.Body>
                            <Card.Header>{student.name}</Card.Header>
                            <Card.Body>{student.birthday}</Card.Body>
                        </Card.Body>
                    </Card>
                ))
            ) : !isLoading ? (
                <p>No student present in the class {props.selectedClass}</p>
            ) : null}

        </Container>
    );

};

export default Classes;
