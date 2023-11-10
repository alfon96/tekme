import classes from "./Spinner.module.css";

const Spinner = () => {
  return (
    <div className={`container-lg d-flex justify-content-center align-items-center vh-100 ${classes.SpinnerContainer}`}>
      <div className={classes.SpinnerAnimateContainer}>
        <div className={classes.Spinner}></div>
        <div className={classes.Spinner}></div>
        <div className={classes.Spinner}></div>
        <div className={classes.Spinner}></div>
      </div>

      <p className={classes.LoadingText}>Fetching Data...</p>
    </div>
  );
};

export default Spinner;
