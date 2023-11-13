import Table from 'react-bootstrap/Table';
import classes from './DataTable.module.scss';
import TableRow from "./TableRow";
import InputTableRow from "./InputTableRow";
import Toolbar from "../HomePage/Toolbar";
import { useSelector, useDispatch } from 'react-redux';
import { Container } from 'react-bootstrap';
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faPlus, faCheck, faMinus } from "@fortawesome/free-solid-svg-icons";


const DataTable = () => {
    const dispatch = useDispatch();
    const { dataTitle, currentData } = useSelector((state) => state.editing);
    const hasData = currentData.length > 0;

    return (<>

        <Container fluid className="d-flex justify-content-between ">
            <h2 className="mb-2">{dataTitle}</h2>
            <Toolbar />
        </Container>

        <div className={classes.scrollContainer}>
            <Table borderless className={`${classes.table} mb-0 table-primary`}>
                <thead>
                    <tr>

                        <th>Name</th>
                        <th>Surname</th>
                        <th>Birth Date</th>
                        <th>  <Container className="d-flex align-items-center justify-content-center p-0 m-0 gap-1">

                            <>
                                <FontAwesomeIcon
                                    icon={faMinus}
                                    size="1x"
                                    className={`text-primary p-1 bg-light ${classes.cursorPointer}`}

                                />
                                <button
                                    className={classes.submitBtn}

                                    type="submit"
                                >
                                    <FontAwesomeIcon
                                        icon={faCheck}
                                        size="1x"
                                        className={`text-success p-1 bg-light ${classes.cursorPointer}`}
                                    />
                                </button>
                            </>

                        </Container></th>
                    </tr>
                </thead>
            </Table>
            <Table borderless className={`${classes.table} table-primary mb-0  `}>
                <tbody>
                    <InputTableRow />
                </tbody>
            </Table>
            <div className={classes.scrollTableBody}>
                <Table className={`${classes.table} mb-0 table-light`}>
                    <tbody>
                        {hasData ? (
                            currentData.map((student, index) => (

                                <TableRow key={index} student={student} index={index} />
                            ))
                        ) : null}
                    </tbody>
                </Table>
            </div>

        </div>
    </>);
}

export default DataTable;