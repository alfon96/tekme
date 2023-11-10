import classes from "./FetchPage.module.scss";
import { useEffect, useState } from "react";
import Spinner from "../Spinner/Spinner";


const FetchPage = (props) => {
    const [fetchedData, setFetchedData] = useState([]);
    const [isLoading, setIsLoading] = useState(false);
    const [isError, setIsError] = useState(false);
    const [fetchingMonth, setFetchingMonth] = useState(11);
    const [fetchingUri, setFetchingURI] = useState('http://localhost:8000/teachers/Spopovic/11');

    useEffect(() => {
        async function simpleFetch() {
            try {
                setIsError(false);
                setIsLoading(true);
                const Uri = fetchingUri;
                const response = await fetch(Uri);
                if (!response.ok) {
                    console.log('Uri');
                    console.log(fetchingUri);
                    throw new Error("Network response was not ok");
                }
                const result = await response.json();
                setFetchedData(result);
            } catch (error) {
                setIsError(true);
                console.error("Fetch error:", error);

            }
            setIsLoading(false);
        }
        simpleFetch();
    }, [fetchingUri]);

    const handleMonthSelection = (next) => {
        const actualSelectedMonth = fetchingMonth;
        if (next) {
            if (actualSelectedMonth != 12) {
                setFetchingMonth((prevValue) => prevValue + 1);
                setFetchingURI(`http://localhost:8000/teachers/Spopovic/${actualSelectedMonth + 1}}`);
            }
            else {
                setFetchingMonth(1);
                setFetchingURI(`http://localhost:8000/teachers/Spopovic/${1}}`);
            }
        }

        if (actualSelectedMonth != 1) {
            setFetchingMonth((prevValue) => prevValue - 1);
            setFetchingURI(`http://localhost:8000/teachers/Spopovic/${actualSelectedMonth - 1}}`);
        }
        else {
            setFetchingMonth(1);
            setFetchingURI(`http://localhost:8000/teachers/Spopovic/${1}}`);
        }

    }

    return (
        <>
            {isLoading && !isError && <Spinner></Spinner>}
            {isError && <p>Some Error Occurred</p>}
            {!isError && !isLoading && <props.Component fetchedData={fetchedData} handleMonthSelection={handleMonthSelection} selectedMonthYear={`${fetchingMonth}, 2023`}></props.Component>}

        </>
    );
};

export default FetchPage;