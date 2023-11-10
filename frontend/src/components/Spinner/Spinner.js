import classes from "./Spinner.module.scss";

const Spinner = () => {
  return (
    <div className={`container-sm  h-25 align-items-center justify-content-center ${classes.SpinnerContainer}`}>
      <div className={classes.SpinnerAnimateContainer}>
        <div className={classes.Spinner}></div>
        <div className={classes.Spinner}></div>
        <div className={classes.Spinner}></div>
        <div className={classes.Spinner}></div>
      </div>

      <p className={`text-muted mt-2 fw-semibold `}>Fetching Data...</p>
    </div>
  );
};

export default Spinner;
