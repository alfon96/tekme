import classes from "./AddCardBtn.module.css";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faAdd } from "@fortawesome/free-solid-svg-icons";
import { useState } from "react";
import Modal from "../../UI/Modal";
import AddChildCard from "../AddChildCard/AddChildCard";
const AddCardBtn = (props) => {
  const [isAddingCard, setIsAddingCard] = useState(false);

  const toggleisAddingCard = () => {
    setIsAddingCard((prevState) => !prevState);
  };

  return (
    <>
      {isAddingCard && (
        <Modal onClose={toggleisAddingCard}>
          <AddChildCard onAdded={props.appendChildData}></AddChildCard>
        </Modal>
      )}
      <div className={classes.AddCardBtnContainer}>
        <button className={classes.addBtn} onClick={toggleisAddingCard}>
          {" "}
          <FontAwesomeIcon icon={faAdd} className={classes.addIcon} />
        </button>
      </div>
    </>
  );
};

export default AddCardBtn;
