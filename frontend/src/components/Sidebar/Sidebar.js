import classes from './Sidebar.module.scss'
import { useState } from 'react';
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faChevronLeft, faChevronRight } from "@fortawesome/free-solid-svg-icons";
import Button from 'react-bootstrap/Button';
import { Container, Row, Col } from 'react-bootstrap';

const Sidebar = (props) => {
    const [isCollapse, setIsCollapse] = useState(false);
    return <div className={`py-6  ${isCollapse ? classes.collapsed : 'w-100'} ${classes.sidebar}`} >

        <button className={classes.toggleBtn} onClick={() => setIsCollapse((prevValue) => !prevValue)}>
            <FontAwesomeIcon
                icon={faChevronRight}
                size="1x"
                className={`text-dark z-3  ${isCollapse ? classes.sidebarIconLeft : classes.sidebarIconRight}`}
            />

        </button>

        {!isCollapse && props.children}

    </div >;
}

export default Sidebar;