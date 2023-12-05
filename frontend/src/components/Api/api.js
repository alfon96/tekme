function getGradeAndNameForClass(inputString) {
  const numbersMatch = inputString.match(/\d+/g); // Match one or more digits
  const lettersMatch = inputString.match(/[a-zA-Z]+/g); // Match one or more letters (both lowercase and uppercase)

  const grade = numbersMatch ? parseInt(numbersMatch[0]) : 0; // Convert the first matched number to an integer
  const className = lettersMatch ? lettersMatch.join("") : ""; // Combine matched letters into a single string

  return { grade, className };
}

const getClasses = async (gradeName, multi = false, sendRequest, token) => {
  try {
    const { grade, className } = getGradeAndNameForClass(gradeName);
    const url = `http://localhost:8000/classes/?query=name%3D${className}%26grade%3D${grade}&multi=${multi}`;
    const headers = { Authorization: `Bearer ${token}` };

    const response = await sendRequest({
      url: url,
      method: "GET",
      headers: headers,
    });
    if (!response.results) {
      throw new Error("Network response was not ok");
    }
    return response.results;
  } catch (error) {
    throw new Error("Failed to load data", error);
  }
};

export default getClasses;
