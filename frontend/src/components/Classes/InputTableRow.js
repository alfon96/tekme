import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button';
import { useFormValidation } from '../../hooks/use-form-validation';
import { Container } from "react-bootstrap";
import { useState } from 'react';

const InputTableRow = (props) => {
    const [showAddRow, setShowAddRow] = useState(false);
    const {
        formState,
        errors,
        handleChange,
        handleBlur,
        isSubmitting,
    } = useFormValidation({
        name: '',
        surname: '',
        dateOfBirth: ''
    });

    const inputRow = <>

        <tr>
            <th>-</th>
            <th>
                <Form.Group>
                    <Form.Control
                        type="text"
                        name="name"
                        placeholder="Name"
                        className="m-0 py-0"
                        value={formState.name}
                        onChange={handleChange}
                        onBlur={handleBlur}
                    />
                    {errors.name && <Form.Text className="text-muted fw-normal">{errors.name}</Form.Text>}
                </Form.Group>
            </th>
            <th>
                <Form.Group>
                    <Form.Control
                        type="text"
                        name="surname"
                        placeholder="Surname"
                        className="m-0 py-0"
                        value={formState.surname}
                        onChange={handleChange}
                        onBlur={handleBlur}
                    />
                    {errors.surname && <Form.Text className="text-muted fw-normal">{errors.surname}</Form.Text>}
                </Form.Group>
            </th>
            <th>
                <Form.Group>
                    <Form.Control
                        type="date"
                        name="dateOfBirth"
                        placeholder="Birth Date"
                        className="m-0 py-0"
                        value={formState.dateOfBirth}
                        onChange={handleChange}
                        onBlur={handleBlur}
                    />
                    {errors.dateOfBirth && <Form.Text className="text-muted fw-normal">{errors.dateOfBirth}</Form.Text>}
                </Form.Group>
            </th>
        </tr>

        {/* Submit new row */}
        <tr>
            <td colSpan={4}>
                <Container fluid className="d-flex justify-content-end ">
                    <Button
                        variant="outline-dark"
                        type="submit"
                        size="lg"
                        className="py-0 me-2"
                        onClick={() => setShowAddRow((prevValue) => !prevValue)}
                    >
                        -
                    </Button>
                    <Button
                        variant="outline-dark"
                        size="lg"
                        className="py-0 my-0"
                        disabled={isSubmitting}
                        type="submit"
                        onClick={() => props.handleSubmission(formState)}
                    >
                        Submit
                    </Button>
                </Container>
            </td>
        </tr>

    </>

    const addRowBtn = <tr>
        <td colSpan={4}>
            <Container fluid className="d-flex justify-content-center">
                <Button
                    variant="outline-dark"
                    type="submit"
                    size="lg"
                    className="py-0 my-0"
                    onClick={() => setShowAddRow((prevValue) => !prevValue)}
                >
                    +
                </Button>
            </Container>
        </td>
    </tr>

    return (
        <>
            {showAddRow && inputRow}
            {!showAddRow && addRowBtn}
        </>
    );
};

export default InputTableRow;
