import classes from "./CalendarCard.module.scss";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faEye, faComment } from "@fortawesome/free-solid-svg-icons";
import { Card, Button, Modal } from "react-bootstrap";
import { Tooltip, OverlayTrigger } from "react-bootstrap";
import { useEffect, useState } from "react";

const CalendarCard = (props) => {

    function getDayNumber(dateTimeObj) {
        const date = new Date(dateTimeObj);
        return date.getDate().toString().padStart(2, "0");
    }

    const getColorDetailsIcon = (data) => {

        if (data.detail && (data.classes >= 2 && data.breaks >= 2))
            return "text-primary opacity-75";
        if (data.detail && (data.classes === 1 || data.breaks === 1))
            return "text-secondary";
        return "text-muted opacity-50";

    }

    const getColorContactIcon = (data) => {
        if (data.detail && (data.classes === 1 || data.breaks === 1))
            return "text-dark";
        return "text-muted opacity-75";

    }


    return (
        <Card className={`bg-light border-0 shadow ${classes.customCard}`}>
            <Card.Body>
                {/* Date info */}
                <Card.Title className="text-start fw-bold fs-3">
                    {getDayNumber(props.data.date)}
                </Card.Title>
                {/* Score Info */}
                <ul className="list-unstyled">
                    {/* Classes Score  */}
                    <li className="list-item d-flex justify-content-between">
                        <span>Classes</span>
                        <span>
                            <strong>{props.data.classes}</strong>/5
                        </span>
                    </li>
                    {/* Break Score  */}
                    <li className="list-item d-flex justify-content-between">
                        <span>Break</span>
                        <span>
                            <strong>{props.data.breaks}</strong>/5
                        </span>
                    </li>
                </ul>
                {/* Details info */}
                <div className="d-flex ">
                    <OverlayTrigger
                        key="top"
                        placement="top"
                        overlay={
                            <Tooltip id={`${props.data.id}_details_btn`}>See Details</Tooltip>
                        }
                    >
                        <Button
                            variant="link"
                            className="p-0 text-start me-auto"
                            onClick={() => props.handleModalShow(props.data)}
                        >
                            <FontAwesomeIcon
                                icon={faEye}
                                size="1x"
                                className={`${getColorDetailsIcon(props.data)}`}
                            />
                        </Button>
                    </OverlayTrigger>

                    {/* Ask Teacher  */}
                    <OverlayTrigger
                        key="top"
                        placement="top"
                        overlay={
                            <Tooltip
                                id={`${props.data.id}_teacher_btn`}
                                className={classes.customTooltip}
                            >
                                Contact Teacher
                            </Tooltip>
                        }
                    >
                        <Button variant="link" className="p-0 text-end ms-auto">
                            <FontAwesomeIcon
                                icon={faComment}
                                size="1x"
                                className={`${getColorContactIcon(props.data)}`}
                            />
                        </Button>
                    </OverlayTrigger>
                </div>
            </Card.Body>
        </Card>
    );
};

export default CalendarCard;
