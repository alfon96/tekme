import React, { useCallback } from "react";
import classes from './TableRow.module.scss';
import { useDispatch, useSelector } from 'react-redux';
import { toggleSelectElement } from '../../store/editingSlice';

const TableRow = (props) => {
    const dispatch = useDispatch();
    const student = props.student;

    // Selector to check if the current student is selected
    const { selectedElements, editableData } = useSelector(state => state.editing);

    const isSelected = selectedElements.includes(student);
    const isEditing = editableData && editableData.id === props.student.id;

    // Function to toggle the selection of the current student
    const handleToggleSelect = useCallback(() => {
        dispatch(toggleSelectElement(student));
    }, [dispatch, student]);

    return (
        <tr className={`${isSelected ? isEditing ? 'table-dark' : 'table-warning' : ''} ${classes.cursor}`} onClick={handleToggleSelect}>

            <th className="fw-normal">{student.name}</th>
            <td>{student.surname}</td>
            <td>{student.dateOfBirth}</td>
            <td>{props.index + 1}</td>
        </tr>
    );
};

export default TableRow;
