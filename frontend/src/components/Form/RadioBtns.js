import classes from "./RadioBtns.module.css";

const RadioBtns = (props) => {
  return (
    <div>
      <input type="radio" id="option1" name="choice" value="1" />
      <label htmlFor="option1">Very Bad</label>
      <input type="radio" id="option2" name="choice" value="2" />
      <label for="option2">Bad</label>
      <input type="radio" id="option3" name="choice" value="3" />
      <label for="option3">Sufficient</label>
      <input type="radio" id="option4" name="choice" value="4" />
      <label for="option4">Good</label>
      <input type="radio" id="option5" name="choice" value="5" />
      <label for="option5">Excellent</label>{" "}
    </div>
  );
};

export default RadioBtns;
