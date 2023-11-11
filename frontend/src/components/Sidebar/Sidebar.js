import classes from './Sidebar.module.scss'
import { useState } from 'react';
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faChevronLeft, faChevronRight } from "@fortawesome/free-solid-svg-icons";
import Button from 'react-bootstrap/Button';
import { Container, Row, Col } from 'react-bootstrap';

const Sidebar = (props) => {
    const [isCollapse, setIsCollapse] = useState(false);
    return <Container fluid className={`vh-100 bg-light ms-0 py-6 position-relative ${isCollapse ? classes.collapsed : 'w-100'} ${classes.sidebar}`} >
        <Row className='gap-3'>
            <Col md={12}>
                <button className={classes.toggleBtn} onClick={() => setIsCollapse((prevValue) => !prevValue)}>
                    <FontAwesomeIcon
                        icon={faChevronRight}
                        size="1x"
                        className={`text-dark z-3  ${isCollapse ? classes.sidebarIconLeft : classes.sidebarIconRight}`}
                    />

                </button>
            </Col>
            <Col md={12}>
                {!isCollapse && props.children}
            </Col>


        </Row >
    </Container >;
}

export default Sidebar;