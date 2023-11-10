import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faChevronLeft, faChevronRight } from "@fortawesome/free-solid-svg-icons";
import { Button } from "react-bootstrap";
import classes from './CalendarHeader.module.scss'

const CalendarHeader = (props) => {
    return <div className="container position-relative z-3 mb-5">
        <div className="text-container">
            <h2 className="display-4 fw-bold mt-5 mb-4 text-primary">
                {props.childName}
            </h2>
            <div className="d-flex gap-5 align-items-center justify-content-center ">
                <Button className={`border-0 py-1 ${classes.monthSelection} bg-dark`} onClick={() => props.handleMonthSelection(false)} >
                    <FontAwesomeIcon
                        icon={faChevronLeft}
                        size="1x"
                        className={`text-white`}
                    />
                </Button>
                <h3 className="text-muted fs-5 px-3">{props.selectedMonthYear}</h3>
                <Button className={`border-0 py-1 ${classes.monthSelection} bg-primary`} onClick={() => props.handleMonthSelection(true)} >
                    <FontAwesomeIcon
                        icon={faChevronRight}
                        size="1x"
                        className={`text-white`}
                    />
                </Button>

            </div>

        </div>
    </div>;
}

export default CalendarHeader;