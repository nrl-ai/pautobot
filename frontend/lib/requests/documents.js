export const ingestData = (contextId) => {
  return fetch(`/api/${contextId}/documents/ingest`, {
    method: "POST",
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

export const uploadDocument = (contextId, file) => {
  const formData = new FormData();
  formData.append("file", file);
  return fetch(`/api/${contextId}/documents`, {
    method: "POST",
    body: formData,
  }).then(async (response) => {
    let data = await response.json();
    if (!response.ok) {
      const error = (data && data.message) || response.status;
      console.log(error);
      return Promise.reject(error);
    }
    return Promise.resolve(data);
  });
};

export const openDocument = (contextId, documentId) => {
  return fetch(
    `/api/${contextId}/documents/${documentId}/open_in_file_explorer`,
    {
      method: "POST",
    }
  );
};

export const getDocuments = (contextId) => {
  return fetch(`/api/${contextId}/documents`, {
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

export const deleteDocument = (contextId, documentId) => {
  return fetch(`/api/${contextId}/documents/${documentId}`, {
    method: "DELETE",
  }).then(async (response) => {
    let data = await response.json();
    if (!response.ok) {
      const error = (data && data.message) || response.status;
      return Promise.reject(error);
    }
    return Promise.resolve(data);
  });
};
