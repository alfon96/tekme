import { Container, Card } from 'react-bootstrap';
import classes from './Classes.module.scss'

const Classes = (props) => {
    return <Container fluid className="bg-light opacity-75 ">
        <p>No student present in this class.</p>
        <Card>
            <Card.Body>
                <Card.Header>

                </Card.Header>
            </Card.Body>

        </Card>
    </Container>;
}

export default Classes;