import classes from "./CalendarCard.module.scss";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faEye, faComment } from "@fortawesome/free-solid-svg-icons";
import { Card } from "react-bootstrap";


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

    const getColorDay = (data) => {
        if (data.detail && (data.classes === 1 || data.breaks === 1))
            return "text-secondary";
        return 'text-dark';
    }


    return (

        <Card className={`bg-light border-0 shadow ${classes.customCard}`}
            onClick={() => props.handleModalShow(props.data)}>
            <Card.Body>
                {/* Date info */}
                <Card.Title className={`text-start fw-bold fs-3 ${getColorDay(props.data)}`}>
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

            </Card.Body>
        </Card >

    );
};

export default CalendarCard;




// MAYBE GET RID OF THIS CODE:

// {/* Details info */}
// <div className="d-flex ">
// {
//     props.data.classes === 1 || props.data.breaks === 1 &&
//     <>
//         <OverlayTrigger
//             key="top"
//             placement="top"
//             overlay={
//                 <Tooltip id={`${props.data.id}_details_btn`}>See Details</Tooltip>
//             }
//         >
//             <Button
//                 variant="link"
//                 className="p-0 text-start me-auto"
//                 onClick={() => props.handleModalShow(props.data)}
//             >
//                 <FontAwesomeIcon
//                     icon={faEye}
//                     size="1x"
//                     className={`text-secondary`}
//                 />
//             </Button>
//         </OverlayTrigger>

//         {/* Ask Teacher  */}
//         <OverlayTrigger
//             key="top"
//             placement="top"
//             overlay={
//                 <Tooltip
//                     id={`${props.data.id}_teacher_btn`}
//                     className={classes.customTooltip}
//                 >
//                     Contact Teacher
//                 </Tooltip>
//             }
//         >
//             <Button variant="link" className="p-0 text-end ms-auto">
//                 <FontAwesomeIcon
//                     icon={faComment}
//                     size="1x"
//                     className={`$text-dark`}
//                 />
//             </Button>
//         </OverlayTrigger>
//     </>
// }


// </div>