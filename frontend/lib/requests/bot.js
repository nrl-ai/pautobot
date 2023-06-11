export const getBotInfo = () => {
  return fetch("/api/bot_info", {
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
    return Promise.resolve(data);
  });
};

export const ask = (contextId, mode, message) => {
  return fetch(`/api/${contextId}/ask`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ mode: mode, query: message }),
  }).then(async (response) => {
    let data = await response.json();
    if (!response.ok) {
      const error = (data && data.message) || response.status;
      return Promise.reject(error);
    }
    return Promise.resolve(data);
  });
};

export const queryBotResponse = (contextId) => {
  return fetch(`/api/${contextId}/get_answer`, {
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
    return Promise.resolve(data);
  });
};
