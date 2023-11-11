export const validateEmail = (email) => {
    const emailPattern = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/;
    if (!email.match(emailPattern)) {
        return 'Invalid Email address';
    } else {
        return '';
    }
};

export const validatePassword = (password) => {
    const passwordPattern = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@#$%^&*!])[A-Za-z\d@#$%^&*!]{8,}$/;
    if (!password.match(passwordPattern)) {
        return 'Password must contain at least one uppercase, lowercase, number, special character and it has to be at least of length 8';
    } else {
        return '';
    }
};
