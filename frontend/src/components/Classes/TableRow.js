import React, { useCallback } from "react";
import classes from "./TableRow.module.scss";
import { useDispatch, useSelector } from "react-redux";
import { toggleSelectElement } from "../../store/editingSlice";
import { parse, format } from "date-fns";

const TableRow = (props) => {
  const dispatch = useDispatch();
  const student = props.student;

  const { selectedElements, editableData } = useSelector(
    (state) => state.editing
  );

  const isSelected = selectedElements.includes(student);
  const isEditing = editableData && editableData.id === student.id;

  const handleToggleSelect = useCallback(() => {
    dispatch(toggleSelectElement(student));
  }, [dispatch, student]);

  // Funzione per convertire la data nel formato desiderato (dd-MM-yyyy)
  const formatDate = (dateString) => {
    // Verifica se la data è nel formato yyyy-MM-dd
    if (dateString.match(/^\d{4}-\d{2}-\d{2}$/)) {
      return format(parse(dateString, "yyyy-MM-dd", new Date()), "dd-MM-yyyy");
    }
    // Se la data è già nel formato dd-MM-yyyy, restituiscila così com'è
    return dateString;
  };

  return (
    <tr
      className={`${
        isSelected ? (isEditing ? "table-dark" : "table-warning") : ""
      } ${classes.cursor}`}
      onClick={handleToggleSelect}
    >
      <th>{props.index + 1}</th>
      <td className="fw-normal">{student.name}</td>
      <td>{student.surname}</td>
      <td>{formatDate(student.dateOfBirth)}</td>
    </tr>
  );
};

export default TableRow;
