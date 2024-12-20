import React, { useEffect, useRef, useState } from "react";

const otpCss = {
  width: "40px",
  height: "40px",
  margin: "100px",
  textAlign: "center",
  fontSize: "1.2em",
};

const Otp = ({ length, onSubmit }) => {
  const inputRef = useRef([]);
  const [value, setValue] = useState(new Array(length).fill(""));

  const onChangeHandler = ({ target: { value: inputValue } }, index) => {
    if (isNaN(inputValue)) return;

    const newValue = [...value];
    newValue[index] = inputValue.slice(-1);
    setValue(newValue);

    if (inputValue && index < length - 1) inputRef.current[index + 1].focus();

    const finalValue = newValue.join("");
    finalValue.length === length && onSubmit(finalValue);
  };

  const onClickHandler = (index) => inputRef.current[index].setSelectionRange(1, 1);

  const onKeyDownHandler = (e, index) => {
    if (e.key === "Backspace" && index > 0 && !value[index]) {
      inputRef.current[index - 1].focus();
    }
  };

  useEffect(() => {
    if (inputRef.current[0]) inputRef.current[0].focus();
  }, []);

  return (
    <div>
      <h3>Enter Your OTP</h3>
      <form>
        {value.map((item, index) => (
          <input
            key={index}
            ref={(input) => (inputRef.current[index] = input)}
            value={item}
            style={otpCss}
            placeholder="0"
            onChange={(e) => onChangeHandler(e, index)}
            onClick={() => onClickHandler(index)}
            onKeyDown={(e) => onKeyDownHandler(e, index)}
          />
        ))}
      </form>
    </div>
  );
};
export default Otp;