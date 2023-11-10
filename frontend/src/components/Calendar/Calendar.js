import classes from "./Calendar.module.scss";
import { useEffect, useState } from "react";
import SimpleModal from "../../UI/SimpleModal";
import CalendarCard from "./CalendarCard";
import { Button } from "react-bootstrap";

const DUMMY_ENTRIES = [
  {
    id: 0,
    classes: 5,
    break: 5,
    date: "01",
    detail: { Olga: "Spopovic was a good boy" },
  },
  {
    id: 1,
    classes: 4,
    break: 5,
    date: "02",
    detail: { Olga: "Spopovic was a good kid" },
  },
  {
    id: 2,
    classes: 5,
    break: 4,
    date: "03",
    detail: { Olga: "Spopovic slept all day" },
  },
  {
    id: 3,
    classes: 3,
    break: 3,
    date: "04",
    detail: { Olga: "Spopovic created drawing of putin" },
  },

  {
    id: 4,
    classes: 1,
    break: 2,
    date: "05",
    detail: { Olga: "Spopovic mixed elements to create vodka" },
  },
  {
    id: 5,
    classes: 3,
    break: 5,
    date: "08",
    detail: { Olga: "Spopovic jumped on a table and spit on Lenovic" },
  },
  { id: 6, classes: 5, break: 5, date: "09" },
  { id: 7, classes: 5, break: 5, date: "10" },
  {
    id: 8,
    classes: 4,
    break: 5,
    date: "11",
    detail: { Karola: "Spopovic created mathematical formula" },
  },
  { id: 9, classes: 5, break: 4, date: "12" },
  { id: 10, classes: 3, break: 3, date: "15" },

  {
    id: 11,
    classes: 5,
    break: 5,
    date: "16",
    detail: { Karola: "Spopovic stopped believing in Christmas values" },
  },
  { id: 12, classes: 5, break: 5, date: "17" },
  {
    id: 13,
    classes: 4,
    break: 5,
    date: "18",
    detail: { Karola: "Spopovic adehers to communist party" },
  },
  {
    id: 14,
    classes: 5,
    break: 4,
    date: "19",
    detail: { Karola: "Spopovic lost free thinking ability" },
  },
  { id: 15, classes: 3, break: 3, date: "20" },

  { id: 16, classes: 5, break: 5, date: "23" },
  { id: 17, classes: 5, break: 5, date: "24" },
  {
    id: 18,
    classes: 4,
    break: 5,
    date: "25",
    detail: { Karola: "Spopovic collects wheat during break" },
  },
  { id: 19, classes: 5, break: 4, date: "26" },
  {
    id: 20,
    classes: 3,
    break: 3,
    date: "27",
    detail: { Karola: "Spopovic buys car from 1920" },
  },

  { id: 21, classes: 5, break: 5, date: "30" },
  {
    id: 22,
    classes: 5,
    break: 5,
    date: "31",
    detail: {
      Karola:
        "Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt. Neque porro quisquam est, qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit, sed quia non numquam eius modi tempora incidunt ut labore et dolore magnam aliquam quaerat voluptatem. Ut enim ad minima veniam, quis nostrum exercitationem ullam corporis suscipit laboriosam, nisi ut aliquid ex ea commodi consequatur? Quis autem vel eum iure reprehenderit qui in ea voluptate velit esse quam nihil molestiae consequatur, vel illum qui dolorem eum fugiat quo voluptas nulla pariatur?",
    },
  },
];

const Calendar = (props) => {
  const [modalInfo, setModalInfo] = useState({ show: false, data: {} });

  const handleModalShow = (dayInfo) => {
    setModalInfo({ show: true, data: { ...dayInfo } });
  };
  const handleModalClose = () => setModalInfo({ show: false, data: {} });

  function getDayNumber(dateTimeObj) {
    const date = new Date(dateTimeObj);
    return date.getDate().toString().padStart(2, "0");
  }

  const childData = props.fetchedData;

  function getModalBody(data) {
    // Create the Body of the Modal with Classes and Breaks Score and
    // adding the details and teacher's name 
    return (
      <>

        {/* Classes And Breaks Score */}
        {data && (
          <div className="mb-5">
            <p className=" mb-2">
              <strong>Classes:</strong> {data.classes}/5
            </p>
            <p className="">
              <strong>Break:</strong> {data.breaks}/5
            </p>
          </div>
        )}

        {/* Details And Teacher's Name */}
        {data && data.detail ? (
          <>
            <p className="text-center fst-italic mb-5">
              "{data.detail}"
            </p>
            <span className="d-block text-end">
              {" "}
              Tr -{" "}
              <span className="text-center text-dark fw-semibold fst-italic">
                {data.teacher}
              </span>
            </span>
          </>
        ) : (
          <p className="text-center fst-italic mb-5">
            No details present for this day
          </p>
        )}
      </>
    );
  }

  return (
    <>
      <section
        className={`text-center overflow-x-hidden`}
      >
        {/* Actual Calendar */}
        {childData.length > 0 ?
          <div className="row p-5 justify-content-start">
            {
              childData.map((dayInfo) => (
                <div className="col-xl-2 col-lg-3 col-md-3 col-sm-4 col-xs-6 mb-3">
                  <CalendarCard data={dayInfo} handleModalShow={handleModalShow} />
                </div>
              ))

            }

            {/* Details Modal */}
            <SimpleModal
              show={modalInfo.show}
              title={`${getDayNumber(
                modalInfo.data.date
              )} - ${props.selectedMonthYear}`}
              body={getModalBody(modalInfo.data)}
              handleModalClose={handleModalClose}
              actionBtnText="Ask Teacher"
            />

          </div>
          :
          <div className="container-sm mx-auto w-75 my-6 py-5 opacity-75 rounded-5 bg-light">
            <h5 className="text-center text-dark">No entries for this month</h5>
          </div>

        }
      </section>
    </>
  );
};

export default Calendar;
