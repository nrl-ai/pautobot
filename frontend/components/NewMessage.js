import { useEffect, useRef, useState } from "react";

export default function NewMessage({ onSubmitMessage }) {
  const defaultMode = "QA";
  const [mode, setMode] = useState(defaultMode);
  const [message, setMessage] = useState("");
  const textAreaRef = useRef(null);
  const MAX_LINES = 5; // Change this value to set the maximum number of lines
  useEffect(() => {
    // get number of lines in message
    const lines = message.split("\n").length;

    if (lines > MAX_LINES) {
      textAreaRef.current.rows = MAX_LINES;
      textAreaRef.current.style.overflowY = "auto";
    } else {
      textAreaRef.current.rows = lines;
      textAreaRef.current.style.overflowY = "hidden";
    }

    const borderRadius = lines > 1 ? "1rem" : "0";
    const borderWidth = lines > 1 ? "1px" : "0px";

    const styles = {
      transition: "all 0.1s ease-in-out",
      borderTopLeftRadius: borderRadius,
      borderBottomLeftRadius: borderRadius,
      borderLeftWidth: borderWidth
    };

    Object.assign(textAreaRef.current.style, styles);
  }, [message]);

  return (
    <>
      <form className="w-full px-6">
        <label htmlFor="chat" className="sr-only">
          Your message
        </label>
        <div className="flex items-center bg-gray-100 pt-6 rounded-2xl overflow-hidden pb-8 px-2 border-2">
          <select
            className="text-lg border-gray-500 text-gray-900 py-3 rounded-l-2xl ml-4 border focus:ring-gray-500 focus:border-gray-500 block w-[200px] px-2 focus:outline-none bg-gray-200"
            defaultValue={defaultMode}
            onChange={(e) => setMode(e.target.value)}
          >
            <option value="QA">Documents Q&A</option>
            <option value="CHAT">Chat</option>
          </select>
          <textarea
            rows="1"
            className="block mr-4 p-2.5 w-full text-lg text-gray-900 bg-white rounded-r-2xl border-gray-500 border-y border-r focus:ring-gray-500 focus:outline-none resize-none overflow-hidden"
            placeholder="How can I help?..."
            value={message}
            ref={textAreaRef}
            onChange={(e) => setMessage(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter" && !e.shiftKey) {
                e.preventDefault();
                if (!message) return;
                onSubmitMessage(mode, message);
                setMessage("");
              }
            }}
          ></textarea>
          <button
            type="submit"
            className="inline-flex justify-center p-2 text-gray-600 rounded-full cursor-pointer hover:bg-blue-100"
            onClick={(e) => {
              e.preventDefault();
              if (!message) return;
              onSubmitMessage(mode, message);
              setMessage("");
            }}
          >
            <svg
              aria-hidden="true"
              className="w-8 h-8 rotate-90"
              fill="currentColor"
              viewBox="0 0 20 20"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path d="M10.894 2.553a1 1 0 00-1.788 0l-7 14a1 1 0 001.169 1.409l5-1.429A1 1 0 009 15.571V11a1 1 0 112 0v4.571a1 1 0 00.725.962l5 1.428a1 1 0 001.17-1.408l-7-14z"></path>
            </svg>
            <span className="sr-only">Send message</span>
          </button>
        </div>
      </form>
    </>
  );
}
