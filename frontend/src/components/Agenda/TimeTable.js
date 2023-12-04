import { Row, Card } from "react-bootstrap";
import SingleTimeEntry from "./SingleTimeEntry";

const TimeTable = (props) => {
  if (!props.timeTable) {
    return null; // or display a loading message or handle the case when data is undefined
  }
  const timeEntries = props.timeTable.map((element) => (
    <SingleTimeEntry key={element.id} singleEntry={element} />
  ));

  return <>{timeEntries}</>;
};

export default TimeTable;
