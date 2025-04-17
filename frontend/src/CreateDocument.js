// frontend/src/CreateDocument.js
import React, { useState, useEffect } from 'react';
import axios from 'axios';

const CreateDocument = ({ onDocumentCreated }) => {
  const [templates, setTemplates] = useState([]);
  const [selectedTemplate, setSelectedTemplate] = useState('');
  const [keywords, setKeywords] = useState('');
  const [classOption, setClassOption] = useState('סודי');

  useEffect(() => {
    axios.get('http://127.0.0.1:5000/api/templates')
      .then(response => {
        setTemplates(response.data.templates);
        if (response.data.templates.length > 0) {
          setSelectedTemplate(response.data.templates[0]);
        }
      })
      .catch(error => console.error(error));
  }, []);

  const handleCreate = () => {
    axios.post('http://127.0.0.1:5000/api/create-document', {
      template: selectedTemplate,
      keywords: keywords,
      class: classOption
    })
    .then(response => {
      alert("Document created successfully.");
      if (onDocumentCreated) {
        onDocumentCreated();
      }
    })
    .catch(error => {
      console.error(error);
      alert("Error creating document.");
    });
  };

  return (
    <div className="card">
      <h2>צור מסמך</h2>
      <div>
        <label>
          Select Template:&nbsp;
          <select value={selectedTemplate} onChange={e => setSelectedTemplate(e.target.value)}>
            {templates.map((template, idx) => (
              <option key={idx} value={template}>{template}</option>
            ))}
          </select>
        </label>
      </div>
      <div>
        <label>Keywords: 
          <input type="text" value={keywords} onChange={e => setKeywords(e.target.value)} />
        </label>
      </div>
<div>
  <label>
    סיווג:
      <select value={classOption} onChange={e => setClassOption(e.target.value)}>
        <option value="סודי">סודי</option>
        <option value="שמור">שמור</option>
        <option value='בלמ"ס'>בלמ"ס</option>
      </select>
  </label>
</div>

      <button onClick={handleCreate}>Create Document</button>
    </div>
  );
};

export default CreateDocument;