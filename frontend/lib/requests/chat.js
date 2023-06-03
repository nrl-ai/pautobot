export const getChatHistory = () => {
  const response = fetch("/api/chat_history", {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  });
  return response;
};

export const clearChatHistory = () => {
  const response = fetch("/api/chat_history", {
    method: "DELETE",
    headers: {
      "Content-Type": "application/json",
    },
  });
  return response;
};
