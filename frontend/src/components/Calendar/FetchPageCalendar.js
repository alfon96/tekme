import classes from "./FetchPageCalendar.module.scss";
import { useEffect, useState } from "react";
import Spinner from "../Spinner/Spinner";
import Calendar from "./Calendar";
import CalendarHeader from "./CalendarHeader";
import useApiCall from "../../hooks/use-api-call";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faComment, faChat } from "@fortawesome/free-solid-svg-icons";

const FetchPageCalendar = (props) => {
    const defaultMonthYear = () => {
        const now = new Date();
        const year = now.getFullYear();
        const month = (now.getMonth() + 1).toString().padStart(2, '0'); // Ensure it is two digits
        return `${month}/${year}`;
    }

    function getMonthYearName(monthYear) {
        const [month, year] = monthYear.split('/');
        const date = new Date(parseInt(year, 10), parseInt(month, 10) - 1, 1);
        const monthName = date.toLocaleString('en-US', { month: 'long' });
        return `${monthName}, ${year}`;
    }

    const [fetchedData, setFetchedData] = useState([]);
    const [monthYear, setMonthYear] = useState(defaultMonthYear());

    const uri = `http://localhost:8000/teachers/Spopovic/${monthYear}`;
    console.log(uri); // Now this will log every time the component renders

    const applyData = (fetchedData) => {
        // Save dadta coming from the http request handled by the custom hook
        setFetchedData(fetchedData);
    };

    // Custom Hook for API call
    const { callApi, loading, error } = useApiCall(uri, applyData);


    useEffect(() => {
        // Call the API everytime fetching Uri changes (that is due to the handleMonthSelection function)
        callApi();
    }, [monthYear])


    // Calculate the next or previous month and year
    const handleMonthSelection = (goToNext) => {
        setMonthYear((currentMonthYear) => {
            const [month, year] = currentMonthYear.split('/').map(Number);
            const newDate = new Date(year, month - 1 + (goToNext ? 1 : -1), 1);

            const newYear = newDate.getFullYear();
            const newMonth = (newDate.getMonth() + 1).toString().padStart(2, '0'); // Ensure it is two digits
            return `${newMonth}/${newYear}`;
        });
    };

    const childName = props.childName;

    return (
        <div className={`position-relative vh-100 text-center ${classes.calendarContainer} overflow-x-hidden`}>
            {/* Basic Information: Name, Age, Current Displayed Month & Year And Control Current Month Year */}
            <CalendarHeader childName={childName} handleMonthSelection={handleMonthSelection} selectedMonthYear={getMonthYearName(monthYear)} />

            {/* Handle Loading State And Possible Error in Fetching Data */}
            {loading && !error && <Spinner />}
            {error && <div className=" container-sm w-50 opacity-75 rounded-5 py-3 my-8 text-bg-danger fw-bold">Some Error Occurred</div>}

            {/* Show the Month Details using the fetched data */}
            {!error && !loading &&
                <Calendar fetchedData={fetchedData} handleMonthSelection={handleMonthSelection} selectedMonthYear={getMonthYearName(monthYear)}></Calendar>}

            {/* Show the Chat Btn */}
            {!error && !loading && <button className={classes.chatBtn}>
                <FontAwesomeIcon icon={faComment} size="2x" className="text-white"></FontAwesomeIcon></button>
            }
        </div >
    );
};

export default FetchPageCalendar;