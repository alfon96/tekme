import React, { useEffect, useRef, useState } from "react";
import { Container } from "react-bootstrap";
import Spinner from "../Spinner/Spinner";
import DataTable from "./DataTable";
import { useDispatch, useSelector } from "react-redux";
import { updateData } from "../../store/editingSlice";
import useHttp from "../../hooks/use-http";
import classes from "./Classes.module.scss";
import { v4 as uuidv4 } from "uuid";

const Classes = () => {
  const dispatch = useDispatch();
  const { isLoading, error, sendRequest } = useHttp();
  const { dataTitle, currentData } = useSelector((state) => state.editing);

  const token = useSelector((state) => state.auth.token);

  const addUniqueIds = (inputList) => {
    return inputList.map((item) => ({
      ...item,
      id: uuidv4(),
    }));
  };

  // Use Effect Needed to fetch ddata from the API
  useEffect(() => {
    const fetchData = async () => {
      if (currentData.length === 0) {
        try {
          const url = `http://localhost:8000/users/classes/${dataTitle}`;
          const headers = { Authorization: `Bearer ${token}` };
          const response = await sendRequest({ url, method: "GET", headers });
          const studentsWithIds = addUniqueIds(response.students);

          dispatch(updateData(...studentsWithIds));
        } catch (error) {
          console.error(`An error occurred: ${error}`);
        }
      }
    };

    fetchData();
  }, [dataTitle, sendRequest]);

  return (
    <Container fluid className={`${classes.tableContainer} py-4 rounded-5`}>
      {isLoading && <Spinner />}
      {!isLoading && !error && <DataTable />}
      {error && <p>There was an error</p>}
    </Container>
  );
};

export default Classes;
