import { useFormValidation } from "../../hooks/use-form-validation";
import { useEffect, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { format, parse } from "date-fns";
import RowForm from "./RowForm";
const InputTableRow = (props) => {
  const dispatch = useDispatch();
  const { editableData, showForm } = useSelector((state) => state.editing);
  const disableEdit = useSelector((state) => state.editing.disableEdit);

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
     
      setFormState({
        id: editableData.id,
        name: editableData.name,
        surname: editableData.surname,
        dateOfBirth: format(
          parse(editableData.dateOfBirth, "dd-MM-yyyy", new Date()),
          "yyyy-MM-dd"
        ),
      });
    }
  }, [editableData]);

  return <RowForm />;
};

export default InputTableRow;
