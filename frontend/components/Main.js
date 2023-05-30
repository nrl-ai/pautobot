"use client";
import React, { useState, useRef, useEffect } from "react";
import { toast } from "react-toastify";
import NewMessage from "./NewMessage";

export default function Main() {
  const [messages, setMessages] = useState([]);
  const [thinking, setThinking] = useState(false);
  const messageBottomRef = useRef(null);

  useEffect(() => {
    const localData = localStorage.getItem("messages");
    if (!localData) {
      return;
    }
    let bkMessages = JSON.parse(localData);
    // Remove last message if it is "Thinking..."
    if (bkMessages && bkMessages.length > 0) {
      if (bkMessages[bkMessages.length - 1].answer === "Thinking...") {
        bkMessages.pop();
      }
    }
    setMessages(bkMessages);
  }, []);

  const saveMessages = (messages) => {
    localStorage.setItem("messages", JSON.stringify(messages));
  };

  const onSubmitMessage = (mode, message) => {
    if (thinking) {
      toast.warning("I am thinking about previous question! Please wait...");
      return;
    }
    setThinking(true);
    let newMessages = [
      ...messages,
      { query: message },
      { answer: "Thinking..." },
    ];
    setMessages(newMessages);
    saveMessages(newMessages);
    // Scroll to bottom
    setTimeout(() => {
      messageBottomRef.current.scrollTop =
        messageBottomRef.current.scrollHeight;
    }, 500);

    // Submit to PrivateGPT /api/ask
    fetch("/api/ask", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ mode: mode, query: message }),
    })
      .then(async (response) => {
        let data = await response.json();
        if (!response.ok) {
          const error = (data && data.message) || response.status;
          return Promise.reject(error);
        }

        // Query data from /api/get_answer
        const interval = setInterval(async () => {
          fetch("/api/get_answer", {
            method: "GET",
            headers: {
              "Content-Type": "application/json",
            },
          }).then(async (response) => {
            let data = await response.json();
            if (!response.ok) {
              const error = (data && data.message) || response.status;
              return Promise.reject(error);
            }
            if (data.status == "THINKING" && data.answer) {
              newMessages.pop();
              newMessages = [
                ...newMessages,
                { answer: data.answer, docs: null },
              ];
              setMessages(newMessages);
              saveMessages(newMessages);
              setTimeout(() => {
                messageBottomRef.current.scrollIntoView({ behavior: "smooth" });
              }, 500);
            } else if (data.status == "READY") {
              clearInterval(interval);
              newMessages.pop();
              newMessages = [
                ...newMessages,
                { answer: data.answer, docs: data.docs },
              ];
              setMessages(newMessages);
              saveMessages(newMessages);
              setTimeout(() => {
                messageBottomRef.current.scrollIntoView({ behavior: "smooth" });
              }, 500);
              setThinking(false);
            }
          });
        }, 2000);
      })
      .catch((error) => {
        console.error("There was an error!", error);
        toast.error("There was an error!");
        setThinking(false);
      });
  };

  return (
    <>
      <div className="flex flex-col w-full xl:max-w-[800px] xl:mx-auto">
        <div className="mx-2 md:px-5 sm:py-4 flex-grow mb-[150px] pb-8 max-h-full pt-[50px] rounded-xl mt-8">
          <div className="text-black">
            {messages.map((message, index) => {
              if (message.query) {
                return (
                  <div key={index} className="flex justify-end mb-2">
                    <div className="bg-gray-50 rounded-lg p-3 md:max-w-[80%] break-all">
                      <p className="text-gray-700">{message.query}</p>
                    </div>
                  </div>
                );
              } else {
                return (
                  <div key={index} className="flex justify-start mb-2">
                    <div className="bg-gray-100 rounded-lg p-3 md:max-w-[80%] break-all">
                      <p className="text-gray-700 font-bold">
                        {message.answer}
                        {message.answer === "Thinking..." && (
                          <img src="/loading.svg" alt="Thinking..."></img>
                        )}
                      </p>
                      {message.docs && (
                        <div className="mt-2">
                          <div className="list-disc list-inside">
                            {message.docs.map((doc, index) => {
                              return (
                                <div key={index}>
                                  <p
                                    href={doc.url}
                                    target="_blank"
                                    className="text-blue-500"
                                  >
                                    {doc.source}
                                  </p>
                                  <p className="text-gray-700">{doc.content}</p>
                                </div>
                              );
                            })}
                          </div>
                        </div>
                      )}
                    </div>
                  </div>
                );
              }
            })}
            {messages.length === 0 && (
              <div className="text-center pt-20">
                <h1 className="text-4xl mb-4">Hello World!</h1>
                <h3 className="text-2xl text-gray-500 max-w-[600px] mx-auto">
                  We are in the mission of building an all-in-one task assistant
                  with PrivateGPT!
                </h3>
              </div>
            )}
            <div ref={messageBottomRef}></div>
          </div>
        </div>
        <div className="fixed left-[400px] right-0 bottom-0 xl:max-w-[1000px] xl:mx-auto">
          <NewMessage
            onSubmitMessage={(mode, message) => {
              onSubmitMessage(mode, message);
            }}
          />
          <div className="h-8 bg-white"></div>
        </div>
      </div>
    </>
  );
}
