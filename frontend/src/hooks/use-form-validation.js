import { useState, useEffect } from 'react';
import * as Yup from 'yup';

// Define the validation schema outside the hook for performance reasons
const validationSchema = Yup.object().shape({
    email: Yup.string().email('Invalid email').required('Email is required'),
    password: Yup.string().matches(
        /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@#$%^&*!])[A-Za-z\d@#$%^&*!]{8,}$/,
        'Invalid Password'
    ).required('Password is required'),
    name: Yup.string().required('Name is required'),
    surname: Yup.string().required('Surname is required'),
    dateOfBirth: Yup.date()
        .transform((value, originalValue) => {
            // Se la stringa è vuota, restituisci null per evitare "Invalid Date"
            return originalValue === '' ? null : new Date(originalValue);
        })
        .max(new Date(), 'Date of birth cannot be in the future')
        .required('Date of birth is required')
        .typeError('Date of birth is not valid'), // Messaggio personalizzato per tipo non valido
});

export const useFormValidation = (initialState) => {
    const [formState, setFormState] = useState(initialState);
    const [errors, setErrors] = useState({});
    const [touched, setTouched] = useState({}); // Aggiunto per tenere traccia dei campi che sono stati modificati
    const [isSubmitting, setIsSubmitting] = useState(false);

    // Validate the field on blur or change if it's already been touched
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

        // Se il campo è stato già toccato, valida al cambiamento
        if (touched[name]) {
            validateField(name, value);
        }
    };

    const handleBlur = (e) => {
        const { name, value } = e.target;
        setTouched((prev) => ({ ...prev, [name]: true })); // Imposta il campo come "toccato"
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
