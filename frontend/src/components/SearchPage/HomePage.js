import { Container, Row, Col } from 'react-bootstrap';
import CustomNavbar from '../Navbar/CustomNavbar';
import classes from './HomePage.module.scss';
import ListGroup from 'react-bootstrap/ListGroup';
import Accordion from 'react-bootstrap/Accordion';
import Button from 'react-bootstrap/Button';
import React, { useState } from 'react';
import { Offcanvas } from 'react-bootstrap';

import Sidebar from '../Sidebar/Sidebar'
const HomePage = () => {
    const [show, setShow] = useState(false);

    const handleToggle = () => setShow(!show);

    return <>
        <CustomNavbar />
        <Container fluid className={`${classes.bgImage}`}>
            <Row>
                <Col md={3} className='ps-0'>
                    <Sidebar>
                        <Accordion defaultActiveKey="0">
                            <Accordion.Item eventKey="0">
                                <Accordion.Header>Section A</Accordion.Header>
                                <Accordion.Body className="text-center">
                                    <Button className="m-1">1A</Button>
                                    <Button className="m-1">2A</Button>
                                    <Button className="m-1">3A</Button>
                                    <Button className="m-1">4A</Button>
                                    <Button className="m-1">5A</Button>
                                </Accordion.Body>
                            </Accordion.Item>
                            <Accordion.Item eventKey="1">
                                <Accordion.Header>Section B</Accordion.Header>
                                <Accordion.Body>
                                    Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do
                                    eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad
                                    minim veniam, quis nostrud exercitation ullamco laboris nisi ut
                                    aliquip ex ea commodo consequat. Duis aute irure dolor in
                                    reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla
                                    pariatur. Excepteur sint occaecat cupidatat non proident, sunt in
                                    culpa qui officia deserunt mollit anim id est laborum.
                                </Accordion.Body>
                            </Accordion.Item>
                        </Accordion>

                    </Sidebar>
                </Col>
                <Col md={8}>
                    
                </Col>
            </Row>
        </Container >
    </>
}

export default HomePage;








// <Col xs={3} id="sidebar-wrapper" className='bg-light py-4 '>

// <Accordion>
//     <Accordion.Item eventKey="0">
//         <Accordion.Header>Accordion Item #1</Accordion.Header>
//         <Accordion.Body className="d-flex flex-column gap-2 px-5">
//             <Button>1 A</Button>
//             <Button>2 A</Button>
//             <Button>3 A</Button>
//             <Button>4 A</Button>
//             <Button>5 A</Button>
//         </Accordion.Body>
//     </Accordion.Item>
//     <Accordion.Item eventKey="1">
//         <Accordion.Header>Accordion Item #2</Accordion.Header>
//         <Accordion.Body>
//             Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do
//             eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad
//             minim veniam, quis nostrud exercitation ullamco laboris nisi ut
//             aliquip ex ea commodo consequat. Duis aute irure dolor in
//             reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla
//             pariatur. Excepteur sint occaecat cupidatat non proident, sunt in
//             culpa qui officia deserunt mollit anim id est laborum.
//         </Accordion.Body>
//     </Accordion.Item>
// </Accordion>

// </Col>
// <Col xs={9} id="page-content-wrapper">
// {/* Qui puoi aggiungere i tuoi widget come componenti di React */}
// </Col>