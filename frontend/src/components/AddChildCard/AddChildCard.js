import classes from "./AddChildCard.module.css";
import { useState } from "react";
import FormField from "../Form/NumericFormField";
const AddChildCard = (props) => {
  const CHAR_LIMIT = 250;
  const [actualChar, setActualChar] = useState(0);
  const [classesScore, setClassesScore] = useState(5);
  const [breaksScore, setBreaksScore] = useState(5);
  const [detail, setDetail] = useState("");

  const handleClassScoreChange = (event) => {
    setClassesScore(event.target.value);
  };
  const handleBreaksScoreChange = (event) => {
    setBreaksScore(event.target.value);
  };
  const handleDetailChange = (event) => {
    const count = event.target.value.length;
    if (count <= CHAR_LIMIT) {
      setDetail(event.target.value);
      setActualChar(count);
    }
  };

  return (
    <div className={classes.addChildCard}>
      <form className={classes.formChildDayLog}>
        <div className={classes.scoreBoard}>
          <div className={classes.formRow}>
            <FormField
              label="Classes Score"
              id="classes-score-field"
              value={classesScore}
              onChange={handleClassScoreChange}
              min="1"
              max="5"
            ></FormField>
          </div>
          <div className={classes.formRow}>
            <label htmlFor="child-breaks-score">Breaks score</label>
            <input
              className={`${classes.inputField}`}
              id="child-breaks-score"
              type="number"
              value={breaksScore}
              onChange={handleBreaksScoreChange}
              min="1" // Set the minimum allowed value
              max="5"
            />
          </div>
        </div>
        <div className={classes.formRow}>
          <label htmlFor="teacher-additional-detail">Details</label>
          <textarea
            className={`${classes.inputField} ${classes.details}`}
            id="child-breaks-score"
            value={detail}
            onChange={handleDetailChange}
            rows="4"
          />
          <p>
            {actualChar}/{CHAR_LIMIT}
          </p>
        </div>
        <div className={classes.formActionRow}>
          <button type="submit" className={`${classes.btn} ${classes.cancel}`}>
            Cancel
          </button>
          <button type="submit" className={`${classes.btn} ${classes.add}`}>
            Add
          </button>
        </div>
      </form>
    </div>
  );
};

export default AddChildCard;
