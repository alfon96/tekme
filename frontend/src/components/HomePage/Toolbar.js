import Button from "react-bootstrap/Button";
import ButtonGroup from "react-bootstrap/ButtonGroup";
import ButtonToolbar from "react-bootstrap/ButtonToolbar";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";

import {
  faTrash,
  faRotateRight,
  faRotateLeft,
  faFloppyDisk,
  faPen,
  faMinus,
  faPlus,
} from "@fortawesome/free-solid-svg-icons";
import { useSelector, useDispatch } from "react-redux";
import {
  redo,
  undo,
  del,
  startEdit,
  toggleShowForm,
} from "../../store/editingSlice";

function Toolbar(props) {
  const dispatch = useDispatch();
  const {
    disableRedo,
    disableUndo,
    disableDel,
    disableSave,
    disableEdit,
    toggleAddMinus,
  } = useSelector((state) => state.editing);

  return (
    <ButtonToolbar aria-label="Toolbar with button groups">
      <ButtonGroup className="mb-3" aria-label="Toolbar buttons group">
        <Button
          variant="info"
          size="sm"
          onClick={() => dispatch(toggleShowForm())}
        >
          <FontAwesomeIcon
            icon={toggleAddMinus ? faMinus : faPlus}
            size="1x"
            className={`text-white`}
          />
        </Button>
        <Button
          variant="success"
          size="sm"
          disabled={disableSave}
          onClick={() => props.handleSave()}
        >
          <FontAwesomeIcon
            icon={faFloppyDisk}
            size="1x"
            className={`text-white`}
          />
        </Button>
        <Button
          variant="dark"
          size="sm"
          disabled={disableUndo}
          onClick={() => dispatch(undo())}
        >
          <FontAwesomeIcon
            icon={faRotateLeft}
            size="1x"
            className={`text-white `}
          />
        </Button>{" "}
        <Button
          variant="primary"
          size="sm"
          disabled={disableRedo}
          onClick={() => dispatch(redo())}
        >
          <FontAwesomeIcon
            icon={faRotateRight}
            size="1x"
            className={`text-white `}
          />
        </Button>{" "}
        <Button
          variant="warning"
          size="sm"
          disabled={disableEdit}
          onClick={() => dispatch(startEdit())}
        >
          <FontAwesomeIcon icon={faPen} size="1x" className={`text-white`} />
        </Button>
        <Button
          variant="danger"
          size="sm"
          disabled={disableDel}
          onClick={() => dispatch(del())}
        >
          <FontAwesomeIcon icon={faTrash} size="1x" className={`text-white`} />
        </Button>
      </ButtonGroup>
    </ButtonToolbar>
  );
}

export default Toolbar;
