import { useState } from "react";
import classes from './TableRow.module.scss';


const TableRow = (props) => {

    const [isSelected, setIsSelected] = useState(false);


    return (
        <tr className={`${isSelected && 'table-warning'} ${classes.tableRow}`} onClick={() => setIsSelected((prevValue) => !prevValue)}>
            <th >{props.index + 1}</th>
            <td>{props.student.name}</td>
            <td>{props.student.surname}</td>
            <td>{props.student.dateOfBirth}</td>
        </tr>)
        ;
}

export default TableRow;