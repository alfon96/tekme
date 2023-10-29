import classes from "./NumericFormField.module.css";

const FormField = (props) => {
  return (
    <>
      <label htmlFor={props.id}>{props.label}</label>
      <input
        className={`${classes.inputField}`}
        id={props.id}
        type="radio"
        value={props.value}
        onChange={props.onChange}
        min={props.min}
        max={props.max}
      />
    </>
  );
};

export default FormField;
