import { useState } from "react";

export default function NewMessage({ onSubmitMessage }) {
  const [mode, setMode] = useState("CHAT");
  const [message, setMessage] = useState("");

  return (
    <>
      <form className="w-full px-6">
        <label htmlFor="chat" className="sr-only">
          Your message
        </label>
        <div className="flex items-center bg-gray-200 pt-6 rounded-2xl overflow-hidden pb-8 px-2 shadow-lg">
          <select
            className="text-lg border border-gray-300 text-gray-900 py-3 rounded-l-2xl ml-4 border-l border-y focus:ring-gray-500 focus:border-gray-500 block w-[200px] px-2 focus:outline-none bg-gray-100"
            defaultValue={"CHAT"}
            onChange={(e) => setMode(e.target.value)}
          >
            <option value="CHAT">Chat</option>
            <option value="QA">Chat + Q&A</option>
          </select>
          <textarea
            rows="1"
            className="block mr-4 p-2.5 w-full text-lg text-gray-900 bg-white rounded-r-2xl border-gray-300 focus:border focus:ring-gray-500 focus:border-gray-600 focus:outline-none"
            placeholder="What are you thinking about?..."
            value={message}
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
