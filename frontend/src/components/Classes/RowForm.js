import { useEffect, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { useFormValidation } from "../../hooks/use-form-validation";
import Form from "react-bootstrap/Form";
import { v4 as uuidv4 } from "uuid";
import { format, parse } from "date-fns";
import {
  updateData,
  toggleDisableAdd,
  applyEdit,
} from "../../store/editingSlice";
import { Button } from "react-bootstrap";

const RowForm = () => {
  const dispatch = useDispatch();
  const { editableData, toggleShowForm, disableEdit } = useSelector(
    (state) => state.editing
  );

  const {
    formState,
    setFormState,
    errors,
    handleChange,
    handleBlur,
    isSubmitting,
  } = useFormValidation({
    name: editableData ? editableData.name : "",
    surname: editableData ? editableData.surname : "",
    dateOfBirth: editableData ? editableData.dateOfBirth : "",
  });

  useEffect(() => {
    if (editableData) {
      const formattedDate = editableData.dateOfBirth
        ? format(
            parse(editableData.dateOfBirth, "dd-MM-yyyy", new Date()),
            "yyyy-MM-dd"
          )
        : "";

      setFormState({
        id: editableData.id,
        name: editableData.name,
        surname: editableData.surname,
        dateOfBirth: formattedDate,
      });
    }
  }, [editableData, setFormState]);

  const handleSubmit = (e) => {
    try {
      e.preventDefault();

      const submitData = formState;

      if (disableEdit) {
        // If editing is disabled, it means we're adding a new entry
        const newEntry = { ...submitData, id: uuidv4() };

        dispatch(updateData(newEntry));
      } else {
        // If editing is enabled, we're updating an existing entry

        const updatedEntry = { ...submitData, id: editableData.id };
        dispatch(applyEdit(updatedEntry));
      }
    } catch (error) {
      console.error("Errore nella formattazione della data:", error);
      // Gestisci l'errore come preferisci
    }
  };

  return (
    <tr>
      <th>
        <Button
          type="submit"
          disabled={isSubmitting || formState.dateOfBirth === ""}
          onClick={(e) => handleSubmit(e)}
        ></Button>
      </th>
      <td>
        <Form.Group>
          <Form.Control
            type="text"
            name="name"
            placeholder="Name"
            className="m-0 py-0 bg-light "
            value={formState.name}
            onChange={handleChange}
            onBlur={handleBlur}
          />
          {errors.name && (
            <Form.Text className="text-muted fw-normal">
              {errors.name}
            </Form.Text>
          )}
        </Form.Group>
      </td>
      <td>
        <Form.Group>
          <Form.Control
            type="text"
            name="surname"
            placeholder="Surname"
            className="m-0 py-0 bg-light "
            value={formState.surname}
            onChange={handleChange}
            onBlur={handleBlur}
          />
          {errors.surname && (
            <Form.Text className="text-muted fw-normal">
              {errors.surname}
            </Form.Text>
          )}
        </Form.Group>
      </td>
      <td>
        <Form.Group>
          <Form.Control
            type="date"
            name="dateOfBirth"
            placeholder="Birth Date"
            className="m-0 py-0 bg-light "
            value={formState.dateOfBirth}
            onChange={handleChange}
            onBlur={handleBlur}
          />
          {errors.dateOfBirth && (
            <Form.Text className="text-muted fw-normal">
              {errors.dateOfBirth}
            </Form.Text>
          )}
        </Form.Group>
      </td>
    </tr>
  );
};

export default RowForm;
