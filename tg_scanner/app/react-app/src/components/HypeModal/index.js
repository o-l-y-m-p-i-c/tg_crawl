import { useContext } from "react";
import { AppContext } from "../../providers/AppProvider";

const HypeModal = () => {
  const { modalData, closeModal } = useContext(AppContext);
  return (
    <div
      style={{
        display: "flex",
        gap: 20,
      }}
    >
      {/* {JSON.stringify(modalData)} */}

      {modalData && (
        <a
          className="button open-button"
          target={"blank"}
          href={`https://t.me/@${modalData.telegram_username}`}
        >
          Open channel
        </a>
      )}
      <button className="button close-button" onClick={closeModal}>
        <svg
          fill="#000000"
          height="15px"
          width="15px"
          version="1.1"
          id="Capa_1"
          xmlns="http://www.w3.org/2000/svg"
          xmlnsXlink="http://www.w3.org/1999/xlink"
          viewBox="0 0 490 490"
          xmlSpace="preserve"
        >
          <polygon
            points="456.851,0 245,212.564 33.149,0 0.708,32.337 212.669,245.004 0.708,457.678 33.149,490 245,277.443 456.851,490 
489.292,457.678 277.331,245.004 489.292,32.337 "
          ></polygon>
        </svg>
      </button>
    </div>
  );
};

export { HypeModal };
