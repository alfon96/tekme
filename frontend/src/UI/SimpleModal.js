import classes from './SimpleModal.module.scss';
import { Button, Modal } from 'react-bootstrap';

const SimpleModal = (props) => {
    return <Modal show={props.show} className={classes.simpleModal} onHide={props.handleModalClose} centered>
        <Modal.Header closeButton >
            <Modal.Title className="text-dark">{props.title}</Modal.Title>
        </Modal.Header>
        <Modal.Body>
            {props.body}
        </Modal.Body>
        <Modal.Footer>
            <Button variant="outline-secondary" onClick={props.handleModalClose}>
                {props.closeBtnText ?? 'Close'}
            </Button>
            <Button variant="dark">{props.actionBtnText}</Button>
        </Modal.Footer>
    </Modal>
}

export default SimpleModal;


// {modalInfo.data && (
//     <div className="mb-5">
//         <p className=" mb-2" ><strong>Classes:</strong> {modalInfo.data.classes}/5</p>
//         <p className=""><strong>Break:</strong> {modalInfo.data.breaks}/5</p>
//     </div>
// )}

// {
//     modalInfo.data && modalInfo.data.detail ?
//         <>
//             <p className="text-center fst-italic mb-5">"{modalInfo.data.detail}"</p>
//             <span className="d-block text-end"> Tr - <span className="text-center text-dark fw-semibold fst-italic">{modalInfo.data.teacher}</span></span>
//         </>
//         : <p className="text-center fst-italic mb-5">No details present for this day</p>
// }