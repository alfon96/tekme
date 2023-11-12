import { Container } from 'react-bootstrap';
import CustomNavbar from '../Navbar/CustomNavbar';
import classes from './HomePage.module.scss';
import Accordion from 'react-bootstrap/Accordion';
import Button from 'react-bootstrap/Button';
import React, { useState } from 'react';
import Sidebar from '../Sidebar/Sidebar'
import Classes from '../Classes/Classes';

const HomePage = () => {
    const [selectedClass, setSelectedClass] = useState('');

    return <>
        <CustomNavbar />
        <Container fluid className={`${classes.bgImage} m-0 p-0 d-flex gap-0`}>
            <Sidebar >
                <Accordion defaultActiveKey="0">
                    <Accordion.Item eventKey="0">
                        <Accordion.Header>Section A</Accordion.Header>
                        <Accordion.Body className="text-center">
                            <Button className="m-1" onClick={() => { setSelectedClass('1A') }}>1A</Button>
                            <Button className="m-1" onClick={() => { setSelectedClass('2A') }}>2A</Button>
                            <Button className="m-1" onClick={() => { setSelectedClass('3A') }}>3A</Button>
                            <Button className="m-1" onClick={() => { setSelectedClass('4A') }}>4A</Button>
                            <Button className="m-1" onClick={() => { setSelectedClass('5A') }}>5A</Button>
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

            <div className="px-5 flex-grow-1">
                <p className='pt-6'>Widgets</p>

                {selectedClass != '' && <Classes selectedClass={selectedClass}></Classes>}

            </div>
        </Container>
    </>
}

export default HomePage;

