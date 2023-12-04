import { Card } from "react-bootstrap";
import { Form, Button, Row, Container, Col } from "react-bootstrap";
import { useState } from "react";
import classes from "./LoginPage.module.scss";
import useHttp from "../hooks/use-http";
import { useDispatch } from "react-redux";
import { login } from "../store/userSlice";
import { useNavigate } from "react-router-dom";
import { useFormValidation } from "../hooks/use-form-validation";

const LoginPage = () => {
  const [role, setRole] = useState("teachers");
  const { isLoading, error, sendRequest } = useHttp();
  let navigate = useNavigate();

  const { formState, errors, handleChange, handleBlur, isSubmitting } =
    useFormValidation({
      email: "",
      password: "",
    });

  const dispatch = useDispatch();

  const handleSubmit = async (event) => {
    event.preventDefault();

    if (!isSubmitting) {
      // Perform the submission logic
      try {
        const url = `http://localhost:8000/users/signin?user_role=${role}`;
        const body = { email: formState.email, password: formState.password };

        const data = await sendRequest({
          url: url,
          method: "POST",
          body: body,
        });

        const userData = {
          user_id: data.user_id,
          role: data.role,
          token: data.token,
          fullName: data.full_name,
        };

        dispatch(login(userData));
        navigate("/home");
      } catch (error) {
        console.error(`An error occurred: ${error}`);
      }
    }
  };

  return (
    <Container
      fluid
      className={`d-flex vh-100 justify-content-center align-items-center ${classes.bgImage}`}
    >
      <Card
        className={`bg-lightshadow border-0 rounded-5 p-4 ${classes.customCard}`}
      >
        <Card.Body>
          <Card.Title className="text-primary fs-1 mb-4">Signin</Card.Title>
          <Row className="justify-content-center">
            <Col>
              <Form onSubmit={handleSubmit}>
                <Form.Group controlId="formBasicEmail">
                  <Form.Label className="fw-semibold">Email address</Form.Label>
                  <Form.Control
                    type="email"
                    name="email"
                    placeholder="Enter email"
                    value={formState.email}
                    onChange={handleChange}
                    onBlur={handleBlur}
                  />
                  {errors.email && (
                    <Form.Text className="text-danger">
                      {errors.email}
                    </Form.Text>
                  )}
                </Form.Group>

                <Form.Group controlId="formBasicPassword" className="mb-3">
                  <Form.Label className="fw-semibold mt-2">Password</Form.Label>
                  <Form.Control
                    type="password"
                    name="password"
                    placeholder="Password"
                    value={formState.password}
                    onChange={handleChange}
                    onBlur={handleBlur}
                  />
                  {errors.password && (
                    <Form.Text className="text-danger d-block">
                      {errors.password}
                    </Form.Text>
                  )}

                  <Form.Text
                    className={`text-muted text-center ${classes.passwordInfo} `}
                  >
                    {" "}
                    Password must be at least 8 characters long, contain
                    uppercase/lowercase letters, numbers and special characters.
                  </Form.Text>
                </Form.Group>

                <Form.Group>
                  <Form.Text className="text-muted d-block mt-3">
                    <a href="/forgot-password">Forgot your password?</a>
                  </Form.Text>
                </Form.Group>

                <Form.Group className="mt-2 d-flex gap-3">
                  <Form.Check
                    type="radio"
                    label="Teachers"
                    id="teachers"
                    checked={role === "teachers"}
                    onChange={() => setRole("teachers")}
                  />
                  <Form.Check
                    type="radio"
                    label="Students"
                    id="Students"
                    checked={role === "students"}
                    onChange={() => setRole("students")}
                  />
                  <Form.Check
                    type="radio"
                    label="Relatives"
                    id="relatives"
                    checked={role === "relatives"}
                    onChange={() => setRole("relatives")}
                  />
                </Form.Group>

                <Row className="mt-4">
                  <Col sm={6} xs={12}>
                    <Button
                      variant="primary"
                      className={`${isLoading ? classes.glowing : ""}`}
                      disabled={isSubmitting}
                      type="submit"
                    >
                      Sign In
                    </Button>
                  </Col>
                  <Col xs={6}>
                    <Form.Text className="text-muted">
                      Don't have an account? <a href="/signup">Signup</a>
                    </Form.Text>
                  </Col>
                </Row>

                {error && (
                  <p className="text-bg-danger p-0 m-0 mt-4 text-center rounded-pill opacity-75">
                    Looks Like our server is down, sorry!
                  </p>
                )}
              </Form>
            </Col>
          </Row>
        </Card.Body>
      </Card>
    </Container>
  );
};

export default LoginPage;
