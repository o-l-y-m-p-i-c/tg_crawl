import { useContext } from "react";
import { HypeChart } from "../../components/HypeChart";
import { SearchForm } from "../../components/SearchForm";
import { AppContext } from "../../providers/AppProvider";
import { HypeModal } from "../../components/HypeModal";
import Modal from "react-modal";
import { ModalOptions } from "../../constants";

const Home = () => {
  const { searchInput, modalIsOpen, closeModal, openModal } =
    useContext(AppContext);
  return (
    <>
      <SearchForm />
      <HypeChart searchInput={searchInput} openModal={openModal} />
      <Modal
        isOpen={modalIsOpen}
        onRequestClose={closeModal}
        style={ModalOptions}
        contentLabel="Example Modal"
      >
        <HypeModal />
      </Modal>
    </>
  );
};

export { Home };
