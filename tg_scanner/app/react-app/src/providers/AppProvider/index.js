import { createContext, useState } from "react";

export const AppContext = createContext({});

export const AppProvider = ({ children }) => {
  const [modalIsOpen, setIsOpen] = useState(false);
  const [searchInput, setSearchInput] = useState(null);
  const [modalData, setModalData] = useState(null);

  function closeModal() {
    setIsOpen(false);
    setModalData(null);
  }

  function openModal(data) {
    setModalData(data);
    setIsOpen(true);
  }

  const onChange = (e) => {
    setSearchInput(e.target.value === "" ? null : e.target.value);
  };

  return (
    <AppContext.Provider
      value={{
        modalIsOpen,
        setIsOpen,
        searchInput,
        setSearchInput,
        modalData,
        setModalData,
        closeModal,
        openModal,
        onChange,
      }}
    >
      {children}
    </AppContext.Provider>
  );
};
