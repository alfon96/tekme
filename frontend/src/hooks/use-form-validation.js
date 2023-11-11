import { useState, useEffect } from 'react';
import { object, string } from 'yup';

// Define the validation schema outside the hook for performance reasons
const validationSchema = object().shape({
    email: string().email('Invalid email').required('Email is required'),
    password: string().matches(
        /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@#$%^&*!])[A-Za-z\d@#$%^&*!]{8,}$/,
        'Invalid Password'
    ).required('Password is required'),
});

export const useFormValidation = (initialState) => {
    const [formState, setFormState] = useState(initialState);
    const [errors, setErrors] = useState({});
    const [isSubmitting, setIsSubmitting] = useState(false);

    // Validate the field on blur
    const validateField = async (name, value) => {
        try {
            // Validate the field only
            await validationSchema.validateAt(name, { [name]: value });
            setErrors((prev) => ({ ...prev, [name]: '' }));
        } catch (error) {
            setErrors((prev) => ({ ...prev, [name]: error.message }));
        }
    };

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormState((prev) => ({ ...prev, [name]: value }));
    };

    const handleBlur = (e) => {
        const { name, value } = e.target;
        validateField(name, value);
    };

    const isFormValid = () => Object.values(errors).every((error) => error === '');

    useEffect(() => {
        // Disable the submit button if there are any validation errors
        setIsSubmitting(!isFormValid());
    }, [errors]);

    return {
        formState,
        setFormState,
        errors,
        handleChange,
        handleBlur,
        isSubmitting,
    };
};
