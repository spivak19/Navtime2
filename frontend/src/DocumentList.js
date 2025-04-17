import React, { useState, useEffect } from 'react';
import axios from 'axios';

const DocumentList = () => {
  const [documents, setDocuments] = useState([]);
  const [sortBy, setSortBy] = useState('created_at');
  const [search, setSearch] = useState('');
  const [userFilter, setUserFilter] = useState('');

  const fetchDocuments = () => {
    axios.get(`http://127.0.0.1:5000/api/documents?sort_by=${sortBy}&search=${search}&user=${userFilter}`)
      .then(response => setDocuments(response.data.documents))
      .catch(error => console.error(error));
  };

  useEffect(() => {
    fetchDocuments();
  }, [sortBy, search, userFilter]);  // re-fetch when any filter changes


  // Handle F5 key to refresh without reloading page
  useEffect(() => {
    const handleKeyDown = (e) => {
      if (e.key === 'F5') {
        e.preventDefault();
        fetchDocuments();
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => {
      window.removeEventListener('keydown', handleKeyDown);
    };
  }, [fetchDocuments]);

  return (
    <div>
      <h2>סימוכין</h2>
      <div>
        <label>
          חיפוש: <input type="text" value={search} onChange={e => setSearch(e.target.value)} />
        </label>
        <br />
        <br />
        <label>
          מיין לפי:&nbsp;
          <select value={sortBy} onChange={e => setSortBy(e.target.value)}>
            <option value="created_at">תאריך</option>
            <option value="user">משתמש</option>
          </select>
        </label>
      </div>
      <table border="1" cellPadding="5">
        <thead>
          <tr>
            {/* <th>ID</th> */}
            <th>מס' סימוכין</th>
            <th>תאריך</th>
            <th>משתמש</th>
            <th>כותרת</th>
            <th>קישור</th>
          </tr>
        </thead>
        <tbody>
          {documents.map(doc => (
            <tr key={doc.id}>
              {/* <td>{doc.id}</td> */}
              <td>{doc.file_name}</td>
              <td>{doc.created_at}</td>
              <td>{doc.user}</td>
              <td>{doc.keywords}</td>
              <td>
              {/* <a href={`file://${doc.file_path}`} target="_blank" rel="noopener noreferrer">Open</a>
              </a> */}
              <button
                onClick={() => {
                  axios.post(`http://127.0.0.1:5000/api/launch-file/${doc.file_name}`)
                    .then(() => {
                      // Optionally show a confirmation
                    })
                    .catch(err => {
                      console.error(err);
                      alert('Failed to open file');
                    });
                }}
              >
                Open
              </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      <button onClick={fetchDocuments}>Refresh</button>
    </div>
  );
};

export default DocumentList;
