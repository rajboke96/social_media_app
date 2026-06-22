import { createPortal } from 'react-dom';
import style from './Modal.module.css';

function Modal({ open, onClose, children }) {
  if (!open) return null;

  return createPortal(
    <div className={style.overlay} onClick={onClose}>
      <div className={style.modal} onClick={(e) => e.stopPropagation()}>
        <button className={style.close} onClick={onClose}>×</button>
        {children}
      </div>
    </div>,
    document.body
  );
}

export default Modal;
