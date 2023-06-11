export const getChatHistory = (contextId) => {
  const response = fetch(`/api/${contextId}/chat_history`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  });
  return response;
};

export const clearChatHistory = (contextId) => {
  const response = fetch(`/api/${contextId}/chat_history`, {
    method: "DELETE",
    headers: {
      "Content-Type": "application/json",
    },
  });
  return response;
};
