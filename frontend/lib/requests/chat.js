export const getChatHistory = () => {
  const response = fetch("/api/0/chat_history", {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  });
  return response;
};

export const clearChatHistory = () => {
  const response = fetch("/api/0/chat_history", {
    method: "DELETE",
    headers: {
      "Content-Type": "application/json",
    },
  });
  return response;
};
