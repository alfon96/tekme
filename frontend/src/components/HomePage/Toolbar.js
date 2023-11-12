import Button from 'react-bootstrap/Button';
import ButtonGroup from 'react-bootstrap/ButtonGroup';
import ButtonToolbar from 'react-bootstrap/ButtonToolbar';
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faTrash, faPlus, faRotateLeft, faFloppyDisk } from "@fortawesome/free-solid-svg-icons";

function Toolbar(props) {
    return (
        <ButtonToolbar aria-label="Toolbar with button groups">
            <ButtonGroup className="mb-3  ms-auto" aria-label="First group">


                <Button variant="primary" disabled={props.disableUndo} onClick={() => props.undo()}>
                    <FontAwesomeIcon
                        icon={faRotateLeft}
                        size="1x"
                        className={`text-white `}
                    />
                </Button>{' '}

                <Button variant="danger">
                    <FontAwesomeIcon
                        icon={faTrash}
                        size="1x"
                        className={`text-white`}
                        onClick={() => props.del()}
                    />
                </Button> <Button variant="dark"><FontAwesomeIcon
                    icon={faFloppyDisk}
                    size="1x"
                    className={`text-white`}
                    onClick={() => props.save()}
                /></Button>{' '}
            </ButtonGroup>
        </ButtonToolbar>
    );
}

export default Toolbar;