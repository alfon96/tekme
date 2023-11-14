import Table from "react-bootstrap/Table";
import classes from "./DataTable.module.scss";
import TableRow from "./TableRow";
import InputTableRow from "./InputTableRow";
import Toolbar from "../HomePage/Toolbar";
import { useSelector } from "react-redux";
import { Col, Row } from "react-bootstrap";
import useHttp from "../../hooks/use-http";
import Spinner from "../Spinner/Spinner";

const DataTable = () => {
  const { isLoading, error, sendRequest } = useHttp();

  const handleSave = async () => {
    const url = `http://localhost:8000/users/signin?role=$`;
    const body = {};

    await sendRequest({
      url: url,
      method: "POST",
      body: body,
    });
  };
  const { dataTitle, currentData, showForm } = useSelector(
    (state) => state.editing
  );
  const hasData = currentData.length > 0;

  return (
    <>
      <Row className="m-0">
        <Col xs={12} className="pt-5 ">
          {error && <p>An error occurred. Try later...</p>}
        </Col>
        <Col xs={12} className="pt-5 ">
          {isLoading && <Spinner></Spinner>}
        </Col>
        <Col md={12} lg={3} className="p-0 d-flex justify-content-center">
          <h2 className="display-5 fw-bold">{dataTitle}</h2>
        </Col>
        <Col md={12} lg={9} className="ms-auto  d-flex justify-content-center">
          <Toolbar handleSave={handleSave} />
        </Col>
      </Row>

      <div className={classes.scrollContainer}>
        <Table borderless className={`${classes.table} mb-0 table-primary`}>
          <thead>
            <tr>
              <th> # </th>
              <th>Name</th>
              <th>Surname</th>
              <th>Birth Date</th>
            </tr>
          </thead>
          {showForm && (
            <tbody>
              <InputTableRow />
            </tbody>
          )}
        </Table>

        <div className={classes.scrollTableBody}>
          <Table className={`${classes.table} mb-0 table-light`}>
            <tbody>
              {hasData
                ? currentData.map((student, index) => (
                    <TableRow key={index} student={student} index={index} />
                  ))
                : null}
            </tbody>
          </Table>
        </div>
      </div>
    </>
  );
};

export default DataTable;
