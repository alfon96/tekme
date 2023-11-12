import { Container, Card } from "react-bootstrap";
import classes from "./Classes.module.scss";
import useHttp from "../../hooks/use-http";
import { useEffect, useState } from "react";
import { useSelector } from "react-redux";
import Spinner from "../Spinner/Spinner";
import Table from 'react-bootstrap/Table';
import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button';
import TableRow from "./TableRow";
import InputTableRow from "./InputTableRow";
import Toolbar from "../HomePage/Toolbar";

const Classes = (props) => {
    const { isLoading, error, sendRequest } = useHttp();
    const [classData, setClassData] = useState([]);
    const token = useSelector((state) => state.token);
    const [historyEdit, setHistoryEdit] = useState([]);
    const [initialDataLoaded, setInitialDataLoaded] = useState(false);

    const handleSubmission = (newStudent) => {
        console.log(newStudent);
        setClassData((prevClassValue) => {
            if (initialDataLoaded) {
                setHistoryEdit((prevValue) => [...prevValue, [...prevClassValue]]);
            }
            return [...prevClassValue, newStudent];
        });

    }

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
                console.log(response);
                setClassData(response.students);
                setInitialDataLoaded(true);
            } catch (error) {
                console.error(`An error occurred: ${error}`);
                // Handle error here, maybe set an error state
            }
        };

        fetchData();
    }, [props.selectedClass, token, sendRequest]);


    const isDataPresent = !isLoading && classData && classData.length > 0;

    const undo = () => {
        const previousEdit = historyEdit.pop();
        if (previousEdit) {
            console.log(previousEdit);
            setClassData(previousEdit);
        }

    };
    const save = () => { };
    const del = () => { };
    console.log(`The value is : ${historyEdit}`);
    return (
        <Container fluid className={`${classes.tableContainer} py-4 rounded-5`}>
            {isLoading && <Spinner />}

            {!isLoading && (
                <>
                    <Toolbar undo={undo} disableUndo={historyEdit.length === 0} />
                    <h2 className="mb-2">{props.selectedClass}</h2>
                    <div className={classes.scrollContainer}>
                        <Table borderless className={`${classes.table} mb-0 table-primary`}>
                            <thead>
                                <tr>
                                    <th>#</th>
                                    <th>Name</th>
                                    <th>Surname</th>
                                    <th>Birth Date</th>
                                </tr>
                            </thead>
                        </Table>
                        <div className={classes.scrollTableBody}>
                            <Table className={`${classes.table} mb-0 table-light`}>
                                <tbody>
                                    {isDataPresent ? (
                                        classData.map((student, index) => (
                                            <TableRow key={index} student={student} index={index} />
                                        ))
                                    ) : null}
                                </tbody>
                            </Table>
                        </div>
                        <Table borderless className={`${classes.table} table-primary `}>
                            <tfoot>
                                <InputTableRow handleSubmission={handleSubmission} />
                            </tfoot>
                        </Table>
                    </div>
                </>
            )}
        </Container>
    );



};

export default Classes;
