import Form from "react-bootstrap/Form";
import Button from "react-bootstrap/Button";
import { useFormValidation } from "../../hooks/use-form-validation";
import { Container } from "react-bootstrap";
import { useEffect, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { updateData, applyEdit } from "../../store/editingSlice";
import { v4 as uuidv4 } from "uuid";
import { format, parse } from "date-fns";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import classes from "./InputTableRow.module.scss";
import { faPlus, faCheck, faMinus } from "@fortawesome/free-solid-svg-icons";

const InputTableRow = (props) => {
    const dispatch = useDispatch();
    const { editableData } = useSelector((state) => state.editing);
    const disableEdit = useSelector((state) => state.editing.disableEdit);

    const [showForm, setShowAddRow] = useState(false);
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
            console.log(editableData.dateOfBirth);
            setFormState({
                id: editableData.id,
                name: editableData.name,
                surname: editableData.surname,
                dateOfBirth: format(
                    parse(editableData.dateOfBirth, "dd-MM-yyyy", new Date()),
                    "yyyy-MM-dd"
                ),
            });
            setShowAddRow(true);
        }
    }, [editableData]);

    const handleSubmit = () => {
        const submitData = {
            ...formState,
            dateOfBirth: format(
                parse(formState.dateOfBirth, "yyyy-MM-dd", new Date()),
                "dd-MM-yyyy"
            ),
        };

        console.log(disableEdit);
        if (disableEdit) {
            // If editing is disabled, it means we're adding a new entry
            const newEntry = { ...submitData, id: uuidv4() };
            dispatch(updateData(newEntry));
        } else {
            // If editing is enabled, we're updating an existing entry
            // Make sure to pass the existing ID to retain the link to the entry being edited
            console.log(submitData);

            const updatedEntry = { ...submitData, id: editableData.id };
            dispatch(applyEdit(updatedEntry));
        }
    };

    const inputRow = (
        <tr>
            {showForm && (
                <>
                    <th>
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
                    </th>
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
                </>
            )}

            <td>
                <Container className="d-flex align-items-center justify-content-center p-0 m-0 gap-1">
                    {!showForm ? (
                        <FontAwesomeIcon
                            icon={faPlus}
                            size="1x"
                            className={`text-primary p-1 bg-light ${classes.cursorPointer}`}
                            onClick={() => setShowAddRow((prevValue) => !prevValue)}
                        />
                    ) : (
                        <>
                            <FontAwesomeIcon
                                icon={faMinus}
                                size="1x"
                                className={`text-primary p-1 bg-light ${classes.cursorPointer}`}
                                onClick={() => setShowAddRow((prevValue) => !prevValue)}
                            />
                            <button
                                className={classes.submitBtn}
                                onClick={handleSubmit}
                                type="submit"
                            >
                                <FontAwesomeIcon
                                    icon={faCheck}
                                    size="1x"
                                    className={`text-success p-1 bg-light ${classes.cursorPointer}`}
                                />
                            </button>
                        </>
                    )}
                </Container>
            </td>
        </tr>
    );

    return <>{inputRow}</>;
};

export default InputTableRow;
