import classes from "./Details.module.css";

const Details = (props) => {
  const teacher = Object.keys(props.data);
  const content = props.data[teacher];
  return (
    <div className={classes.detailsCard}>
      <h2>Details</h2>
      <p className={classes.teacher}>
        <strong>Teacher</strong>: {teacher}
      </p>
      <span className={classes.noteSpan}>Note:</span>
      <p className={classes.noteContent}>
        <i>" {content} "</i>
      </p>
    </div>
  );
};

export default Details;
