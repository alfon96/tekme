import classes from "./Details.module.css";

const Details = (props) => {
  return (
    <div className={classes.detailsCard}>
      <h2>Details</h2>
      <p className={classes.teacher}>
        <strong>Teacher</strong>: {props.teacher}
      </p>
      <span className={classes.noteSpan}>Note:</span>
      <p className={classes.noteContent}>
        <i>" {props.detail} "</i>
      </p>
    </div>
  );
};

export default Details;
