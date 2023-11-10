import { Card } from "react-bootstrap";
import { Form, Button, Row, Container, Col, Check } from 'react-bootstrap';
import { useState } from 'react';
import classes from './LoginPage.module.scss'
import useHttp from "../hooks/use-http";
import { useDispatch } from 'react-redux';
import { login } from '../store/userSlice';


const LoginPage = () => {
    const [email, setEmail] = useState('');
    const [role, setRole] = useState('Teachers');
    const [password, setPassword] = useState('');
    const { isLoading, error, sendRequest } = useHttp();

    const dispatch = useDispatch();

    const handleSubmit = async (event) => {

        event.preventDefault();
        console.log("Entered ")
        const url = `http://localhost:8000/signin?role=${role}`
        console.log(url)
        const data = await sendRequest({ url: `http://localhost:8000/users/signin?role=${role}`, method: 'POST', body: { email, password } });

        const userData = {
            user_id: data.user_id,
            role: data.role,
            token: data.token,
        };
        
        console.log(userData);
        dispatch(login(userData));

    };

    const handleCheckboxChange = (event) => {
        const value = event.target.checked ? event.target.id : '';
        console.log(value)
        setRole(value);
    };

    return (
        <Container fluid className={`d-flex vh-100  overflow-x-hidden justify-content-center align-items-center position-relative ${classes.bgImage}`}>
            <Card className={`bg-light shadow border-0 rounded-5 p-4 position-relative z-3 ${classes.customCard}`}>
                <Card.Body>
                    <Card.Title className="text-primary fs-1 mb-4">Signin</Card.Title>
                    <Row className="justify-content-center">
                        <Col>
                            <Form onSubmit={handleSubmit}>

                                <Form.Group controlId="formBasicEmail">
                                    <Form.Label className="fw-semibold">Email address</Form.Label>
                                    <Form.Control
                                        type="email"
                                        placeholder="Enter email"
                                        value={email}
                                        onChange={(e) => setEmail(e.target.value)}
                                    />
                                </Form.Group>

                                <Form.Group controlId="formBasicPassword">
                                    <Form.Label className="fw-semibold mt-2">Password</Form.Label>
                                    <Form.Control
                                        type="password"
                                        placeholder="Password"
                                        value={password}
                                        onChange={(e) => setPassword(e.target.value)}
                                    />
                                </Form.Group>

                                <Form.Group>
                                    <Form.Text className="text-muted d-block mt-2">
                                        <a href="/forgot-password">Forgot your password?</a>
                                    </Form.Text>

                                </Form.Group>

                                <Form.Group className="mt-2 d-flex gap-3">
                                    <Form.Check
                                        type="checkbox"
                                        label="Teachers"
                                        id="Teachers"
                                        checked={role === 'Teachers'}
                                        onChange={handleCheckboxChange}
                                    />
                                    <Form.Check
                                        type="checkbox"
                                        label="Students"
                                        id="Students"
                                        checked={role === 'Students'}
                                        onChange={handleCheckboxChange}
                                    />
                                    <Form.Check
                                        type="checkbox"
                                        label="Parents"
                                        id="Parents"
                                        checked={role === 'Parents'}
                                        onChange={handleCheckboxChange}
                                    />
                                </Form.Group>


                                <Row className="mt-4">
                                    <Col sm={6} xs={12}>
                                        <Button variant="primary" type="submit">
                                            Sign In
                                        </Button>
                                    </Col>
                                    <Col xs={6}>
                                        <Form.Text className="text-muted">
                                            Don't have an account? <a href="/signup">Signup</a>
                                        </Form.Text>
                                    </Col>
                                </Row>

                            </Form>
                        </Col>
                    </Row>
                </Card.Body>
            </Card >
        </Container >
    );
};

export default LoginPage;