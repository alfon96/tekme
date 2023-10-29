import classes from "./ChildCard.module.css";
import { useState } from "react";
import Details from "../Details/Details";
import Modal from "../../UI/Modal";

const ChildCard = (props) => {
  const [showDetails, setShowDetails] = useState(false);
  // const [showTeacher, setShowTeacher] = useState(false);
  const childData = props.childData;

  const dateObj = new Date(childData.date);
  const dayNumber = dateObj.getDate();

  const toggleDetails = () => {
    setShowDetails((prevState) => !prevState);
  };
  return (
    <>
      {showDetails && (
        <Modal onClose={toggleDetails}>
          <Details teacher={childData.teacher} detail={childData.detail} />
        </Modal>
      )}

      <div
        className={`${
          childData.classes === 1 || childData.break === 1
            ? classes.poorValue
            : ""
        } ${classes.childCard}`}
        id={childData.id}
      >
        <h2 className={classes.date}>{dayNumber}</h2>
        <div className={classes.childData}>
          <p className={classes.dataRow}>
            Class
            <span>
              <strong>{childData.classes}</strong>/5
            </span>
          </p>
          <p className={classes.dataRow}>
            Break
            <span>
              <strong>{childData.breaks}</strong>/5
            </span>
          </p>
        </div>
        {childData.detail && (
          <div className={classes.actions}>
            <button onClick={toggleDetails} className={classes.actionBtn}>
              Details
            </button>
            <button className={classes.actionBtn}>Teacher</button>
          </div>
        )}
      </div>
    </>
  );
};

export default ChildCard;
