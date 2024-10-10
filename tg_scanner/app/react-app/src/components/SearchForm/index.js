import { useContext } from "react";
import { AppContext } from "../../providers/AppProvider";

const SearchForm = () => {
  const { onChange } = useContext(AppContext);

  const onSubmit = (e) => {
    e.preventDefault();
  };

  return (
    <form onSubmit={onSubmit} className="form">
      <input type="text" onChange={onChange} placeholder="Search" />
    </form>
  );
};

export { SearchForm };
