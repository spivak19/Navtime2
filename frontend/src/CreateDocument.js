// frontend/src/CreateDocument.js
import React, { useState, useEffect } from 'react';
import axios from 'axios';

const CreateDocument = ({ onDocumentCreated }) => {
  const [templates, setTemplates] = useState([]);
  const [selectedTemplate, setSelectedTemplate] = useState('');
  const [keywords, setKeywords] = useState('');
  const [classOption, setClassOption] = useState('סודי');
  const [existingFile, setExistingFile] = useState(null);
  const [existingKeywords, setExistingKeywords] = useState('');

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

  const handleFileSelect = e => {
    setExistingFile(e.target.files[0]);
  };

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

   // Handler to add an existing local file
 const handleAddFile = () => {
   if (!existingFile) {
     alert('Please select a file first.');
     return;
   }

   const form = new FormData();
   form.append('file', existingFile);
   form.append('keywords', existingKeywords);

   axios.post('http://127.0.0.1:5000/api/add-file', form)
   .then(() => {
     alert('File added successfully.');
     setExistingFile(null);
     setExistingKeywords('');
     if (onDocumentCreated) onDocumentCreated();
   })
   .catch(err => {
     console.error(err);
     alert('Error adding file.');
   });
 };

  return (
    <div className="card">
      <h2>צור מסמך</h2>
      <div>
        <label>
          בחר סגנון:&nbsp;
          <select value={selectedTemplate} onChange={e => setSelectedTemplate(e.target.value)}>
            {templates.map((template, idx) => (
              <option key={idx} value={template}>{template}</option>
            ))}
          </select>
        </label>
      </div>
      <div>
        <label>כותרת: 
          <input type="text" value={keywords} onChange={e => setKeywords(e.target.value)} placeholder='לדוגמא: סיכום דיון'/>
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

      <button onClick={handleCreate}>צור מסמך</button>
           <hr />

     <h2>הוסף קובץ קיים</h2>
     <div>
        <input type="file" onChange={handleFileSelect} accept="*/*"/>
        <br/>
        <label>
          כותרת:&nbsp;
          <input
            type="text"
            value={existingKeywords}
            onChange={e => setExistingKeywords(e.target.value)}
            placeholder='לדוגמא: מצגת FTRR'
          />
        </label>       
       
     </div>
     <button onClick={handleAddFile}>הוסף קובץ</button>
    </div>
  );
};

export default CreateDocument;